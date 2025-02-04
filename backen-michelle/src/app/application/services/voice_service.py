from typing import Optional
import speech_recognition as sr
from app.application.interfaces.storage import IFileStorage
from app.domain.schemas.user import UserInDB

class VoiceService:
    def __init__(self, file_storage: IFileStorage):
        self.file_storage = file_storage
        self.recognizer = sr.Recognizer()

    async def process_command(self, audio_data: bytes, user_id: int) -> dict:
        try:
            # Guardar audio temporalmente
            filename = f"voice_command_{user_id}_{int(time.time())}.wav"
            await self.file_storage.save_file(audio_data, filename)

            # Convertir audio a texto
            text = await self.transcribe_audio(audio_data)

            # Procesar comando
            command = self._parse_command(text)
            return {
                "text": text,
                "command": command,
                "success": True
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    async def transcribe_audio(self, audio_data: bytes) -> str:
        try:
            with sr.AudioFile(audio_data) as source:
                audio = self.recognizer.record(source)
                return self.recognizer.recognize_google(audio, language='es-ES')
        except sr.UnknownValueError:
            raise ValueError("No se pudo entender el audio")
        except sr.RequestError:
            raise ConnectionError("Error al conectar con el servicio de reconocimiento")

    def _parse_command(self, text: str) -> dict:
        text = text.lower()
        
        # Comandos de documento
        if "crear documento" in text:
            return {"type": "create_document"}
        elif "guardar documento" in text:
            return {"type": "save_document"}
        elif text.startswith("título"):
            title = text.replace("título", "").strip()
            return {"type": "set_title", "value": title}
        
        # Comandos de IA
        elif text.startswith("generar"):
            prompt = text.replace("generar", "").strip()
            return {"type": "generate_text", "value": prompt}
        
        return {"type": "unknown"}