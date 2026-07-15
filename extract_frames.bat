@echo off
REM Extrai frames do GIF para análise manual

echo.
echo ===============================================
echo    Extrator de Frames - Fishing Bot (Manual)
echo ===============================================
echo.

if "%~1"=="" (
    echo ERRO: Nenhum arquivo GIF especificado!
    echo.
    echo Uso: extract_frames.bat fishing_gameplay.gif
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

echo Extraindo frames de: %~1
echo.

REM Ativar venv e extrair frames
call venv\Scripts\activate.bat
python extract_frames.py "%~1"

echo.
echo ===============================================
echo    Frames extraidos!
echo ===============================================
echo.
echo PROXIMOS PASSOS:
echo.
echo 1. Abra a pasta: artifacts\gif_frames
echo 2. Veja as imagens 'annotated_frame_XXX.png'
echo 3. Anote os numeros dos frames COM BOLHAS
echo 4. Execute:
echo    analyze_bubble_manual.bat fishing_gameplay.gif 5,12,18,23
echo    (substitua pelos numeros que voce anotou)
echo.

pause

