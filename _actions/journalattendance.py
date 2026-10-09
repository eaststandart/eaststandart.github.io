#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@module journalattendance.py
@about Главный диспетчер конвейера Журнала посещений
@purpose Координация работы модулей генерации отчетов и рассылки уведомлений в Телеграм
@author TechLab
@version 1.0.0
"""

import os
import sys
import yaml

def main():
    print("=== [ГЛАВНЫЙ ДИСПЕТЧЕР] ЗАПУСК УПРАВЛЯЮЩЕГО КОНВЕЙЕРА ===")
    
    # Жестко прописываем путь к папке _actions, чтобы модули импортировались без сбоев
    current_dir = os.path.dirname(os.path.abspath(__file__))
    if current_dir not in sys.path:
        sys.path.append(current_dir)
        
    print("[ГЛАВНЫЙ ДИСПЕТЧЕР] Запуск формирующего блока отчетов...")
    
    try:   
        import ja_report_builder
        success, reports_list = ja_report_builder.run_generator()

        if not success or not reports_list:
            print("[ГЛАВНЫЙ ДИСПЕТЧЕР] 🛑 Формирующий блок не вернул готовых отчетов. Мягко завершаем конвейер.")
            return
            
        print(f"[ГЛАВНЫЙ ДИСПЕТЧЕР] 🟢 УСПЕХ! Данные получены. Очередь на отправку: {len(reports_list)} отчетов.")
        data_dir = os.path.join(os.getcwd(), '_data')

        # ЗАПУСКАЕМ ЦИКЛ ОТПРАВКИ ТЕЛЕГРАМ ДЛЯ КАЖДОГО ОТЧЕТА ИНДИВИДУАЛЬНО
        for report_item in reports_list:
            markdown_body = report_item["markdown"]
            comment_url = report_item["url"]
            target_day = report_item["day"]
            teacher_login = report_item["teacher_login"]
            
            print(f"\n[ДИСПЕТЧЕР] Начинаем рассылку в ТГ отчета преподавателя: {teacher_login} 🚀")
            
            # Считываем конфигурацию Телеграм строго из личного YAML-файла текущего преподавателя
            yaml_path = os.path.join(data_dir, f"journal-attendance-{teacher_login}.yml")
            if not os.path.exists(yaml_path):
                print(f"[ГЛАВНЫЙ ДИСПЕТЧЕР] ⚠️ Файл расписания {yaml_path} не найден для чтения настроек чатов. Пропуск.")
                continue
                
            with open(yaml_path, 'r', encoding='utf-8') as f:
                yaml_data = yaml.safe_load(f) or {}
            
            config_data = yaml_data.get('config', {})
            
            # --- ПОТОК 1: ЛИЧНЫЕ УВЕДОМЛЕНИЯ ---
            personal_ids = config_data.get('tg_personal_id', [])
            if personal_ids:
                print(f"[ГЛАВНЫЙ ДИСПЕТЧЕР] Запуск модуля ja_tgbot_personal для {teacher_login}...")
                import ja_tgbot_personal
                ja_tgbot_personal.send_personal_report(markdown_body, comment_url, target_day, personal_ids)
            else:
                print(f"[ГЛАВНЫЙ ДИСПЕТЧЕР] ℹ️ Поле tg_personal_id пустое для {teacher_login}, пропуск.")

            # --- ПОТОК 2: ОБЩИЕ АНОНСЫ В КАНАЛЫ ---
            public_config = config_data.get('tg_public_notify', [])
            if public_config:
                print(f"[ГЛАВНЫЙ ДИСПЕТЧЕР] Запуск модуля ja_tgbot_notify для {teacher_login}...")
                import ja_tgbot_notify
                ja_tgbot_notify.send_public_notification(markdown_body, comment_url, public_config)
            else:
                print(f"[ГЛАВНЫЙ ДИСПЕТЧЕР] ℹ️ Поле tg_public_notify пустое для {teacher_login}, пропуск.")
                
        print("=== [ГЛАВНЫЙ ДИСПЕТЧЕР] ВСЕ СФОРМИРОВАННЫЕ ОТЧЕТЫ УСПЕШНО РАЗОСЛАНЫ В ТЕЛЕГРАМ! ===")

        # ВКЛЮЧЕНИЕ СЕТЕВОГО ЗАКРЫВАТЕЛЯ ШЛЮЗА ПОСЛЕ ПОЛНОГО ЗАВЕРШЕНИЯ ТЕЛЕГРАМА
        try:
            import ja_gate_closer
            ja_gate_closer.close_gate_pipeline(reports_list)
        except Exception as e_closer:
            print(f"[ГЛАВНЫЙ ДИСПЕТЧЕР] ❌ Ошибка выполнения модуля ja_gate_closer: {str(e_closer)}")
       
    except Exception as err:
        print(f"[ГЛАВНЫЙ ДИСПЕТЧЕР] ❌ Критическая ошибка конвейера: {str(err)}")

if __name__ == "__main__":
    main()
