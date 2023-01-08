import requests
import json

def dns_query(name, type):

    req = requests.get(f'https://8.8.8.8/resolve?name={name}&type={type}')
    
    jsonResponse = json.loads(req.content)

    return jsonResponse['Answer'][0]['data']
