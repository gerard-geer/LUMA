#module: requesthandler.py
from datetime import datetime
from lightmanager import LightManager
from aliasmanager import AliasManager
from clientmanager import ClientManager

from singleton import Singleton

@Singleton
class RequestHandler(object):
	"""
	A Singleton that tidies up all "onRequest" behaviours.
	
	Slots:
		_lm (LightManager): Private. A LightManager singleton for use in
		parsing lights in requests.
		_am (AliasManager): Private. An AliasManager singleton used to convert
		client names to client IPs.
		_cm (ClientManager) Private. A ClientManager singleton used to
		communicate with clients.
	"""
	__slots__ = ('_lm', '_am', '_cm')
	def __init__(self):
		self._lm = LightManager.Instance()
		self._am = AliasManager.Instance()
		self._cm = ClientManager.Instance()
		
		self._lm.load()
		self._am.load()
		
	def _sanitizeLightQuery(self, req):
		"""
		Sanitizes a light query. This makes sure that a light query is a
		JSON Dictionary, then that it has the required keys, and the data 
		types of those keys' values	are correct.
		
		Parameters:
			req (JSON): The Dictionary that contains the request.
			
		Returns:
			True if the light query was valid, false otherwise.
			
		Preconditions:
			None.
		"""
		# Make sure the request is a Dictionary.
		if not isinstance(req, dict):
			return False
			
		# Make sure all required keys are present.
		for key in ['uuid', 'query']:
			if key not in req.keys():
				return False
		
		# Verify the types of the keys' values.
		if not isinstance(req['uuid'], str):
			return False
		if not isinstance(req['query'], str):
			return False
			
		# Finally after all that checks out we can return True.
		return True
		
	def _sanitizeStateQuery(self, req):
		"""
		Sanitizes a state query. This makes sure that a state query is a
		JSON Dictionary, then that it has the required keys, and the data 
		types of those keys' values	are correct.
		
		Parameters:
			req (JSON): The Dictionary that contains the request.
			
		Returns:
			True if the light query was valid, false otherwise.
			
		Preconditions:
			None.
		"""
		# Make sure the request is a Dictionary.
		if not isinstance(req, dict):
			return False
			
		# Make sure all required keys are present.
		for key in ['uuid', 'id']:
			if key not in req.keys():
				return False
		
		# Verify the types of the keys' values.
		if not isinstance(req['uuid'], str):
			return False
		if not isinstance(req['id'], str):
			return False
			
		# Finally after all that checks out we can return True.
		return True
		
	def lightQuery(self, req):
		"""
		Handles a query for light instances.
		
		Parameters:
			req (JSON): The Dictionary that contains the request.
			
		Returns:
			A dictionary containing the response to the request.
			
		Preconditions:
			The request be a valid JSON object for this request type.
			
		Postconditions:
			None.
		"""
		# If the request was invalid, we need to transparently return
		# nothing.
		if not self._sanitizeLightQuery(req):
			return {'lights':[]}
			
		requested = []
		
		# Get the subset of all allowed lights.
		allowed = self._lm.getAllowedSubset(req['uuid'])
		print('num allowed: '+str(len(allowed)))
		
		# Gets possible aliases should the query be an IP address.
		possible = self._am.getPossibleAliases(req['query'])
		
		# If the user just sends us nothing, we just send all that's possible.
		if len(req['query']) == 0:
			requested.extend(allowed)
		
		else:
			for light in allowed:
				if 	req['query'] in light['name'] or	\
					req['query'] in	light['id'] or 		\
					req['query'] in light['client']:
					
					requested.append({'id':light['id'],		\
									'name':light['name'],	\
									'client':light['client']})
				else:
				
					for alias in possible:
						if alias in light['client']:
							
							requested.append({'id':light['id'],		\
											'name':light['name'],	\
											'client':light['client']})
		
		return {'lights':requested}
		
	def stateQuery(self, req):
		"""
		Handles a request for a light's state.
		
		Parameters:
			req (JSON): The Dictionary that contains the request.
			
		Returns:
			A dictionary containing the response to the request.
			
		Preconditions:
			The request be a valid JSON object for this request type.
			
		Postconditions:
			The state of the lights supplied is updated, if they exist.
		"""					
		# Sanitize the request.
		if not self._sanitizeStateQuery(req):
			return {'success': False,
					'message': 'Invalid query/request.',
					'id': None}
		# Get the light.
		light = self._lm.getLight(req['id'])
		if light == None:
			return {'success': False,
					'message': 'Light does not exist.',
					'id': req['id']}
					
		# Check to see if the user can access the light.
		if not self._lm.isAllowed(req['uuid'], req['id']):
			return {'success': False,
					'message': 'User not allowed to access light.',
					'id': req['id']}
		
		# Try to parlay an address from the client alias. If we can't,
		# that's another problem.
		address = self._am.getAddress(light['client'])
		if address == None:
			return {'success': False,
					'message': 'Client alias not recognized.',
					'id': req['id'],
					'client': light['client']}
		
		# If we can, well, that's good.
		res = self._cm.sendStatusRequest(address, req['id'])
		
		# Now if we were unable to connect to the client we have to adapt.
		if res['type'] == 'error':
			return {'success': False,
					'message': 'Could not connect to client.',
					'id': req['id'],
					'client': light['client']}
		else:
			print('merging dicts')
			resp = {'success': res['type'] == 'status',
					'message': res['message'],
					'client': light['client']}
			resp.update(res['data'])
			return resp
				
	def lightUpdate(self, req):
		"""
		Handles a request to update the state of one or more lights.
		
		Parameters:
			req (JSON): The Dictionary that contains the request.
			
		Returns:
			A dictionary containing the response to the request.
			
		Preconditions:
			The request be a valid JSON object for this request type.
			
		Postconditions:
			The state of the lights supplied is updated, if they exist.
		"""
		# Create a list to store the updated state of the lights, or errors.
		updated = []
		# For each requested light
		for light in req['lights']:
		
			# Get the light from the manager.
			l = self._lm.getLight(light['id'])
			if l == None:
				light['success'] = False
				light['message'] = 'Light does not exist.'
				updated.append(light)
				continue
				
			# Make sure the user can access the light.
			if not self._lm.isAllowed(req['uuid'], light['id']):
				light['success'] = False
				light['message'] = 'User not allowed to access light.'
				updated.append(light)
				continue

			# We need to translate the client name/alias to an IP.
			address = self._am.getAddress(light['client'])
			if address == None:
				light['success'] = False
				light['message'] = 'Alias not recognized.'
				updated.append(light)
				continue

			# Next validate the light.
			validation = self._cm.validateLight(light)
			# If there was a validation error we just append the light request
			# and the error message and failure.
			if validation != None:
				light['success'] = False
				light['message'] = validation
				updated.append(light)
				continue
				
			# Send the request and store the response.
			response = self._cm.sendChangeRequest(address, light)
			# Response documentation is in lumajson.py on the client.
			response['success'] = ( response['type'] == 'success' )
			response['message'] = response['message']
			# If a light was returned we append it, otherwise we return
			# the original light.
			updated.append(response['data'] if	\
					response['data']!=None else light)
	
				
		return {'lights':updated}
				
	def addUUID(self, req):
		"""
		Does what's asked of in the request: Adds a UUID to the given lights.
		
		Parameters:
			req (JSON): The Dictionary that contains the request.
			
		Returns:
			A dictionary containing the response to the request.
			
		Preconditions:
			The request be a valid JSON object for this request type.
			
		Postconditions:
			The given UUID is added to the given lights if they exist.
		"""
		return self._lm.addUUIDtoSubset(req['uuid'], req['lights'])
		
	def removeUUID(self, req):
		"""
		Removes a UUID from one or more lights.
		
		Parameters:
			req (JSON): The Dictionary that contains the request.
			
		Returns:
			A dictionary containing the response to the request.
			
		Preconditions:
			The request be a valid JSON object for this request type.
			
		Postconditions:
			The given UUID is removed from the given lights, if they exist.
		"""
		return self._lm.removeUUIDfromSubset(req['uuid'], req['lights'])
		
	def addLight(self, req):
		"""
		Adds a new light to the light manager.
		
		Parameters:
			req (JSON): The Dictionary that contains the request.
			
		Returns:
			A dictionary containing the response to the request.
			
		Preconditions:
			The request be a valid JSON object for this request type.
			
		Postconditions:
			The light specified is added if it doesn't exist.
		"""
		if self._lm.addLight(req['name'], req['client'], req['permitted']):
			self._am.addAlias(req['client'], req['address'])
			return {'success':True, 'message':None}
		return {'success':False, 'message':'Light name already taken.'}
		
	def removeLight(self, req):
		"""
		Removes a light from the light manager.
		
		Parameters:
			req (JSON): The Dictionary that contains the request.
			
		Returns:
			A dictionary containing the response to the request.
			
		Preconditions:
			The request be a valid JSON object for this request type.
			
		Postconditions:
			The light specified is removed if it existed.
		"""
		if not self._lm.isAllowed(req['uuid'], req['id']):
			return {'success':False,	\
					'message': 'User not allowed to access light.'}
		if self._lm.deleteLight(req['id']):
			return {'success':True,'message':None}
		return {'success':False,'message':'Light does not exist.'}
	
	def backup(self, req):
		"""
		Backs up aliases and lights.
		
		Parameters:
			req (JSON): The Dictionary that contains the request.
			
		Returns:
			A dictionary containing the response to the request.
			
		Preconditions:
			The request be a valid JSON object for this request type.
			
		Postconditions:
			The light specified is removed if it existed.
		"""
		timest_amp = str(datetime.now())
		self._lm.save("REMOTE LIGHT BACKUP "+timest_amp+".json")
		self._am.save("REMOTE ALIAS BACKUP "+timest_amp+".json")
		return {'success':True, 'message':None}
		