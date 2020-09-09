import flask
from flask import request
import os
import psycopg2
import dweepy
from json import dumps
from httplib2 import Http
from flask import render_template
import time
from datetime import datetime
from threading import Thread


datosbot = lambda x: {str(i[0]):{'humedad':str(i[1]),'temperatura':i[2]} for i in x}


def run(): 
    # This might take more than 15 minutes to complete
    consultar= lambda a:dweepy.get_latest_dweet_for(a)
    for i in range(1,16):  
        a=consultar('thecore')[0]['content']
        cursor.execute("INSERT INTO thecore(hora, temperatura , humedad) VALUES (%s,%s,%s)", (datetime.now(),a["temperature"],a["humidity"]))
        time.sleep(60)
    conn.commit()
    cursor.execute("Select * from thecore ORDER BY hora DESC")
    a=datosbot(cursor.fetchall())
    webhook(a)

#DATABASE_URL = os.environ['DATABASE_URL']
#conn = psycopg2.connect(DATABASE_URL, sslmode='require')
#Conexion de la base en el servidor que no es de heroku
conn = psycopg2.connect(user="ecxzqtzfjeihgc",
                                password="618dfca07119f8cf853cd7e9985ed4d7701c8bf4412804c8644f4120e04f03cb",
                                host="ec2-35-153-12-59.compute-1.amazonaws.com",
                                port="5432",
                                database="deeuk8ikachdv6")
cursor = conn.cursor()

def datosmoneda(x):
    msg={'argetina':{},'chile':{},'euro':{}}
    for i in x:
        msg[i[2]].update({str(i[0]):str(i[1])})
    return msg

app= flask.Flask(__name__)

def webhook(msg):
    url = 'https://webhook.site/e1c8e1e6-e06c-4e1c-8a2c-176eb1a4f634' #link todo legal
    #url='https://webhook.site/4cb7980d-edf2-4ebc-b19f-92e34aeb7719' #link myhook
    message_headers = {'Content-Type': 'application/json; charset=UTF-8'}
    http_obj = Http()
    response = http_obj.request(
        uri=url,
        method='POST',
        headers=message_headers,
        body=dumps(msg),
    )
@app.route('/')
def Home():
    return render_template('main.html')
@app.route('/1')
def Uno():
    cursor.execute("Select * from conversiondolares")
    moneda=cursor.fetchall()
    msg=datosmoneda(moneda)
    webhook(msg)
    return msg
@app.route('/2')
def Dos():
    cursor.execute("Select * from conversiondolaresMockup")
    moneda=cursor.fetchall()
    msg=datosmoneda(moneda)
    webhook(msg)
    return msg

@app.route('/3')
def Tres():
    cursor.execute("Select * from thecore ORDER BY hora DESC LIMIT 15")
    msg=datosbot(cursor.fetchall())
    thread = Thread(target=run)
    thread.daemon = True
    thread.start()
    return msg


if __name__ == '__main__':
    app.run()