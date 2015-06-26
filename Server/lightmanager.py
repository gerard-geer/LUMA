#module lightmanager.py

from json import load, dump
from uuid import uuid4
from singleton import Singleton

@Singleton
class LightManager(object):
	"""
	A singleton manager to manage the server's knowledge of the various
	lighting fixtures in the field. This wraps file operations and light
	representation manipulation.
	Each light is its own Dictionary:
	{
		"name":<Light name>,
		"client":<Client name>
		"permitted":<list of permitted UUIDs.
	}
	
	Slots:
		_filename (String): Private. The name of the light configuration file.
			lights.
		_lights (Dictionary): Private. The dictionary of light dictionaries.
	"""
	__slots__ = ('_filename', '_lights')
	
	def __init__(self):
		"""
		Initializes the LightManager. Don't call this directly; use Instance()
		instead for singleton safety.
		
		Parameters:
			None.
			
		Returns:	
			None.
			
		Preconditions:
			None.
			
		Postconditions:
			None.
		"""
		self._filename = 'config/lights.json'
		self._lights = None
		
	def load(self):
		"""
		Loads all lighting fixtures from file.
		
		Parameters:
			None.
		
		Returns:
			None.
			
		Preconditions:
			The restricted global filename points to a valid configuration 
			JSON file.
			
		Postconditions:
			The lights loaded from file are stored in the restricted global light
			list.
		"""
		file = open(self._filename, 'r')
		self._lights = load(file)
		file.close()
		
	def save(self, filename=None):
		"""
		Saves the lights to the locally global configuration file.
		
		Parameters:
			None.
			
		Returns:
			None.
			
		Preconditions:
			You probably want to make sure the lights have been loaded.
			
		Postconditions:
			The current list of lights are stored into the file. This operation 
			overwrites the pre-existing contents of the configuration file.
		"""
		file = open(filename if filename else self._filename, 'w')
		dump(self._lights, file, indent=4, sort_keys=True)
		file.close()
		
	def getAllowedSubset(self, uuid):
		"""
		Returns a subset of the lights that are accessible to the given UUID.
		
		Parameters:
			uuid (String): The UUID to consider.
			
		Returns:
			A list of lights that the UUID is allowed to access.
			
		Preconditions:
			The lights have been loaded.
			
		Postconditions:
			None.
		"""
		allowed = []
		for light in self._lights.values():
			if uuid in light['permitted']:
				allowed.append(light)
		return allowed
		
	def addLight(self, name, client, permitted):
		"""
		Adds a new light, creating a UUID to uniquely identify it. The
		permitted list is not manipulated, but shallow copied into
		the new light.
		Also, the light is keyed into the light dictionary by its id.
		
		Parameters:
			name (String): The name of the new light.
			client (String): The alias of the client that the light is on.
			permitted ([String]): A white-list of UUIDs.
		
		Returns:
			True if the light was added, False otherwise.
		
		Preconditions:
			The lights are loaded.
			
		Postconditions:
			The light is added to the list.
		"""
		id = str(uuid4())
			
		light = {'id':id, 'name':name,'client':client,'permitted':[]}
		light['permitted'].extend(permitted)
		self._lights[id] = light
		return True
		
	def changeLightName(self, id, new):
		"""
		Changes the name of a light.
		
		Parameters:
			id (String): The light's ID.
			new (String): The new name for the light.
			
		Returns:
			True if the light name was changed, False otherwise.
			
		Preconditions:
			Lights must have have been loaded.
			
		Postconditions:
			The light's name has been changed.
		"""
		if id in self._lights.keys():
			self._lights[id]['name'] = new
			return True
		return False
			
	def changeLightClient(self, name, client):
		"""
		Change the client alias stored with a light.
		
		Parameters:
			name (String): The name of the light to change.
			client (String): The new client alias.
			
		Returns:
			True if the client was changed, False otherwise.
		
		Preconditions:
			Lights must have been loaded.
			
		Postconditions:
			The light's client alias has been changed.
		"""
		if name in self._lights.keys():
			self._lights[name]['client'] = client
			return True
		return False
			
	def deleteLight(self, name):
		"""
		Deletes a light.
		
		Parameters:
			name(String): The name of the light to delete.
		
		Returns:
			True if deleted, false otherwise.
			
		Preconditions:
			The light should exist if you want this to go off without a hitch.
			
		Postconditions:
			The light is wiped from local storage. The representation on the
			client still remains.
		"""
		if name in self._lights.keys():
			del self._lights[name]
			return True
		return False
			
	def addUUIDtoSubset(self, uuid, names):
		"""
		Adds the given UUID to each of the lights specified by the list of
		names.
		
		Parameters:
			uuid(String): The UUID to add.
			names([String]): The list of light names.
			
		Returns:
			A dictionary describing the results of each add operation.
			
		Preconditions:
			The lights have been loaded from file.
			
		Postconditions:
			The UUID is added to each light that exists, where it doesn't
			already exist.
		"""
		result = {}
		for name in names:
			result[name] = {}
			if name in self._lights.keys():
				if uuid not in self._lights[name]['permitted']:
					self._lights[name]['permitted'].append(uuid)
					result[name]['success']=True
					result[name]['message']=None
				else:
					result[name]['success'] = False
					result[name]['message'] = 'UUID already exists.'
			else:
				result[name]['success'] = False
				result[name]['message'] = 'UUID already exists.'
		return result
					
	def removeUUIDfromSubset(self, uuid, names):
		"""
		Removes the given UUID from each of the lights specified by the list of
		names.
		
		Parameters:
			uuid(String): The UUID to remove.
			names(String]): The list of light names.
			
		Returns:
			A dictionary describing the results of each remove operation.
			
		Preconditions:
			The lights have been loaded from file.
			
		Postconditions:
			The UUID is removed from each light that exists, where it exists.
		"""
		result = {}
		for name in names:
			result[name] = {}
			if name in self._lights.keys():
				new=[id for id in self._lights[name]['permitted'] if id != uuid]
				old = self._lights[name]['permitted']
				if len(new) == len(old):
					result[name]['success'] = False
					result[name]['message'] = 'UUID does not exist.'
				else:
					result[name]['success'] = True
					result[name]['message'] = None
			else:
				result[name]['success'] = False
				result[name]['message'] = 'Light does not exist.'
		return result
		
	def lightExists(self, name):
		"""
		Returns whether or not the light exists on the server.
		
		Parameters:
			name (String): The name of the light to check for.
			
		Returns:
			True if the light exists, false otherwise.
			
		Preconditions:
			As usual, the lights must have been loaded.
		
		Postconditions:
			None.
		"""
		return name in self._lights.keys()
		
	def getLight(self, name):
		"""
		Returns a light given a name.
		
		Parameters:
			name (String): The name of the light.
		
		Returns:
			The light or None, depending on its existence.
			
		Preconditions:
			The lights have been loaded.
			
		Postconditions:
			None.
		"""
		try:
			return self._lights[name]
		except KeyError:
			return None
		
	def isAllowed(self, uuid, name):
		"""
		Returns whether or not the given UUID can access the given light.
		
		Parameters:
			uuid (String): The UUID to check for.
			name (String): The name of the light to check in.
			
		Returns:
			True if the light is accessible, false otherwise.
			
		Preconditions:
			Lights have been loaded.
		
		Postconditions:
			None.
		"""
		if name in self._lights.keys():
			if uuid in self._lights[name]['permitted']:
				return True
		return False