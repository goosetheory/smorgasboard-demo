import json
import re
import time
import pprint
import urllib
import time

from jose import jwk, jwt
from jose.utils import base64url_decode
from cognitoutils import get_keys

from secrets_client import SecretsClient

# # instead of re-downloading the public keys every time
# # we download them only on cold start
# # https://aws.amazon.com/blogs/compute/container-reuse-in-lambda/
keys = get_keys()

secrets_client = SecretsClient()
app_client_id = secrets_client.get_cognito_app_client_id()

def handler(event, context):
	"""validate the incoming token"""
	"""and produce the principal user identifier associated with the token"""

	"""this could be accomplished in a number of ways:"""
	"""1. Call out to OAuth provider"""
	"""2. Decode a JWT token inline"""
	"""3. Lookup in a self-managed DB"""
	token = event.get('queryStringParameters', {}).get('authorizer')
	if not token:
		raise Exception('Unauthorized')
	unverified_claims = jwt.get_unverified_claims(token)
	principalId = jwt.get_unverified_claims(token).get('cognito:username')

	"""you can send a 401 Unauthorized response to the client by failing like so:"""
	"""raise Exception('Unauthorized')"""

	"""if the token is valid, a policy must be generated which will allow or deny access to the client"""

	"""if access is denied, the client will recieve a 403 Access Denied response"""
	"""if access is allowed, API Gateway will proceed with the backend integration configured on the method that was called"""

	"""this function must generate a policy that is associated with the recognized principal user identifier."""
	"""depending on your use case, you might store policies in a DB, or generate them on the fly"""

	"""keep in mind, the policy is cached for 5 minutes by default (TTL is configurable in the authorizer)"""
	"""and will apply to subsequent calls to any method/resource in the RestApi"""
	"""made with the same token"""

	"""the example policy below denies access to all resources in the RestApi"""

	tmp = event['methodArn'].split(':')
	apiGatewayArnTmp = tmp[5].split('/')
	awsAccountId = tmp[4]

	policy = AuthPolicy(principalId, awsAccountId)
	policy.restApiId = apiGatewayArnTmp[0]
	policy.region = tmp[3]
	policy.stage = apiGatewayArnTmp[1]

	try:
		print('getting claims...')
		claims = get_claims(event, context)
		print('claims: ' + json.dumps(claims))
		if claims != False:
			policy.allowAllRoutes()
		else:
			policy.denyAllRoutes()

	except:
		policy.denyAllRoutes()


	# Finally, build the policy
	authResponse = policy.build()

	# new! -- add additional key-value pairs associated with the authenticated principal
	# these are made available by APIGW like so: $context.authorizer.<key>
	# additional context is cached
	context = {
		'key': 'value', # $context.authorizer.key -> value
		'number' : 1,
		'bool' : True
	}
	# context['arr'] = ['foo'] <- this is invalid, APIGW will not accept it
	# context['obj'] = {'foo':'bar'} <- also invalid

	authResponse['context'] = context

	return authResponse


def get_claims(event, context):
	token = event.get('queryStringParameters', {}).get('authorizer')
	if not token:
		raise Exception('Unauthorized')

	# get the kid from the headers prior to verification
	headers = jwt.get_unverified_headers(token)
	kid = headers['kid']
	# search for the kid in the downloaded public keys
	key_index = -1
	for i in range(len(keys)):
		if kid == keys[i]['kid']:
			key_index = i
			break
	if key_index == -1:
		print('Public key not found in jwks.json')
		return False
	# construct the public key
	public_key = jwk.construct(keys[key_index])
	# get the last two sections of the token,
	# message and signature (encoded in base64)
	message, encoded_signature = str(token).rsplit('.', 1)
	# decode the signature
	decoded_signature = base64url_decode(encoded_signature.encode('utf-8'))
	# verify the signature
	if not public_key.verify(message.encode("utf8"), decoded_signature):
		print('Signature verification failed')
		return False

	print('Signature successfully verified')
	# since we passed the verification, we can now safely
	# use the unverified claims
	claims = jwt.get_unverified_claims(token)
	# additionally we can verify the token expiration
	if time.time() > claims['exp']:
		print('Token is expired')
		return False

	# and the Audience  (use claims['client_id'] if verifying an access token)
	if 'aud' in claims and claims['aud'] != app_client_id:
		print('Token was not issued for this audience')
		return False

	# now we can use the claims
	return claims

# {
#   "sub": "b57ea0ae-ad5a-4ff0-aa6b-1661c0c5725a",
#   "aud": "52qvpq4g4fr31h9r02cfnijf71",
#   "email_verified": true,
#   "token_use": "id",
#   "auth_time": 1547619208,
#   "iss": "https://cognito-idp.us-east-1.amazonaws.com/us-east-1_PUkU7rkEP",
#   "cognito:username": "foobar@gmail.com",
#   "exp": 1547622808,
#   "iat": 1547619208,
#   "email": "foobar@gmail.com"
# }

