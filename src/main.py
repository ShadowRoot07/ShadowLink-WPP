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

# Función de callback para el código
def on_qr(client, qr):
    # No usaremos QR, pero la librería a veces lo requiere definido
    pass

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

# Si no hay sesión, solicitamos el código de vinculación
if not os.path.exists("session.db"):
    print(f"🔗 Solicitando código de vinculación para: {phone}")
    # En la versión 0.3.15, el método suele ser este:
    client.pair_code(phone, on_wait_code=lambda _, code: print(f"\n✅ TU CÓDIGO: {code}\n"))

print("📡 Iniciando conexión...")
client.connect()

