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
        import ja_report_generator
        
        # Принимаем четыре параметра от генератора (успех, отчет, ссылка, день недели)
        success, markdown_body, comment_url, target_day = ja_report_generator.run_generator()
        
        if not success:
            print("[ГЛАВНЫЙ ДИСПЕТЧЕР] 🛑 Формирующий block вернул False. Мягко завершаем конвейер.")
            return
            
        print("[ГЛАВНЫЙ ДИСПЕТЧЕР] 🟢 УСПЕХ! Данные получены от генератора отчетов.")
        print(f"[ГЛАВНЫЙ ДИСПЕТЧЕР] Ссылка для рассылки: '{comment_url}'")
        print(f"[ГЛАВНЫЙ ДИСПЕТЧЕР] День недели: '{target_day}'")

        # Читаем конфигурацию чатов из YAML расписания преподавателя
        data_dir = os.path.join(os.getcwd(), '_data')
        yaml_files = [f for f in os.listdir(data_dir) if f.startswith('journal-attendance-') and f.endswith('.yml')]
        
        if not yaml_files:
            print("[ГЛАВНЫЙ ДИСПЕТЧЕР] ❌ Ошибка: Личный файл расписания YAML не найден для чтения настроек!")
            return
            
        yaml_path = os.path.join(data_dir, yaml_files[0])
        with open(yaml_path, 'r', encoding='utf-8') as f:
            yaml_data = yaml.safe_load(f) or {}
            
        config_data = yaml_data.get('config', {})
        
        # --- ПОТОК 1: ЛИЧНЫЕ УВЕДОМЛЕНИЯ ---
        personal_ids = config_data.get('tg_personal_id', [])
        if personal_ids:
            print("[ГЛАВНЫЙ ДИСПЕТЧЕР] Запуск модуля ja_tgbot_personal...")
            import ja_tgbot_personal
            ja_tgbot_personal.send_personal_report(markdown_body, comment_url, target_day, personal_ids)
        else:
            print("[ГЛАВНЫЙ ДИСПЕТЧЕР] ℹ️ Поле tg_personal_id пустое, пропуск личного информирования.")

        # --- ПОТОК 2: ОБЩИЕ АНОНСЫ В КАНАЛЫ ---
        public_config = config_data.get('tg_public_notify', [])
        if public_config:
            print("[ГЛАВНЫЙ ДИСПЕТЧЕР] Запуск модуля ja_tgbot_notify...")
            import ja_tgbot_notify
            ja_tgbot_notify.send_public_notification(markdown_body, comment_url, public_config)
        else:
            print("[ГЛАВНЫЙ ДИСПЕТЧЕР] ℹ️ Поле tg_public_notify пустое, пропуск родительских анонсов.")
            
        print("=== [ГЛАВНЫЙ ДИСПЕТЧЕР] ВСЕ ЭТАПЫ КОНВЕЙЕРА УСПЕШНО ЗАВЕРШЕНЫ В 1 ШАГ! ===")
        
    except Exception as err:
        print(f"[ГЛАВНЫЙ ДИСПЕТЧЕР] ❌ Критическая ошибка конвейера: {str(err)}")

if __name__ == "__main__":
    main()
