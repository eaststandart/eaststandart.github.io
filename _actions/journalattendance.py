import os
import sys

def main():
    print("=== [ГЛАВНЫЙ ДИСПЕТЧЕР] ЗАПУСК УПРАВЛЯЮЩЕГО КОНВЕЙЕРА ===")
    
    # Жестко прописываем путь к папке _actions, чтобы модули импортировались без сбоев
    current_dir = os.path.dirname(os.path.abspath(__file__))
    if current_dir not in sys.path:
        sys.path.append(current_dir)
        
    print("[ГЛАВНЫЙ ДИСПЕТЧЕР] Запуск формирующего блока отчетов...")
    
    try:
        import ja_report_generator
        
        # Принимаем строго ТРИ параметра от генератора (включая прямую ссылку comment_url)
        success, markdown_body, comment_url = ja_report_generator.run_generator()
        
        if not success:
            print("[ГЛАВНЫЙ ДИСПЕТЧЕР] 🛑 Формирующий блок вернул False (комплект не собран или ошибка). Мягко завершаем конвейер.")
            return
            
        print("[ГЛАВНЫЙ ДИСПЕТЧЕР] 🟢 УСПЕХ! Формирующий блок вернул True. Данные в памяти диспетчера!")
        print(f"[ГЛАВНЫЙ ДИСПЕТЧЕР] Длина полученного отчета: {len(markdown_body)} символов.")
        print(f"[ГЛАВНЫЙ ДИСПЕТЧЕР] Живой лог ссылки для Телеграм-ботов: '{comment_url}'")
        
        # Сюда мы будем постепенно, маленькими шагами дописывать вызовы ja_tgbot_personal и ja_tgbot_notify
        print("[ГЛАВНЫЙ ДИСПЕТЧЕР] Конвейер успешно приостановлен. Ожидаем подключение Телеграм-модулей...")
        
    except Exception as err:
        print(f"[ГЛАВНЫЙ ДИСПЕТЧЕР] ❌ Критическая ошибка при управлении модулем генератора: {str(err)}")

if __name__ == "__main__":
    main()
