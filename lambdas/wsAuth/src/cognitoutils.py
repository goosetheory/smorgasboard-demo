import json
import urllib.request
import os

region = os.environ['AWS_REGION']
userpool_id = os.environ['AUTH_AMPLIFYCOGNITO_USERPOOLID']
keys_url = 'https://cognito-idp.{}.amazonaws.com/{}/.well-known/jwks.json'.format(region, userpool_id)

def get_keys():
    with urllib.request.urlopen(keys_url) as response:
    	return json.loads(response.read())['keys']
