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

# Creamos un objeto que simule ser el tipo de cliente
class FakeType:
    def __init__(self, name):
        self.name = name

# Esta es la función que recibirá el código
def mi_callback(client, code):
    print("\n" + "⚡" * 20)
    print(f" TU CÓDIGO DE WHATSAPP: {code}")
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
    # Creamos los objetos que la librería quiere inspeccionar
    # client_type y client_name (ambos necesitan .name según el log anterior)
    tipo = FakeType("Chrome")
    nombre = FakeType("Linux")
    
    # Intentamos pasar los 4 argumentos: JID, show_qr, tipo, callback
    # Si la librería pide 5, usaremos 'nombre' también, pero probemos así:
    try:
        client.PairPhone(phone, 0, tipo, mi_callback)
    except TypeError:
        # Si falla por falta de argumentos, le damos el 5to (nombre)
        client.PairPhone(phone, 0, tipo, nombre, mi_callback)

print("📡 Conectando...")
client.connect()

