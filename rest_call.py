#!/bin/python

# Import the modules required to make REST-API calls
import requests
import json
from requests.auth import HTTPBasicAuth

# Disable warnings
requests.packages.urllib3.disable_warnings()


def settings():
 '''Set all variables.


 Takes no argument. Set server IP address or hostname and username and password.
 The "rest_call" variable is only used for requesting a aut ticket on APIC-EM systems.


 Returns: tuple (Server, REST-API call, payload, headers)
 '''
 rest_call = '/api/v1/ticket'
 apic_em_ip = 'https://sandboxapicem.cisco.com'
 payload = {'username':'devnetuser','password':'Cisco123!'}
 headers = {'content-type' : 'application/json'}
 #rest_call = '/api/v1/ticket'
 #apic_em_ip = 'https://primeinfrasandbox.cisco.com'
 #payload = {'username':'devnetuser','password':'DevNet123!'}
 #headers = {'content-type' : 'application/json'}

 return ((apic_em_ip, rest_call, payload, headers))


def getToken():
 '''Get APIC-EM authentication token


 Doesn't take any keyword arguments. Only calls settings() and connects
 to APIC-EM to receive a authentication token. This function is only used
 for APIC-EM systems.


 Returns: string
 '''
 # Read the settings to set the variables needed to call for the authentication token
 setting = settings()
 # Build the URL (IP address + rest_call)
 url = setting[0] + setting[1]
 # Call POST and assign the response to a variable and put it into JSON formatting
 response = requests.post(url, data=json.dumps(setting[2]), headers=setting[3], verify=False).json()
 # Extract the authentication token
 token = response['response']['serviceTicket']

 # Return the authentication token
 return (token)


def callApic(rest_uri):
 '''REST-API GET request


 Use this class to perform a REST-API call against a APIC-EM server.
 Takes two arguments:
 rest_uri = eg /network-device


 Returns: dictionary
 '''
 # Get authentication token with function "token"
 token = getToken()
 # Build the header
 headers = {'X-AUTH-TOKEN': token}
 # Get settings for REST-API call
 setting = settings()
 # Build the URL
 url = setting[0] + rest_uri
 # Call GET and assign the response to a variable
 response = requests.get(url, headers=headers, verify=False).json()

 # Return the respons as dictionary json
 return (response)


def callPrime(rest_uri):
 '''REST-API GET request


 Use this class to perform a REST-API call against a Cisco Prime Server server.
 Takes two arguments:
 rest_uri = eg /network-device


 Returns: dictionary
 '''
 # Get settings
 setting = settings()
 # Build the HTTP authentication
 basic_auth = HTTPBasicAuth(setting[2]['username'], setting[2]['password'])
 # Build the URL
 url = setting[0] + rest_uri
 # Call GET and assign the response to a variable
 response = requests.get(url, auth=basic_auth, verify=False).json()

 # Return the respons as dictionary json
 return (response)


def hJson(jsonDict):
 '''Print json in a human readable format
 
 
 Takes one argument:
 jsonDict = A json formatted data
 
 
 Returns: string
 '''
 readable = json.dumps(jsonDict, sort_keys=True, indent=4)
 return (readable)


def demoApic(): 
 # Demo using Cisco APIC-EM controller
 output = callApic('/api/v1/network-device')
 for device in output['response']:
     print ('Hostname: ' + device['hostname'])


def demoPrime():
 # Demo using Cisco Prime Infrastructure
 output = callPrime('/webacs/api/v3/data/Devices.json')
 for device in output['queryResponse']['entityId']:
     device_detail_url = device['@url']
     device_detail_url = device_detail_url.lstrip('https://primeinfrasandbox.cisco.com')
     device_detail = callPrime('/' + device_detail_url + '.json')
     try:
        print (device_detail['queryResponse']['entity'][0]['devicesDTO']['deviceType'])
     except KeyError:
        print (device_detail['queryResponse']['entity'][0]['devicesDTO']['managementStatus'])


def main():
 demoApic()

if __name__ == '__main__':
 main()

