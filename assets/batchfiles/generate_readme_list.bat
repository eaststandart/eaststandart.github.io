@echo off
chcp 65001 > nul
setlocal enabledelayedexpansion

:: @about Скрипт автоматического сбора описаний и документирования файлов папки
:: @purpose Сканирует элементы текущего каталога, игнорирует подпапки, извлекает технические паспорта из комментариев кода (@about/@purpose) или Front Matter (about:/purpose:) и генерирует готовый упорядоченный список Markdown для README.md
:: @author TechLab

set "output_list=readme_list_snapshot.txt"

echo ## Список файлов > "%output_list%"
echo. >> "%output_list%"

:: Перебираем элементы в папке строго по алфавиту
for /f "delims=" %%f in ('dir /b /o:n 2^>nul') do (
    
    :: Пропускаем подпапки (например, arch/)
    if not exist "%%f\*" (
        
        :: Пропускаем сам батник, файл результата и файлы README
        if not "%%f"=="generate_readme_list.bat" if not "%%f"=="%output_list%" if not "%%~xf"==".md" if not "%%~nxf"=="README.md" (
            
            set "file_about="
            set "file_purpose="
            
            :: Читаем файл напрямую построчно без findstr
            for /f "usebackq delims=" %%l in ("%%f") do (
                set "line=%%l"
                
                :: Безопасная проверка через кавычки защищает от ошибок со скобками
                if not "!line!"=="" (
                    set "test_line=!line!"
                    
                    :: Ищем @about
                    if not "!test_line:*@about=!"=="!test_line!" (
                        set "temp_line=!test_line:*@about=!"
                        for /f "tokens=* delims=*/{}%% " %%i in ("!temp_line!") do set "file_about=%%i"
                    )
                    
                    :: Ищем @purpose
                    if not "!test_line:*@purpose=!"=="!test_line!" (
                        set "temp_line=!test_line:*@purpose=!"
                        for /f "tokens=* delims=*/{}%% " %%i in ("!temp_line!") do set "file_purpose=%%i"
                    )
                )
            )
            
            if defined file_about (
                set "desc=!file_about!"
                if defined file_purpose set "desc=!desc! !file_purpose!"
                if not "!desc:~-1!"=="." set "desc=!desc!."
                echo *   **`%%f`** — !desc! >> "%output_list%"
            ) else (
                echo *   **`%%f`** — . >> "%output_list%"
            )
        )
        
        :: Логика парсинга Front Matter для .md файлов (кроме README.md)
        if "%%~xf"==".md" if not "%%~nxf"=="README.md" (
            set "file_about="
            set "file_purpose="
            
            for /f "usebackq delims=" %%l in ("%%f") do (
                set "line=%%l"
                if not "!line!"=="" (
                    set "test_line=!line!"
                    
                    :: Ищем about:
                    if not "!test_line:*about:=!"=="!test_line!" (
                        set "temp_line=!test_line:*about:=!"
                        set "temp_line=!temp_line:"=!"
                        for /f "tokens=* delims= " %%i in ("!temp_line!") do set "file_about=%%i"
                    )
                    
                    :: Ищем purpose:
                    if not "!test_line:*purpose:=!"=="!test_line!" (
                        set "temp_line=!test_line:*purpose:=!"
                        set "temp_line=!temp_line:"=!"
                        for /f "tokens=* delims= " %%i in ("!temp_line!") do set "file_purpose=%%i"
                    )
                )
            )
            
            if defined file_about (
                set "desc=!file_about!"
                if defined file_purpose set "desc=!desc! !file_purpose!"
                if not "!desc:~-1!"=="." set "desc=!desc!."
                echo *   **`%%f`** — !desc! >> "%output_list%"
            ) else (
                echo *   **`%%f`** — . >> "%output_list%"
            )
        )
        
    )
)

echo Готово! Блок списка сгенерирован в файл %output_list%.
pause
