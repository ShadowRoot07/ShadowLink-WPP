import os
import sys
from dotenv import load_dotenv

# Ajuste de rutas
sys.path.append(os.path.join(os.path.dirname(__file__), "."))

try:
    from neonize.client import NewClient
    # Importamos el módulo de eventos completo
    from neonize import events
    from core.ai_handler import AIHandler
except ImportError as e:
    print(f"❌ Error de importación: {e}")
    sys.exit(1)

load_dotenv()
ai = AIHandler()

def on_wait_code(client, code):
    print("\n" + "█" * 40)
    print(f"   CÓDIGO DE VINCULACIÓN: {code}")
    print("█" * 40 + "\n")

client = NewClient("session.db")

# Usamos la referencia directa desde el módulo 'events'
@client.event(events.MessageEvent)
def handle_message(client: NewClient, message: events.MessageEvent):
    try:
        # Extraer texto de forma segura según la versión 0.3.x
        msg_content = message.Message
        text = (
            getattr(msg_content, "conversation", "") or 
            getattr(msg_content.extendedTextMessage, "text", "") or
            ""
        )
        
        if not text or message.Info.IsFromMe:
            return

        chat_id = message.Info.Chat
        print(f"📩 Mensaje recibido: {text}")

        respuesta = ai.ask(text)
        client.send_message(chat_id, respuesta)
    except Exception as e:
        print(f"⚠️ Error en handle_message: {e}")

phone = os.getenv("PHONE_NUMBER")

if not os.path.exists("session.db"):
    print(f"🔗 Generando enlace para: {phone}...")
    client.link_with_code(phone, on_wait_code)

print("📡 Conectando a WhatsApp...")
client.connect()

