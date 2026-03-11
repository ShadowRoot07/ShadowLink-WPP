from google import genai
import os

class AIHandler:
    def __init__(self):
        # La nueva librería usa una estructura distinta
        self.client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))
        self.model_id = "gemini-2.0-flash"

    def ask(self, prompt, history=""):
        instruction = (
            "Eres ShadowLink, asistente Cyberpunk en WhatsApp. "
            "Estilo: Directo, técnico, verde neón. Responde en español."
        )
        try:
            # Nueva forma de llamar a la generación de contenido
            response = self.client.models.generate_content(
                model=self.model_id,
                contents=f"{instruction}\n\nUsuario: {prompt}"
            )
            return response.text
        except Exception as e:
            return f"❌ Error en la matriz: {e}"

