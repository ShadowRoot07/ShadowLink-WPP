import google.generativeai as genai
import os

class AIHandler:
    def __init__(self):
        genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
        # Usamos el 2.0-flash que ya sabemos que te funciona
        self.model = genai.GenerativeModel('gemini-2.0-flash')

    def ask(self, prompt, history=""):
        instruction = (
            "Eres ShadowLink, un asistente Cyberpunk en WhatsApp. "
            "Estilo: Directo, técnico, verde neón. Responde en español.\n"
            f"Historial previo: {history}"
        )
        try:
            response = self.model.generate_content(f"{instruction}\n\nUsuario: {prompt}")
            return response.text
        except Exception as e:
            return f"❌ Error en la matriz: {e}"

