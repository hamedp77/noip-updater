import requests
import datetime
from base64 import b64encode, b64decode
from time import sleep
from google_doh_api import dns_query

ENDPOINT = 'https://dynupdate.no-ip.com/nic/update'
USERNAME = 'hamedp77@gmail.com'
PASSWORD = 'h@med103070'
HOSTNAME = 'hmdnetwork.ddns.net'
INTERVAL = 5 # in seconds
AUTHSTRING = b64encode(USERNAME.encode() + ':'.encode() + PASSWORD.encode())

def getIP():
    
    # get current public IPv4 address of the client machine

    ipInfoEndpoint = 'https://2ip.io'
    headers = {'User-Agent': 'curl/7.83.1'}

    r = requests.get(ipInfoEndpoint, headers=headers)

    return r.text.replace('\n', '')


def updateHostname(newIP):

    # update the hostname if any IP change is detected

    headers = {'User-Agent': 'curl/7.83.1', 'Authorization': 'Basic ' + AUTHSTRING.decode()}

    r = requests.get(ENDPOINT + f'?hostname={HOSTNAME}&myip={newIP}', headers=headers)

    if r.status_code != 200:
        print(datetime.datetime.now(), ': Update Failed!')
    else:
        errorHandling(r.text.replace('\r\n', ''))


def checkForIpChange(interval):

    '''
    Query Google DoH servers and get the A record that the HOSTNAME is pointing to.
    Compare that with current IP address and update if necessary.

    '''

    currentIP = dns_query(HOSTNAME, 'a')
    while True:
        if getIP() != currentIP:
            print(datetime.datetime.now(), ': New IP Detected, Updating Hostname...')
            currentIP = getIP()
            updateHostname(currentIP)
        else:
            print(datetime.datetime.now(), ': No IP Change Detected')
        sleep(interval)

def errorHandling(noipResponse):

    # Parse the response from No-IP and output the errors, if any occured

    if 'good' in noipResponse:
        print(datetime.datetime.now(), ': Update Successful! ', noipResponse.split(' ')[1])
    elif 'nohost' in noipResponse:
        print(datetime.datetime.now(), ''': Hostname supplied does not exist under specified account.
                Please double check your information and try again.''')
        exit()



checkForIpChange(INTERVAL)