import psycopg2
import random


conn = psycopg2.connect(user="ecxzqtzfjeihgc",
                                password="618dfca07119f8cf853cd7e9985ed4d7701c8bf4412804c8644f4120e04f03cb",
                                host="ec2-35-153-12-59.compute-1.amazonaws.com",
                                port="5432",
                                database="deeuk8ikachdv6")
cursor = conn.cursor()
n=0.0
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
        date="20%s/%s/%s"%(year,mounth,day)
        if i=='argentina':
            n = round(random.uniform(0.009,0.02),4)
        elif i=='chile':
            n = round(random.uniform(0.001,0.0015),4)
        else:
            n = round(random.uniform(1.3,1),4)
        cursor.execute("insert into conversiondolaresMockup (dia,valor,moneda) values (%s,%s,%s)",(date,n,i))
conn.commit()