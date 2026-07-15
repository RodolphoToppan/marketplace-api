@echo off
REM Analisar GIF de gameplay para otimizar detecção de bolhas

echo.
echo ===================================
echo    Analisador de GIF - Fishing Bot
echo ===================================
echo.

if "%~1"=="" (
    echo ERRO: Nenhum arquivo GIF especificado!
    echo.
    echo Uso: analyze_gif.bat fishing_gameplay.gif
    echo.
    pause
    exit /b 1
)

if not exist "%~1" (
    echo ERRO: Arquivo nao encontrado: %~1
    echo.
    pause
    exit /b 1
)

echo Analisando: %~1
echo.

REM Ativar venv e executar análise
call venv\Scripts\activate.bat
python analyze_gif.py "%~1"

echo.
echo ===================================
echo    Analise completa!
echo ===================================
echo Resultados salvos em: artifacts/gif_analysis/
echo.

pause

