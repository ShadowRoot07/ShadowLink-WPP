import os
import sys
from dotenv import load_dotenv

# Ajuste de rutas
directorio_actual = os.path.dirname(os.path.abspath(__file__))
sys.path.append(directorio_actual)

from neonize.client import NewClient
from neonize.events import Event, MessageEvent
from core.ai_handler import AIHandler

load_dotenv()
ai = AIHandler()

def on_wait_code(client, code):
    print("\n" + "█" * 40)
    print(f"   CÓDIGO DE VINCULACIÓN: {code}")
    print("█" * 40 + "\n")

# Nueva forma de registrar eventos en neonize moderno
client = NewClient("session.db")

@client.event(MessageEvent)
def on_message(client: NewClient, message: MessageEvent):
    text = message.Message.conversation or message.Message.extendedTextMessage.text
    if not text or message.Info.IsFromMe:
        return

    chat_id = message.Info.Chat
    print(f"📩 Mensaje recibido: {text}")

    respuesta = ai.ask(text)
    client.send_message(chat_id, respuesta)

phone = os.getenv("PHONE_NUMBER")

if not os.path.exists("session.db"):
    print(f"🔗 Generando enlace para: {phone}...")
    client.link_with_code(phone, on_wait_code)

print("📡 Conectando a WhatsApp...")
client.connect()

