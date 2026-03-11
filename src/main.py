import os
from neonize.client import NewClient
from neonize.events import MessageEvent
from core.ai_handler import AIHandler
from dotenv import load_dotenv

load_dotenv()

ai = AIHandler()

def on_wait_code(client, code):
    print("\n" + "█"*40)
    print(f"   CÓDIGO DE VINCULACIÓN: {code}")
    print("█"*40 + "\n")

def on_message(client, message: MessageEvent):
    # Evitar responderse a sí mismo o mensajes vacíos
    text = message.Message.conversation or message.Message.extendedTextMessage.text
    if not text or message.Info.IsFromMe:
        return

    sender = message.Info.Sender.User
    chat_id = message.Info.Chat
    
    print(f"📩 Mensaje de {sender}: {text}")
    
    # Procesar con IA
    respuesta = ai.ask(text)
    client.send_message(chat_id, respuesta)

# Usamos session.db para guardar la conexión
client = NewClient("session.db")
client.event_handler.register(on_message)

# Pon tu número con código de país sin el '+' (Ej: 57300...)
phone = os.getenv("PHONE_NUMBER")

if not os.path.exists("session.db"):
    print(f"🔗 Generando enlace para {phone}...")
    client.link_with_code(phone, on_wait_code)

client.connect()

