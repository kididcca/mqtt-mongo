import time, os
import paho.mqtt.client as mqtt
from pymongo import MongoClient 

cliente = MongoClient(os.getenv('MONGO_SERVER', 'nuvem.sj.ifsc.edu.br'))
db = cliente[os.getenv('DATABASE', 'estacao')]

def on_connect(client, userdata, flags, rc):
    client.subscribe(os.getenv('TOPIC', 'estacao/#'))

def on_message(client, userdata, msg):
    topico = msg.topic.strip().split('/')
    arduino = topico[0]
    sensor = topico[1]
    valoratual = bytes(msg.payload).decode('utf-8')
    data_atual = time.time()
    posts = db[sensor]
    post = {'nome':arduino, 'valor':valoratual, 'data':data_atual}
    post_id = posts.insert_one(post).inserted_id
    print('Tópico: ' + topico[0]
          + ', sensor: ' + topico[1]
          + ', valor: ' + valoratual + '\n')

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(os.getenv('MQTT_BROKER', 'nuvem.sj.ifsc.edu.br'), 1883, 60)
client.loop_forever()
