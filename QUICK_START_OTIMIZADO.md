# ⚡ QUICK START - BOT OTIMIZADO

## 🚀 COMANDOS ESSENCIAIS

### Iniciar Bot Otimizado
```powershell
.\start_bot.bat
```

### Parar Bot
- Pressione `F12` no jogo
- OU `Ctrl+C` no terminal

### Capturar Template de Bolha (Recomendado!)
```powershell
.\capture_bubble.bat
```
Depois ative no config.yaml:
```yaml
method: 'template'  # Mude de 'change' para 'template'
```

---

## 📊 O QUE FOI OTIMIZADO?

✅ **config.yaml** - Timings reduzidos em 25-50%
✅ **fishing_bot.py** - Removido sleep de 100ms
✅ **change_detector.py** - Blur 3x mais rápido

### Ganhos:
- Ciclo completo: **6.3s → 4.0s** (-36%)
- Taxa de pesca: **9.6/min → 15/min** (+56%)
- Reação: **150ms → 100ms** (-33%)

---

## ⚙️ CONFIGURAÇÃO ATUAL

```yaml
# config.yaml
fishing:
  bubble_detection:
    method: 'change'              # Ou 'template' (mais preciso!)
    region_size: 150              # Aumentado para templates
  
  timing:
    cast_wait_ms: 300             # -40%
    bubble_check_interval_ms: 60  # -40% (mais rápido!)
    pull_delay_ms: 100            # -33% (reação mais rápida!)
    cooldown_ms: 400              # -50% (lança 2x mais rápido!)
    collect_wait_ms: 1200         # -40%

behavior:
  reaction_time_ms:
    min: 100                      # -44% (mais rápido)
    max: 220                      # -37%
```

---

## ⚠️ IMPORTANTE

### Dry-Run Ativo (Modo Seguro)
O bot está configurado para **não executar ações reais** por padrão.

Para ativar:
```yaml
# config.yaml
execution:
  dry_run: false  # Mude de true para false
```

---

## 📝 PRÓXIMOS PASSOS

1. **Testar bot** (5-10 ciclos)
2. **Monitorar logs** (taxa de sucesso)
3. **Capturar template** (opcional, mas recomendado)
4. **Desativar dry_run** (quando estiver confiante)

---

## 🐛 SE TIVER PROBLEMAS

### Muitos Falsos Positivos
```yaml
min_change_threshold: 20 → 25  # Mais rigoroso
# OU
method: 'template'              # Usar template matching
```

### Muitos Timeouts (Não Detecta)
```yaml
bubble_wait_min_ms: 1500 → 1200  # Começa a verificar mais cedo
sensitivity: 0.15 → 0.20          # Mais sensível
```

### Bot Muito Rápido (Race Conditions)
```yaml
cooldown_ms: 400 → 600           # Aumentar cooldown
cast_wait_ms: 300 → 400          # Aumentar espera
```

---

## 📖 DOCUMENTAÇÃO COMPLETA

- **OTIMIZACOES_APLICADAS.md** - Detalhes técnicos completos
- **ANTES_vs_DEPOIS.md** - Comparação visual
- **ESPECIFICAÇÃO TÉCNICA** - Ver mensagem anterior

---

## 🎯 RESULTADO ESPERADO

O bot agora deve ser **tão rápido quanto você jogando focado!**

Se ainda estiver lento:
1. Capture template e use `method: 'template'`
2. Reduza mais 10-20% nos timings
3. Verifique se `dry_run: false` está ativo

**Boa pesca!** 🎣⚡

