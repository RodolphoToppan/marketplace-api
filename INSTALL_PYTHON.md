# 🐍 GUIA DE INSTALAÇÃO DO PYTHON E CONFIGURAÇÃO DO PROJETO

## 📥 **PASSO 1: INSTALAR O PYTHON**

### **Opção A: Download Direto (Recomendado)**

1. **Acesse o site oficial:**
   - Abra: https://www.python.org/downloads/
   - Ou diretamente: https://www.python.org/ftp/python/3.12.10/python-3.12.10-amd64.exe

2. **Baixe o instalador:**
   - Clique em "Download Python 3.12.x" (versão mais recente)
   - Ou use o link direto acima para Python 3.12.10

3. **Execute o instalador:**
   - ⚠️ **IMPORTANTE:** Marque a opção **"Add Python to PATH"** ✅
   - Clique em **"Install Now"**
   - Aguarde a instalação (2-5 minutos)

4. **Verifique a instalação:**
   ```powershell
   python --version
   ```
   - Deve mostrar: `Python 3.12.x`

---

### **Opção B: Microsoft Store (Alternativa)**

1. Abra a **Microsoft Store**
2. Busque por **"Python 3.12"**
3. Clique em **"Obter"** ou **"Instalar"**
4. Aguarde a instalação
5. Verifique:
   ```powershell
   python --version
   ```

---

## ✅ **PASSO 2: VERIFICAR INSTALAÇÃO**

Abra o **PowerShell** ou **Terminal** e execute:

```powershell
# Verificar Python
python --version

# Verificar pip (gerenciador de pacotes)
pip --version

# Deve mostrar algo como:
# Python 3.12.10
# pip 24.x.x from ...
```

Se aparecer erro "python não é reconhecido":
- Reinicie o terminal
- Reinicie o computador
- Reinstale marcando "Add to PATH"

---

## 📦 **PASSO 3: CONFIGURAR O PROJETO**

### **3.1. Navegar até o projeto:**

```powershell
cd C:\Users\rodolpho.toppan\Desktop\marketplace-api
```

### **3.2. Criar ambiente virtual:**

```powershell
python -m venv venv
```

Isso cria uma pasta `venv` com Python isolado.

### **3.3. Ativar ambiente virtual:**

```powershell
.\venv\Scripts\Activate.ps1
```

Você verá `(venv)` no início da linha.

**⚠️ Se der erro "execução de scripts desabilitada":**

Execute **como Administrador**:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Depois tente novamente:
```powershell
.\venv\Scripts\Activate.ps1
```

### **3.4. Instalar dependências:**

```powershell
pip install -r requirements.txt
```

Isso instala:
- mss (captura de tela)
- opencv-python (visão computacional)
- numpy (processamento)
- pyautogui (controle de mouse/teclado)
- keyboard (hotkeys)
- pyyaml (configuração)
- pydantic (validação)
- pytest (testes)

**Aguarde 2-5 minutos** para instalar tudo.

---

## 🎮 **PASSO 4: CONFIGURAR O JOGO**

### **4.1. Abrir o jogo:**
- Execute o jogo em **modo janela** (não tela cheia)

### **4.2. Descobrir posição da janela:**

Execute este script para ajudar:

```powershell
python -c "import pyautogui; import time; print('Mova o mouse para o CANTO SUPERIOR ESQUERDO da janela do jogo em 3 segundos...'); time.sleep(3); x, y = pyautogui.position(); print(f'Posição: x={x}, y={y}')"
```

Depois, mova para o canto inferior direito:

```powershell
python -c "import pyautogui; import time; print('Mova o mouse para o CANTO INFERIOR DIREITO da janela do jogo em 3 segundos...'); time.sleep(3); x, y = pyautogui.position(); print(f'Posição: x={x}, y={y}')"
```

**Calcule:**
- `width` = x_direito - x_esquerdo
- `height` = y_baixo - y_cima

### **4.3. Editar config.yaml:**

Abra o arquivo `config.yaml` e ajuste:

```yaml
regions:
  game_area:
    x: [x_esquerdo]      # Exemplo: 100
    y: [y_cima]          # Exemplo: 100
    width: [largura]     # Exemplo: 800
    height: [altura]     # Exemplo: 600
```

---

## 🚀 **PASSO 5: EXECUTAR O BOT**

### **5.1. Executar em modo seguro (dry-run):**

```powershell
python run.py
```

Você verá:
```
🎣 local-game-automation v0.2.0
Academic Computer Vision Project - Fishing Automation
============================================================
🔒 Running in DRY-RUN mode (safe, no real actions)
...
✅ Bot ready! Press f12 to start fishing...
```

### **5.2. Testar:**

1. **Abra o jogo** e posicione na área de pesca
2. **Pressione F12** no teclado
3. Observe os logs no terminal
4. **Pressione F12** novamente para parar

