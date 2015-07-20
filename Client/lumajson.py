#module: lumajson 
# LUMA copyright (C) Gerard Geer 2014-2015

"""
Performs all our JSON encoding-decoding needs.
"""

from json import dumps, loads, JSONEncoder
from light import Light
from colorchannel import ColorChannel

def _encode_light(l, type='state'):
	"""
	Encodes a light object into a dictionary.
	
	Parameters:
		l (Light): The Light instance to encode.
		type (String): The type of encoding to perform.
		-state: Returns data encoded for a state request.
		-save: Returns a more complete light meant for saving to file.
		-info: Returns that of save, with also the current time.
		(Default = "state")
	
	Returns:
		A dictionary containing all the fields of the Light instance.
		
	Preconditions:
		None.
		
	Postconditions:
		None.
	"""
	d = {}
	if type == 'state':
		d['name'] = l.name
		d['id'] = l.id
		d['r_t'] = l.r.times.aslist()
		d['r_v'] = l.r.vals.aslist()
		d['g_t'] = l.g.times.aslist()
		d['g_v'] = l.g.vals.aslist()
		d['b_t'] = l.b.times.aslist()
		d['b_v'] = l.b.vals.aslist()
	if type == 'save':
		d['r_c'] = l.r.chan
		d['g_c'] = l.g.chan
		d['b_c'] = l.b.chan
	if type == 'info':
		d['time'] = l.r.chan.cur

	return d

class _LightEncoder(JSONEncoder):
	"""
	A custom JSONEncoder that specifies its own way of doing things.
	"""
	def default(self, obj):
		"""
		Overrides JSONEncoder.default() to call _encode_light() if the
		object being encoded is actually a Light instance.
		
		Parameters:
			obj (Any): The object to encode.
			
		Returns:
			The object transformed to be encoded.
			
		Preconditions:
			None.
		
		Postconditions:
			None.
		"""
		try:
			return _encode_light(obj)
		except:
			return JSONEncoder.default(self, obj)
			
class _LightSaveEncoder(JSONEncoder):
	"""
	A custom JSONEncoder that specifies its own way of doing things, this
	time for saving the LUMAClient to file.
	"""
	def default(self, obj):
		"""
		Overrides JSONEncoder.default() to call _encode_light() if the
		object being encoded is actually a Light instance.
		
		Parameters:
			obj (Any): The object to encode.
			
		Returns:
			The object transformed to be encoded.
			
		Preconditions:
			None.
		
		Postconditions:
			None.
		"""
		try:
			return _encode_light(obj, True)
		except:
			return JSONEncoder.default(self, obj)

def _decode_light(d):
	"""
	Creates a Light instance from a dictionary containing the guts of a Light
	instance.
	
	Parameters:
		d (Dictionary): The dictionary that contains the organs and ideas of
		the Light we are trying to coax into existence.
		
	Returns:
		A cultivated Light.
	
	Preconditions:
		The dictionary actually does specify a light. (i.e. it was encoded
		using _encode_light().)
		
	Postconditions:
		A Light is created.
	"""
	# Create the three different ColorChannels from members of the dictionary.
	r = ColorChannel(d['r_t'], d['r_v'], d['r_c'])
	g = ColorChannel(d['g_t'], d['g_v'], d['g_c'])
	b = ColorChannel(d['b_t'], d['b_v'], d['b_c'])
	# Construct and return the Light instance that wraps the ColorChannels.
	return Light(r, g, b, d['name'], d['id'])

def decodeRequest(r):
	"""
	Takes a String received as a request over a socket and decodes it as
	a JSON object into a dictionary.
	
	There are three types of requests.
		-status: These request the status of a Light or all Lights. If in want
			of a single Light, the data field contains the name of the light.
			If the status of all lights is desired, then the data field contains
			None.
		-change: These signal to change the pattern of a single Light. In this
			this Light is not decoded beyond Dictionary form.
		-add:	 These requests add lights to the client. These requests come
			packaged with a name, ID, and three pin numbers.
	
	Parameters:
		r (String): The request. It should be a JSON String that encodes:
		{
			"type":"status"|"change"|"add"
			"data":<encoded light object>|null
		}
		
	Returns:
		A dictionary that contains the following items:
		{
			"type":"status"|"change"
			"data":<decoded light object>|None
		}
		
	Preconditions:
		The request is a valid JSON String encoding the above data.
		
	Postconditions:
		A dictionary is created and returned.
	"""
	return loads(r)
	
