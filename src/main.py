import os
import sys

# Ajuste de rutas
directorio_actual = os.path.dirname(os.path.abspath(__file__))
sys.path.append(directorio_actual)

try:
    from neonize.client import NewClient
    # Intentamos importar de forma más abierta para evitar el error de nombre
    import neonize.events as events
    from core.ai_handler import AIHandler
    from dotenv import load_dotenv
except ImportError as e:
    print(f"❌ Error de importación crítica: {e}")
    sys.exit(1)

load_dotenv()

ai = AIHandler()

def on_wait_code(client, code):
    print("\n" + "█" * 40)
    print(f"   CÓDIGO DE VINCULACIÓN: {code}")
    print("█" * 40 + "\n")

# Cambiamos la firma de la función para que acepte el evento genérico
def on_message(client, message):
    try:
        # Intentamos extraer el texto buscando en los campos comunes
        msg_content = message.Message
        text = (
            msg_content.conversation or 
            msg_content.extendedTextMessage.text or 
            ""
        )
        
        if not text or message.Info.IsFromMe:
            return

        sender = message.Info.Sender.User
        chat_id = message.Info.Chat

        print(f"📩 Mensaje de {sender}: {text}")

        respuesta = ai.ask(text)
        client.send_message(chat_id, respuesta)
    except Exception as e:
        # Si algo falla al procesar el mensaje, lo ignoramos para no tumbar el bot
        pass

client = NewClient("session.db")

# Registramos el evento de mensaje usando el nombre del atributo interno
# que suele ser 'Message' o 'on_message'
client.event_handler.register(on_message)

phone = os.getenv("PHONE_NUMBER")

if not phone:
    print("❌ ERROR: PHONE_NUMBER no configurado.")
    sys.exit(1)

if not os.path.exists("session.db"):
    print(f"🔗 Generando enlace para: {phone}...")
    client.link_with_code(phone, on_wait_code)

print("📡 Conectando a WhatsApp...")
client.connect()

