#db

import os
import psycopg2
import csv

conn = psycopg2.connect(user="ecxzqtzfjeihgc",
                                password="618dfca07119f8cf853cd7e9985ed4d7701c8bf4412804c8644f4120e04f03cb",
                                host="ec2-35-153-12-59.compute-1.amazonaws.com",
                                port="5432",
                                database="deeuk8ikachdv6")
cursor = conn.cursor()

for i in ['argetina.csv','chile.csv','euro.csv']:
    with open(i) as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        c=0
        for row in readCSV:
            if c!=0:
                if c>5:
                    break
                else:
                    cursor.execute("insert into conversiondolares(dia,valor,moneda) values (%s,%s,%s)",(row[0].replace('.','/'),row[1].replace(',','.'),i.replace('.csv','')))                
            c+=1


conn.commit()
