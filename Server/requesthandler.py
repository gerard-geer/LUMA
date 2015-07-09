#module: requesthandler.py
# LUMA copyright (C) Gerard Geer 2014-2015

from datetime import datetime
from lightmanager import LightManager
from aliasmanager import AliasManager
from clientmanager import ClientManager
from json import loads
from uuid import uuid4

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
		
	def load(self):
		"""
		Loads the alias and light manager configurations from file.
		
		Parameters:
			None.
			
		Returns:
			(bool, bool) Where the first term is the success in loading
			the Alias Manager and the second the Light Manager.
			
		Preconditions:
			None.
			
		Postconditions:
			The Light and Alias Managers configurations are attempted to
			be loaded.
		"""
		return (self._am.load(), self._lm.load())
	
		
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
		
	def _sanitizeAddQuery(self, req):
		"""
		Sanitizes a light adding query. This makes sure that the query is a
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
		for key in ['name', 'client', 'address', 'permitted',
					'exists', 'id', 'r_c', 'g_c', 'b_c']:
			if key not in req.keys():
				print(key + ' not in req.keys()')
				return False
		
		# Verify the types of the keys' values.
		if  not isinstance(req['name'], str) and	\
			not isinstance(req['name'], unicode):
			print('name is not string. Type: '+str(type(req['name'])))
			return False
		if  not isinstance(req['client'], str) and	\
			not isinstance(req['client'], unicode):
			print('client is not string. Type: '+str(type(req['client'])))
			return False
		if  not isinstance(req['address'], str) and	\
			not isinstance(req['address'], unicode):
			print('address is not string. Type: '+str(type(req['address'])))
			return False
		if  not isinstance(req['permitted'], list):
			print('permitted is not a list. Type: '+str(stype(req['permitted'])))
			return False
		if  not isinstance(req['exists'], bool):
			print('exists is not a boolean. Type: '+str(stype(req['exists'])))
			return False
		if  req['exists'] and	\
			not isinstance(req['id'], str) and	\
			not isinstance(req['id'], unicode):
			print('id is not a string. Type: '+str(stype(req['string'])))
			return False
		if  not isinstance(req['r_c'], int):
			print('r_c is not an integer. Type: '+str(type(req['r_c'])))
			return False
		if  not isinstance(req['g_c'], int):
			print('g_c is not an integer. Type: '+str(type(req['g_c'])))
			return False
		if  not isinstance(req['b_c'], int):
			print('b_c is not an integer. Type: '+str(type(req['b_c'])))
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
		print(' By UUID: '+req['uuid'])
		if light == None:
			print(' Light does not exist on server.')
			return {'success': False,
					'message': 'Light does not exist on server.',
					'id': req['id']}
		print(' For: '+str(light['id'])+' ('+str(light['name'])+')')
					
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
		print(' To: '+address+' ('+light['client']+')')
		res = self._cm.sendRequest(address, 'status', req['id'])
		
		# Now if we were unable to connect to the client we have to adapt.
		if res['type'] == 'error':
			print(' Could not connect to client. '+res['message'])
			return {'success': False,
					'message': 'Could not connect to client. Error: '+res['message'],
					'id': req['id'],
					'client': light['client']}
		else:
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
			print(' Could not decode JSON request.')
			return {'lights':None,
					'success': False,
					'message': 'Request poorly formed.'}
					
		print(' By UUID: '+req['uuid'])
		
		# Create a list to store our updated states in.
		updated = []
		# Go through each submitted state and try to abide.
		for submitted in req['lights']:
			print(' Updating light: '+submitted['id']+' ('+submitted['name']+'):')
			# Validate the light.
			validationError = self._cm.validateLight(submitted)
			# If it fails validation, we have to reject it and move on.
			if validationError:
				print('   Light failed validation: '+validationError)
				submitted['success'] = False
				submitted['message'] = validationError
				updated.append(submitted)
				continue
			# At this point we have a valid light. Now we have to
			# get our own copy of it.
			serverVersion = self._lm.getLight(submitted['id'])
			# If we don't have a record of the light well poop.
			if not serverVersion:
				print('   Light not in server records.')
				submitted['success'] = False
				submitted['message'] = 'Light not in server records.'
				updated.append(submitted)
				continue
			# If the client doesn't match, we have a problem.
			if serverVersion['client'] != submitted['client']:
				print('   Client does not match server records.')
				submitted['success'] = False
				submitted['message'] = 'Client does not match server records.'
				updated.append(submitted)
				continue
			# Finally we can start making headway. Let's get the address of
			# where this update goes.
			addr = self._am.getAddress(submitted['client'])
			# If we can't figure that out, well...
			if not addr:
				print('   Client not recognized.')
				submitted['success'] = False
				submitted['message'] = 'Client not recognized.'
				updated.append(submitted)
				continue
			# Now that we have a valid light and a valid address, let's
			# send the update.
			print('   To: '+str(addr)+' ('+str(submitted['client'])+')')
			clientRes = self._cm.sendRequest(addr, 'change', submitted)
			# If that action errors out, we have to pass it up the ladder too.
			if clientRes['type'] == 'error':
				print('   Error in client interaction: '+clientRes['message'])
				submitted['success'] = False
				submitted['message'] = clientRes['message']
				updated.append(submitted)
				continue
			# At this point we should have finally had a successful update.
			print('   Light successfully updated.')
			submitted['success'] = True
			submitted['message'] = clientRes['message']
			updated.append(submitted)
	
		print(' All requested lights handled.')
		return {'lights': updated,
				'success': True,
				'message': None}
	
	def addQuery(self, req):
		"""
		Handles a query for adding a Light.
		
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
			return {'success':False, 'message':'Could not decode JSON of request.'}
			
		# If the request was invalid, we need to transparently return
		# nothing.
		if not self._sanitizeAddQuery(req):
			print(' Request did not pass sanitation.')
			return {'success':False, 'message':'Request did not pass sanitation.'}
			
		# Print some info.
		print(' Name: '+str(req['name']))
		print(' Client: '+str(req['client']))
		print(' Exists: '+str(req['exists']))
		if req['exists']:
			print(' ID: '+str(req['id']))
		print(' # Permitted: '+str(len(req['permitted'])))
		print(' Pins: r={1} g={2} b={3}'.format(req['r_c'],req['g_c'],req['b_c']))
		
		# Just to make sure we're not adding a light to a rogue client, we
		# make sure we know where it's going.
		addr = self._am.getAddress(req['client'])
		if addr != req['address']:
			print(" Request address '"+str(req['address'])+	\
					"' did not match server record")
			return {'success':False, 'message':"Request address '"+	\
						str(req['address'])+"' did not match server record"}
		
		if not req['exists']:
			# Finally we create the new light ID.
			freshID = uuid4()
			
			# Need to create the request we're sending to the client.
			cReq = {
				'name': req['name'],
				'id': freshID,
				'r_c': req['r_c'],
				'g_c': req['g_c'],
				'b_c': req['b_c']
			}
			
			# Send the client our request.
			print(' Adding light to client.')
			res = self._cm.sendRequest(addr, 'add', cReq)
		
			# If the request errors out, then the light wasn't added to the client
			# and we shan't add it to the server either.
			if res['type'] == 'error':
				print(' '+res['message'])
				return {'success': False, 'message': res['message']}
			
				
			# Finally since the response was good we add the light to the server.
			print(' Adding new light to server.')
			self._lm.addLight(freshID, req['name'], req['client'], req['permitted'])
		
		else:
			# Finally since the response was good we add the light to the server.
			print(' Adding existing light to server.')
			self._lm.addLight(req['id'], req['name'], req['client'], req['permitted'])
		
		return {'success':True, 'message':None}
		

				
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
		