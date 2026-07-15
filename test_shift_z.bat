@echo off
REM Teste de Shift+Z como Administrador

echo ========================================
echo   TESTE SHIFT+Z (ADMINISTRADOR)
echo ========================================
echo.
echo Este script vai testar se o Shift+Z funciona.
echo.
echo INSTRUCOES:
echo 1. Mantenha este terminal aberto
echo 2. Foque na janela do jogo
echo 3. Aguarde 5 segundos
echo 4. O script vai pressionar Shift+Z
echo 5. Veja se a vara foi lancada
echo.

REM Verificar se está rodando como admin
net session >nul 2>&1
if %errorLevel% == 0 (
    echo [OK] Rodando como Administrador
) else (
    echo [AVISO] NAO esta rodando como Administrador!
    echo Isso pode causar problemas.
)

echo.
pause

REM Ativar ambiente virtual e executar teste
call venv\Scripts\activate.bat
python test_shift_z.py

pause

