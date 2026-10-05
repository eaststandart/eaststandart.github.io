import os
import sys

def main():
    print("=== [ГЛАВНЫЙ ДИСПЕТЧЕР] ЗАПУСК УПРАВЛЯЮЩЕГО СКОНВЕЙЕРА ===")
    
    # Жестко прописываем путь к папке _actions, чтобы модули импортировались без сбоев
    current_dir = os.path.dirname(os.path.abspath(__file__))
    if current_dir not in sys.path:
        sys.path.append(current_dir)
        
    # ПОДКЛЮЧАЕМ ШАГ 1: Запуск формирующего блока ja_report_generator
    print("[ГЛАВНЫЙ ДИСПЕТЧЕР] Запуск формирующего блока отчетов...")
    try:
        import ja_report_generator
        
        # Запускаем генератор и ловим два его сигнала наружу
        success, markdown_body = ja_report_generator.run_generator()
        
        if not success:
            print("[ГЛАВНЫЙ ДИСПЕТЧЕР] 🛑 Формирующий блок вернул False (комплект не собран или ошибка). Мягко завершаем конвейер.")
            return
            
        print("[ГЛАВНЫЙ ДИСПЕТЧЕР] 🟢 УСПЕХ! Формирующий блок вернул True. Markdown таблица в памяти диспетчера!")
        print(f"[ГЛАВНЫЙ ДИСПЕТЧЕР] Длина полученного отчета: {len(markdown_body)} символов.")
        
        # Сюда мы будем постепенно, маленькими шагами дописывать вызовы ja_tgbot_personal и ja_tgbot_notify
        print("[ГЛАВНЫЙ ДИСПЕТЧЕР] Конвейер успешно приостановлен. Ожидаем подключение Телеграм-модулей...")
        
    except Exception as err:
        print(f"[ГЛАВНЫЙ ДИСПЕТЧЕР] ❌ Критическая ошибка при управлении модулем генератора: {str(err)}")

if __name__ == "__main__":
    main()
