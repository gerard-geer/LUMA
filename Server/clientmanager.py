#module clientmanager.py
# LUMA copyright (C) Gerard Geer 2014-2015

from singleton import Singleton
from socket import socket, AF_INET, SOCK_STREAM, error, herror, gaierror, timeout
from json import dumps, loads

_CONN_ERR = {'type': 'error',	\
			'message': None,	\
			'data': None}
_DATAREAD = 65536
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
		
		
	def sendStatusRequest(self, address, id):
		"""
		Sends a status request to the client at the given address and returns
		its response.
		
		Parameters:
			address (String): The address of the client.
			id (String): The ID of the lighting fixture whose status is
				desired. Passing None returns the status of all lights.
				
		Returns:	
			The response to the request as a JSON object.
			
		Preconditions:
			The socket is initialized and not overworked.
			
		Postconditions:
			A message is sent to the address specified on port 8641, and its
			response is returned.
		"""
		req = {'type':'status', 'data':id}
		try:
			# Encode the request before opening the socket for timeliness.
			try:
				m = dumps(req, separators=(',',':'))
			except ValueError as e:
				_CONN_ERR['message'] = 'Error encoding JSON when sending status to '+str(address)+	\
				'. ('+str(e)+')'
				return _CONN_ERR
				
			print('Client-bound status request length: '+str(len(m)))
			
			# Perform socket IO.
			s = socket(AF_INET, SOCK_STREAM)
			s.settimeout(_TIMEOUT)
			s.connect((address, self._PORT))
			s.sendall(m)
			res = s.recv(_DATAREAD)
			s.close()
			# Return the client's response.
			print('Interface-bound status response length: '+str(len(res)))
			try:
				return loads(res)
			except ValueError as e:
				_CONN_ERR['message'] = 'Error decoding JSON when receiving status from '+str(address)+	\
				'. ('+str(e)+')\n'+str(res)
				return _CONN_ERR
			
		except ValueError as e:
			_CONN_ERR['message'] = 'Error parsing JSON when sending status to '+str(address)+	\
			'. ('+str(e)+')'
			return _CONN_ERR
		# Socket.error
		except error as e:
			_CONN_ERR['message'] = 'Could not connect to address '+str(address)+	\
			'. ('+str(e)+')'
			return _CONN_ERR
		# Socket.herror
		except herror as e:
			_CONN_ERR['message'] = 'H Error: Could not connect to address '+str(address)+	\
			'. ('+str(e)+')'
			return _CONN_ERR
		# Socket.gaierror
		except gaierror as e:
			_CONN_ERR['message'] = 'GAI Error: Could not connect to address '+str(address)+	\
			'. ('+str(e)+')'
			return _CONN_ERR
		# Socket.timeout
		except timeout as e:
			_CONN_ERR['message'] = 'Timeout: Could not connect to address '+str(address)+	\
			'. ('+str(e)+')'
			return _CONN_ERR
			
	def sendChangeRequest(self, address, dict):
		"""
		Sends a change request to the client at the given address and returns
		its response.
		
		Parameters:
			address(String): The address to send the request to.
			dict(Dictionary): A dictionary containing the to-be lighting state,
				formatted as follows:
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
		
		Returns:
			The response to this request as a JSON object.
			
		Preconditions:
			The socket is initialized and not overworked.
			
		Postconditions:
			A message is sent to the client at the address:port, and its
			response is decoded and returned.
		"""
		req = {'type':'change', 'data':dict}
		try:
			# Form the message ahead of time.
			try:
				m = dumps(req, separators=(',',':'))
			except ValueError as e:
				_CONN_ERR['message'] = 'Error encoding JSON when sending change to '+str(address)+	\
				'. ('+str(e)+')'
				return _CONN_ERR
				
			print('Client-bound change request length: '+str(len(m)))
			
			# Perform socket IO.
			s = socket(AF_INET, SOCK_STREAM)
			s.settimeout(_TIMEOUT)
			s.connect((address, self._PORT))
			s.sendall(m)
			res = s.recv(_DATAREAD)
			s.close()
			
			# Return the client's response.
			print('Interface-bound change response length: '+str(len(res)))
			try:
				return loads(res)
			except ValueError as e:
				_CONN_ERR['message'] = 'Error decoding JSON when receiving change from '+str(address)+	\
				'. ('+str(e)+')'
				return _CONN_ERR
			
		except ValueError as e:
			_CONN_ERR['message'] = 'Error parsing JSON when sending change to '+str(address)+	\
			'. ('+str(e)+')'
			return _CONN_ERR
		# Socket.error
		except error as e:
			_CONN_ERR['message'] = 'Could not connect to address '+str(address)+	\
			'. ('+str(e)+')'
			return _CONN_ERR
		# Socket.herror
		except herror as e:
			_CONN_ERR['message'] = 'H Error: Could not connect to address '+str(address)+	\
			'. ('+str(e)+')'
			return _CONN_ERR
		# Socket.gaierror
		except gaierror as e:
			_CONN_ERR['message'] = 'GAI Error: Could not connect to address '+str(address)+	\
			'. ('+str(e)+')'
			return _CONN_ERR
		# Socket.timeout
		except timeout as e:
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