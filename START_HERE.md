# 🚀 INÍCIO RÁPIDO - SEM PYTHON INSTALADO

## ✅ **VOCÊ ESTÁ AQUI**

Você **não tem Python instalado** e quer usar o Fishing Bot.

---

## 📋 **O QUE VOCÊ PRECISA FAZER**

### **ETAPA 1: INSTALAR O PYTHON** ⏱️ 5-10 minutos

1. **Baixe o instalador:**
   - Link direto: https://www.python.org/ftp/python/3.12.10/python-3.12.10-amd64.exe
   - Ou acesse: https://www.python.org/downloads/

2. **Execute o instalador:**
   - ⚠️ **MUITO IMPORTANTE:** Marque **"Add Python to PATH"** ✅
   - Clique em **"Install Now"**
   - Aguarde 2-5 minutos

3. **Verifique a instalação:**
   - Abra o **PowerShell** ou **Terminal**
   - Digite: `python --version`
   - Deve mostrar: `Python 3.12.10`

**Se der erro:** Veja o arquivo `INSTALL_PYTHON.md` para detalhes.

---

### **ETAPA 2: CONFIGURAR O PROJETO** ⏱️ 5 minutos

Abra o **PowerShell** ou **Terminal** e execute:

```powershell
# 1. Navegar até a pasta do projeto
cd C:\Users\rodolpho.toppan\Desktop\marketplace-api

# 2. Criar ambiente virtual
python -m venv venv

# 3. Ativar ambiente virtual
.\venv\Scripts\Activate.ps1

# 4. Instalar dependências (aguarde 3-5 minutos)
pip install -r requirements.txt
```

**⚠️ Se der erro no passo 3:**
Execute como **Administrador** e rode:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```
Depois tente o passo 3 novamente.

---

### **ETAPA 3: CONFIGURAR A JANELA DO JOGO** ⏱️ 2 minutos

1. **Abra o jogo em modo janela** (não tela cheia)

2. **Execute o script auxiliar:**
   ```powershell
   python setup_window_position.py
   ```

3. **Siga as instruções** para capturar a posição da janela

4. **Copie os valores** para `config.yaml`

**OU configure manualmente:**
- Edite `config.yaml`
- Ajuste a seção `regions.game_area` com a posição da sua janela

---

### **ETAPA 4: TESTAR O BOT** ⏱️ 2 minutos

```powershell
# Execute o bot
python run.py
```

Você verá:
```
🎣 local-game-automation v0.2.0
...
🔒 Running in DRY-RUN mode (safe, no real actions)
...
✅ Bot ready! Press f12 to start fishing...
```

**No jogo:**
- Pressione **F12** → Bot inicia (modo seguro, não faz nada real)
- Observe os **logs** no terminal
- Pressione **F12** novamente → Bot para

---

## 🎮 **QUANDO ESTIVER PRONTO PARA O MODO REAL**

1. **Edite config.yaml:**
   ```yaml
   execution:
     dry_run: false  # CUIDADO!
   ```

2. **Execute:**
   ```powershell
   python run.py
   ```

3. **Confirme com "yes"**

4. **Pressione F12** no jogo

---

## 📚 **DOCUMENTAÇÃO COMPLETA**

- **INSTALL_PYTHON.md** → Guia completo de instalação do Python
- **QUICK_START.md** → Guia de início rápido
- **README.md** → Guia completo de uso
- **FISHING_BOT_SUMMARY.md** → Documentação técnica

---

## 🆘 **PRECISA DE AJUDA?**

### **Erro: "python não é reconhecido"**
→ Reinstale o Python marcando **"Add to PATH"** ✅

### **Erro: "Activate.ps1 não pode ser carregado"**
→ Execute como Admin: `Set-ExecutionPolicy RemoteSigned`

### **Erro: "ModuleNotFoundError"**
→ Ative o venv: `.\venv\Scripts\Activate.ps1`
→ Reinstale: `pip install -r requirements.txt`

### **Bot não detecta água**
→ Ajuste `hue_min` e `hue_max` em `config.yaml`

---

## ✅ **CHECKLIST RÁPIDO**

- [ ] Python 3.12 instalado
- [ ] Ambiente virtual criado
- [ ] Dependências instaladas
- [ ] config.yaml configurado
- [ ] Bot testado em dry-run
- [ ] Pronto para usar!

---

## 🎯 **TEMPO TOTAL ESTIMADO**

- **Instalação do Python:** 10 minutos
- **Configuração do projeto:** 10 minutos
- **Teste inicial:** 5 minutos
- **TOTAL:** ~25 minutos (primeira vez)

---

## 🎉 **DEPOIS DE CONFIGURADO**

Para usar nas próximas vezes:

```powershell
# 1. Navegar
cd C:\Users\rodolpho.toppan\Desktop\marketplace-api

# 2. Ativar ambiente
.\venv\Scripts\Activate.ps1

# 3. Executar
python run.py

# 4. No jogo: F12 para ligar/desligar
```

---

**Está tudo documentado e pronto para uso!**

🐍 Comece instalando o Python: https://www.python.org/downloads/

📖 Guia completo: Abra `INSTALL_PYTHON.md`

