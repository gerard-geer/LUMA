#module sanitizer.py
# LUMA copyright (C) Gerard Geer 2014-2015

"""
Provides sanitization for all requests.
"""

def sanitizeLightQuery(req):
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
	
def sanitizeStateQuery(req):
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
	
def sanitizeAddQuery(req):
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
		print('permitted is not a list. Type: '+str(type(req['permitted'])))
		return False
	if  not isinstance(req['exists'], bool):
		print('exists is not a boolean. Type: '+str(type(req['exists'])))
		return False
	if  req['exists'] and	\
		not isinstance(req['id'], str) and	\
		not isinstance(req['id'], unicode):
		print('id is not a string. Type: '+str(type(req['string'])))
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
	
def sanitizeChangeQuery(req):
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
	
def sanitizeLightInfoUpdate(req):
	"""
	Sanitizes a request to change the info of a light.
	
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
		
	for key in ['id', 'name', 'client', 'permitted']:
		if key not in req.keys():
			return False
	
	if  not isinstance(req['id'],str) and	\
		not isinstance(req['id'],unicode):
		return False
	
	if  not isinstance(req['name'],str) and	\
		not isinstance(req['name'],unicode):
		return False
	
	if  not isinstance(req['client'],str) and	\
		not isinstance(req['client'],unicode):
		return False
	
	if  not isinstance(req['permitted'],list):
		return False
		
	for id in req['permitted']:
		if  not isinstance(id,str) and	\
			not isinstance(id,unicode):
			return False
			
	return True
	
def sanitizeClientInfoUpdate(req):
	"""
	Sanitizes a request to change the info of a client.
	
	Parameters:
		req (JSON): The Dictionary that contains the request.
		
	Returns:
		True if the info update was valid, false otherwise.
		
	Preconditions:
		None.
		
	Postconditions:
		None.
	"""
	if not isinstance(req, dict):
		return False
		
	for key in ['name', 'address']:
		if key not in req.keys():
			return False
			
	if  not isinstance(req['name'],str) and	\
		not isinstance(req['name'],unicode):
		return False
	
	if  not isinstance(req['address'],str) and	\
		not isinstance(req['address'],unicode):
		return False
			
	return True
	
def sanitizeClientAddQuery(req):
	"""
	Sanitizes a request to add a client.
	
	Parameters:
		req (JSON): The Dictionary that contains the request.
		
	Returns:
		True if the info update was valid, false otherwise.
		
	Preconditions:
		None.
		
	Postconditions:
		None.
	"""
	# Yeah yeah I know it's the same as the client info update.
	# But as these two requests are not guaranteed to have
	# the same contents, it's unsafe to sanitize both as one.
	if not isinstance(req, dict):
		return False
		
	for key in ['name', 'address']:
		if key not in req.keys():
			return False
			
	if  not isinstance(req['name'],str) and	\
		not isinstance(req['name'],unicode):
		return False
	
	if  not isinstance(req['address'],str) and	\
		not isinstance(req['address'],unicode):
		return False
			
	return True