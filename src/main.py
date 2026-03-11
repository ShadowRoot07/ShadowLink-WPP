import os
import sys
from dotenv import load_dotenv

# Ajuste de rutas
sys.path.append(os.path.join(os.path.dirname(__file__), "."))

try:
    from neonize.client import NewClient
    from neonize import events
    from neonize.types import CHROME  # Importamos el tipo de cliente
    from core.ai_handler import AIHandler
except ImportError as e:
    print(f"❌ Error de importación: {e}")
    sys.exit(1)

load_dotenv()
ai = AIHandler()

def mi_callback(client, code):
    print("\n" + "⚡" * 20)
    print(f" CÓDIGO DE VINCULACIÓN: {code}")
    print("⚡" * 20 + "\n")

client = NewClient("session.db")

@client.event(events.MessageEv)
def handle_message(client: NewClient, message: events.MessageEv):
    try:
        msg = message.Message
        text = getattr(msg, "conversation", "") or \
               getattr(msg.extendedTextMessage, "text", "") or ""
        
        if not text or message.Info.IsFromMe:
            return

        chat_id = message.Info.Chat
        print(f"📩 Mensaje: {text}")
        respuesta = ai.ask(text)
        client.send_message(chat_id, respuesta)
    except Exception as e:
        print(f"⚠️ Error: {e}")

phone = os.getenv("PHONE_NUMBER")

if not os.path.exists("session.db"):
    print(f"🔗 Vinculando {phone}...")
    # Firma detectada por el error:
    # 1. JID (phone)
    # 2. show_qr (0/False)
    # 3. client_type (Aquí esperaba algo con .name, como CHROME)
    # 4. on_wait_code (Tu función)
    client.PairPhone(phone, 0, CHROME, mi_callback)

print("📡 Conectando...")
client.connect()

