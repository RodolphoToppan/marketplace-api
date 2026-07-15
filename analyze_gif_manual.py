"""
Analisador de GIF - Modo Manual.
Analisa apenas os frames que você especificar como contendo bolhas.
"""

import cv2
import numpy as np
from pathlib import Path
import argparse


def analyze_bubble_frames(gif_path: str, frame_numbers: list, output_dir: str = "artifacts/bubble_analysis"):
    """
    Analisa frames específicos que contêm bolhas.

    Args:
        gif_path: Caminho do arquivo GIF
        frame_numbers: Lista de números dos frames com bolhas
        output_dir: Diretório para salvar análise
    """
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    print(f"🔍 Analisando frames selecionados de: {gif_path}")
    print(f"📋 Frames com bolhas: {frame_numbers}")

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
        frame_count += 1
        frames.append((frame_count, frame))

    cap.release()

    print(f"✅ Total de frames: {frame_count}")

    # Analisar frames selecionados
    bubble_frames = [f for f in frames if f[0] in frame_numbers]

    if not bubble_frames:
        print(f"⚠️ Nenhum dos frames especificados foi encontrado no GIF")
        return

    print(f"\n💧 Analisando {len(bubble_frames)} frames com bolhas...")

    # Salvar frames de bolha
    for idx, (frame_num, frame) in enumerate(bubble_frames):
        bubble_path = output_path / f"bubble_frame_{frame_num:03d}.png"
        cv2.imwrite(str(bubble_path), frame)
        print(f"   Salvo: bubble_frame_{frame_num:03d}.png (Frame #{frame_num})")

    # Analisar características dos frames com bolhas
    print(f"\n📊 Analisando características das bolhas...")

    # Comparar frames COM bolha vs frames SEM bolha (anteriores)
    changes = []

    for frame_num, bubble_frame in bubble_frames:
        if frame_num > 1:
            # Pegar frame anterior (sem bolha)
            prev_frame = frames[frame_num - 2][1]  # -2 porque lista é 0-indexed

            # Converter para grayscale
            prev_gray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)
            bubble_gray = cv2.cvtColor(bubble_frame, cv2.COLOR_BGR2GRAY)

            # Calcular diferença
            diff = cv2.absdiff(prev_gray, bubble_gray)

            # Testar diferentes thresholds
            for thresh_val in [10, 15, 20, 25, 30]:
                _, thresh = cv2.threshold(diff, thresh_val, 255, cv2.THRESH_BINARY)

                change_pixels = np.count_nonzero(thresh)
                total_pixels = thresh.shape[0] * thresh.shape[1]
                change_percent = (change_pixels / total_pixels) * 100

                changes.append({
                    'frame': frame_num,
                    'threshold': thresh_val,
                    'change_percent': change_percent
                })

                # Salvar visualização da diferença
                diff_path = output_path / f"diff_frame_{frame_num:03d}_thresh_{thresh_val}.png"
                cv2.imwrite(str(diff_path), thresh)

    # Estatísticas
    if changes:
        print(f"\n📈 Estatísticas de mudança por threshold:")

        for thresh_val in [10, 15, 20, 25, 30]:
            changes_at_thresh = [c['change_percent'] for c in changes if c['threshold'] == thresh_val]
            avg_change = np.mean(changes_at_thresh)
            min_change = np.min(changes_at_thresh)
            max_change = np.max(changes_at_thresh)

            print(f"\n   Threshold {thresh_val}:")
            print(f"      Mudança média: {avg_change:.2f}%")
            print(f"      Mudança mínima: {min_change:.2f}%")
            print(f"      Mudança máxima: {max_change:.2f}%")

        # Recomendações
        print(f"\n⚙️ RECOMENDAÇÕES PARA config.yaml:")
        print(f"\n   Opção CONSERVADORA (menos falsos positivos):")
        print(f"   bubble_detection:")
        print(f"     sensitivity: 0.20")
        print(f"     min_change_threshold: 20")

        print(f"\n   Opção EQUILIBRADA:")
        print(f"   bubble_detection:")
        print(f"     sensitivity: 0.25")
        print(f"     min_change_threshold: 15")

        print(f"\n   Opção AGRESSIVA (detecta tudo):")
        print(f"   bubble_detection:")
        print(f"     sensitivity: 0.30")
        print(f"     min_change_threshold: 10")

        # Recomendação específica baseada nos dados
        best_thresh = 15
        changes_at_best = [c['change_percent'] for c in changes if c['threshold'] == best_thresh]
        avg_at_best = np.mean(changes_at_best)

        recommended_sensitivity = min(0.35, max(0.15, avg_at_best / 100))

        print(f"\n   🎯 RECOMENDAÇÃO BASEADA NOS SEUS DADOS:")
        print(f"   bubble_detection:")
        print(f"     sensitivity: {recommended_sensitivity:.2f}")
        print(f"     min_change_threshold: {best_thresh}")
        print(f"     region_size: 150")

    print(f"\n✅ Análise completa! Resultados em: {output_path}")
    print(f"\n💡 PRÓXIMO PASSO:")
    print(f"   1. Veja as imagens 'diff_frame_XXX_thresh_YY.png'")
    print(f"   2. Escolha o threshold que destaca melhor as bolhas")
    print(f"   3. Aplique os valores recomendados no config.yaml")
    print(f"   4. Teste o bot: .\\start_bot.bat")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Analisar frames específicos com bolhas")
    parser.add_argument("gif_path", help="Caminho do arquivo GIF")
    parser.add_argument("--frames", "-f", required=True, help="Números dos frames com bolhas (ex: 5,12,18,23)")
    parser.add_argument("--output", "-o", default="artifacts/bubble_analysis", help="Diretório de saída")

    args = parser.parse_args()

    # Converter string "5,12,18,23" para lista [5, 12, 18, 23]
    try:
        frame_numbers = [int(x.strip()) for x in args.frames.split(',')]
    except ValueError:
        print("❌ Erro: --frames deve ser uma lista de números separados por vírgula")
        print("   Exemplo: --frames 5,12,18,23")
        exit(1)

    analyze_bubble_frames(args.gif_path, frame_numbers, args.output)

