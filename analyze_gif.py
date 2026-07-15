"""
Analisador de GIF para detectar padrões de bolhas.
Extrai frames e analisa mudanças visuais para otimizar detecção.
"""

import cv2
import numpy as np
from pathlib import Path
import argparse


def analyze_gif(gif_path: str, output_dir: str = "artifacts/gif_analysis"):
    """
    Analisa GIF para encontrar padrões de bolhas.

    Args:
        gif_path: Caminho do arquivo GIF
        output_dir: Diretório para salvar análise
    """
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    print(f"🔍 Analisando GIF: {gif_path}")

    # Tentar carregar GIF com OpenCV
    cap = cv2.VideoCapture(gif_path)

    if not cap.isOpened():
        print(f"❌ Erro ao abrir GIF: {gif_path}")
        return

    frames = []
    frame_count = 0

    # Extrair todos os frames
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frames.append(frame)
        frame_count += 1

        # Salvar frame individual
        frame_path = output_path / f"frame_{frame_count:03d}.png"
        cv2.imwrite(str(frame_path), frame)

    cap.release()

    print(f"✅ Extraídos {frame_count} frames")

    if frame_count < 2:
        print("⚠️ Muito poucos frames para análise")
        return

    # Analisar mudanças entre frames consecutivos
    print("\n📊 Analisando mudanças entre frames...")

    changes = []
    for i in range(1, len(frames)):
        prev_gray = cv2.cvtColor(frames[i-1], cv2.COLOR_BGR2GRAY)
        curr_gray = cv2.cvtColor(frames[i], cv2.COLOR_BGR2GRAY)

        # Calcular diferença
        diff = cv2.absdiff(prev_gray, curr_gray)

        # Aplicar threshold
        _, thresh = cv2.threshold(diff, 15, 255, cv2.THRESH_BINARY)

        # Calcular percentual de mudança
        change_pixels = np.count_nonzero(thresh)
        total_pixels = thresh.shape[0] * thresh.shape[1]
        change_percent = (change_pixels / total_pixels) * 100

        changes.append(change_percent)

        print(f"Frame {i-1} → {i}: {change_percent:.2f}% mudança")

        # Salvar visualização da diferença
        diff_path = output_path / f"diff_{i-1:03d}_to_{i:03d}.png"
        cv2.imwrite(str(diff_path), thresh)

    # Encontrar maiores mudanças (prováveis bolhas)
    if changes:
        avg_change = np.mean(changes)
        max_change = np.max(changes)
        std_change = np.std(changes)

        print(f"\n📈 Estatísticas de mudança:")
        print(f"   Média: {avg_change:.2f}%")
        print(f"   Máxima: {max_change:.2f}%")
        print(f"   Desvio padrão: {std_change:.2f}%")

        # Detectar spikes (prováveis bolhas)
        threshold = avg_change + std_change
        bubble_frames = [i for i, c in enumerate(changes) if c > threshold]

        print(f"\n💧 Frames com provável bolha (mudança > {threshold:.2f}%):")
        for frame_idx in bubble_frames:
            print(f"   Frame {frame_idx} → {frame_idx+1}: {changes[frame_idx]:.2f}%")

        # Recomendações para config
        print(f"\n⚙️ Recomendações para config.yaml:")
        print(f"   sensitivity: {min(0.3, avg_change / 100):.2f}")
        print(f"   min_change_threshold: {max(10, int(avg_change / 2))}")

        # Criar imagem composta com frames de bolha
        if bubble_frames:
            print(f"\n💾 Salvando frames de bolha...")
            for idx in bubble_frames[:5]:  # Primeiras 5 bolhas
                if idx < len(frames) - 1:
                    bubble_frame = frames[idx + 1]
                    bubble_path = output_path / f"bubble_candidate_{idx:03d}.png"
                    cv2.imwrite(str(bubble_path), bubble_frame)
                    print(f"   Salvo: {bubble_path.name}")

    print(f"\n✅ Análise completa! Resultados em: {output_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Analisar GIF de pesca para otimizar detecção")
    parser.add_argument("gif_path", help="Caminho do arquivo GIF")
    parser.add_argument("--output", "-o", default="artifacts/gif_analysis", help="Diretório de saída")

    args = parser.parse_args()

    analyze_gif(args.gif_path, args.output)

