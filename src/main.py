import os
import sys
from dotenv import load_dotenv

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

# El "Duck Typing" al rescate
class FakeType:
    def __init__(self, name):
        self.name = name

def mi_callback(client, code):
    print("\n" + "⚡" * 20)
    print(f" TU CÓDIGO DE WHATSAPP: {code}")
    print("⚡" * 20 + "\n")

client = NewClient("session.db")

@client.event(events.MessageEv)
def handle_message(client: NewClient, message: events.MessageEv):
    # (Lógica de mensajes igual que antes...)
    pass

phone = os.getenv("PHONE_NUMBER")

if not os.path.exists("session.db"):
    print(f"🔗 Vinculando {phone}...")
    
    # Preparamos los "señuelos" para la librería
    tipo_dispositivo = FakeType("Chrome")
    nombre_sesion = FakeType("ShadowLink")
    
    # Pasamos los 5 argumentos en el orden que la librería parece exigir:
    # 1. JID (Teléfono)
    # 2. show_qr (0 o False)
    # 3. client_type (Objeto con .name)
    # 4. client_name (Objeto con .name) <--- AQUÍ estaba fallando antes
    # 5. on_wait_code (Tu función)
    client.PairPhone(phone, 0, tipo_dispositivo, nombre_sesion, mi_callback)

print("📡 Conectando...")
client.connect()

