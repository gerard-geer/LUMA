#module: requesthandler.py
# LUMA copyright (C) Gerard Geer 2014-2015

from datetime import datetime
from lightmanager import LightManager
from aliasmanager import AliasManager
from clientmanager import ClientManager
from json import loads
from uuid import uuid4

from singleton import Singleton
from sanitizer import *

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
		if not sanitizeLightQuery(req):
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
		if not sanitizeStateQuery(req):
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
				
	def lightChange(self, req):
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
		
		if not sanitizeChangeQuery(req):
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
	
	def lightAddQuery(self, req):
		"""
		Handles a query for adding a Light.
		
		Parameters:
			req (JSON String): The JSON String that describes the request.
			
		Returns:
			A dictionary containing the response to the request.
			
		Preconditions:
			The request be a valid JSON object for this request type.
			
		Postconditions:
			A new light is added.
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
		if not sanitizeLightAddQuery(req):
			print(' Request did not pass sanitation.')
			return {'success':False, 'message':'Request did not pass sanitation. '}
			
		# Print some info.
		print(' Name: '+str(req['name']))
		print(' Client: '+str(req['client']))
		print(' Exists: '+str(req['exists']))
		if req['exists']:
			print(' ID: '+str(req['id']))
		print(' # Permitted: '+str(len(req['permitted'])))
		print(' Pins: r={0} g={1} b={2}'.format(req['r_c'],req['g_c'],req['b_c']))
		
		# Just to make sure we're not adding a light to a rogue client, we
		# make sure we know where it's going.
		addr = self._am.getAddress(req['client'])
		if addr != req['address']:
			print(" Request address '"+str(req['address'])+	\
					"' did not match server record")
			return {'success':False, 'message':"Request address '"+	\
						str(req['address'])+"' did not match server record. "}
		
		if not req['exists']:
			# Finally we create the new light ID.
			freshID = str(uuid4())
			
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
				print(' Client error: '+res['message'])
				return {'success': False, 'message': res['message']}
			
				
			# Finally since the response was good we add the light to the server.
			print(' Adding new light to server.')
			if not self._lm.addLight(freshID, req['name'], req['client'], req['permitted']):
				print(' Could not add light to server.')
				return {'success':False, 'message':' Could not add light to server.'}
		
		# If the light supposedly already exists, we should check to make sure.
		else:
			print(' Checking if light actually exists.')
			res = self._cm.sendRequest(addr, 'status', req['id'])
			if res['type'] != 'status':
				print(" The '"+str(req['name'])+"' Light doesn't actually exist"+	\
				" on the '"+str(req['client'])+"' client, or the given ID was wrong.")
				return {'success':False, 
				'message':" The '"+str(req['name'])+"' Light doesn't actually exist"+	\
				" on the '"+str(req['client'])+"' client, or the given ID was wrong."}
			else:
				print(' Adding existing light to server.')
				self._lm.addLight(req['id'], req['name'], req['client'], req['permitted'])
		
		print(' done.')
		return {'success':True, 'message':None}
		
	def clientAddQuery(self, req):
		"""
		Handles a query for adding a Client.
		
		Parameters:
			req (JSON String): The JSON String that describes the request.
			
		Returns:
			A dictionary containing the response to the request.
			
		Preconditions:
			The request be a valid JSON object for this request type.
			
		Postconditions:
			A new light is added.
		"""
		# Create our response object.
		resp = {'success':False,
				'message':None}
				
		# Try to decode the JSON.
		try:
			if isinstance(req, unicode) or isinstance(req, str):
				req = loads(req)
		except:
			print(' Could not decode JSON of request.')
			resp['message'] = 'Could not decode JSON of request.'
			return resp
			
		# If the request was invalid, we need to transparently return
		# nothing.
		if not sanitizeClientAddQuery(req):
			print(' Request did not pass sanitation.')
			resp['message']= 'Request did not pass sanitation. '
			return resp
			
		# Oh this is nice and simple. The addAlias function's success and
		# failure scenarios directly reflect the success and failure causes
		# of the request. Therefore there's nothing to do besides sanitation.
		resp['success'] = self._am.addAlias(req['name'],req['address'])
		
		# Create a message if need be.
		if not resp['success']:
			print('Could not create a new client. Either name or '+	\
				  'address already in use.')
			resp['message'] = 'Could not create a new client. Either name or '+	\
							  'address already in use.'
							  
		return resp
		
	def lightInfoUpdate(self, req):
		"""
		Handles requests for changing the information of a light.
		
		Parameters:
			req (JSON String): The JSON String that describes the request.
			
		Returns:
			A dictionary containing the response to the request.
			
		Preconditions:
			The request be a valid JSON object for this request type.
			
		Postconditions:
			The information for a light is updated.		
		"""
		# Since this response is so large, we create it beforehand.
		resp = {
				'id': None,
				'success': False,
				'message': None,
				'name':	{
					'success': False,
					'message': None
					},
				'client':	{
					'success': False,
					'message': None
					},
				'permitted':	{
					'success': False,
					'message': None
					}
			}

		# Try to decode the JSON if hasn't been already.
		try:
			if isinstance(req, unicode) or isinstance(req, str):
				req = loads(req)
		except:
			print(' Could not decode JSON of request.')
			resp['message'] = 'Could not decode request JSON.'
			return resp
			
		# Sanitize the request.
		if not sanitizeLightInfoUpdate(req):
			print(' Request did not pass sanitation.')
			resp['message'] = 'Request did not pass sanitation.'
			return resp
					
		# Get the server's copy of the light.
		light = self._lm.getLight(req['id'])
		if light == None:
			print(' Light does not exist on server.')
			resp['message'] = "Light doesn't exist or invalid ID."
			return resp
		print(' For: '+str(light['id'])+' ('+str(light['name'])+')')
					
		# Check first to see if the request changes the light's client...
		if req['client'] != None:
			# And if it does make sure it's setting the client to a 
			# valid one.
			addr = self._am.getAddress(req['client'])
			if not addr:
				print(' new client not recognized.')
				resp['message'] = 'New client not recognized.'
				return resp
		
		# Now that we have both the request and the existing light we need to
		# see if we need to swap clients.
		if req['client'] != None and req['client'] != light['client']:
			"""
			TODO: Delete light from original client.
			"""
			# We have to report, ya know...
			print("   Updating client from from '"+light['client']+"' to '"+req['client']+"'...")
			resp['name']['success'] = self._lm.changeLightClient(req['id'], req['client'])
			if resp['client']['success']:
				print("  Name updated'.")
				resp['client']['message'] = None
			else:
				print('  ID not recognized when updating client.')
				resp['client']['message'] = 'ID not recognized.'
		print('  Client need not be updated.')
			
		# Now that the hairy bit is over, we change the names and the permitted
		# list.
		# OH AND THE NOT NOT. Since cmp returns numerical values, if the lists aren't
		# equal it will return a non-zero number. When they are the same it returns
		# zero. "not 0" coerces to a boolean value and returns true. However, a boolean
		# value "and"ed with a non-zero number does not return True, but rather the
		# non-zero value. Therefore we have to use the not not to make the if work.
		if req['permitted'] != None and not not cmp(req['permitted'], light['permitted']):
			print("   Updating permissions list...")
			resp['permitted']['success'] = self._lm.setUUIDs(req['id'], req['permitted'])
			if resp['permitted']['success']:
				print('   Permitted list updated.')
				resp['permitted']['message'] = None
			else:
				print('   ID not recognized when updating permissions.')
				resp['permitted']['message'] = 'ID not recognized.'
		print('  Permitted whitelist need not be updated.')
		
		# Changing the name.
		if req['name'] != None and req['name'] != light['name']:
			print("   Updating name from from '"+light['name']+"' to '"+req['name']+"'...")
			resp['name']['success'] = self._lm.changeLightName(req['id'], req['name'])
			if resp['name']['success']:
				print("  Name updated'.")
				resp['name']['message'] = None
			else:
				print('  ID not recognized when updating name.')
				resp['name']['message'] = 'ID not recognized.'
		print('  Name need not be updated.')
		
		# Finally if all things have worked out, then we set the whole success
		# to true and return the response.
		resp['success'] = True
		return resp
	
	def clientInfoUpdate(self, req):
		"""
		Handles requests for changing the information of a client.
		
		Parameters:
			req (JSON String): The JSON String that describes the request.
			
		Returns:
			A dictionary containing the response to the request.
			
		Preconditions:
			The request be a valid JSON object for this request type.
			
		Postconditions:
			The information for a light is updated.		
		"""
		# Create the response for simplicity.
		resp = {'success':False, 'message':None}
		
		# Try to decode the JSON if hasn't been already.
		try:
			if isinstance(req, unicode) or isinstance(req, str):
				req = loads(req)
		except:
			print(' Could not decode JSON of request.')
			resp['message'] = 'Could not decode request JSON.'
			return resp
			
		# Sanitize the request.
		if not sanitizeClientInfoUpdate(req):
			print(' Request did not pass sanitation.')
			resp['message'] = 'Request did not pass sanitation.'
			return resp
			
		# This one is simple. If the client exists this function will
		# return True, and perform all the operations of the success
		# scenario of updating the address of the client.
		resp['success'] = self._am.updateAlias(req['name'],req['address'])
		if not resp['success']:
			print(" Client name '"+req['name']+"' not recognized.")
			resp['message'] = "Client name '"+req['name']+"' not recognized."
		
		# Finally we return the response.
		return resp
		
	def lightCatalogRequest(self):
		"""
		Returns a catalog of all the lights in the server. 
		
		Parameters:
			None.
			
		Returns:
			A catalog of all the lights in the server.
			
		Preconditions:
			The light manager is properly loaded.
			
		Postconditions:
			None.
		"""
		return self._lm.getLightCatalog()
		
	def clientCatalogRequest(self):
		"""
		Returns a catalog of all the clients on the server.
		
		Parameters:
			None.
			
		Returns:
			A catalog of all the clients on the server.
			
		Preconditions:
			The client manager is properly loaded.
			
		Postconditions:
			None.
		"""
		return self._am.getClientCatalog()
		
	def detailedInfoQuery(self, req):
		"""
		Handles a request for detailed information about a client.
		
		Parameters:
			req (JSON String): The JSON String that describes the request.
			
		Returns:
			A dictionary containing the response to the request.
			
		Preconditions:
			The request be a valid JSON object for this request type.
			
		Postconditions:
			The state of the lights supplied is updated, if they exist.
		"""	
		
		# Create a base response object.
		resp = {
			"success": False,
			"message": None,
			"client": None,
			"lights":[]
			}
			
		# Try to decode the JSON.
		try:
			if isinstance(req, unicode) or isinstance(req, str):
				req = loads(req)
		except:
			print(' Could not decode JSON of request.')
			resp['message'] = 'Invalid query.'
			return resp
			
		# Sanitize the request.
		if not sanitizeClientInfoQuery(req):
			print(' Request did not pass sanitation.')
			resp['message'] = 'Invalid query.'
			return resp
					
		# Get the client address given its name.
		address = self._am.getAddress(req['client'])
		if address == None:
			print(' Unrecognized client name/alias.')
			resp['message'] = 'Client alias not recognized.'
			return resp
		
		# If we can, well, that's good.
		print(' To: '+address+' ('+req['client']+')')
		cresp = self._cm.sendRequest(address, 'info', None)
		
		# Now if we were unable to connect to the client we have to adapt.
		if cresp['type'] == 'error':
			print('  Could not connect to client. '+str(cresp['message']))
			resp['message'] = 'Could not connect to client. '+str(cresp['message'])
			return resp
			
		# At this point things have gone pretty smoothly.
		else:
			resp['success'] = True
			resp['client'] = req['client']
			resp['lights'] = cresp['data']
			return resp
			
	def deleteLightRequest(self, req):
		"""
		Handles a request to delete a light. This is for admin action only.
		
		Parameters:
			req (JSON String): The JSON String that describes the request.
			
		Returns:
			A dictionary containing the response to the request.
			
		Preconditions:
			The request be a valid JSON object for this request type.
			
		Postconditions:
			The state of the lights supplied is updated, if they exist.
		"""	
		
		# Create a base response object.
		resp = {
			"success": False,
			"message": None
			}
			
		# Try to decode the JSON.
		try:
			if isinstance(req, unicode) or isinstance(req, str):
				req = loads(req)
		except:
			print(' Could not decode JSON of request.')
			resp['message'] = 'Invalid query.'
			return resp
			
		# Sanitize the request.
		if not sanitizeDeleteLightRequest(req):
			print(' Request did not pass sanitation.')
			resp['message'] = 'Invalid query.'
			return resp
					
		# First we need to get the light, and for that it needs to exist.
		light = self._lm.getLight(req['id'])
		if light == None:
			print(' Light does not exist on the server.')
			resp['message'] = 'Light does not exist on the server.'
			return resp
		
		# Now we need to get the client that the light resides on.
		addr = self._am.getAddress(light['client'])
		if alias == None:
			print(' Cannot resolve client address. Perhaps client has been deleted?')
			resp['message'] = 'Cannot resolve client address. Perhaps client has been deleted?'
			return resp
		
		# If we can, well, that's good.
		print(' To: '+address+' ('+req['client']+')')
		cresp = self._cm.sendRequest(address, 'delete', req['id'])
		
		# Now if we were unable to connect to the client we have to adapt.
		if cresp['type'] == 'error':
			print('  Could not resolve communication with client. '+str(cresp['message']))
			resp['message'] = 'Could not resolve communication with client. '+str(cresp['message'])
			return resp
			
		# At this point things have gone pretty smoothly.
		else:
			resp['success'] = True
			return resp
				
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
			print("   %-20s : "%str(key)+str(lights[key][0]))
		