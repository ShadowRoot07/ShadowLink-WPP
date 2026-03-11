import os
import sys
from dotenv import load_dotenv

# Ajuste de rutas para encontrar 'core'
sys.path.append(os.path.join(os.path.dirname(__file__), "."))

try:
    from neonize.client import NewClient
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

# Inicializamos el cliente
client = NewClient("session.db")

# Usamos el decorador genérico. Si 'MessageEvent' no existe, 
# escuchamos el evento por su nombre de cadena, que es infalible.
@client.event("message") 
def handle_message(client, message):
    try:
        # Extraer texto de forma segura
        text = getattr(message.Message, "conversation", "") or \
               getattr(message.Message.extendedTextMessage, "text", "")
        
        if not text or message.Info.IsFromMe:
            return

        chat_id = message.Info.Chat
        print(f"📩 Mensaje: {text}")

        respuesta = ai.ask(text)
        client.send_message(chat_id, respuesta)
    except Exception as e:
        print(f"⚠️ Error procesando mensaje: {e}")

phone = os.getenv("PHONE_NUMBER")

if not os.path.exists("session.db"):
    print(f"🔗 Generando enlace para: {phone}...")
    client.link_with_code(phone, on_wait_code)

print("📡 Conectando a WhatsApp...")
client.connect()

