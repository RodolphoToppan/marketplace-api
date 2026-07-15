"""
Extrator de frames do GIF - Manual.
Extrai todos os frames para você escolher visualmente quais têm bolhas.
"""

import cv2
from pathlib import Path
import argparse


def extract_frames(gif_path: str, output_dir: str = "artifacts/gif_frames"):
    """
    Extrai todos os frames do GIF para análise manual.

    Args:
        gif_path: Caminho do arquivo GIF
        output_dir: Diretório para salvar frames
    """
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    print(f"🔍 Extraindo frames de: {gif_path}")

    cap = cv2.VideoCapture(gif_path)

    if not cap.isOpened():
        print(f"❌ Erro ao abrir GIF: {gif_path}")
        return

    frame_count = 0

    # Extrair todos os frames
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame_count += 1

        # Salvar frame com número grande e visível no nome
        frame_path = output_path / f"frame_{frame_count:03d}.png"
        cv2.imwrite(str(frame_path), frame)

        # Também salvar com anotação no frame
        annotated = frame.copy()
        cv2.putText(
            annotated,
            f"Frame #{frame_count}",
            (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            1.0,
            (0, 255, 0),
            2
        )
        annotated_path = output_path / f"annotated_frame_{frame_count:03d}.png"
        cv2.imwrite(str(annotated_path), annotated)

    cap.release()

    print(f"\n✅ Extraídos {frame_count} frames")
    print(f"📁 Salvos em: {output_path}")
    print(f"\n📋 PRÓXIMOS PASSOS:")
    print(f"   1. Abra a pasta: {output_path}")
    print(f"   2. Veja as imagens 'annotated_frame_XXX.png'")
    print(f"   3. Anote os números dos frames COM BOLHAS")
    print(f"   4. Execute: python analyze_gif_manual.py fishing_gameplay.gif --frames 5,12,18,23")
    print(f"      (substitua pelos números que você anotou)")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extrair frames do GIF para análise manual")
    parser.add_argument("gif_path", help="Caminho do arquivo GIF")
    parser.add_argument("--output", "-o", default="artifacts/gif_frames", help="Diretório de saída")

    args = parser.parse_args()

    extract_frames(args.gif_path, args.output)

