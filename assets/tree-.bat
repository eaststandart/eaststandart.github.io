@echo off
chcp 65001 > nul
set "output_file=structure.txt"

echo eaststandart.github.io/ > "%output_file%"

:: Выводим только реальные папки и файлы, полностью игнорируя скрытый мусор .git
for /f "delims=" %%i in ('dir /b /a-h 2^>nul') do (
    echo ├── %%i >> "%output_file%"
    if exist "%%i\*" (
        for /f "delims=" %%j in ('dir /b /a-h "%%i" 2^>nul') do (
            echo │   └── %%j >> "%output_file%"
        )
    )
)

echo Готово! Результат в файле structure.txt.
pause
