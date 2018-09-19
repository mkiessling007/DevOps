#!/bin/python

# Import the modules required to make API calls
import requests
import json
from requests.auth import HTTPBasicAuth

# Disable warnings
requests.packages.urllib3.disable_warnings()


def settings():
 '''Set all variables.


 Takes no argument.


 Returns: tuple (APIC-EM, REST-API call, payload, headers)
 '''
 #rest_call = '/api/v1/ticket'
 #apic_em_ip = 'https://sandboxapicem.cisco.com'
 #payload = {'username':'devnetuser','password':'Cisco123!'}
 #headers = {'content-type' : 'application/json'}
 rest_call = '/api/v1/ticket'
 apic_em_ip = 'https://primeinfrasandbox.cisco.com'
 payload = {'username':'devnetuser','password':'DevNet123!'}
 headers = {'content-type' : 'application/json'}

 return ((apic_em_ip, rest_call, payload, headers))


def getToken():
 '''Get APIC-EM authentication token


 Doesn't take any keyword arguments. Only calls settings() and connects
 to APIC-EM to receive a authentication token.


 Returns: string
 '''
 # Read the settings on write to variable
 setting = settings()
 # Build the URL
 url = setting[0] + setting[1]
 # Call POST and assign the response to a variable and put it into JSON formatting
 response = requests.post(url, data=json.dumps(setting[2]), headers=setting[3], verify=False).json()
 # Extract the authentication token
 token = response['response']['serviceTicket']

 # Return the authentication token
 return (token)


def callRest(rest_uri, token):
 '''REST-API GET request


 Takes two arguments:
 rest_uri = eg /network-device
 token = authentication token to build the header


 Returns: dictionary
 '''
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
 

def main():
 #token = getToken()
 #output = callRest('/api/v1/network-device', token)
 #for device in output['response']:
     #print ('Hostname: ' + device['hostname'])
 output = callPrime('/webacs/api/v3/data/Devices.json')
 print (hJson(output))

if __name__ == '__main__':
 main()

