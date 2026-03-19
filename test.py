import yt_dlp

url = "https://youtu.be/p3URn9M2LKo"

ydl_opts = {
    'format': 'bv*+ba/best',
    'merge_output_format': 'mp4',
    'ignoreerrors': True,
    'outtmpl': '%(title)s.%(ext)s',
    'noplaylist': True,
}

with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    ydl.download([url])

print("Download completed.")