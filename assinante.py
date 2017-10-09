import paho.mqtt.client as mqtt
from pymongo import MongoClient
import time

cliente = MongoClient('mongo')
db = cliente.arduino
posts = db.temperatura

def on_connect(client, userdata, flags, rc):
    client.subscribe("arduino/ard")

def on_message(client, userdata, msg):
    topico = msg.topic.strip().split('/')
    arduino = topico[0]
    sensor = topico[1]
    valoratual = bytes(msg.payload).decode('utf-8')
    data_atual = time.time()
    post = {'nome': arduino, 'valor': valoratual, 'data': data_atual}
    post_id = posts.insert_one(post).inserted_id
    dados_recebidos = []
    dados_recebidos = posts.find({'nome':'arduino'})
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

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect("mqtt", 1883, 60)
client.loop_forever()
