@echo off
REM Script de instalação universal - funciona em qualquer caminho

echo ========================================
echo   FISHING BOT - INSTALACAO AUTOMATICA
echo ========================================
echo.

REM Verificar se Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERRO] Python nao esta instalado!
    echo Baixe em: https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)

echo [OK] Python encontrado
python --version

REM Remover ambiente virtual antigo se existir
if exist venv (
    echo.
    echo [LIMPEZA] Removendo ambiente virtual antigo...
    rmdir /s /q venv
)

REM Criar novo ambiente virtual
echo.
echo [CRIANDO] Novo ambiente virtual...
python -m venv venv
if errorlevel 1 (
    echo [ERRO] Falha ao criar ambiente virtual!
    pause
    exit /b 1
)

echo [OK] Ambiente virtual criado

REM Ativar ambiente e instalar
echo.
echo [INSTALANDO] Dependencias (isso pode levar 3-5 minutos)...
call venv\Scripts\activate.bat
python -m pip install --upgrade pip setuptools wheel --quiet
pip install -r requirements.txt

if errorlevel 1 (
    echo.
    echo [ERRO] Falha na instalacao!
    echo Tente executar manualmente:
    echo   1. venv\Scripts\activate.bat
    echo   2. python -m pip install --upgrade pip setuptools wheel
    echo   3. pip install -r requirements.txt
    pause
    exit /b 1
)

echo.
echo ========================================
echo   INSTALACAO CONCLUIDA COM SUCESSO!
echo ========================================
echo.
echo Para usar o bot:
echo   1. Execute: start_bot.bat
echo   OU
echo   2. venv\Scripts\activate.bat
echo   3. python run.py
echo.
pause

