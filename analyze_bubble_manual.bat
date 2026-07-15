@echo off
REM Analisa frames específicos com bolhas (modo manual)

echo.
echo ===============================================
echo    Analisador de Bolhas - Modo Manual
echo ===============================================
echo.

if "%~1"=="" (
    echo ERRO: Nenhum arquivo GIF especificado!
    echo.
    echo Uso: analyze_bubble_manual.bat fishing_gameplay.gif 5,12,18,23
    echo      (substitua pelos numeros dos frames com bolhas)
    echo.
    pause
    exit /b 1
)

if "%~2"=="" (
    echo ERRO: Nenhum frame especificado!
    echo.
    echo Uso: analyze_bubble_manual.bat fishing_gameplay.gif 5,12,18,23
    echo.
    echo Primeiro execute: extract_frames.bat fishing_gameplay.gif
    echo Depois veja as imagens e anote os numeros dos frames com bolhas.
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

echo Analisando frames: %~2
echo Do arquivo: %~1
echo.

REM Ativar venv e analisar
call venv\Scripts\activate.bat
python analyze_gif_manual.py "%~1" --frames %~2

echo.
echo ===============================================
echo    Analise completa!
echo ===============================================
echo Resultados salvos em: artifacts/bubble_analysis/
echo.

pause