**Em modo dry-run:**
- ✅ Bot detecta água
- ✅ Bot detecta borbulhas
- ✅ Logs são gerados
- ❌ **NENHUMA ação real é executada** (seguro!)

### **5.3. Quando estiver pronto para modo real:**

1. Edite `config.yaml`:
   ```yaml
   execution:
     dry_run: false  # Atenção!
   ```

2. Execute novamente:
   ```powershell
   python run.py
   ```

3. Confirme com `yes` quando perguntado

4. **Pressione F12** no jogo para iniciar

---

## 🔧 **COMANDOS ÚTEIS**

### **Ativar ambiente virtual:**
```powershell
.\venv\Scripts\Activate.ps1
```

### **Desativar ambiente virtual:**
```powershell
deactivate
```

### **Reinstalar dependências:**
```powershell
pip install -r requirements.txt --upgrade
```

### **Executar bot:**
```powershell
python run.py
```

### **Parar bot:**
- **F12** (dentro do jogo)
- **Ctrl+C** (no terminal)

---

## 🐛 **PROBLEMAS COMUNS**

### **Problema 1: "python não é reconhecido"**

**Causa:** Python não está no PATH

**Solução:**
1. Desinstale o Python
2. Reinstale marcando **"Add Python to PATH"** ✅
3. Reinicie o terminal

### **Problema 2: "pip não é reconhecido"**

**Solução:**
```powershell
python -m ensurepip --default-pip
```

### **Problema 3: "Activate.ps1 não pode ser carregado"**

**Solução (Como Administrador):**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### **Problema 4: "ModuleNotFoundError: No module named 'mss'"**

**Causa:** Ambiente virtual não ativado ou dependências não instaladas

**Solução:**
```powershell
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### **Problema 5: Instalação lenta**

**Solução:** Use mirror brasileiro:
```powershell
pip install -r requirements.txt -i https://pypi.python.org/simple/
```

---

## 📋 **CHECKLIST COMPLETO**

### **Instalação:**
- [ ] Python instalado (python --version funciona)
- [ ] pip instalado (pip --version funciona)
- [ ] Ambiente virtual criado (pasta venv existe)
- [ ] Ambiente virtual ativado (venv) aparece
- [ ] Dependências instaladas (sem erros)

### **Configuração:**
- [ ] config.yaml ajustado (região do jogo)
- [ ] Jogo aberto em modo janela
- [ ] Água visível na tela

### **Teste:**
- [ ] python run.py executa sem erros
- [ ] Bot detecta água (veja nos logs)
- [ ] F12 liga/desliga o bot
- [ ] Modo dry-run funcionando

### **Pronto para uso real:**
- [ ] Ajustou dry_run: false
- [ ] Testou em modo seguro primeiro
- [ ] Configurações otimizadas

---

## 🎯 **RESUMO RÁPIDO**

```powershell
# 1. Instalar Python 3.12
# https://www.python.org/downloads/

# 2. Verificar
python --version

# 3. Navegar
cd C:\Users\rodolpho.toppan\Desktop\marketplace-api

# 4. Criar ambiente
python -m venv venv

# 5. Ativar
.\venv\Scripts\Activate.ps1

# 6. Instalar
pip install -r requirements.txt

# 7. Configurar
# Editar config.yaml com posição do jogo

# 8. Executar
python run.py

# 9. Usar
# F12 para ligar/desligar
```

---

## 💡 **DICAS IMPORTANTES**

1. **Sempre ative o ambiente virtual** antes de executar:
   ```powershell
   .\venv\Scripts\Activate.ps1
   python run.py
   ```

2. **Execute o terminal como Administrador** para hotkeys funcionarem

3. **Comece em dry-run** e só mude depois de testar

4. **Ajuste as cores** da água se não detectar:
   ```yaml
   fishing:
     water_detection:
       hue_min: 100  # Ajustar
       hue_max: 140  # Ajustar
   ```

5. **Monitore os logs** para entender o que está acontecendo

---

## 📞 **PRECISA DE AJUDA?**

### **Verificar se tudo está OK:**
```powershell
# Teste completo
cd C:\Users\rodolpho.toppan\Desktop\marketplace-api
.\venv\Scripts\Activate.ps1
python -c "from src.configuration import load_settings; print('✓ Tudo OK!')"
```

Se mostrar `✓ Tudo OK!`, está tudo configurado corretamente!

---

## 🎉 **PRONTO!**

Depois de seguir esses passos, você terá:
- ✅ Python instalado
- ✅ Ambiente configurado
- ✅ Bot pronto para usar
- ✅ F12 funcionando

**Tempo estimado:** 15-30 minutos (primeira vez)

---

**Data:** 2026-07-14  
**Versão:** 1.0  
**Status:** Guia Completo de Instalação