class AuthPolicy(object):
	awsAccountId = ""
	"""The AWS account id the policy will be generated for. This is used to create the method ARNs."""
	principalId = ""
	"""The principal used for the policy, this should be a unique identifier for the end user."""
	version = "2012-10-17"
	"""The policy version used for the evaluation. This should always be '2012-10-17'"""
	pathRegex = "^[/.a-zA-Z0-9-\*]+$"
	"""The regular expression used to validate resource paths for the policy"""

	"""these are the internal lists of allowed and denied methods. These are lists
	of objects and each object has 2 properties: A resource ARN and a nullable
	conditions statement.
	the build method processes these lists and generates the approriate
	statements for the final policy"""
	allowMethods = []
	denyMethods = []

	restApiId = "*"
	"""The API Gateway API id. By default this is set to '*'"""
	region = "*"
	"""The region where the API is deployed. By default this is set to '*'"""
	stage = "*"
	"""The name of the stage used in the policy. By default this is set to '*'"""

	def __init__(self, principal, awsAccountId):
		self.awsAccountId = awsAccountId
		self.principalId = principal
		self.allowMethods = []
		self.denyMethods = []

	def _addRoute(self, effect, route, conditions):
		"""Adds a route to the internal lists of allowed or denied methods. Each object in
		the internal list contains a resource ARN and a condition statement. The condition
		statement can be null."""
		resourceArn = ("arn:aws:execute-api:" +
			self.region + ":" +
			self.awsAccountId + ":" +
			self.restApiId + "/" +
			self.stage + "/" +
			route)

		if effect.lower() == "allow":
			self.allowMethods.append({
				'resourceArn' : resourceArn,
				'conditions' : conditions
			})
		elif effect.lower() == "deny":
			self.denyMethods.append({
				'resourceArn' : resourceArn,
				'conditions' : conditions
			})

	def _getEmptyStatement(self, effect):
		"""Returns an empty statement object prepopulated with the correct action and the
		desired effect."""
		statement = {
			'Action': 'execute-api:Invoke',
			'Effect': effect[:1].upper() + effect[1:].lower(),
			'Resource': []
		}

		return statement

	def _getStatementForEffect(self, effect, methods):
		"""This function loops over an array of objects containing a resourceArn and
		conditions statement and generates the array of statements for the policy."""
		statements = []

		if len(methods) > 0:
			statement = self._getEmptyStatement(effect)

			for curMethod in methods:
				if curMethod['conditions'] is None or len(curMethod['conditions']) == 0:
					statement['Resource'].append(curMethod['resourceArn'])
				else:
					conditionalStatement = self._getEmptyStatement(effect)
					conditionalStatement['Resource'].append(curMethod['resourceArn'])
					conditionalStatement['Condition'] = curMethod['conditions']
					statements.append(conditionalStatement)

			statements.append(statement)

		return statements

	def allowAllRoutes(self):
		"""Adds a '*' allow to the policy to authorize access to all methods of an API"""
		self._addRoute("Allow", "*", [])

	def denyAllRoutes(self):
		"""Adds a '*' allow to the policy to deny access to all methods of an API"""
		self._addRoute("Deny", "*", [])

	def allowRoute(self, route):
		"""Adds an API Gateway method (Http verb + Resource path) to the list of allowed
		methods for the policy"""
		self._addRoute("Allow", route, [])

	def denyRoute(self, verb, resource):
		"""Adds an API Gateway method (Http verb + Resource path) to the list of denied
		methods for the policy"""
		self._addRoute("Deny", route, [])

	def allowRouteWithConditions(self, route, conditions):
		"""Adds an API Gateway method (Http verb + Resource path) to the list of allowed
		methods and includes a condition for the policy statement. More on AWS policy
		conditions here: http://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_elements.html#Condition"""
		self._addRoute("Allow", route, conditions)

	def denyRouteWithConditions(self, route, conditions):
		"""Adds an API Gateway method (Http verb + Resource path) to the list of denied
		methods and includes a condition for the policy statement. More on AWS policy
		conditions here: http://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_elements.html#Condition"""
		self._addRoute("Deny", route, conditions)

	def build(self):
		"""Generates the policy document based on the internal lists of allowed and denied
		conditions. This will generate a policy with two main statements for the effect:
		one statement for Allow and one statement for Deny.
		Methods that includes conditions will have their own statement in the policy."""
		if ((self.allowMethods is None or len(self.allowMethods) == 0) and
			(self.denyMethods is None or len(self.denyMethods) == 0)):
			raise NameError("No statements defined for the policy")

		policy = {
			'principalId' : self.principalId,
			'policyDocument' : {
				'Version' : self.version,
				'Statement' : []
			}
		}

		policy['policyDocument']['Statement'].extend(self._getStatementForEffect("Allow", self.allowMethods))
		policy['policyDocument']['Statement'].extend(self._getStatementForEffect("Deny", self.denyMethods))

		return policy
