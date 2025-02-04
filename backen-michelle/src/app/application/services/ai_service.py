from typing import Optional
import openai
from app.application.interfaces.services import IAIService
from app.infrastructure.config import get_settings

settings = get_settings()
openai.api_key = settings.OPENAI_API_KEY

class OpenAIService(IAIService):
    async def generate_text(self, prompt: str, max_tokens: int = 500) -> str:
        try:
            response = await openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Eres un asistente útil que ayuda a generar texto."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=max_tokens,
                temperature=0.7
            )
            return response.choices[0].message.content
        except Exception as e:
            raise Exception(f"Error generating text: {str(e)}")

    async def analyze_sentiment(self, text: str) -> dict:
        try:
            response = await openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Analiza el sentimiento del siguiente texto y responde con JSON."},
                    {"role": "user", "content": text}
                ],
                temperature=0
            )
            return {
                "sentiment": response.choices[0].message.content,
                "confidence": 0.9
            }
        except Exception as e:
            raise Exception(f"Error analyzing sentiment: {str(e)}")

    async def summarize_text(self, text: str, max_length: int = 200) -> str:
        try:
            response = await openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": f"Resume el siguiente texto en no más de {max_length} caracteres."},
                    {"role": "user", "content": text}
                ],
                max_tokens=max_length,
                temperature=0.3
            )
            return response.choices[0].message.content
        except Exception as e:
            raise Exception(f"Error summarizing text: {str(e)}")