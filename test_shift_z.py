"""
Script de teste para verificar se o Shift+Z está funcionando.
Execute este script e depois pressione Shift+Z manualmente.
Se funcionar, o problema pode ser com o jogo bloqueando inputs sintéticos.
"""

import time
import keyboard

print("=" * 70)
print("TESTE DE SHIFT+Z")
print("=" * 70)
print()
print("Este script vai:")
print("1. Aguardar 3 segundos")
print("2. Pressionar Shift+Z automaticamente")
print("3. Mostrar se funcionou")
print()
print("PREPARE-SE: Foque na janela do jogo em 5 segundos...")
print()

for i in range(5, 0, -1):
    print(f"  {i}...", end="\r")
    time.sleep(1)

print("\n")
print("Enviando Shift+Z...")

try:
    # Método 1: keyboard library (mais compatível com jogos)
    keyboard.press_and_release('shift+z')
    print("✓ Shift+Z enviado com keyboard library")
    time.sleep(0.5)

except Exception as e:
    print(f"❌ Erro ao enviar Shift+Z: {e}")

print()
print("=" * 70)
print("RESULTADO:")
print("=" * 70)
print()
print("Se a vara foi lançada no jogo:")
print("  ✓ As teclas ESTÃO funcionando!")
print("  ✓ O bot DEVERIA estar funcionando também")
print("  → Pode ser necessário rodar como Administrador")
print()
print("Se a vara NÃO foi lançada:")
print("  ❌ O jogo pode estar bloqueando inputs sintéticos")
print("  → Tente executar este script como Administrador")
print("  → Alguns jogos não aceitam teclas de automação")
print()
input("Pressione Enter para sair...")

