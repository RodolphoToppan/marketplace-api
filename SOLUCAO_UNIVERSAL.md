# 🔧 SOLUÇÃO UNIVERSAL - FUNCIONA EM QUALQUER CAMINHO

## ✅ Arquivos Criados para Você

Criei 2 scripts **`.bat`** que funcionam em **qualquer lugar**:

### 📦 **install.bat**
- Instala tudo automaticamente
- Funciona em qualquer pasta
- Não precisa digitar comandos

### 🚀 **start_bot.bat**
- Inicia o bot
- Não precisa ativar venv manualmente

---

## 🎯 COMO USAR (Super Simples)

### **Opção 1: Scripts Automáticos (Recomendado)**

1. **Duplo clique** em `install.bat`
2. Aguarde a instalação (3-5 minutos)
3. Depois, **duplo clique** em `start_bot.bat`
4. Pronto! Pressione F12 no jogo

### **Opção 2: Manual (Se preferir)**

No PowerShell, **na pasta do projeto**:

```powershell
# 1. Limpar ambiente antigo
Remove-Item -Recurse -Force venv -ErrorAction SilentlyContinue

# 2. Criar ambiente virtual
python -m venv venv

# 3. Ativar
.\venv\Scripts\Activate.ps1

# 4. Atualizar ferramentas (IMPORTANTE!)
python -m pip install --upgrade pip setuptools wheel

# 5. Instalar dependências
pip install -r requirements.txt

# 6. Executar
python run.py
```

---

## 🐛 SE DER ERRO NO PASSO 4 (setuptools)

Execute isto ANTES de instalar as dependências:

```powershell
python -m pip install --upgrade pip setuptools wheel
```

Depois:

```powershell
pip install -r requirements.txt
```

---

## 📋 COMANDOS UNIVERSAIS

**Estes comandos funcionam em QUALQUER pasta onde você tenha o projeto:**

### Windows (PowerShell):
```powershell
cd [CAMINHO_DO_SEU_PROJETO]
Remove-Item -Recurse -Force venv -ErrorAction SilentlyContinue
python -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
python run.py
```

### Windows (CMD):
```cmd
cd [CAMINHO_DO_SEU_PROJETO]
rmdir /s /q venv
python -m venv venv
venv\Scripts\activate.bat
python -m pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
python run.py
```

---

## ✅ RESUMO

**Mais fácil:**
1. Duplo clique em `install.bat`
2. Duplo clique em `start_bot.bat`

**Manual:**
1. Abra PowerShell na pasta do projeto
2. Execute os comandos acima

---

## 🔑 A SOLUÇÃO DO SEU PROBLEMA

O erro era porque:
- `numpy==1.24.3` não tem wheel para Python 3.12
- Tentou compilar mas `setuptools` não estava instalado

**Já corrigi:**
- ✅ `requirements.txt` atualizado com versões flexíveis
- ✅ Scripts `.bat` instalam `setuptools` automaticamente
- ✅ Funciona em **qualquer caminho**

---

**Use o install.bat agora!** 🚀

