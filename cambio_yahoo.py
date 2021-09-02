#db

import os

import csv
import sqlite3
import pandas as pd

conn = sqlite3.connect("./test.db")

list_df=[]
for country in ['argetina.csv','chile.csv','euro.csv']:
    df=pd.read_csv('csv/'+country) 
    df["moneda"]=country[:-4].capitalize()
    list_df.append(df) 

result = pd.concat(list_df)[["Fecha","Último","moneda"]].rename(columns={'Último': 'valor', 'Fecha': 'dia'})
result['dia']= result['dia'].apply(lambda x:x.replace('.','-'))
result['valor']= result['valor'].apply(lambda x:x.replace(',','.'))
result.to_sql('cambio_normal', con=conn, if_exists='append')
