"""
Script auxiliar para descobrir a posição da janela do jogo.
Execute este script e siga as instruções para configurar o config.yaml.
"""

import time
import sys

print("=" * 70)
print("🎮 AUXILIAR DE CONFIGURAÇÃO - POSIÇÃO DA JANELA DO JOGO")
print("=" * 70)
print()

# Verificar se pyautogui está instalado
try:
    import pyautogui
except ImportError:
    print("❌ PyAutoGUI não está instalado!")
    print()
    print("Execute primeiro:")
    print("  pip install pyautogui")
    print()
    sys.exit(1)

print("Este script ajuda a descobrir a posição e tamanho da janela do jogo.")
print()
print("INSTRUÇÕES:")
print("1. Abra o jogo em MODO JANELA (não tela cheia)")
print("2. Posicione a janela onde você quer que fique")
print("3. Siga as instruções abaixo")
print()
print("=" * 70)
print()

# Passo 1: Canto superior esquerdo
input("Pressione ENTER quando estiver pronto para começar...")
print()
print("PASSO 1: CANTO SUPERIOR ESQUERDO")
print("-" * 70)
print("Em 5 segundos, mova o mouse para o CANTO SUPERIOR ESQUERDO da")
print("janela do jogo (borda superior esquerda).")
print()

for i in range(5, 0, -1):
    print(f"  {i}...", end="\r")
    time.sleep(1)

x1, y1 = pyautogui.position()
print(f"✓ Posição capturada: x={x1}, y={y1}")
print()

# Passo 2: Canto inferior direito
input("Pressione ENTER para continuar para o próximo passo...")
print()
print("PASSO 2: CANTO INFERIOR DIREITO")
print("-" * 70)
print("Em 5 segundos, mova o mouse para o CANTO INFERIOR DIREITO da")
print("janela do jogo (borda inferior direita).")
print()

for i in range(5, 0, -1):
    print(f"  {i}...", end="\r")
    time.sleep(1)

x2, y2 = pyautogui.position()
print(f"✓ Posição capturada: x={x2}, y={y2}")
print()

# Calcular dimensões
width = x2 - x1
height = y2 - y1

# Mostrar resultados
print("=" * 70)
print("📊 RESULTADOS")
print("=" * 70)
print()
print("Copie estes valores para o seu config.yaml:")
print()
print("regions:")
print("  game_area:")
print(f"    x: {x1}")
print(f"    y: {y1}")
print(f"    width: {width}")
print(f"    height: {height}")
print()
print("=" * 70)
print()

# Perguntar se quer testar captura
try:
    import cv2
    import mss
    import numpy as np

    resposta = input("Deseja testar a captura desta região? (s/n): ").lower()

    if resposta == 's':
        print()
        print("Capturando região em 3 segundos...")
        time.sleep(3)

        with mss.mss() as sct:
            monitor = {
                "left": x1,
                "top": y1,
                "width": width,
                "height": height
            }
            screenshot = sct.grab(monitor)
            img = np.array(screenshot)

            # Salvar
            test_file = "test_capture.png"
            cv2.imwrite(test_file, img)
            print(f"✓ Captura salva em: {test_file}")
            print("  Abra o arquivo para verificar se capturou a área correta!")
            print()

except ImportError:
    print("ℹ️  Instale opencv-python e mss para testar a captura:")
    print("  pip install opencv-python mss")
    print()

print("=" * 70)
print("✅ CONFIGURAÇÃO COMPLETA!")
print("=" * 70)
print()
print("Próximos passos:")
print("1. Copie os valores acima para config.yaml")
print("2. Execute: python run.py")
print("3. Pressione F12 no jogo para iniciar")
print()

