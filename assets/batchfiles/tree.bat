@echo off
chcp 65001 > nul

:: @about Скрипт автоматической генерации интерактивной структуры репозитория.
:: @purpose Сканирует файлы проекта, группирует папки вверху, файлы внизу, сортирует их по алфавиту и выстраивает в графическое дерево с правильными уголками.
:: @author TechLab

set "output_file=structure.txt"

:: Записываем корень проекта
echo eaststandart.github.io/ > "%output_file%"

:: Запускаем обход с пустым отступом
call :scan_folder "." ""

echo Готово! Безупречная структура сохранена в файл %output_file%.
pause
exit /b

:scan_folder
setlocal enabledelayedexpansion
set "current_path=%~1"
set "indent=%~2"

:: Сначала считаем общее количество валидных элементов в этой папке (включая tree.bat)
set "total_items=0"
for /f "delims=" %%a in ('dir "%current_path%" /b /o:gn /a-h 2^>nul') do (
    if not "%%a"=="%output_file%" if not "%%a"=="arch" (
        set /a total_items+=1
    )
)

:: Теперь запускаем ваш основной цикл с выводом
set "current_item=0"
for /f "delims=" %%i in ('dir "%current_path%" /b /o:gn /a-h 2^>nul') do (
    
    :: Проверяем исключения: файл результата и папки arch (tree.bat НЕ исключаем)
    if not "%%i"=="%output_file%" if not "%%i"=="arch" (
        set /a current_item+=1
        
        :: Если текущий номер равен общему количеству элементов — это последний элемент
        if !current_item! equ !total_items! (
            set "branch_symbol=└── "
            set "next_indent=%indent%    "
        ) else (
            set "branch_symbol=├── "
            set "next_indent=%indent%│   "
        )
        
        :: Если это папка
        if exist "%current_path%\%%i\*" (
            echo %indent%!branch_symbol!%%i/ >> "%output_file%"
            :: Заходим внутрь, передавая правильный отступ
            call :scan_folder "%current_path%\%%i" "!next_indent!"
        ) else (
            :: Если это файл
            echo %indent%!branch_symbol!%%i >> "%output_file%"
        )
    )
)
endlocal
exit /b
