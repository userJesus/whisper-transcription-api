from faster_whisper import WhisperModel

class TranscriberService:
    def __init__(self):
        # Configuração para VPS (CPU + Precisão Turbo)
        self.model = WhisperModel("large-v3-turbo", device="cpu", compute_type="int8")

    def run(self, audio_path):
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

        for segment in segments:
            if start_time is None:
                start_time = segment.start
            
            buffer_text.append(segment.text.strip())
            texto_completo = " ".join(buffer_text)

            # Lógica de agrupamento (pontuação ou tamanho)
            if texto_completo[-1] in [".", "!", "?", ";"] or len(texto_completo) > 130:
                results.append({
                    "start": round(start_time, 2),
                    "end": round(segment.end, 2),
                    "text": texto_completo
                })
                buffer_text = []
                start_time = None

        # Adiciona o resto do buffer, se houver
        if buffer_text:
            results.append({
                "start": round(start_time, 2),
                "end": round(segment.end, 2),
                "text": " ".join(buffer_text)
            })

        return results
