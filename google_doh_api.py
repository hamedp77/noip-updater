import requests
import json

def dns_query(name, type):

    r = requests.get(f'https://8.8.8.8/resolve?name={name}&type={type}')
    
    return r.json()['Answer'][0]['data']
