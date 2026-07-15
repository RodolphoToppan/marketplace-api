"""
Script para capturar templates de borbulhas.
Use este script para criar imagens que o bot vai procurar.
"""

import cv2
import numpy as np
import mss
import time
from pathlib import Path

print("=" * 70)
print("  CAPTURADOR DE TEMPLATE - BORBULHAS")
print("=" * 70)
print()
print("Este script ajuda a capturar a imagem da borbulha para detecção precisa.")
print()
print("INSTRUÇÕES:")
print("1. Abra o jogo e lance a vara manualmente")
print("2. Aguarde as borbulhas aparecerem")
print("3. Quando as borbulhas estiverem VISÍVEIS:")
print("   - Pressione ENTER neste terminal")
print("4. O script vai capturar a tela")
print("5. Você poderá selecionar a área da borbulha com o mouse")
print()
print("=" * 70)
print()

# Esperar usuário preparar
input("Pressione ENTER quando as borbulhas estiverem VISÍVEIS na tela...")

print()
print("Capturando tela em 3 segundos...")
print("Posicione a tela do jogo de forma que as borbulhas estejam visíveis!")
print()

for i in range(3, 0, -1):
    print(f"  {i}...")
    time.sleep(1)

# Capturar tela inteira
with mss.mss() as sct:
    monitor = sct.monitors[1]  # Monitor principal
    screenshot = sct.grab(monitor)
    img = np.array(screenshot)
    img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)

print()
print("✓ Tela capturada!")
print()
print("=" * 70)
print("  SELEÇÃO DE REGIÃO")
print("=" * 70)
print()
print("INSTRUÇÕES:")
print("1. Uma janela vai abrir com a captura da tela")
print("2. Use o MOUSE para selecionar a área da BORBULHA")
print("   - Clique e arraste para criar um retângulo")
print("3. Pressione ESPAÇO ou ENTER quando estiver satisfeito")
print("4. Pressione 'r' para recomeçar a seleção")
print("5. Pressione ESC para cancelar")
print()
print("DICA: Selecione apenas a BORBULHA, não a água ao redor!")
print()

# Variáveis para seleção
roi = None
x_start, y_start, x_end, y_end = 0, 0, 0, 0
selecting = False
img_copy = img.copy()

def select_roi(event, x, y, flags, param):
    global x_start, y_start, x_end, y_end, selecting, img_copy

    if event == cv2.EVENT_LBUTTONDOWN:
        x_start, y_start = x, y
        selecting = True

    elif event == cv2.EVENT_MOUSEMOVE:
        if selecting:
            img_copy = img.copy()
            cv2.rectangle(img_copy, (x_start, y_start), (x, y), (0, 255, 0), 2)

    elif event == cv2.EVENT_LBUTTONUP:
        x_end, y_end = x, y
        selecting = False
        img_copy = img.copy()
        cv2.rectangle(img_copy, (x_start, y_start), (x_end, y_end), (0, 255, 0), 2)

# Redimensionar se a imagem for muito grande
height, width = img.shape[:2]
max_width = 1280
if width > max_width:
    scale = max_width / width
    new_width = int(width * scale)
    new_height = int(height * scale)
    display_img = cv2.resize(img, (new_width, new_height))
    scale_factor = scale
else:
    display_img = img.copy()
    scale_factor = 1.0

cv2.namedWindow('Selecione a BORBULHA', cv2.WINDOW_NORMAL)
cv2.setMouseCallback('Selecione a BORBULHA', select_roi)

while True:
    if scale_factor != 1.0:
        display = cv2.resize(img_copy, (int(width * scale_factor), int(height * scale_factor)))
    else:
        display = img_copy

    cv2.imshow('Selecione a BORBULHA', display)

    key = cv2.waitKey(1) & 0xFF

    # ESC para cancelar
    if key == 27:
        print("\n❌ Cancelado pelo usuário")
        cv2.destroyAllWindows()
        exit(0)

    # 'r' para resetar
    elif key == ord('r'):
        img_copy = img.copy()
        x_start, y_start, x_end, y_end = 0, 0, 0, 0
        print("Seleção resetada. Selecione novamente.")

    # ESPAÇO ou ENTER para confirmar
    elif key == 32 or key == 13:  # SPACE or ENTER
        if x_end > x_start and y_end > y_start:
            break
        else:
            print("Selecione uma área válida primeiro!")

cv2.destroyAllWindows()

# Extrair ROI
x1 = min(x_start, x_end)
y1 = min(y_start, y_end)
x2 = max(x_start, x_end)
y2 = max(y_start, y_end)

roi = img[y1:y2, x1:x2]

if roi.size == 0:
    print("\n❌ Região inválida!")
    exit(1)

print()
print("✓ Região selecionada!")
print(f"  Tamanho: {roi.shape[1]}x{roi.shape[0]} pixels")
print()

# Mostrar preview
cv2.namedWindow('Preview do Template', cv2.WINDOW_NORMAL)
cv2.imshow('Preview do Template', roi)
print("Visualize o template capturado.")
print("Pressione qualquer tecla para continuar...")
cv2.waitKey(0)
cv2.destroyAllWindows()

# Salvar template
templates_dir = Path("assets/templates")
templates_dir.mkdir(parents=True, exist_ok=True)

template_path = templates_dir / "bubble.png"
cv2.imwrite(str(template_path), roi)

print()
print("=" * 70)
print("  ✅ TEMPLATE SALVO COM SUCESSO!")
print("=" * 70)
print()
print(f"Arquivo: {template_path}")
print(f"Tamanho: {roi.shape[1]}x{roi.shape[0]} pixels")
print()
print("PRÓXIMOS PASSOS:")
print()
print("1. Abra o arquivo config.yaml")
print()
print("2. Encontre a seção 'bubble_detection' e altere:")
print()
print("   bubble_detection:")
print("     method: 'template'  # Mudar de 'change' para 'template'")
print("     template: 'bubble.png'")
print("     threshold: 0.8  # Ajuste se necessário (0.7 a 0.95)")
print()
print("3. Execute o bot normalmente: python run.py")
print()
print("4. Se não detectar, REDUZA o threshold (ex: 0.7)")
print("   Se detectar muito (falsos positivos), AUMENTE (ex: 0.9)")
print()
print("=" * 70)
print()
input("Pressione ENTER para sair...")

