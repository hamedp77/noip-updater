import requests

def dns_query(name, type_):

    doh_url = 'https://8.8.8.8/resolve'
    payload = {'name': name, 'type': type_}
    
    r = requests.get(doh_url, params=payload)
    
    return r.json()['Answer'][0]['data']
