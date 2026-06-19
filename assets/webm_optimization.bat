@echo off
chcp 65001 > nul

set "SOURCE_DIR=%~dp0"
if "%SOURCE_DIR:~-1%"=="\" set "SOURCE_DIR=%SOURCE_DIR:~0,-1%"

set "BACKUP_ROOT=%SOURCE_DIR%\webm-sources"
set "LOG_FILE=%SOURCE_DIR%\webm_optimization_log.txt"

echo === ВЕБ-ОПТИМИЗАЦИЯ WEB-M С АВТОПРОПУСКОМ ===
echo Корневая папка: "%SOURCE_DIR%"
echo Папка оригиналов: "%BACKUP_ROOT%"
echo --------------------------------------------------

echo ЗАПУСК СКРИПТА: %DATE% %TIME% > "%LOG_FILE%"
echo -------------------------------------------------- >> "%LOG_FILE%"

:: Тест запуска утилиты в начале лога
echo [ТЕСТ ЗАПУСКА FFPROBE В СИСТЕМЕ]: >> "%LOG_FILE%"
ffprobe -version >> "%LOG_FILE%" 2>&1
echo -------------------------------------------------- >> "%LOG_FILE%"

for /r "%SOURCE_DIR%" %%f in (*.webm) do (
    echo "%%~dpf" | findstr /i "webm-sources" >nul
    if errorlevel 1 (
        echo.
        echo --------------------------------------------------
        echo Найдено видео: "%%~nxf"
        echo В папке: "%%~dpf"
        
        echo [ПРОВЕРКА ИНДЕКСА ДЛИТЕЛЬНОСТИ ДЛЯ %%~nxf]:
        echo [ТЕСТ FFPROBE ДЛЯ %%~nxf]: >> "%LOG_FILE%"
        
        :: Инициализируем метку значением 0
        set "duration=0"
        
        echo ЛОГ: Исходное значение метки duration=0
        echo ЛОГ: Исходное значение метки duration=0 >> "%LOG_FILE%"
        
        :: Экспорт во временный файл в режиме тишины
        ffprobe -v quiet -show_entries format=duration "%%f" > "%TEMP%\dur_check.tmp" 2>&1
        
        :: Копируем технический вывод в лог и на экран
        type "%TEMP%\dur_check.tmp"
        type "%TEMP%\dur_check.tmp" >> "%LOG_FILE%" 2>&1
        echo --------------------------------------------------
        
        :: ТОЧНАЯ И БЕЗОПАСНАЯ ПРОВЕРКА ЧЕРЕЗ ОПЕРАТОРЫ && И ||
        findstr "duration=N/A" "%TEMP%\dur_check.tmp" >nul && (
            set "duration=1"
            echo ЛОГ: Поиск нашел строку duration=N/A. Метке присвоено значение 1.
            echo ЛОГ: Поиск нашел строку duration=N/A. Метке присвоено значение 1. >> "%LOG_FILE%"
        ) || (
            set "duration=0"
            echo ЛОГ: Поиск НЕ нашел совпадений с N/A. Метка остается duration=0.
            echo ЛОГ: Поиск НЕ нашел совпадений с N/A. Метка остается duration=0. >> "%LOG_FILE%"
        )
        del /f /q "%TEMP%\dur_check.tmp" >nul 2>&1
        
        set "RELATIVE_PATH=%%~dpf"
        setlocal enabledelayedexpansion
        set "BACKUP_DEST=!RELATIVE_PATH:%SOURCE_DIR%=%BACKUP_ROOT%!"
        
        echo ЛОГ: Финальная проверка условия. Текущее значение в цикле: duration=!duration!
        echo ЛОГ: Финальная проверка условия. Текущее значение в цикле: duration=!duration! >> "%LOG_FILE%"
        
        if "!duration!"=="1" (
            :: ЕСЛИ ДЛИТЕЛЬНОСТЬ РАВНА 1 (duration=N/A) - СПРАШИВАЕМ РАЗРЕШЕНИЕ НА ЗАМЕНУ
            echo - Внимание: Требуется оптимизация.
            
            choice /m "Оптимизировать этот файл?"
            
            if !errorlevel! equ 1 (
                echo - Запуск оптимизации...
                ffmpeg -y -i "%%f" -c copy -reserve_index_space 1024K "%%~dpf%%~nf_optimized.webm" >nul 2>&1
                
                if exist "%%~dpf%%~nf_optimized.webm" (
                    mkdir "!BACKUP_DEST!" 2>nul
                    move /y "%%f" "!BACKUP_DEST!%%~nxf" >nul
                    ren "%%~dpf%%~nf_optimized.webm" "%%~nxf"
                    
                    echo - Успешно обработано.
                    endlocal
                    echo %DATE% %TIME% [УСПЕШНО ОПТИМИЗИРОВАН] "%%~nxf" >> "%LOG_FILE%"
                ) else (
                    echo - ОШИБКА: FFmpeg не смог обработать файл.
                    endlocal
                    echo %DATE% %TIME% [ОШИБКА ОБРАБОТКИ] "%%~nxf" >> "%LOG_FILE%"
                )
            ) else (
                echo - Пропущено пользователем.
                endlocal
                echo %DATE% %TIME% [ПРОПУЩЕНО ПОЛЬЗОВАТЕЛЕМ] "%%~nxf" >> "%LOG_FILE%"
            )
        ) else (
            :: ВО ВСЕХ ОСТАЛЬНЫХ СЛУЧАЯХ (duration=0) - АВТО-ПРОПУСК БЕЗ ВОПРОСОВ
            echo - Статус: Уже оптимизирован. Авто-пропуск.
            endlocal
            echo %DATE% %TIME% [ИЗНАЧАЛЬНО ОПТИМИЗИРОВАН] "%%~nxf" >> "%LOG_FILE%"
        )
    )
)

echo -------------------------------------------------- >> "%LOG_FILE%"
echo ВСЕ ОПЕРАЦИИ ВЫПОЛНЕНЫ >> "%LOG_FILE%"
echo.
echo Все готово! Результаты и отладочный лог записаны в "optimization_log.txt".
pause
