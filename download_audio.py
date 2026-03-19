import yt_dlp

url = "https://youtu.be/p3URn9M2LKo?si=W3lFN9AZtCRlg_ht"

ydl_opts = {
    'format': 'bestaudio/best',
    'ignoreerrors': True,   # <<< ESSENCIAL
    'outtmpl': '%(title)s.%(ext)s',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
}

with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    ydl.download([url])
print("Download completed.")