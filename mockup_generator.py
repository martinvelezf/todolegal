import sqlite3
import random
import pandas as pd


conn = sqlite3.connect("./test.db")

n=0.0
lista=[]
for i in ['argetina','chile','euro']:
    for row in range(0,5):
        mounth=str(random.randint(1,12))
        year=str(random.randint(15,20))
        day=str(random.randint(1,28))
        if len(day)==1:
            day='0'+day
        if len(year)==1:
            year='0'+year
        if len(mounth)==1:
            mounth='0'+mounth
        date="20%s-%s-%s"%(year,mounth,day)
        if i=='argentina':
            n = round(random.uniform(0.009,0.02),4)
        elif i=='chile':
            n = round(random.uniform(0.001,0.0015),4)
        else:
            n = round(random.uniform(1.3,1),4)
        cursor = conn.cursor()
        lista.append({'dia':date,'valor':n,'moneda':i})
pd.DataFrame(lista).to_sql('cambio_artificial', con=conn, if_exists='append') 
        