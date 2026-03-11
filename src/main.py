import os
import sys

# Ajuste de rutas para que reconozca los módulos correctamente
directorio_actual = os.path.dirname(os.path.abspath(__file__))
sys.path.append(directorio_actual)

try:
    from neonize.client import NewClient
    from neonize.events import MessageEvent
    from core.ai_handler import AIHandler  # Importación directa desde core
    from dotenv import load_dotenv
except ImportError as e:
    print(f"❌ Error de importación crítica: {e}")
    sys.exit(1)

load_dotenv()

# Inicializar IA
ai = AIHandler()

def on_wait_code(client, code):
    print("\n" + "█" * 40)
    print(f"   CÓDIGO DE VINCULACIÓN: {code}")
    print("█" * 40 + "\n")

def on_message(client, message: MessageEvent):
    # Extraer texto de diferentes tipos de mensajes
    text = (
        message.Message.conversation or 
        message.Message.extendedTextMessage.text or 
        ""
    )
    
    # Evitar responderse a sí mismo o mensajes vacíos
    if not text or message.Info.IsFromMe:
        return

    sender = message.Info.Sender.User
    chat_id = message.Info.Chat

    print(f"📩 Mensaje de {sender}: {text}")

    # Procesar con IA
    respuesta = ai.ask(text)
    client.send_message(chat_id, respuesta)

# Configuración del cliente
# Nota: 'session.db' se creará en la raíz de donde se ejecute el script
client = NewClient("session.db")
client.event_handler.register(on_message)

# Obtener número de los Secrets de GitHub
phone = os.getenv("PHONE_NUMBER")

if not phone:
    print("❌ ERROR: La variable PHONE_NUMBER no está configurada en los Secrets.")
    sys.exit(1)

# Solo pedir código si no hay una sesión activa
if not os.path.exists("session.db"):
    print(f"🔗 Generando enlace para el número: {phone}...")
    try:
        client.link_with_code(phone, on_wait_code)
    except Exception as e:
        print(f"❌ Fallo al generar código de enlace: {e}")
        sys.exit(1)

print("📡 Conectando a los servidores de WhatsApp...")
client.connect()

