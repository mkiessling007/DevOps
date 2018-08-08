#!python

# Import the modules required to make API calls
import requests
import json

# Disable warnings
requests.packages.urllib3.disable_warnings()

def settings(rest_call = '/api/v1/ticket'):
 '''Set all variables.


 Doesn't take any keyword arguments. Set directly within script.


 Returns: tuple (APIC-EM, REST-API call, payload, headers)
 '''
 apic_em_ip = 'https://sandboxapicem.cisco.com'
 payload = {'username':'devnetuser','password':'Cisco123!'}
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
 # Assign the response to a variable and put it into JSON formatting
 response = requests.post(url, data=json.dumps(setting[2]), headers=setting[3], verify=False).json()

 # Return the response body
 return (response)

def main():
 token = getToken()
 #print (token)
 token = token['response']['serviceTicket']
 print ('Authentication Token: ' + token)

if __name__ == '__main__':
 main()