import dweepy
import time
from json import dumps

from httplib2 import Http
msg={}
for i in range(1,16):  
    a=dweepy.get_latest_dweet_for('thecore')
    msg[i]={"humidity":a[0]['content']["humidity"],"temperature":a[0]['content']["temperature"]}
    print(a[0]['content']["humidity"])
    print(a[0]['content']["temperature"])
    time.sleep(60)

url = 'https://webhook.site/4cb7980d-edf2-4ebc-b19f-92e34aeb7719'
    

message_headers = {'Content-Type': 'application/json; charset=UTF-8'}
http_obj = Http()
response = http_obj.request(
    uri=url,
    method='POST',
    headers=message_headers,
    body=dumps(msg),
)

#ahumidity
