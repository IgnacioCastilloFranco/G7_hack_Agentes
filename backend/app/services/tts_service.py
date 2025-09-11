import os
import uuid
import tempfile
from typing import Optional
from elevenlabs.client import ElevenLabs
from elevenlabs import VoiceSettings
from app.core.config import settings

class TTSService:
    def __init__(self):
        self.client = ElevenLabs(api_key=settings.ELEVENLABS_API_KEY)
        # Voz por defecto para el Ratoncito Pérez (puedes cambiarla)
        self.default_voice_id = "iFhPOZcajR7W3sDL39qJ"  # ratoncito voice
        self.default_model = "eleven_multilingual_v2"
    
    def text_to_speech(
        self,
        text: str,
        voice_id: Optional[str] = None,
        model_id: Optional[str] = None,
        stability: Optional[float] = 0.5,
        similarity_boost: Optional[float] = 0.8,
        speed: Optional[float] = 1.0
    ) -> str:
        """
        Convierte texto a audio usando ElevenLabs.
        Retorna la ruta del archivo de audio generado.
        """
        try:
            # Usar valores por defecto si no se especifican
            voice_id = voice_id or self.default_voice_id
            model_id = model_id or self.default_model
            
            # Configurar ajustes de voz
            voice_settings = VoiceSettings(
                stability=stability,
                similarity_boost=similarity_boost,
                speed=speed
            )
            
            # Generar audio
            audio_generator = self.client.text_to_speech.convert(
                voice_id=voice_id,
                text=text,
                model_id=model_id,
                output_format="mp3_44100_128",
                voice_settings=voice_settings
            )
            
            # Crear archivo temporal
            temp_dir = tempfile.gettempdir()
            filename = os.path.join(temp_dir, f"ratoncito_{uuid.uuid4()}.mp3")
            
            # Escribir el audio desde el generador
            with open(filename, "wb") as f:
                for chunk in audio_generator:
                    f.write(chunk)
            
            return filename
            
        except Exception as e:
            print(f"❌ Error en TTS: {e}")
            raise e
    
    def get_available_voices(self):
        """
        Obtiene las voces disponibles en ElevenLabs.
        """
        try:
            voices = self.client.voices.get_all()
            return voices
        except Exception as e:
            print(f"❌ Error obteniendo voces: {e}")
            return []

# Instancia global del servicio
tts_service = TTSService()