#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@module  cb_comment_builder.py
@about   Публикация комментариев в GitHub Discussions.
@purpose Публикует тело Markdown из пакета парсера как новый комментарий.
@author  TechLab
@version 1.0.0
"""

import logging
import os

import requests


GRAPHQL_URL = "https://api.github.com/graphql"
DISCUSSION_OWNER = "eaststandart"
DISCUSSION_REPOSITORY = "eaststandart.github.io"
DISCUSSION_BASE_URL = (
    f"https://github.com/{DISCUSSION_OWNER}/"
    f"{DISCUSSION_REPOSITORY}/discussions"
)
REQUEST_TIMEOUT = 30

logger = logging.getLogger(__name__)


class CommentBuilderPublishError(Exception):
    """Ошибка подготовки или публикации комментария."""


def _graphql_request(token, query, variables):
    """Выполняет один GraphQL-запрос и проверяет HTTP- и GraphQL-ошибки."""
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
        "Content-Type": "application/json",
        "X-GitHub-Api-Version": "2022-11-28",
        "User-Agent": "TechLab-Comment-Builder",
    }

    try:
        response = requests.post(
            GRAPHQL_URL,
            json={"query": query, "variables": variables},
            headers=headers,
            timeout=REQUEST_TIMEOUT,
        )
    except requests.RequestException as error:
        raise CommentBuilderPublishError(
            f"Не удалось связаться с GitHub GraphQL API: {error}"
        ) from error

    try:
        response.raise_for_status()
    except requests.HTTPError as error:
        detail = response.text[:1000]
        raise CommentBuilderPublishError(
            f"GitHub GraphQL API вернул HTTP {response.status_code}: {detail}"
        ) from error

    try:
        payload = response.json()
    except ValueError as error:
        raise CommentBuilderPublishError(
            "GitHub GraphQL API вернул некорректный JSON."
        ) from error

    if not isinstance(payload, dict):
        raise CommentBuilderPublishError(
            "GitHub GraphQL API вернул неожиданный формат ответа."
        )

    errors = payload.get("errors")
    if errors:
        details = "; ".join(
            item.get("message", str(item)) if isinstance(item, dict) else str(item)
            for item in errors
        )
        raise CommentBuilderPublishError(
            f"GraphQL сообщил об ошибке: {details}"
        )

    return payload.get("data")


def publish_comment(package, dry_run=True):
    """
    Публикует тело Markdown из пакета парсера в указанном Discussion.

    Возвращает сведения о созданном комментарии. Вложенные файлы пока
    не загружаются: ссылки в исходном Markdown остаются без изменений.
    """
    if not isinstance(package, dict):
        raise CommentBuilderPublishError("Парсер передал пакет неверного типа.")

    metadata = package.get("metadata")
    if not isinstance(metadata, dict):
        raise CommentBuilderPublishError("В пакете отсутствуют метаданные.")

    discussion_number = metadata.get("discussion_number")
    if isinstance(discussion_number, bool) or not isinstance(discussion_number, int):
        raise CommentBuilderPublishError(
            "discussion_number должен быть целым положительным числом."
        )
    if discussion_number < 1:
        raise CommentBuilderPublishError(
            "discussion_number должен быть больше нуля."
        )

    markdown_body = package.get("body")
    if not isinstance(markdown_body, str) or not markdown_body.strip():
        raise CommentBuilderPublishError(
            "В пакете отсутствует непустое тело Markdown."
        )

    manifest_name = package.get("manifest_name", "неизвестный манифест")
    logger.info(
        "Манифест %s: Discussion #%s, тело Markdown — %d символов.",
        manifest_name,
        discussion_number,
        len(markdown_body),
    )

    if dry_run:
        logger.info("Пробный режим: публикация отключена. GraphQL-запросы не выполнялись.")
        return {
            "success": True,
            "dry_run": True,
            "discussion_number": discussion_number,
            "body_length": len(markdown_body),
            "comment_id": None,
            "url": None,
            "manifest_name": manifest_name,
        }

    token = os.environ.get("MY_ADMIN_TOKEN") or os.environ.get("GITHUB_TOKEN")
    if not token:
        raise CommentBuilderPublishError(
            "Для публикации не найден токен MY_ADMIN_TOKEN или GITHUB_TOKEN."
        )

    logger.info(
        "Начинаю реальную публикацию манифеста %s в Discussion #%s.",
        manifest_name,
        discussion_number,
    )

    lookup_query = """
    query($owner: String!, $repo: String!, $number: Int!) {
      repository(owner: $owner, name: $repo) {
        discussion(number: $number) {
          id
          number
        }
      }
    }
    """
    lookup_data = _graphql_request(
        token,
        lookup_query,
        {
            "owner": DISCUSSION_OWNER,
            "repo": DISCUSSION_REPOSITORY,
            "number": discussion_number,
        },
    )

    repository = (lookup_data or {}).get("repository")
    discussion = repository.get("discussion") if isinstance(repository, dict) else None
    if not isinstance(discussion, dict) or not discussion.get("id"):
        raise CommentBuilderPublishError(
            f"Обсуждение #{discussion_number} не найдено "
            f"в {DISCUSSION_OWNER}/{DISCUSSION_REPOSITORY}."
        )

    logger.info(
        "Обсуждение #%s найдено. Создаю новый комментарий.",
        discussion_number,
    )

    # Защита от повторной публикации после неоднозначного результата предыдущего POST.
    # Сравниваем точное тело среди последних 100 комментариев Discussion.
    existing_query = """
    query($owner: String!, $repo: String!, $number: Int!) {
      repository(owner: $owner, name: $repo) {
        discussion(number: $number) {
          comments(first: 100) {
            nodes {
              databaseId
              url
              body
            }
          }
        }
      }
    }
    """
    existing_data = _graphql_request(
        token,
        existing_query,
        {
            "owner": DISCUSSION_OWNER,
            "repo": DISCUSSION_REPOSITORY,
            "number": discussion_number,
        },
    )
    existing_repository = (existing_data or {}).get("repository")
    existing_discussion = (
        existing_repository.get("discussion")
        if isinstance(existing_repository, dict) else None
    )
    existing_connection = (
        existing_discussion.get("comments")
        if isinstance(existing_discussion, dict) else None
    )
    existing_nodes = (
        existing_connection.get("nodes", [])
        if isinstance(existing_connection, dict) else []
    )
    for existing in existing_nodes:
        if isinstance(existing, dict) and existing.get("body") == markdown_body:
            comment_id = existing.get("databaseId")
            comment_url = existing.get("url")
            if comment_id and comment_url:
                logger.warning(
                    "Найден комментарий с полностью совпадающим текстом "
                    "(ID %s). Повторная публикация отменена.",
                    comment_id,
                )
                return {
                    "success": True,
                    "duplicate": True,
                    "discussion_number": discussion_number,
                    "comment_id": comment_id,
                    "url": comment_url,
                    "manifest_name": manifest_name,
                }

    mutation = """
    mutation($discussionId: ID!, $body: String!) {
      addDiscussionComment(input: {
        discussionId: $discussionId,
        body: $body
      }) {
        comment {
          databaseId
          url
        }
      }
    }
    """
    mutation_data = _graphql_request(
        token,
        mutation,
        {
            "discussionId": discussion["id"],
            "body": markdown_body,
        },
    )

    mutation_result = (mutation_data or {}).get("addDiscussionComment")
    comment = (
        mutation_result.get("comment")
        if isinstance(mutation_result, dict)
        else None
    )
    if not isinstance(comment, dict) or not comment.get("databaseId"):
        raise CommentBuilderPublishError(
            "GitHub не вернул идентификатор созданного комментария."
        )

    comment_id = comment["databaseId"]
    comment_url = comment.get("url") or (
        f"{DISCUSSION_BASE_URL}/{discussion_number}"
        f"?sort=new#discussioncomment-{comment_id}"
    )

    result = {
        "success": True,
        "discussion_number": discussion_number,
        "comment_id": comment_id,
        "url": comment_url,
        "manifest_name": manifest_name,
    }

    logger.info(
        "Комментарий #%s опубликован: %s",
        comment_id,
        comment_url,
    )
    return result
