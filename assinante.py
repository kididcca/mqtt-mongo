import paho.mqtt.client as mqtt
from pymongo import MongoClient
import time
import os

if "MONGO_SERVER" in os.environ:
    mongo_server = os.environ["MONGO_SERVER"]
else:
    mongo_server = 'mongo'

if "MQTT_BROKER" in os.environ:
    mqtt_broker = os.environ["MQTT_BROKER"]
else:
    mqtt_broker = 'mqtt'

if "MQTT_TOPIC" in os.environ:
    mqtt_topic = os.environ["MQTT_TOPIC"]
else:
    mqtt_topic = 'arduino/sensor'

def on_connect(client, userdata, flags, rc):
    client.subscribe(mqtt_topic)

def on_message(client, userdata, msg):
    topico = msg.topic.strip().split('/')
    arduino = topico[0]
    sensor = topico[1]
    valoratual = bytes(msg.payload).decode('utf-8')
    data_atual = time.time()
    post = {'nome': arduino, 'valor': valoratual, 'data': data_atual}
    print(post)
    post_id = posts.insert_one(post).inserted_id
    dados_recebidos = []
    dados_recebidos = posts.find({'nome':topico[0]})
    saida = open('html/dados.js', 'w')
    saida.write("new Chartist.Line('.ct-chart', {\n")
    saida.write("    series: [\n")
    for sensores in dados_recebidos:
        saida.write("        {\n")
        saida.write("            name: '" + sensores['nome'] + "',\n")
        saida.write("            data: [\n")
        for linha in dados_recebidos:
            saida.write("                {\n")
            saida.write("                    x: new moment.unix(" + str(linha['data']).split('.')[0] + "),\n")
            saida.write("                    y: " + linha['valor'] + "\n")
            saida.write("                },\n")
        saida.write("            ]\n")
        saida.write("        },\n")
    saida.write("    ]\n")
    saida.write("},\n")
    saida.write("{\n")
    saida.write("    axisX: {\n")
    saida.write("        type: Chartist.FixedScaleAxis,\n")
    saida.write("        divisor: 5,\n")
    saida.write("        labelInterpolationFnc: function (value) {\n")
    saida.write("            return moment(value).format('HH:MM-DD/MM');\n")
    saida.write("        }\n")
    saida.write("    }\n")
    saida.write("});\n")
    saida.close()

mongo_client = MongoClient(mongo_server)
db = mongo_client.arduino
posts = db.temperatura

mqtt_sub = mqtt.Client()
mqtt_sub.on_connect = on_connect
mqtt_sub.on_message = on_message
mqtt_sub.connect(mqtt_broker, 1883, 60)
mqtt_sub.loop_forever()
