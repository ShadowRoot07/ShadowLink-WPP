import os
import sys
from dotenv import load_dotenv

# Ajuste de rutas
sys.path.append(os.path.join(os.path.dirname(__file__), "."))

try:
    from neonize.client import NewClient
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

# Usamos el nombre que la librería sugirió: MessageEv
@client.event(events.MessageEv)
def handle_message(client: NewClient, message: events.MessageEv):
    try:
        # En esta versión, el contenido suele estar en message.Message
        msg = message.Message
        text = (
            getattr(msg, "conversation", "") or 
            getattr(msg.extendedTextMessage, "text", "") or
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

if not phone:
    print("❌ ERROR: PHONE_NUMBER no configurado en Secrets.")
    sys.exit(1)

if not os.path.exists("session.db"):
    print(f"🔗 Generando enlace para: {phone}...")
    client.link_with_code(phone, on_wait_code)

print("📡 Conectando a WhatsApp...")
client.connect()

