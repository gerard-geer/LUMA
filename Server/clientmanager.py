#module clientmanager.py
# LUMA copyright (C) Gerard Geer 2014-2015

from singleton import Singleton
from socket import socket, AF_INET, SOCK_STREAM, error, herror, gaierror, timeout
from json import dumps, loads

_CONN_ERR = {'type': 'error',	\
			'message': None,	\
			'data': None}
_DATAREAD = 64
_TIMEOUT = 5.0

@Singleton
class ClientManager(object):
	"""
	A singleton manager that encapsulates all the functionality of talking
	to LUMA clients.
	
	Slots:
		_socket (socket): Private. The socket used for communication.
		_PORT (Integer): Private. The port aimed at on each client. 8641.
	"""
	__slots__ = ('_socket', '_PORT')
	def __init__(self):
		"""
		Initializes the Manager. Do not call this, rather call .Instance()
		so that Singleton functionality is preserved.
		
		Parameters:
			None.
			
		Returns:
			None.
			
		Preconditions:
			None.
			
		Postconditions:
			A socket instance is created.
		"""
		self._socket = socket(AF_INET, SOCK_STREAM)
		self._PORT = 8641
		
	def sendRequest(self, address, type, data):
		"""
		Sends a request to the client at the given address, with the given
		type and data, then returns	its response.
		
		Parameters:
			Status Requests are formatted as follows:
			{
				address (String): The address of the client.
				id (String): The ID of the lighting fixture whose status is
					desired. Passing None returns the status of all lights.
			}	
			
			Change Requests are formatted as follows:
			{
				'id': The ID of the light.
				'name': The name of the light.
				'r_t': List of red timings.
				'r_v': List of red values.
				'g_t': List of green timings.
				'g_v': List of green values.
				'b_t': List of blue timings.
				'b_v': List of blue values.
			}
			
			Add requests meant for the client are formatted like so:
			{
				"name": "<example light name>",
				"id": "<example light id>",
				"r_c": <red channel pin number>,
				"g_c": <green channel pin number>,
				"b_c": <blue channel pin number>
			}
				
		Returns:	
			The response to the request as a JSON object.
			
		Preconditions:
			The socket is initialized and not overworked.
			
		Postconditions:
			A message is sent to the address specified on port 8641, and its
			response is returned.
		"""
		req = {'type':type, 'data':data}
		try:
			# Encode the request before opening the socket for timeliness.
			try:
				m = dumps(req, separators=(',',':'))+'\n'
			except ValueError as e:
				print(' Error encoding JSON when sending '+type+' request to '+str(address))
				_CONN_ERR['message'] = 'Error encoding JSON when sending '+type+' to '+str(address)+	\
				'. ('+str(e)+')'
				return _CONN_ERR
				
			print(' Sending request. (Length: '+str(len(m))+')')
			# Perform socket IO.
			s = socket(AF_INET, SOCK_STREAM)
			s.settimeout(_TIMEOUT)
			s.connect((address, self._PORT))
			s.sendall(m)
			# Receive in the response.
			chunk = s.recv(_DATAREAD)
			res = chunk
			while chunk != '':
				chunk = s.recv(_DATAREAD)
				res += chunk
			s.close()
			# Return the client's response.
			print(' Response received. (length: '+str(len(res))+')')
			try:
				return loads(res)
			except ValueError as e:
				print('Error decoding JSON when receiving '+type+' from '+str(address)+	\
				'. ('+str(e)+')\n')
				_CONN_ERR['message'] = 'Error decoding JSON when receiving '+type+' from '+str(address)+	\
				'. ('+str(e)+')\n'+str(res)
				return _CONN_ERR
			
		# Socket.error
		except error as e:
			print(' Could not connect to address '+str(address))
			_CONN_ERR['message'] = 'Could not connect to address '+str(address)+	\
			'. ('+str(e)+')'
			return _CONN_ERR
		# Socket.herror
		except herror as e:
			print(' H Error: Could not connect to address '+str(address))
			_CONN_ERR['message'] = 'H Error: Could not connect to address '+str(address)+	\
			'. ('+str(e)+')'
			return _CONN_ERR
		# Socket.gaierror
		except gaierror as e:
			print(' GAI Error: Could not connect to address '+str(address))
			_CONN_ERR['message'] = 'GAI Error: Could not connect to address '+str(address)+	\
			'. ('+str(e)+')'
			return _CONN_ERR
		# Socket.timeout
		except timeout as e:
			print(' Timeout error: Could not connect to address '+str(address))
			_CONN_ERR['message'] = 'Timeout: Could not connect to address '+str(address)+	\
			'. ('+str(e)+')'
			return _CONN_ERR
			
	def validateLight(self, dict):
		"""
		Validates a light dictionary for sending to a client. 
		
		Parameters:
			dict (Dictionary): The dictionary that we suppose is a light.
			
		Returns:
			The first reason the light is invalid, as a String, or None if
			the light is valid.
			
		Preconditions:
			None.
			
		Postconditions:
			None.
		"""
		# Incorrect number of keys.
		if len(dict.keys()) != 9:
			return 'Incorrect number of keys.'
		# Check for necessary keys.
		for test in ['r_t','r_v','g_t','g_v','b_t','b_v','name','client','id']:
			if test not in dict.keys():
				return 'Light does not contain a '+test+' key.'
		# Test each list key.
		for test in ['r_t','r_v','g_t','g_v','b_t','b_v']:
			# Make sure each is a list.
			if not isinstance(dict[test], list):
				return test+' is not a list.'
			# Make sure each value is a number.
			for val in dict[test]:
				if not isinstance(val, (int, float)):
					return test+' does not contain only numbers.'
		# Others not a string?
		for test in ['name','client','id']:
			if  not isinstance(dict[test], str) and	\
				not isinstance(dict[test], unicode):
				return test+' is not a string.'
				
		return None