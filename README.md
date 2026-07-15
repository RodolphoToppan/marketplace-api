# 🎣 Local Game Automation - Fishing Bot

![Python](https://img.shields.io/badge/python-3.11+-blue.svg)
![Status](https://img.shields.io/badge/status-Ready%20for%20Testing-brightgreen.svg)
![License](https://img.shields.io/badge/license-Educational-orange.svg)

## ⚠️ Academic Purpose Only

This project is developed **exclusively for educational purposes** to learn about:
- Computer vision techniques (color detection, change detection)
- Automation and state machines
- Input simulation (keyboard and mouse)
- Decision-making based on visual input

**This automation is designed for use only with a local game environment developed for academic learning.**

---

## 🎯 Project Goal

**Automate the fishing action in a local game** using:
- **Color detection** to find water (blue areas)
- **Change detection** to identify bubbles
- **Keyboard simulation** to cast and pull the rod (Shift+Z)
- **Mouse positioning** over water
- **Hotkey control** (F12) to start/stop the bot

---

## 🎣 HOW IT WORKS

### Fishing Workflow:
```
1. Press F12 → Bot starts
2. Bot detects water (blue area)
3. Bot positions mouse over water
4. Bot presses Shift+Z (cast rod)
5. Bot waits for bubbles to appear
6. When bubbles detected → Bot presses Shift+Z (pull fish)
7. Bot waits for loot collection
8. Repeat from step 2
9. Press F12 again → Bot stops
```

---

## 📦 Installation

### 1. Navigate to project directory

```powershell
cd C:\Users\rodolpho.toppan\Desktop\marketplace-api
```

### 2. Create virtual environment

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```powershell
pip install -r requirements.txt
```

---

## ⚙️ Configuration

Edit `config.yaml`:

### Important Settings:

```yaml
execution:
  dry_run: true  # Set to false to enable REAL actions

regions:
  game_area:  # Adjust to match your game window
    x: 100
    y: 100
    width: 800
    height: 600

fishing:
  water_detection:
    hue_min: 100      # Blue color range
    hue_max: 140
  
  hotkeys:
    fishing_action: "shift+z"  # Cast and pull key
    toggle_bot: "f12"          # Start/stop bot
```

---

## 🚀 Usage

### Run the bot:

```powershell
python run.py
```

### Controls:
- **F12** → Start/Stop fishing
- **Ctrl+C** → Exit application

---

## 🛡️ Safety

- **Dry-run mode** enabled by default (no real actions)
- Set `dry_run: false` to enable real mode
- **F12** to toggle on/off anytime
- Move mouse to corner to abort (PyAutoGUI failsafe)

---

## 🔧 Troubleshooting

### "Could not detect water"
- Adjust `hue_min`/`hue_max` in config
- Make sure water is visible in game window

### "Bubble detection timeout"
- Increase `sensitivity` in config
- Increase `bubble_wait_max_ms`

### "Hotkey not working"
- Run terminal as Administrator
- Try different hotkey (f11, f10, etc.)

---

## 📖 Full Documentation

See `IMPLEMENTATION_SUMMARY.md` for complete technical details.

---

**Version:** 0.2.0  
**Status:** ✅ Ready for Testing  
**Last Updated:** 2026-07-14

