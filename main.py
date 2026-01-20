from fastapi import FastAPI, HTTPException, Query
from transcriber import TranscriberService
from downloader import download_audio
import os

app = FastAPI()
service = TranscriberService()

@app.post("/transcribe")
async def transcribe(url: str = Query(..., description="URL do áudio ou vídeo")):
    try:
        # Baixa o arquivo
        audio_path = download_audio(url)
        
        # Processa
        result_json = service.run(audio_path)
        
        # Deleta o arquivo temporário
        if os.path.exists(audio_path):
            os.remove(audio_path)
            
        return result_json
        
    except Exception as e:
        print(f"ERROR: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
