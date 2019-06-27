import requests


import conf


user = conf.usr
pwd = conf.pas
host = conf.host

headers = {"Content-Type":"application/json","Accept":"application/json"}

query = 'assignment_group=f617a9a7db3ba7000cdf9693db961908^state!=6^active=true'



url=host+'/api/now/table/incident?sysparm_query='+query 
headers = {"Content-Type":"application/json","Accept":"application/json"}



response = requests.get(url, auth=(user, pwd), headers=headers )


if response.status_code != 200: 
    print('Status:', response.status_code, 'Headers:', response.headers, 'Error Response:',response.json())
    exit()

data=response.json().get('result','')
print(response)

for inc in data:
    
    print("incident = {}, sys_id = {} , with sh \" {} \" ".format(inc['number'],inc['sys_id'],inc['short_description']))
        
