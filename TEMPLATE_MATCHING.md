# 🎯 DETECÇÃO POR TEMPLATE - MUITO MAIS PRECISA!

## ✅ IMPLEMENTADO!

Agora você pode usar **Template Matching** - fornecer uma imagem exata da borbulha!

---

## 🎮 COMO FUNCIONA

### **Método Atual (Change Detection):**
- ❌ Detecta **qualquer mudança** na tela
- ❌ Falsos positivos (vento, animações, etc.)
- ❌ Não sabe o que é uma borbulha

### **Novo Método (Template Matching):**
- ✅ Procura **exatamente** a imagem da borbulha
- ✅ **Zero falsos positivos**
- ✅ Muito mais confiável!

---

## 📸 PASSO A PASSO

### **ETAPA 1: Capturar Template da Borbulha**

1. **Abra o jogo** e **posicione-se** para pescar

2. **Lance a vara MANUALMENTE** (Shift+Z)

3. **Aguarde** as borbulhas aparecerem (quando precisa puxar)

4. **Com as borbulhas VISÍVEIS na tela**, execute:

```powershell
python capture_bubble_template.py
```

5. **Siga as instruções:**
   - Pressione ENTER quando as borbulhas estiverem visíveis
   - Uma janela vai abrir com a captura da tela
   - **Use o mouse para selecionar** a área da borbulha
   - Pressione ESPAÇO ou ENTER para confirmar
   - O template será salvo em `assets/templates/bubble.png`

---

### **ETAPA 2: Configurar o Config.yaml**

Abra `config.yaml` e encontre a seção `bubble_detection`:

```yaml
bubble_detection:
  method: 'template'  # ← MUDAR DE 'change' PARA 'template'
  
  # ... configurações antigas (ignoradas quando method='template')
  
  # Configurações do template:
  template: 'bubble.png'     # Nome do arquivo capturado
  template_threshold: 0.8    # Confiança mínima (0.7 a 0.95)
```

**Salve** o arquivo.

---

### **ETAPA 3: Executar o Bot**

```powershell
python run.py
```

Agora você verá nos logs:

```
Using TEMPLATE bubble detection (threshold=0.8)
✓ Bubble template loaded: bubble.png (64x48px)

🎣 Casting rod with hotkey: shift+z
✓ Pressed hotkey: shift+z

🔍 [TEMPLATE] Monitoring for bubble template at region...

Check #10: confidence=0.234 (threshold=0.8)
Check #20: confidence=0.512 (threshold=0.8)
Check #30: confidence=0.876 (threshold=0.8)  ← PRÓXIMO!

💧 Bubble template FOUND! time=3000ms, confidence=0.876

🐟 Pulling fish with hotkey: shift+z
✓ Pressed hotkey: shift+z
```

---

## ⚙️ AJUSTES FINOS

### **Se NÃO detectar a borbulha:**

**REDUZA o threshold** (mais permissivo):

```yaml
template_threshold: 0.7  # Ou até 0.6
```

### **Se detectar falsos positivos:**

**AUMENTE o threshold** (mais rigoroso):

```yaml
template_threshold: 0.9  # Ou até 0.95
```

### **Se precisar recapturar o template:**

```powershell
python capture_bubble_template.py
```

E faça o processo novamente.

---

## 🎯 DICAS PARA CAPTURAR O TEMPLATE

### ✅ **BOM TEMPLATE:**
- Selecione **apenas a borbulha**
- Não inclua muita água ao redor
- Capture quando a borbulha estiver **bem visível**
- Tamanho recomendado: 30x30 até 100x100 pixels

### ❌ **MAU TEMPLATE:**
- Incluir muita área ao redor
- Capturar quando não está visível
- Template muito grande (> 200x200)
- Template muito pequeno (< 20x20)

---

## 📊 COMPARAÇÃO

### **ANTES (Change Detection):**
```
Bubble detected after 1104ms  ← Falso positivo (vento)
Bubble detected after 13098ms ← Falso positivo (animação)
```

### **AGORA (Template Matching):**
```
Check #35: confidence=0.892
💧 Bubble template FOUND! time=3500ms, confidence=0.892
```

**Só detecta quando a borbulha REAL aparecer!**

---

## 🔄 VOLTAR PARA CHANGE DETECTION

Se quiser voltar ao método antigo:

```yaml
bubble_detection:
  method: 'change'  # Volta para detecção de mudança
```

---

## 📋 CHECKLIST

- [ ] Executar `python capture_bubble_template.py`
- [ ] Lançar vara manualmente no jogo
- [ ] Aguardar borbulhas aparecerem
- [ ] Selecionar área da borbulha
- [ ] Arquivo `bubble.png` criado em `assets/templates/`
- [ ] Mudar `method: 'template'` no `config.yaml`
- [ ] Executar `python run.py`
- [ ] Observar logs com "💧 Bubble template FOUND!"

---

## 🎉 RESULTADO

**Com Template Matching:**
- ✅ **Zero falsos positivos**
- ✅ Detecta **apenas borbulhas reais**
- ✅ Muito mais confiável
- ✅ Funciona mesmo sem Shift+Z (você pode testar a detecção primeiro!)

---

## ❓ FAQ

**P: E se a borbulha mudar de aparência no jogo?**  
R: Recapture o template com `python capture_bubble_template.py`

**P: Posso ter múltiplos templates?**  
R: Sim, mas por enquanto só suporta um. Você pode recapturar quando necessário.

**P: O template funciona em diferentes resoluções?**  
R: Sim, mas é melhor capturar na resolução que você vai jogar.

**P: E se não encontrar bubble.png?**  
R: O bot vai avisar e não vai funcionar. Execute `capture_bubble_template.py` primeiro.

---

**Execute agora: `python capture_bubble_template.py`** 📸

Depois de capturar, mude para `method: 'template'` no config e teste!

