#module: requesthandler.py
# LUMA copyright (C) Gerard Geer 2014-2015

from datetime import datetime
from lightmanager import LightManager
from aliasmanager import AliasManager
from clientmanager import ClientManager
from json import loads

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
			print('Not a dictionary.')
			return False
			
		# Make sure all required keys are present.
		for key in ['uuid', 'query']:
			if key not in req.keys():
				print(key + ' not in req.keys()')
				return False
		
		# Verify the types of the keys' values.
		if  not isinstance(req['uuid'], str) and	\
			not isinstance(req['uuid'], unicode):
			print('uuid not string. Type: '+str(type(req['uuid'])))
			return False
		if  not isinstance(req['query'], str) and	\
			not isinstance(req['query'], unicode):
			print('query not string. Type: '+str(type(req['query'])))
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
			
		Postconditions:
			None.
		"""
		# Make sure the request is a Dictionary.
		if not isinstance(req, dict):
			print('Not a dictionary.')
			return False
			
		# Make sure all required keys are present.
		for key in ['uuid', 'id']:
			if key not in req.keys():
				print(key + ' not in req.keys()')
				return False
		
		# Verify the types of the keys' values.
		if  not isinstance(req['uuid'], str) and	\
			not isinstance(req['uuid'], unicode):
			print('uuid not string. Type: '+str(type(req['uuid'])))
			return False
		if  not isinstance(req['id'], str) and	\
			not isinstance(req['id'], unicode):
			print('id not string. Type: '+str(type(req['id'])))
			return False
			
		# Finally after all that checks out we can return True.
		return True
		
	def _sanitizeStateUpdate(self, req):
		"""
		Sanitizes a state update request. This makes sure that the form of the
		object passed as the request is valid for the request. Again, this does
		key and type testing.
		
		Parameters:
			req (JSON): The Dictionary that contains the request.
			
		Returns:
			True if the light query was valid, false otherwise.
			
		Preconditions:
			None.
			
		Postconditions:
			None.
		"""
		if not isinstance(req, dict):
			return False
			
		for key in ['uuid', 'lights']:
			if key not in req.keys():
				return False
		
		if  not isinstance(req['uuid'],str) and	\
			not isinstance(req['uuid'],unicode):
			return False
		
		if not isinstance(req['lights'], list):
			return False
			
		return True
		
	def lightQuery(self, req):
		"""
		Handles a query for light instances.
		
		Parameters:
			req (JSON String): The JSON String that describes the request.
			
		Returns:
			A dictionary containing the response to the request.
			
		Preconditions:
			The request be a valid JSON object for this request type.
			
		Postconditions:
			None.
		"""
		# Try to decode the JSON.
		try:
			if isinstance(req, unicode) or isinstance(req, str):
				req = loads(req)
		except:
			print(' Could not decode JSON of request.')
			return {'lights':[]}
			
		# If the request was invalid, we need to transparently return
		# nothing.
		if not self._sanitizeLightQuery(req):
			print(' Request did not pass sanitation.')
			return {'lights':[]}
			
		# Print the query.
		printedQuery = req['query']
		if len(printedQuery) > 71: 
			printedQuery = printedQuery[:68]+'...'
		print(' Query: '+printedQuery)
		
		# Create a place to store the query results.
		requested = []
		
		# Get the subset of all allowed lights.
		allowed = self._lm.getAllowedSubset(req['uuid'])
		# Gets possible aliases should the query be an IP address.
		possible = self._am.getPossibleAliases(req['query'])
		
		# If the user just sends us nothing, we just send all that's possible.
		if len(req['query']) == 0:
			requested.extend(allowed)
		
		else:
			for light in allowed:
				if 	req['query'].lower() in light['name'].lower() or	\
					req['query'].lower() in	light['id'].lower() or 		\
					req['query'].lower() in light['client'].lower():
					
					requested.append({'id':light['id'],		\
									'name':light['name'],	\
									'client':light['client']})
				else:
				
					for alias in possible:
						if alias in light['client']:
							
							requested.append({'id':light['id'],		\
											'name':light['name'],	\
											'client':light['client']})
		
		print(' Query returned '+str(len(requested))+' lights.')
		return {'lights':requested}
		
	def stateQuery(self, req):
		"""
		Handles a request for a light's state.
		
		Parameters:
			req (JSON String): The JSON String that describes the request.
			
		Returns:
			A dictionary containing the response to the request.
			
		Preconditions:
			The request be a valid JSON object for this request type.
			
		Postconditions:
			The state of the lights supplied is updated, if they exist.
		"""	
		# Try to decode the JSON.
		try:
			if isinstance(req, unicode) or isinstance(req, str):
				req = loads(req)
		except:
			print(' Could not decode JSON of request.')
			return {'success': False,
					'message': 'Invalid query.',
					'id': None}
			
		# Sanitize the request.
		if not self._sanitizeStateQuery(req):
			print(' Request did not pass sanitation.')
			return {'success': False,
					'message': 'Invalid query.',
					'id': None}
					
		# Get the light.
		light = self._lm.getLight(req['id'])
		if light == None:
			print(' Light does not exist.')
			return {'success': False,
					'message': 'Light does not exist.',
					'id': req['id']}
					
		# Check to see if the user can access the light.
		if not self._lm.isAllowed(req['uuid'], req['id']):
			print(' User tried to access forbidden light.')
			return {'success': False,
					'message': 'User not allowed to access light.',
					'id': req['id']}
		
		# Try to parlay an address from the client alias. If we can't,
		# that's another problem.
		address = self._am.getAddress(light['client'])
		if address == None:
			print(' Unrecognized client name/alias.')
			return {'success': False,
					'message': 'Client alias not recognized.',
					'id': req['id'],
					'client': light['client']}
		
		# If we can, well, that's good.
		res = self._cm.sendStatusRequest(address, req['id'])
		
		# Now if we were unable to connect to the client we have to adapt.
		if res['type'] == 'error':
			print(' Could not connect to client. '+res['message'])
			return {'success': False,
					'message': 'Could not connect to client. Error: '+res['message'],
					'id': req['id'],
					'client': light['client']}
		else:
			print(' Light status request successful.')
			resp = {'success': res['type'] == 'status',
					'message': res['message'],
					'client': light['client']}
			# Append the keys from the client's response's data to our response 
			# being sent back to the interface.
			resp.update(res['data'])
			return resp
				
	def lightUpdate(self, req):
		"""
		Handles a request to update the state of one or more lights.
		
		Parameters:
			req (JSON): A JSON String that should describe the request.
			
		Returns:
			A dictionary containing the response to the request.
			
		Preconditions:
			The request be a valid JSON object for this request type.
			
		Postconditions:
			The state of the lights supplied is updated, if they exist.
		"""
		# Since the light update request is already JSON, we don't
		# need to worry about parsing it.
		
		if not self._sanitizeStateUpdate(req):
			return {'lights':None,
					'success': False,
					'message': 'Request poorly formed.'}
					
		# Create a list to store our updated states in.
		updated = []
		
		# Go through each submitted state and try to abide.
		for submitted in req['lights']:
			# Validate the light.
			validationError = self._cm.validateLight(submitted)
			# If it fails validation, we have to reject it and move on.
			if validationError:
				submitted['success'] = False
				submitted['message'] = validationError
				updated.append(submitted)
				continue
			# At this point we have a valid light. Now we have to
			# get our own copy of it.
			serverVersion = self._lm.getLight(submitted['id'])
			# If we don't have a record of the light well poop.
			if not serverVersion:
				submitted['success'] = False
				submitted['message'] = 'Light not in server records.'
				updated.append(submitted)
				continue
			# If the client doesn't match, we have a problem.
			if serverVersion['client'] != submitted['client']:
				submitted['success'] = False
				submitted['message'] = 'Client does not match server records.'
				updated.append(submitted)
				continue
			# Finally we can start making headway. Let's get the address of
			# where this update goes.
			addr = self._am.getAddress(submitted['client'])
			# If we can't figure that out, well...
			if not addr:
				submitted['success'] = False
				submitted['message'] = 'Could not resolve client IP.'
				updated.append(submitted)
				continue
			# Now that we have a valid light and a valid address, let's
			# send the update.
			clientRes = self._cm.sendChangeRequest(addr, submitted)
			# If that action errors out, we have to pass it up the ladder too.
			if clientRes['type'] == 'error':
				submitted['success'] = False
				submitted['message'] = clientRes['message']
				updated.append(submitted)
				continue
			# At this point we should have finally had a successful update.
			submitted['success'] = True
			submitted['message'] = clientRes['message']
			updated.append(submitted)
	
		return {'lights': updated,
				'success': True,
				'message': None}
				
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
		
	def printInfo(self):
		"""
		Prints info about the Request Handler and its managers.
		
		Parameters:
			None.
		
		Returns:
			None.
		
		Preconditions:
			The Request Handler is initialized.
			
		Postconditions:
			Info is printed.
		"""
		# Get listings of the clients and lights on the server.
		clients = self._am.getPossibleAliases('')
		lights = self._lm.getLightCatalog()
		
		# Print those listings.
		print('\n Clients: ('+str(len(clients))+')')
		for client in self._am.getPossibleAliases(''):
			print('   '+client)
		print('\n Lights: ('+str(len(lights.keys()))+')')
		for key in lights.keys():
			print("   %-20s : "%str(key)+str(lights[key]))
		