#!/usr/bin/env python

# Import the modules required to make REST-API calls
import requests
import json
import argparse
import logging
import sys
from requests.auth import HTTPBasicAuth

# Disable warnings
requests.packages.urllib3.disable_warnings()

def check_args():
 parser = argparse.ArgumentParser(prog=sys.argv[0], description='Make REST-API calls with HTTPS')

 parser.add_argument('-a', '--host', type=str, required=True,
                     help="Device IP address or Hostname")
 parser.add_argument('-u', '--username', type=str, required=True,
                     help="Device Username (REST-API server username)")
 parser.add_argument('-p', '--password', type=str, required=True,
                     help="Device Password (REST-API server password)")
 parser.add_argument('-d', '--debug', action='store_true',
                     help="Enable basic debugging")
 parser.add_argument('--prime', action='store_true',
                     help="REST-API server is Cisco Prime Infrastructure")
 parser.add_argument('--html', action='store_true',
                     help="Output will be HTML formated for use with a web framework (eg Flask)")
 parser.add_argument('-c', '--call', type=str, required=True,
                     help="REST-API call, eg. /api/v1/network-device")

 parser.set_defaults(debug=False)
 args = parser.parse_args()

 if args.debug:
  logging.basicConfig(level=logging.DEBUG)

 return args



def getToken(args):
 '''Get APIC-EM authentication token

 Doesn't take any keyword arguments. Only calls settings() and connects
 to APIC-EM to receive a authentication token. This function is only used
 for APIC-EM systems.

 Returns: string
 '''
 payload = {'username': args.username,'password': args.password}
 headers = {'content-type' : 'application/json'}
 # Build the URL (IP address + rest_call)
 url = 'https://' + args.host + '/api/v1/ticket'
 # Call POST and assign the response to a variable and put it into JSON formatting
 response = requests.post(url, data=json.dumps(payload), headers=headers, verify=False)
 # Check if we received a 401 due to wrong user credentials
 if response.status_code == 404:
      print("404: Wrong user credentials")
      exit(1)
 response = response.json()
 # Extract the authentication token
 token = response['response']['serviceTicket']

 # Return the authentication token
 return (token)


def callApic(args):
 '''REST-API GET request

 Use this class to perform a REST-API call against a APIC-EM server.
 Takes two arguments:
 rest_uri = eg /network-device

 Returns: dictionary
 '''
 # Get authentication token with function "token"
 token = getToken(args)
 # Build the header
 headers = {'X-AUTH-TOKEN': token}
 # Build the URL
 url = 'https://' + args.host + args.call
 # Call GET and assign the response to a variable
 response = requests.get(url, headers=headers, verify=False)
  # Check if we received a 401 due to wrong user credentials
 if response.status_code == 401:
     print("401: Unauthorized Access - Access Prohibited")
     exit(1)
 # Transform the received data into a JSON dictionary
 response=response.json()
 # Return the respons as dictionary json
 return (response)


def callPrime(args):
 '''REST-API GET request

 Use this class to perform a REST-API call against a Cisco Prime Server server.
 Takes two arguments:
 rest_uri = eg /network-device

 Returns: dictionary
 '''
 # Build the HTTP authentication
 basic_auth = HTTPBasicAuth(args.username, args.password)
 # Build the URL
 url = 'https://' + args.host + args.call
 # Call GET and assign the response to a variable
 response = requests.get(url, auth=basic_auth, verify=False)
 # Check if we received a 401 due to wrong user credentials
 if response.status_code == 401:
     print("401: Unauthorized Access - Access Prohibited")
     exit(1)
 # Transform the received data into a JSON dictionary
 response=response.json()
 # Return the respons as dictionary json
 return (response)


def printApicResponse(apic_response):
 for data in apic_response['response']:
     print(json.dumps(data, sort_keys=True, indent=4))


def printHTMLApicResponse(apic_response, args):
 print('<h2>https://' + args.host + args.call + '</h2>')
 # All interresting information should be in key "response"
 for data in apic_response['response']:
     print('<p>')
     print(json.dumps(data, sort_keys=True, indent=4 , separators=('<br>&emsp;', ':')))
     print('</p>')


def printHTMLPrimeResponse(prime_response, args):
 print('<h2>https://' + args.host + args.call + '</h2>')
 # If we have to deal with a Cisco Prime, the received JSON format is different to APIC controllers
 for data in prime_response['queryResponse']['entityId']:
     print('<p>')
     print(json.dumps(data, sort_keys=True, indent=4 , separators=('<br>&emsp;', ':')))
     print('</p>')


def demoApic(args):
 # Demo using Cisco APIC-EM controller
 # use this api call: /api/v1/network-device
 output = callApic(args)
 for device in output['response']:
     print ('Hostname: ' + device['hostname'])


def demoPrime(args):
 # Demo using Cisco Prime Infrastructure
 # Use this api call: /webacs/api/v3/data/Devices.json
 output = callPrime(args)
 for device in output['queryResponse']['entityId']:
     device_detail_url = device['@url']
     device_detail_url = device_detail_url.lstrip('https://primeinfrasandbox.cisco.com')
     device_detail = callPrime('/' + device_detail_url + '.json')
     try:
        print (device_detail['queryResponse']['entity'][0]['devicesDTO']['deviceType'])
     except KeyError:
        print (device_detail['queryResponse']['entity'][0]['devicesDTO']['managementStatus'])


def main():
 args = check_args()
 if args.prime:
  # demoPrime(args)
  output = callPrime(args)
  if args.html:
      printHTMLPrimeResponse(output, args)
  else:
      printPrimeResponse(output)
 else:
  #demoApic(args)
  output = callApic(args)
  if args.html:
   printHTMLApicResponse(output, args)
  else:
   printApicResponse(output)

if __name__ == '__main__':
 main()
