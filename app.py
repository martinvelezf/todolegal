import flask
from flask import request
import os
import sqlite3
import dweepy
from json import dumps
from httplib2 import Http
from flask import render_template
import time
from datetime import datetime
from threading import Thread
import pandas as pd

datosbot = lambda x: {str(i[0]):{'humedad':str(i[1]),'temperatura':i[2]} for i in x}


def run(): 
    conn = sqlite3.connect("./test.db")
    cursor = conn.cursor()
    # This might take more than 15 minutes to complete
    consultar= lambda consulta:dweepy.get_latest_dweet_for(consulta)
    list=[]
    for i in range(1,16):  
        fila=consultar('thecore')[0]['content']
        list.append({'hora':datetime.now(), "temperatura":fila["temperature"] , "humedad":fila["humidity"]})
        time.sleep(60)
    pd.DataFrame(list).to_sql('thecore', con=conn, if_exists='append') 
    cursor.execute("Select * from thecore ORDER BY hora DESC")
    datos_resultado=datosbot(cursor.fetchall())
    webhook(datos_resultado)

#Conexion de la base en el servidor que no es de heroku
conn = sqlite3.connect("./test.db")



def datosmoneda(x):
    msg={'argetina':{},'chile':{},'euro':{}}
    for i in x:
        msg[i[2]].update({str(i[0]):str(i[1])})
    return msg
def datosmoneda2(x):
    try:
        moneda='cambio de moneda %s a USD'%x[0][2]
        msg={moneda:{}}
        for i in x:
            msg[moneda].update({str(i[0]):str(i[1])})   
        return msg
    except:
        return "No existe valores"
app= flask.Flask(__name__)

def webhook(msg):
    url = 'https://webhook.site/4ed54cff-41ba-423e-9f46-b2c87408daf9' 
    my_url='https://webhook.site/40f548cb-15f5-40b1-8b72-9015467ae9ed' #link myhook
    message_headers = {'Content-Type': 'application/json; charset=UTF-8'}
    http_obj = Http()
    response = http_obj.request(
        uri=url,
        method='POST',
        headers=message_headers,
        body=dumps(msg),
    )
    response = http_obj.request(
        uri=my_url,
        method='POST',
        headers=message_headers,
        body=dumps(msg),
    )
@app.route('/')
def Home():
    return render_template('main.html')
@app.route('/1')
def Uno():
    conn = sqlite3.connect("./test.db")
    cursor = conn.cursor()
    cursor.execute("Select dia,valor,moneda from cambio_normal")
    moneda=cursor.fetchall()
    msg=datosmoneda(moneda)
    webhook(msg)
    return msg
@app.route('/1/<moneda>')
def Uno1(moneda):
    conn = sqlite3.connect("./test.db")

    cursor = conn.cursor()
    cursor.execute("Select dia,valor,moneda from cambio_normal where moneda='%s'"%(moneda))
    moneda=cursor.fetchall()
    msg=datosmoneda2(moneda)
    webhook(msg)
    return msg
@app.route('/2')
def Dos():
    conn = sqlite3.connect("./test.db")
    cursor = conn.cursor()
    cursor.execute("Select dia,valor,moneda from cambio_artificial")
    moneda=cursor.fetchall()
    msg=datosmoneda(moneda)
    webhook(msg)
    return msg
@app.route('/2/<moneda>')
def Dos2(moneda):
    conn = sqlite3.connect("./test.db")
    cursor = conn.cursor()
    cursor.execute("Select dia,valor,moneda from cambio_artificial where '%s'"%(moneda))
    moneda=cursor.fetchall()
    msg=datosmoneda2(moneda)
    webhook(msg)
    return msg

@app.route('/3')
def Tres():
    thread = Thread(target=run)
    thread.daemon = True
    thread.start()
    conn = sqlite3.connect("./test.db")
    return "Se ha enviado al webhook"


if __name__ == '__main__':
    app.run()
