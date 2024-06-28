from mqtt_as import MQTTClient
from mqtt_local import config
import uasyncio as asyncio
import ujson as json
import uos as os
import dht, machine, ubinascii, btree

# Constantes
UNIQUE_ID = ubinascii.hexlify(machine.unique_id()).decode('utf-8')

TOPIC = "monitoreo-yatei/" + UNIQUE_ID

PIN_DHT = 13

MP = 5.0 # periodo de monitoreo del sensor

# Objetos globales:
d = dht.DHT22(machine.Pin(PIN_DHT))

# Variables globales:
params = {
    'temperatura':0.0, # grados Celsius 
    'humedad':0.0,     # %
    'periodo':30,      # segundos
}

# Funciones para base de datos
def storedb(per):
    with open('db','wb') as f:
        db = btree.open(f)

        try:
            db[b'periodo'] = str(per).encode()
        except:
            print('Error en los tipos de datos')

        db.flush()
        db.close()

def readdb():
    with open('db','rb') as f:
        db = btree.open(f)

        try:
            per = float(db[b'periodo'].decode())
        except:
            print('Clave/s no encontrada/s')

        db.flush()
        db.close()

    return per

# Funciones generales
def read_dht22():
    try:
        d.measure()
        try:
            params['temperatura'] = d.temperature()
        except OSError as e:
            print("sin sensor temperatura")
        try:
            params['humedad'] = d.humidity()
        except OSError as e:
            print("sin sensor humedad")
    except OSError as e:
        print("sin sensor") 

# Funciones para configuracion del cliente: sub_cb, wifi_han, conn_han
def sub_cb(topic, msg, retained):

    mod = False

    dtopic = topic.decode()
    dmsg = msg.decode()
    print('Topico = {} -> Valor = {}'.format(dtopic, dmsg))

    if dtopic == 'periodo':
        try:
            period = float(dmsg)
            if period < 10.0:
                period = 10.0 # para evitar periodos demasiado bajos
            params[dtopic] = period
            mod = True
        except ValueError:
            print(f'Error: No se puede asignar el valor "{dmsg}" a "{dtopic}"')
    
    if mod is True:
        storedb(params['periodo'])

async def wifi_han(state):
    print('Wifi is ', 'up' if state else 'down')
    await asyncio.sleep(1)

# If you connect with clean_session True, must re-subscribe (MQTT spec 3.1.2.4)
async def conn_han(client):
    await client.subscribe('periodo', 1)

# Funciones principales: main
async def main(client):
    await client.connect()
    await asyncio.sleep(2)
    
    while True:

        read_dht22()

        print('Publicando', params)
        await client.publish(f'{TOPIC}', json.dumps(params), qos=1)

        await asyncio.sleep(params['periodo'])

# Access Data Base
if 'db' not in os.listdir():
    print('Base de datos NO encontrada. CREANDO NUEVA')
    storedb(params['periodo'])
else:
    print('Base de datos encontrada. LEYENDO DATOS')
    try:
        params['periodo'] = readdb()
    except:
        print('No se encontraron datos. GENERANDO')
        storedb(params['periodo'])

# Define client configuration
config['subs_cb'] = sub_cb
config['connect_coro'] = conn_han
config['wifi_coro'] = wifi_han
config['ssl'] = True

# Set up client
MQTTClient.DEBUG = True  # Optional
client = MQTTClient(config)

try:
    asyncio.run(main(client))
finally:
    client.close()
    asyncio.new_event_loop()