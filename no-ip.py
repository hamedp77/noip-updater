import requests
import datetime
from base64 import b64encode
from time import sleep

ENDPOINT = 'https://dynupdate.no-ip.com/nic/update'
USERNAME = 'hamedp77@gmail.com'
PASSWORD = 'h@med103070'
HOSTNAME = 'hmdnetwork.ddns.net'
INTERVAL = 60  # in seconds
AUTHSTRING = b64encode((USERNAME + ':' + PASSWORD).encode())


def get_ip():
    
    # Get current public IPv4 address of the client machine

    ip_info_endpoint = 'https://2ip.io'
    headers = {'User-Agent': 'curl/7.83.1'}

    r = requests.get(ip_info_endpoint, headers=headers)

    if r.ok:
        return r.text.strip()
    else:
        print(datetime.datetime.now(),
              ': [internal error] An error occurred while trying to retrieve machine\'s IP address.')


def dns_query(name, type_='A'):

    # Simple DNS query resolver using Google's DNS over HTTPS endpoint.

    r = requests.get(f'https://8.8.8.8/resolve?name={name}&type={type_}')

    if r.ok:
        try:
            return r.json()['Answer'][0]['data']

        except (IndexError, KeyError):
            pass
    else:
        print(datetime.datetime.now(),
              ': [internal error] An error occurred while trying to retrieve hostname\'s IP address.')


def update_hostname(new_ip):

    # Update the hostname if any IP change is detected

    headers = {'User-Agent': 'curl/7.83.1', 'Authorization': 'Basic ' + AUTHSTRING.decode()}

    r = requests.get(ENDPOINT + f'?hostname={HOSTNAME}&myip={new_ip}', headers=headers)

    response_handler(r.text.strip())


def check_for_ip_change():

    """
    Query Google DoH servers and get the A record that the HOSTNAME is pointing to.
    Compare that with current IP address and update if necessary.

    """

    current_ip = dns_query(HOSTNAME)
    if get_ip() != current_ip:
        print(datetime.datetime.now(), ': [info] New IP Detected, Updating Hostname...')
        current_ip = get_ip()
        update_hostname(current_ip)
    else:
        print(datetime.datetime.now(), ': [info] No IP Change Detected')


def response_handler(noip_response):

    # Parse the response from No-IP and output relevant errors or messages.

    if 'good' in noip_response:
        print(datetime.datetime.now(), ': [good] Update Successful! ', noip_response.split(' ')[1])

    elif 'nochg' in noip_response:
        print(datetime.datetime.now(), ': [nochg] Hostname already up to date.', noip_response.split(' ')[1])

    elif 'nohost' in noip_response:
        print(datetime.datetime.now(),
              f': [{noip_response}] Hostname supplied does not exist under specified account.'
              'Please double check your information and try again.')
        exit()

    elif 'badauth' in noip_response:
        print(datetime.datetime.now(),
              f': [{noip_response}] Invalid username or password.'
              f'Please double check your information and try again.')
        exit()

    elif 'badagent' in noip_response:
        print(datetime.datetime.now(),
              f': [{noip_response}] Client disabled. Contact the developer(s).')
        exit()

    elif '!donator' in noip_response:
        print(datetime.datetime.now(),
              f': [{noip_response}] Feature not available.')

    elif 'abuse' in noip_response:
        print(datetime.datetime.now(),
              f': [{noip_response}] Username is blocked due to abuse.')
        exit()

    elif '911' in noip_response:
        print(datetime.datetime.now(),
              f': [{noip_response}] Fatal Error Occurred! Try again in 30 minutes.')
        exit()


while True:
    check_for_ip_change()
    sleep(INTERVAL)
