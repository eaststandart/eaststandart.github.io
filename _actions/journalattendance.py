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
        
        # Принимаем строго ЧЕТЫРЕ параметра от генератора (успех, отчет, ссылка, день недели)
        success, markdown_body, comment_url, target_day = ja_report_generator.run_generator()
        
        if not success:
            print("[ГЛАВНЫЙ ДИСПЕТЧЕР] 🛑 Формирующий блок вернул False. Мягко завершаем конвейер.")
            return
            
        print("[ГЛАВНЫЙ ДИСПЕТЧЕР] 🟢 УСПЕХ! Данные получены от генератора отчетов.")
        print(f"[ГЛАВНЫЙ ДИСПЕТЧЕР] Живой лог ссылки: '{comment_url}'")
        print(f"[ГЛАВНЫЙ ДИСПЕТЧЕР] День недели для урезания: '{target_day}'")

        # Читаем список персональных ID из сохраненного YAML расписания преподавателя
        data_dir = os.path.join(os.getcwd(), '_data')
        
        # Ищем личный YAML-файл в папке данных (так как имя динамическое, берем первый попавшийся yml журнала)
        yaml_files = [f for f in os.listdir(data_dir) if f.startswith('journal-attendance-') and f.endswith('.yml')]
        if not yaml_files:
            print("[ГЛАВНЫЙ ДИСПЕТЧЕР] ❌ Ошибка: Личный файл расписания YAML не найден в паблике _data для чтения ID!")
            return
            
        yaml_path = os.path.join(data_dir, yaml_files[0])
        with open(yaml_path, 'r', encoding='utf-8') as f:
            yaml_data = yaml.safe_load(f) or {}
            
        config_data = yaml_data.get('config', {})
        # Извлекаем список ID. Если поля нет, подставляем пустой список во избежание сбоев
        personal_ids = config_data.get('tg_personal_id', [])
        
        if not personal_ids:
            print("[ГЛАВНЫЙ ДИСПЕТЧЕР] ⚠️ Предупреждение: Список tg_personal_id пуст или отсутствует в YAML. Бота не запускаем.")
            return

        print(f"[ГЛАВНЫЙ ДИСПЕТЧЕР] Успешно считано получателей из YAML: {personal_ids}")
        
        # ПОДКЛЮЧАЕМ ШАГ 2: Вызов персонального информера ja_tgbot_personal
        print("[ГЛАВНЫЙ ДИСПЕТЧЕР] Запуск модуля ja_tgbot_personal...")
        import ja_tgbot_personal
        
        # Передаем в руки боту все четыре накопленных в памяти параметра
        ja_tgbot_personal.send_personal_report(markdown_body, comment_url, target_day, personal_ids)
        
        # Сюда мы на следующем этапе подключим общий информер в группу родителей (ja_tgbot_notify)
        print("[ГЛАВНЫЙ ДИСПЕТЧЕР] Конвейер успешно приостановлен. Ожидаем подключение Блока Родителей...")
        
    except Exception as err:
        print(f"[ГЛАВНЫЙ ДИСПЕТЧЕР] ❌ Критическая ошибка конвейера: {str(err)}")

if __name__ == "__main__":
    main()
