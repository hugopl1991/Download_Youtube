#conda install -c conda-forge yt-dlp ffmpeg
import yt_dlp

url = "https://youtu.be/p3URn9M2LKo?si=W3lFN9AZtCRlg_ht"

ydl_opts = {
    'format': 'bestvideo+bestaudio/best',
    'ignoreerrors': True,   # <<< ESSENCIAL
    'merge_output_format': 'mp4',
    'outtmpl': '%(title)s.%(ext)s',
}

with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    ydl.download([url])
print("Download completed.")