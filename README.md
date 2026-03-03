🎬 YouTube Downloader (Python + yt-dlp)

Script em Python para baixar vídeos, áudios ou playlists completas do YouTube utilizando yt-dlp.

📌 Funcionalidades

✅ Download de vídeo com áudio (MP4)

✅ Download somente áudio (MP3)

✅ Download de playlists completas

✅ Organização automática por pasta

✅ Conversão automática para MP3

✅ Ignora vídeos privados/removidos

✅ Evita downloads duplicados

🛠️ Requisitos

Python 3.9+

yt-dlp

FFmpeg

📦 Instalação
1️⃣ Criar ambiente (opcional, mas recomendado)
conda create -n yt python=3.10
conda activate yt
2️⃣ Instalar dependências
pip install yt-dlp
conda install -c conda-forge ffmpeg
🚀 Como Usar
▶️ Baixar vídeo com áudio (MP4)
import yt_dlp

url = "https://www.youtube.com/watch?v=VIDEO_ID"

ydl_opts = {
    'format': 'bestvideo+bestaudio/best',
    'merge_output_format': 'mp4',
}

with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    ydl.download([url])
🎵 Baixar somente áudio (MP3)
import yt_dlp

url = "https://www.youtube.com/watch?v=VIDEO_ID"

ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
}

with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    ydl.download([url])
📂 Baixar playlist inteira (somente áudio)
import yt_dlp

playlist_url = "https://www.youtube.com/playlist?list=PLAYLIST_ID"

ydl_opts = {
    'format': 'bestaudio/best',
    'ignoreerrors': True,
    'download_archive': 'baixados.txt',
    'outtmpl': 'playlist_audio/%(playlist_title)s/%(playlist_index)02d - %(title)s.%(ext)s',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
}

with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    ydl.download([playlist_url])
📁 Estrutura de Pastas Gerada
playlist_audio/
 └── Nome da Playlist/
     ├── 01 - Video 1.mp3
     ├── 02 - Video 2.mp3
     └── ...
⚠️ Problemas Comuns
🔹 Vídeo indisponível

Resolvido com:

'ignoreerrors': True
🔹 Aviso sobre JavaScript Runtime

Opcionalmente instalar Node.js:

conda install -c conda-forge nodejs
📚 Opções Úteis
Objetivo	Opção
Melhor áudio	bestaudio/best
Melhor vídeo + áudio	bestvideo+bestaudio
Converter para MP3	FFmpegExtractAudio
Evitar duplicados	download_archive
Baixar intervalo da playlist	playlist_items
🧠 Dicas

Use download_archive para não baixar o mesmo vídeo duas vezes.

Use playlist_items para dividir playlists grandes.

Sempre mantenha yt-dlp atualizado:

pip install -U yt-dlp
📄 Licença

Uso educacional e pessoal.
Respeite sempre os termos de uso do YouTube e os direitos autorais do conteúdo baixado.

👨‍💻 Autor

Hugo Lima
Projeto pessoal para automação de downloads via Python.
