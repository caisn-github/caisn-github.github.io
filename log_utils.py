import time
import requests

site_url="http://experiment.localnas.srcserver.xyz"

with open("../machine.txt","r") as f:
    machineName=f.read().strip()

def log(message:str)->None:
    while True:
        data = {
            'machineName':machineName,
            'message': message
        }
        response=requests.post(f"{site_url}/log/upload/",data=data).text
        if response=="ok":
            break
        time.sleep(1)

def data_upload(table_name:str,record:dict)->None:
    data={}
    data['username']="shao0099876"
    data['password']='shao0123ruo'
    record['machineName']=machineName
    data['record']=record
    while True:
        response=requests.post(f"{site_url}/data/{table_name}/upload/",json=data).text
        if response=="OK":
            break
        time.sleep(1)