import datetime
import json
import time
from faster_whisper import WhisperModel

class TranscriberService:
    def __init__(self):
        # Carrega o modelo na memória (usando medium para estabilidade em 4GB)
        print(f"[{datetime.datetime.now()}] Inicializando modelo Whisper...")
        self.model = WhisperModel("large-v3-turbo", device="cpu", compute_type="int8")

    def run(self, audio_path):
        print(f"[{datetime.datetime.now()}] Iniciando transcrição de: {audio_path}")
        
        segments, _ = self.model.transcribe(
            audio_path,
            beam_size=1,
            language="pt",
            vad_filter=False,
            word_timestamps=True
        )

        results = []
        buffer_text = []
        start_time = None
        inicio_proc = time.time()

        for segment in segments:
            if start_time is None:
                start_time = segment.start
            
            texto_segmento = segment.text.strip()
            buffer_text.append(texto_segmento)
            texto_completo = " ".join(buffer_text)

            # LOG DE PROGRESSO: Imprime no console a cada segmento detectado
            timestamp_atual = str(datetime.timedelta(seconds=int(segment.start))).zfill(8)
            print(f"[{timestamp_atual}] {texto_segmento}")

            # Lógica de agrupamento por pontuação ou tamanho
            if texto_completo[-1] in [".", "!", "?", ";"] or len(texto_completo) > 130:
                results.append({
                    "start": round(start_time, 2),
                    "end": round(segment.end, 2),
                    "text": texto_completo
                })
                buffer_text = []
                start_time = None

        # Limpeza do buffer final
        if buffer_text:
            results.append({
                "start": round(start_time, 2),
                "end": round(segment.end, 2),
                "text": " ".join(buffer_text)
            })

        tempo_total = (time.time() - inicio_proc) / 60
        print(f"[{datetime.datetime.now()}] Transcrição finalizada em {tempo_total:.2f} minutos.")
        return results
