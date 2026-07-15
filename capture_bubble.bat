@echo off
REM Script para capturar template de borbulha

echo ========================================
echo   CAPTURAR TEMPLATE DE BORBULHA
echo ========================================
echo.
echo Este script ajuda a criar uma imagem da borbulha
echo para detecção precisa (sem falsos positivos!).
echo.
echo PREPARE-SE:
echo 1. Abra o jogo
echo 2. Va para area de pesca
echo 3. Lance a vara MANUALMENTE (Shift+Z)
echo 4. Aguarde as borbulhas aparecerem
echo 5. Volte aqui e pressione qualquer tecla
echo.
pause

REM Ativar ambiente virtual e executar
call venv\Scripts\activate.bat
python capture_bubble_template.py

echo.
echo ========================================
echo.
echo PROXIMO PASSO:
echo.
echo Abra config.yaml e mude:
echo   bubble_detection:
echo     method: 'template'
echo.
echo Depois execute: start_bot.bat
echo.
pause

