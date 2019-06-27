import requests
import argparse


import conf


user = conf.usr
pwd = conf.pas
host = conf.host

headers = {"Content-Type":"application/json","Accept":"application/json"}

def copy(sys_id, file_name):

    header = {"Content-Type":"application/xml","Accept":"*/*"}
    url=host+"/api/now/attachment/"+sys_id+"/file"
    response = requests.get(url, auth=(user, pwd), headers=header)

    if response.status_code != 200: 
        print('Status:', response.status_code, 'Headers:', response.headers, 'Error Response:',response.json())
        exit()

    with open(file_name,'wb') as file:
        for chunk in response.iter_content(chunk_size=512):
            if chunk:
                file.write(chunk)



def get_attachment(sys_id):
    
    url=host+'/api/now/table/sys_attachment?sysparm_query=table_sys_id%3D'+sys_id
    response = requests.get(url, auth=(user, pwd), headers=headers )

    if response.status_code != 200: 
        print('Status:', response.status_code, 'Headers:', response.headers, 'Error Response:',response.json())
        exit()
        

    lista = response.json().get('result','')

    if lista:

        for element in lista:
            file_name = element.get('file_name','')
            sys_id = element.get('sys_id','')

            if file_name and sys_id:
                copy(sys_id,file_name)
            else:
                break
            
            
    else:
        print('no attachment')

def read_inc_details(sys_id):
    url = 'https://opusflowtest.service-now.com/api/now/table/incident/'+sys_id
    
    headers = {"Content-Type":"application/json","Accept":"application/json"}
	 
    response = requests.get(url, auth=(user, pwd), headers=headers)
		 
    if response.status_code != 200: 
        print('Status:', response.status_code, 'Headers:', response.headers, 'Error Response:',response.json())

        exit()

    data=response.json().get('result','')


    
    print("Incident number: {}".format(data.get('number','')))
    print("Incident subject: {}".format(data.get('short_description','')))
    print("Incident caller: {}".format(data.get('caller_id','')))
    print("Incident assignment group: {}".format(data.get('assignment_group','')))
    print("Incident status: {}".format(data.get('state','')))


def assign(inc_sys_id,usr_sys_id):
    me = 'f914cc97208b60005df5b16d187aabdc'

    if usr_sys_id =='me':
        usr_sys_id=me

    url = host+'/api/now/table/incident/'+inc_sys_id
      
    response = requests.put(url, auth=(user, pwd), headers=headers ,data='{"assigned_to":"'+usr_sys_id+'"}')
		 
    if response.status_code != 200: 
        print('Status:', response.status_code, 'Headers:', response.headers, 'Error Response:',response.json())
        exit()
    

def worknotes(sys_id,text):
    
    url = host+'/api/now/table/incident/'+sys_id

    response = requests.put(url, auth=(user, pwd), headers=headers ,data='{"work_notes":"'+text+'"}')
		 
    if response.status_code != 200: 
        print('Status:', response.status_code, 'Headers:', response.headers, 'Error Response:',response.json())

        exit()

def change_state(sys_id, s):
    state=1
    if s=='new':
        state = 1
    elif s == 'open':
        state = 2
    elif s == 'wip':
        state = -6

    url = host+'/api/now/table/incident/'+sys_id
    response = requests.put(url, auth=(user, pwd), headers=headers ,data='{"state":"'+str(state)+'"}')
		 
    if response.status_code != 200: 
        print('Status:', response.status_code, 'Headers:', response.headers, 'Error Response:',response.json())

        exit()


if __name__=="__main__":

    

    #https://opusflowtest.service-now.com/incident.do?sys_id=00950ad5db86ff00122017a94b96193e

    parser = argparse.ArgumentParser()
    parser.add_argument('id',help='incident system id')
    parser.add_argument('--get',action='store_true',help='get attachment')
    parser.add_argument('--ch_status','-c', choices=['new','open','wip']) #wip = work in progress, new=1, open=2, wip=-6
    parser.add_argument('--worknotes','-w',help='add worknotes')
    parser.add_argument('--read_details','-r',action='store_true',help='read worknotes')
    parser.add_argument('--assign_to','-a',help='provide your sys_id')

    args = parser.parse_args()
    
    if args.id:
        if args.get:
            get_attachment(args.id)
        if args.ch_status:
            change_state(args.id,args.ch_status)
        if args.worknotes:
            worknotes(args.id,args.worknotes)
        if args.read_details:
            read_inc_details(args.id)
        if args.assign_to:
            assign(args.id,args.assign_to)
