from fastapi import FastAPI, HTTPException, Query
from transcriber import TranscriberService
from downloader import download_audio
import os

app = FastAPI()
# Inicializa o modelo uma vez para ficar na memória da VPS
service = TranscriberService()

@app.post("/transcribe")
async def transcribe(url: str = Query(..., description="URL do áudio ou vídeo")):
    try:
        # 1. Baixa o arquivo temporariamente
        audio_path = download_audio(url)
        
        # 2. Processa a transcrição
        result_json = service.run(audio_path)
        
        # 3. Limpa o arquivo temporário
        if os.path.exists(audio_path):
            os.remove(audio_path)
            
        return result_json
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)