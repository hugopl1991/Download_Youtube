#!/usr/bin/env python3
"""
Baixador de vídeos do YouTube — com merge automático de vídeo + áudio
Dependências: pip install yt-dlp requests

O ffmpeg é baixado automaticamente se não estiver instalado (Windows).
"""

import os
import sys
import shutil
import zipfile
import requests
import yt_dlp


# ──────────────────────────────────────────────
#  CONFIGURAÇÃO — edite aqui antes de rodar
# ──────────────────────────────────────────────

URL = "https://www.youtube.com/live/4x-r3jGoOvE"
PASTA = "meus_videos_youtube"
QUALIDADE = "melhor"   # 'melhor', 'menor', '1080', '720', '480', '360'

# ──────────────────────────────────────────────


FFMPEG_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ffmpeg_bin")
FFMPEG_EXE = os.path.join(FFMPEG_DIR, "ffmpeg.exe")


def verificar_ou_baixar_ffmpeg() -> str:
    """
    Retorna o caminho do executável ffmpeg.
    Tenta, em ordem:
      1. ffmpeg já no PATH do sistema
      2. ffmpeg_bin/ffmpeg.exe ao lado do script
      3. Baixa automaticamente o build estático do ffmpeg para Windows
    """
    # 1. Já está no PATH?
    if shutil.which("ffmpeg"):
        print("✅ ffmpeg encontrado no PATH do sistema.")
        return shutil.which("ffmpeg")

    # 2. Já baixamos antes?
    if os.path.isfile(FFMPEG_EXE):
        print("✅ ffmpeg encontrado em ffmpeg_bin/")
        return FFMPEG_EXE

    # 3. Baixar automaticamente
    print("⬇  ffmpeg não encontrado. Baixando automaticamente (uma única vez)...")
    print("   Isso pode demorar alguns segundos dependendo da sua conexão.\n")

    # Build estático oficial mantido pela comunidade yt-dlp
    url_zip = (
        "https://github.com/yt-dlp/FFmpeg-Builds/releases/download/latest/"
        "ffmpeg-master-latest-win64-gpl.zip"
    )

    os.makedirs(FFMPEG_DIR, exist_ok=True)
    zip_path = os.path.join(FFMPEG_DIR, "ffmpeg.zip")

    try:
        resp = requests.get(url_zip, stream=True, timeout=60)
        resp.raise_for_status()
        total = int(resp.headers.get("content-length", 0))
        baixado = 0

        with open(zip_path, "wb") as f:
            for chunk in resp.iter_content(chunk_size=1024 * 256):
                f.write(chunk)
                baixado += len(chunk)
                if total:
                    pct = baixado / total * 100
                    print(f"\r   {pct:.1f}%  ({baixado // 1_048_576} / {total // 1_048_576} MB)", end="", flush=True)

        print("\n   Extraindo...")

        with zipfile.ZipFile(zip_path, "r") as z:
            for membro in z.namelist():
                # Extrai apenas ffmpeg.exe e ffprobe.exe da pasta bin/
                if membro.endswith("bin/ffmpeg.exe") or membro.endswith("bin/ffprobe.exe"):
                    nome = os.path.basename(membro)
                    destino = os.path.join(FFMPEG_DIR, nome)
                    with z.open(membro) as origem, open(destino, "wb") as dest:
                        dest.write(origem.read())

        os.remove(zip_path)

        if os.path.isfile(FFMPEG_EXE):
            print(f"✅ ffmpeg instalado em: {FFMPEG_DIR}\n")
            return FFMPEG_EXE
        else:
            raise FileNotFoundError("ffmpeg.exe não encontrado após extração.")

    except Exception as e:
        print(f"\n❌ Falha ao baixar ffmpeg automaticamente: {e}")
        print("   Instale manualmente em: https://ffmpeg.org/download.html")
        print("   E coloque o ffmpeg.exe na pasta ffmpeg_bin/ ao lado deste script.")
        sys.exit(1)


def progresso(d):
    """Callback de progresso do yt-dlp."""
    if d["status"] == "downloading":
        total = d.get("total_bytes") or d.get("total_bytes_estimate", 0)
        baixado = d.get("downloaded_bytes", 0)
        velocidade = d.get("speed", 0) or 0
        eta = d.get("eta", 0)

        if total > 0:
            pct = baixado / total * 100
            mb_baixado = baixado / 1_048_576
            mb_total = total / 1_048_576
            vel = velocidade / 1_048_576
            print(
                f"\r  ⬇  {pct:.1f}%  |  {mb_baixado:.1f}/{mb_total:.1f} MB"
                f"  |  {vel:.2f} MB/s  |  ETA: {eta}s      ",
                end="", flush=True,
            )

    elif d["status"] == "finished":
        print(f"\n  ✅ Arquivo pronto: {os.path.basename(d['filename'])}")

    elif d["status"] == "error":
        print("\n  ❌ Erro durante o download.")


def baixar_video(url: str, pasta_destino: str, qualidade: str, ffmpeg_path: str):
    """Baixa o vídeo e faz o merge automático via ffmpeg."""

    if qualidade == "melhor":
        fmt = "bestvideo+bestaudio/best"
    elif qualidade == "menor":
        fmt = "worstvideo+worstaudio/worst"
    else:
        fmt = f"bestvideo[height<={qualidade}]+bestaudio/best[height<={qualidade}]"

    opcoes = {
        "format": fmt,
        "merge_output_format": "mp4",                     # merge sempre em MP4
        "outtmpl": os.path.join(pasta_destino, "%(title)s.%(ext)s"),
        "ffmpeg_location": os.path.dirname(ffmpeg_path),  # pasta do ffmpeg
        "progress_hooks": [progresso],
        "ignoreerrors": True,
        "nooverwrites": True,
        # Copia stream de vídeo e converte áudio para AAC (compatível com MP4)
        "postprocessor_args": {
            "ffmpeg": ["-c:v", "copy", "-c:a", "aac"]
        },
    }

    os.makedirs(pasta_destino, exist_ok=True)

    print(f"\n🎬 Iniciando download...")
    print(f"   URL      : {url}")
    print(f"   Destino  : {os.path.abspath(pasta_destino)}")
    print(f"   Qualidade: {qualidade}")
    print(f"   ffmpeg   : {ffmpeg_path}\n")

    try:
        with yt_dlp.YoutubeDL(opcoes) as ydl:
            info = ydl.extract_info(url, download=False)
            if info:
                if info.get("_type") == "playlist":
                    n = len(info.get("entries", []))
                    print(f"📋 Playlist: {info.get('title')}  ({n} vídeos)\n")
                else:
                    dur = info.get("duration", 0) or 0
                    m, s = divmod(dur, 60)
                    print(f"🎥 Título  : {info.get('title')}")
                    print(f"   Canal   : {info.get('uploader')}")
                    print(f"   Duração : {m}m {s}s\n")

            ydl.download([url])

    except yt_dlp.utils.DownloadError as e:
        print(f"\n❌ Erro de download: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Erro inesperado: {e}")
        sys.exit(1)

    print(f"\n🎉 Concluído! Vídeo(s) em: {os.path.abspath(pasta_destino)}")


if __name__ == "__main__":
    if len(sys.argv) >= 2:
        URL = sys.argv[1]
    if len(sys.argv) >= 3:
        PASTA = sys.argv[2]
    if len(sys.argv) >= 4:
        QUALIDADE = sys.argv[3]

    ffmpeg = verificar_ou_baixar_ffmpeg()
    baixar_video(URL, PASTA, QUALIDADE, ffmpeg)