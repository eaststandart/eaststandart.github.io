{%- comment -%}
@about Изолированный модуль развернутого вывода постов проекта.
@purpose Рендерит готовый массив физических путей, переданный из Python, с нативным обнулением отступов.
@author TechLab
{%- endcomment -%}

<!--1. HTML-СКЕЛЕТ ВЫВОДА ПОЛНОЦЕННЫХ ПУБЛИКАЦИЙ ПРОЕКТА ИЗ ПЕРЕДАННОГО МАССИВА -->
<div id="media-container" class="media-archive-list-wrapper">
  {%- for file_path in include.paths -%}
    {%- assign post = site.posts | where: "path", file_path | first -%}
    {%- if post == nil -%}
      {%- assign post = site.pages | where: "path", file_path | first -%}
    {%- endif -%}
    
    {%- if post -%}
      {%- comment -%} НАДЁЖНОЕ СЕРВЕРНОЕ ОБНУЛЕНИЕ: Обнуляем отступ строго для самого последнего элемента массива {%- endcomment -%}
      <div class="media-entry"{% if forloop.last %} style="margin-bottom: 0px !important;"{% endif %}>
        
        <!-- Контейнер строки даты и заголовка -->
        <div class="media-entry-title-row">
          <span class="media-entry-date">{{ post.date | date: "%d.%m.%Y" }}</span>
          <h3 class="media-entry-title">{{ post.title }}</h3>
        </div>
        
        <!-- Оболочка основного контента статьи (1 в 1 как на старом сайте) -->
        <div class="media-content main-content">
          {%- if post.description and post.description != "" -%}
            <p class="page-description">{{ post.description }}</p>
          {%- endif -%}
          
          {{ post.content }}
          
          {%- if post.author and post.author != "" -%}
          <!-- А. БЛОК ВЫВОДА АВТОРА -->
          <div class="author-inline">
              <strong>Автор:</strong> 
              <div class="sources-content">{{ post.author }}</div>
          </div>
          {%- endif -%}
          
          {%- if post.sources and post.sources != "" -%}
          <!-- Б. БЛОК ВЫВОДА ИСТОЧНИКОВ -->
          <div class="sources-inline">
              <strong>Источники:</strong>
              <div class="sources-content">{{ post.sources | markdownify }}</div>
          </div>
          {%- endif -%}
          
          {%- if post.tags.size > 0 -%}
          <!-- В. БЛОК ВЫВОДА ТЕГОВ -->
          <div class="tag-container">
              {%- for tag in post.tags -%}
                  {%- assign tag_clean = tag | replace: "#", "" | strip -%}
                  <a href="{{ '/tags.html' | relative_url }}#{{ tag_clean | slugify }}" class="tag-item">{{ tag_clean }}</a>
              {%- endfor -%}
          </div>
          {%- endif -%}
        </div>
        
        {%- comment -%} НАСТОЯЩАЯ СЕРВЕРНАЯ ЗАЧИСТКА: Линия создаётся только если впереди есть посты {%- endcomment -%}
        {%- unless forloop.last -%}
          <hr class="media-entry-hr">
        {%- endunless -%}
      </div>
    {%- endif -%}
  {%- endfor -%}
</div>
