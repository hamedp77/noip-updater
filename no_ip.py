"""No-IP Update Client

This script simply updates hostnames provided by No-IP.
No-IP is a DDNS (Dynamic DNS) provider which offers free and paid tier DDNS services.
You can also import it as a module and use its functions like dns_query() or get_ip().
"""

import logging
import os
import sys
from base64 import b64encode
from time import sleep

import requests
from dotenv import load_dotenv

INTERVAL = 60 # in seconds
RETRIES = 3
logging.basicConfig(format='%(asctime)s [%(levelname)s] %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S', level=logging.INFO)


def get_ip():
    """Get current public IPv4 address of the client machine."""

    ip_info_endpoint = 'https://2ip.io'
    headers = {'User-Agent': 'curl/8.0.1'}

    try:
        response = requests.get(ip_info_endpoint, headers=headers, timeout=2)
    except requests.exceptions.Timeout:
        logging.error('%s took too long to respond.',
                      ip_info_endpoint.removeprefix('https://'))
        retry()

    if response.ok:
        return response.text.strip()

    logging.error(
        'An error occurred while trying to retrieve machine\'s IP address. (%s %s)',
        response.status_code, response.reason)
    retry()


def dns_query(name, type_='A'):
    """Simple DNS query resolver using Google's DNS over HTTPS endpoint."""

    doh_url = 'https://8.8.8.8/resolve'
    url_params = {'name': name, 'type': type_}

    try:
        response = requests.get(doh_url, params=url_params, timeout=2)
    except requests.exceptions.Timeout:
        logging.error('DoH server took too long to respond.')
        retry()

    if response.ok:
        try:
            return response.json()['Answer'][0]['data']
        except (IndexError, KeyError):
            logging.error('An error occured while returning DNS response.')
            retry()

    logging.error(
        'An error occurred while trying to retrieve machine\'s IP address. (%s %s)',
        response.status_code, response.reason)
    retry()


def update_hostname(new_ip):
    """Update the hostname if any IP change is detected."""

    update_endpoint = 'https://dynupdate.no-ip.com/nic/update'
    email = os.environ.get('NOIP_EMAIL')
    password = os.environ.get('NOIP_PASSWORD')
    hostname = os.environ.get('NOIP_HOSTNAME')

    if not (email and password and hostname):
        logging.error(
            'Missing account information. Check .env file or system\'s environment variables.')
        logging.info('Stopping service.')
        sys.exit()

    authstring = b64encode(f'{email}:{password}'.encode())
    headers = {'User-Agent': 'curl/8.0.1',
               'Authorization': f'Basic {authstring.decode()}'}
    url_params = {'hostname': hostname, 'myip': new_ip}

    try:
        response = requests.get(update_endpoint, headers=headers,
                                params=url_params, timeout=5)
    except requests.exceptions.Timeout:
        logging.error('No-IP API took too long to respond.')
        retry()

    response_handler(response.text.strip())


def check_for_ip_change():
    """
    Query Google DoH servers and get the A record that the HOSTNAME is pointing to.
    Compare that with current IP address and update if necessary.
    """

    hostname = os.environ.get('NOIP_HOSTNAME')
    if not hostname:
        logging.error(
            'No hostname was provided. Check .env file or system\'s environment variables.')
        logging.info('Stopping service.')
        sys.exit()
    current_ip = dns_query(hostname)
    if get_ip() != current_ip:
        logging.info('New IP Detected, Updating Hostname...')
        current_ip = get_ip()
        update_hostname(current_ip)
    else:
        logging.info('No IP Change Detected.')


def response_handler(noip_response):
    """Parse the response from No-IP and output relevant errors or messages."""

    if 'good' in noip_response:
        logging.info('Update Successful! %s', noip_response.split(' ')[1])
    elif 'nochg' in noip_response:
        logging.info('Hostname already up to date. %s',
                     noip_response.split(' ')[1])
    elif 'nohost' in noip_response:
        logging.error('Hostname supplied does not exist under specified account. '
                      'Please double check your information and try again.')
        logging.info('Stopping service.')
        sys.exit()
    elif 'badauth' in noip_response:
        logging.error('Invalid username or password. '
                      'Please double check your information and try again.')
        logging.info('Stopping service.')
        sys.exit()
    elif 'badagent' in noip_response:
        logging.error('Client disabled. Contact the developer(s).')
        logging.info('Stopping service.')
        sys.exit()
    elif '!donator' in noip_response:
        logging.error('Feature not available.')
        logging.info('Stopping service.')
        sys.exit()
    elif 'abuse' in noip_response:
        logging.error('Username is blocked due to abuse.')
        logging.info('Stopping service.')
        sys.exit()
    elif '911' in noip_response:
        logging.error('Fatal Error Occurred! Try again in 30 minutes.')
        logging.info('Stopping service.')
        sys.exit()


def retry():
    """"Basically the main function but executes the checking loop only.
    This will allow to retry in case of any errors.
    """
    global RETRIES

    if RETRIES:
        logging.info('Retrying...')
        RETRIES -= 1
        while True:
            check_for_ip_change()
            RETRIES = 3
            sleep(INTERVAL)

    logging.info('Reached maximum retries.')
    logging.info('Stopping service.')
    sys.exit()

def main():
    """start the script and check IP changes based on set INTERVAL."""

    load_dotenv()
    logging.info('Starting Service...')
    while True:
        check_for_ip_change()
        sleep(INTERVAL)


if __name__ == '__main__':
    main()
