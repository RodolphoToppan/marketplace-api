@echo off
REM Script para iniciar o bot - funciona em qualquer caminho

echo ========================================
echo   FISHING BOT - INICIANDO
echo ========================================
echo.

REM Verificar se ambiente virtual existe
if not exist venv (
    echo [ERRO] Ambiente virtual nao encontrado!
    echo Execute primeiro: install.bat
    echo.
    pause
    exit /b 1
)

REM Ativar ambiente e executar
call venv\Scripts\activate.bat
python run.py

pause