def sanitizeRequest(r):
	"""
	Sanitizes a request.
	
	Parameters:
		r (JSON): The JSON request dictionary to sanitize.
		
	Returns:
		None if there was nothing wrong, an error message otherwise.
	
	Preconditions:
		None.
		
	Postconditions:
		None.
	"""
	# Make sure the request is a dictionary.
	if not isinstance(r, dict):
		return 'not a dictionary.'
		
	# Make sure all expected keys are present.
	for key in ['type', 'data']:
		if key not in r.keys():
			return key+' not in keys.'
	
	# Make sure the type key points to a String.
	if not (isinstance(r['type'], str) or isinstance(r['type'], unicode)):
		return 'Type not a string. Type: '+str(type(r['type']))
	
	# There are only two acceptable type values at this point in time.
	# THIS LIST MAY NEED EXPANSION LATER.
	if r['type'] != 'status'	\
	and r['type'] != 'change'	\
	and r['type'] != 'add'		\
	and r['type'] != 'info':
		return 'Type is not "status" or "change" or "add" or "info". Type is '+str(r['type'])
		
	# Status requests require an ID in their data field.
	if r['type'] == 'status' and 			\
	(not isinstance(r['data'], str)) and 	\
	(not isinstance(r['data'], unicode)):
		return 'Type is "status" but data is not an ID string. Type: '+str(type(r['data']))
		
	# Change requests require a dict of light data.
	if r['type'] == 'change' and (not isinstance(r['data'], dict)):
		return 'Type is "change" but data is not a dictionary. Type: '+str(type(r['data']))
		
	# Add requests require a dict as well.
	if r['type'] == 'add' and (not isinstance(r['data'], dict)):
		return 'Type is "add" but data is not a dictionary. Type: '+str(type(r['data']))
	
	# Info requests don't use the data field.
	if r['type'] == 'info':
		pass
		
	return None
	
def encodeResponse(type, light_s, message):
	"""
	Takes a response type, light, and encodes them into a JSON
	String to transmit back in response to a request.
	
	There are three types of responses:
		-status: These are in response to status requests. They store in their
			data field the state of the Light[s] requested in the request's data 
			field.
		-success: These indicate a successful update. The affected light's state
			is returned.
		-error: If a light doesn't exist on the client, or if an update could
			not be performed, then an error response is created with the
			affected light's name, and an explanatory message.
	
	Parameters:
		type ("status" | "success" | "error"): The type of response.
		light (Light | Light[] | None): The light to return.
		message (String): A message to send back.
		
	Returns:
		A JSON String that encodes a response as detailed above.
	
	Preconditions:
		The response should be valid as defined above.
		
	Postconditions:
		A response is created and encoded and returned.
	"""
	r = {}
	r['type'] = type
	r['data'] = light_s
	r['message'] = message
	
	print("Response:")
	print("  Type:    "+str(r['type']))
	print("  Message: "+str(r['message']))
	s = dumps(r, cls=_LightEncoder, separators=(',',':'))
	print("  Length:  "+str(len(s)))
	return s
	
def encodeLight(light):
	"""
	Returns a JSON encoded String describing the given Light.
	
	Parameters:
		light (Light): The light to encode.
	
	Returns:
		A JSON encoded String describing the given Light.
		
	Preconditions:
		The Light is kosher.
		
	Postconditions:
		None.
	"""
	return dumps(light, cls=_LightEncoder, sort_keys=True, indent=2)
	
		
def encodeLights(lights):
	"""
	Returns a JSON encoded String describing the list of Lights.
	
	Parameters:
		Lights (List): The list of Lights to encode.
		
	Returns:
		A JSON encoded String describing the list of Lights.
		
	Preconditions:
		The list of Lights is kosher.
		
	Postconditions:
		None.
	"""
	return dumps(lights, cls=_LightEncoder, sort_keys=True, indent=2)
		
def encodeState(name, lights):
	"""
	Encodes a lighting state.
	
	Parameters:
		name (String): The name of the client.
		Lights (List): The list of Lights to save.
		
	Returns:
		A JSON String encoding the given name and lights.
	
	Preconditions:
		The list contains only Light instances.
		
	Postconditions:
		None.
	"""
	# Create a JSON string containing all the lights. This will encode normally
	# until it recurses down to the elements in the list of lights, when it will
	# use the Light encoder.
	return dumps({'name':name, 'lights':lights}, cls=_LightSaveEncoder, sort_keys=True, indent=2)
	
def decodeState(state):
	"""
	Decodes a lighting state.
	
	Parameters:
		state (String): The JSON String that describes lighting state.
	
	Returns:
		A tuple (Client name, dictionary of lights)
		
	Preconditions:
		The JSON encoded state is valid 
		
	Postconditions:
		None.
	"""
	
	# Load the json object from a string. At this point it should be a list of
	# dictionaries, each dictionary a light.
	j = loads(state)
	# Create a dictionary to store all the new Light instances.
	lights = {}
	
	# For each dictionary in the json, we decode the dictionary and append it to
	# the lights list.
	for d in j['lights'].values():
		l = _decode_light(d)
		lights[l.id] = l
		
	# Finally we return the lights.
	return j['name'], lights