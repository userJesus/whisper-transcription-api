import requests
import yt_dlp
import uuid
import os

def download_audio(url):
    file_id = str(uuid.uuid4())
    path = f"temp_{file_id}.mp3"
    
    # Se for link direto (Cloudinary, etc)
    if any(ext in url.lower() for ext in ['.mp3', '.wav', '.m4a']):
        with requests.get(url, stream=True) as r:
            r.raise_for_status()
            with open(path, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
    else:
        # Se for plataforma (YouTube, etc)
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': f"temp_{file_id}",
            'quiet': True,
            'postprocessors': [{'key': 'FFmpegExtractAudio','preferredcodec': 'mp3','preferredquality': '192'}],
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
            path = f"temp_{file_id}.mp3"
            
    return path