import requests
import datetime
from base64 import b64encode, b64decode
from time import sleep

ENDPOINT = 'https://dynupdate.no-ip.com/nic/update'
USERNAME = 'hamedp77@gmail.com'
PASSWORD = 'h@med103070'
HOSTNAME = 'hmdnetwork.ddns.net'
INTERVAL = 60 # in seconds
AUTHSTRING = b64encode((USERNAME + ':' + PASSWORD).encode())


def getIP():
    
    # Get current public IPv4 address of the client machine

    ipInfoEndpoint = 'https://2ip.io'
    headers = {'User-Agent': 'curl/7.83.1'}

    r = requests.get(ipInfoEndpoint, headers=headers)

    if r.status_code == 200:
        return r.text.strip()
    else:
        print(datetime.datetime.now(), ': [internal error] An error occured while trying to retrieve machine\'s IP address.')


def dnsQuery(name, type='A'):

    # Simple DNS query resolver using Google's DNS over HTTPS endpoint.

    r = requests.get(f'https://8.8.8.8/resolve?name={name}&type={type}')

    if r.status_code == 200:
        try:
            return r.json()['Answer'][0]['data']

        except (IndexError, KeyError):
            pass
    else:
        print(datetime.datetime.now(), ': [internal error] An error occured while trying to retreive hostname\'s IP address.')

def updateHostname(newIP):

    # Update the hostname if any IP change is detected

    headers = {'User-Agent': 'curl/7.83.1', 'Authorization': 'Basic ' + AUTHSTRING.decode()}

    r = requests.get(ENDPOINT + f'?hostname={HOSTNAME}&myip={newIP}', headers=headers)

    responseHandler(r.text.strip())


def checkForIpChange():

    '''
    Query Google DoH servers and get the A record that the HOSTNAME is pointing to.
    Compare that with current IP address and update if necessary.

    '''

    currentIP = dnsQuery(HOSTNAME)
    if getIP() != currentIP:
        print(datetime.datetime.now(), ': [info] New IP Detected, Updating Hostname...')
        currentIP = getIP()
        updateHostname(currentIP)
    else:
        print(datetime.datetime.now(), ': [info] No IP Change Detected')


def responseHandler(noipResponse):

    # Parse the response from No-IP and output relevant errors or messages.

    if 'good' in noipResponse:
            print(datetime.datetime.now(), ': [good] Update Successful! ', noipResponse.split(' ')[1])

    elif 'nochg' in noipResponse:
        print(datetime.datetime.now(), ': [nochg] Hostname already up to date.', noipResponse.split(' ')[1])

    elif 'nohost' in noipResponse:
        print(datetime.datetime.now(), f': [{noipResponse}] Hostname supplied does not exist under specified account. Please double check your information and try again.')
        exit()

    elif 'badauth' in noipResponse:
        print(datetime.datetime.now(), f': [{noipResponse}] Invalid username or password. Please double check your information and try again.')
        exit()

    elif 'badagent' in noipResponse:
        print(datetime.datetime.now(), f': [{noipResponse}] Client disabled. Contact the developer(s).')
        exit()

    elif '!donator' in noipResponse:
        print(datetime.datetime.now(), f': [{noipResponse}] Feature not available.')

    elif 'abuse' in noipResponse:
        print(datetime.datetime.now(), f': [{noipResponse}] Username is blocked due to abuse.')
        exit()

    elif '911' in noipResponse:
        print(datetime.datetime.now(), f': [{noipResponse}] Fatal Error Occured! Try again in 30 minutes.')
        exit()


while True:
    checkForIpChange()
    sleep(INTERVAL)
