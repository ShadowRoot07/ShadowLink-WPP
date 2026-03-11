from google import genai
import os

class AIHandler:
    def __init__(self):
        api_key = os.getenv("GOOGLE_API_KEY")
        self.client = genai.Client(api_key=api_key)

    def ask(self, prompt):
        try:
            response = self.client.models.generate_content(
                model="gemini-2.0-flash",
                contents=f"Eres ShadowLink, un bot Cyberpunk. Responde breve: {prompt}"
            )
            return response.text
        except Exception as e:
            return f"❌ Error IA: {e}"

