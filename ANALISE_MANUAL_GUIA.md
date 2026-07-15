# 🎯 ANÁLISE MANUAL DE BOLHAS - GUIA RÁPIDO

## ❌ PROBLEMA

O script automático `analyze_gif.py` não detectou as bolhas corretamente - está detectando o mouse em vez das bolhas.

## ✅ SOLUÇÃO: MODO MANUAL

Criei 2 scripts novos que permitem **VOCÊ escolher** quais frames têm bolhas!

---

## 📋 PASSO A PASSO

### **1. Extrair todos os frames do GIF**

```powershell
.\extract_frames.bat fishing_gameplay.gif
```

Isso vai:
- Extrair todos os frames do GIF
- Salvar em: `artifacts/gif_frames/`
- Criar versões anotadas com o número do frame visível

---

### **2. Visualizar e anotar frames com bolhas**

1. Abra a pasta: `artifacts\gif_frames\`
2. Veja as imagens `annotated_frame_XXX.png`
3. **Anote os números** dos frames que CONTÊM BOLHAS

**Exemplo:**
```
Frame 005 - sem bolha
Frame 006 - sem bolha
Frame 007 - COM BOLHA! ✅ (anotar: 7)
Frame 008 - sem bolha
...
Frame 015 - COM BOLHA! ✅ (anotar: 15)
Frame 016 - sem bolha
...
Frame 023 - COM BOLHA! ✅ (anotar: 23)
```

Sua lista: `7,15,23`

---

### **3. Analisar apenas os frames selecionados**

```powershell
.\analyze_bubble_manual.bat fishing_gameplay.gif 7,15,23
```

Substitua `7,15,23` pelos números que você anotou!

---

## 📊 O QUE VAI ACONTECER

O script vai:
1. ✅ Extrair apenas os frames que você indicou
2. ✅ Comparar com frames anteriores (sem bolha)
3. ✅ Testar diferentes thresholds (10, 15, 20, 25, 30)
4. ✅ Calcular estatísticas de mudança visual
5. ✅ **RECOMENDAR valores ótimos** para `config.yaml`:
   - `sensitivity`
   - `min_change_threshold`
6. ✅ Salvar visualizações das diferenças

---

## 📁 RESULTADOS

Salvos em: `artifacts/bubble_analysis/`

### Arquivos gerados:
- `bubble_frame_XXX.png` - Frames com bolhas
- `diff_frame_XXX_thresh_YY.png` - Visualização das diferenças

### Recomendações no console:
```
⚙️ RECOMENDAÇÕES PARA config.yaml:

   Opção CONSERVADORA (menos falsos positivos):
   bubble_detection:
     sensitivity: 0.20
     min_change_threshold: 20

   Opção EQUILIBRADA:
   bubble_detection:
     sensitivity: 0.25
     min_change_threshold: 15

   Opção AGRESSIVA (detecta tudo):
   bubble_detection:
     sensitivity: 0.30
     min_change_threshold: 10

   🎯 RECOMENDAÇÃO BASEADA NOS SEUS DADOS:
   bubble_detection:
     sensitivity: 0.28
     min_change_threshold: 15
     region_size: 150
```

---

## 🚀 APLICAR AS RECOMENDAÇÕES

Edite `config.yaml` e aplique os valores recomendados:

```yaml
fishing:
  bubble_detection:
    sensitivity: 0.28              # ← Valor recomendado
    min_change_threshold: 15       # ← Valor recomendado
    region_size: 150
```

Depois teste:
```powershell
.\start_bot.bat
```

---

## 💡 DICAS

### Como escolher os frames corretos?
- ✅ Procure frames onde a **bolha é VISÍVEL**
- ✅ Compare com frames adjacentes (antes/depois)
- ✅ Se tiver dúvida, inclua o frame (melhor sobrar que faltar)
- ❌ NÃO inclua frames com mouse, menus, ou outras mudanças

### Quantos frames preciso?
- **Mínimo**: 3-5 frames com bolhas
- **Ideal**: 8-10 frames com bolhas
- **Máximo**: Não há limite, mas 10-15 já é suficiente

### E se não souber os números exatos?
1. Extraia os frames: `.\extract_frames.bat fishing_gameplay.gif`
2. Veja as imagens na pasta `artifacts\gif_frames\`
3. As imagens têm o número do frame no NOME e dentro da imagem
4. Anote os números e use no próximo comando

---

## 🔧 COMANDOS RESUMIDOS

```powershell
# Passo 1: Extrair frames
.\extract_frames.bat fishing_gameplay.gif

# Passo 2: Visualizar e anotar (manual)
# Abrir: artifacts\gif_frames\
# Anotar números dos frames com bolhas

# Passo 3: Analisar frames selecionados
.\analyze_bubble_manual.bat fishing_gameplay.gif 7,15,23,31,42

# Passo 4: Aplicar recomendações no config.yaml

# Passo 5: Testar bot
.\start_bot.bat
```

---

## ❓ FAQ

**P: Posso analisar apenas 1 frame?**
R: Sim, mas não vai ter estatísticas boas. Recomendo no mínimo 3-5 frames.

**P: E se eu errar e incluir frames sem bolha?**
R: Não tem problema! O script vai analisar e você verá pelas imagens `diff_` se tem mudança significativa.

**P: Preciso refazer tudo se mudar os frames?**
R: Não! Os frames já estão extraídos em `artifacts/gif_frames/`. Só execute o passo 3 novamente com novos números.

**P: Posso usar espaços entre os números?**
R: Sim! Tanto `7,15,23` quanto `7, 15, 23` funcionam.

---

## 🎉 VANTAGENS DO MODO MANUAL

✅ **100% preciso** - Você escolhe exatamente os frames com bolhas
✅ **Sem falsos positivos** - Não detecta mouse, menus, etc.
✅ **Valores otimizados** - Recomendações baseadas nos seus dados reais
✅ **Fácil de usar** - Scripts `.bat` automatizam tudo
✅ **Reutilizável** - Extraia frames 1x, analise quantas vezes quiser

---

## 🚀 COMECE AGORA!

```powershell
.\extract_frames.bat fishing_gameplay.gif
```

Depois me diga quantos frames você encontrou com bolhas! 🎣

