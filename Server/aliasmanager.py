#module aliasmanager.py
# LUMA copyright (C) Gerard Geer 2014-2015

from json import loads, dump
from singleton import Singleton

@Singleton
class AliasManager(object):
	"""
	A singleton manager that wraps the dictionary that maps client names
	to client IPs. This is done so that file loading, saving, and updating
	of the IP table are all contained within a single module.
	
	The reason this exists is so that raw IPs are never worked with by the
	web interface. Better readability on part of the requests themselves, and
	a good bit less sketchy.
	
	Slots:
		_filename (String): Private. The name of the aliases configuration file.
			aliases.json.
		_aliases: (Dictionary): Private. The dictionary that translates aliases
			to IPs.
			to IPs.
	"""
	__slots__ = ('_filename', '_aliases')
	
	def __init__(self):
		"""
		Initializes the AliasManager. Don't call this directly; use Instance()
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
		self._filename = 'config/aliases.json'
		self._aliases = None
		
	def load(self):
		"""
		Loads aliases from the aliases configuration file.
		
		Parameters:
			None.
			
		Returns:
			True if the config was able to be loaded, False otherwise.
			
		Preconditions:
			The alias file must exist.
			
		Postconditions:
			The aliases are loaded into the internal dictionary.
		"""
		try:
			file = open(self._filename, 'r')
		except IOError:
			return False
			
		s = ''
		for line in file:
			# Split the line to see if its first token is a comment delimiter.
			tokens = line.split()
			# If it is a comment delimiter, we skip the line.
			if len(tokens) > 0 and tokens[0] in ['#','//',';']:
				continue
			# Otherwise, we take the line and append it to the JSON string.
			s += line
		self._aliases = loads(s)
		file.close()
		return True
		
	def save(self, filename=None):
		"""
		Saves the aliases to the configuration file.
		
		Parameters:
			filename (String): Optional. Specify an alternate filename.
			(for backups.)
			
		Returns:
			None.
			
		Preconditions:
			The alias dictionary is in a state that you want to store.
			
		Postconditions:
			The file is overwritten with the new alias configuration data.
		"""
		file = open(filename if filename else self._filename, 'w')
		dump(self._aliases, file, indent=4, sort_keys=True)
		file.close()
	
	def getAddress(self, alias):
		"""
		Gets an address from an alias.
		
		Parameters:
			alias (String): The alias to anti-alias.
			
		Returns:
			If the alias exists, the address. None otherwise.
			
		Preconditions:
			The aliases must be loaded.
			
		Postconditions:
			None.
		"""
		if alias in self._aliases.keys():
			return self._aliases[alias]
		return None
		
	def getPossibleAliases(self, address):
		"""
		Returns all possible aliases given an address.
		
		Parameters:
			address (String): All or part of an address.
		"""
		possible = []
		rl = {}
		for alias, clientIP in self._aliases.items():
			rl[clientIP] = alias
		
		for clientIP, alias in rl.items():
			if address in clientIP:
				possible.append(alias)
		return possible
		
	def addAlias(self, alias, address):
		"""
		Adds an alias to the dictionary.
		
		Parameters:
			alias (String): The alias to add.
			address (String): The companion address.
			
		Returns:
			True if the alias was added, false otherwise.
			
		Preconditions:	
			The aliases were loaded from file.
			
		Postconditions:
			The alias was added if it didn't already exist.
		"""
		if  alias not in self._aliases.keys()	\
			and address not in self._aliases.values():
			self._aliases[alias] = address
			return True
		return False
	
	def deleteAlias(self, alias):
		"""
		Deletes an alias.
		
		Parameters:
			alias (String): The alias to delete.
			
		Returns:
			True if the alias was deleted, false otherwise.
			
		Preconditions:
			The aliases were loaded from the configuration file.
			
		Postconditions:
			The alias is deleted if it existed.
		"""
		if alias not in self._aliases.keys():
			return False
		del self._aliases[alias]
		return True
		
	def updateAlias(self, alias, newAddr):
		"""
		Changes the address bound to an alias.
		
		Parameters:
			alias (String): The alias to update.
			address (String): The new address.
			
		Returns:
			True if the alias was found, False otherwise.
		
		Preconditions:
			The aliases were loaded from the configuration file.
			
		Postconditions:
			The alias now has a new address if it exists.
		"""
		if alias not in self._aliases.keys():
			return False
		self._aliases[alias] = newAddr
		return True
		
	def getClientCatalog(self):
		"""
		Returns a catalog of all the clients in the manager, with
		names keyed to addresses.
		
		Parameters:
			None.
			
		Returns:
			A dictionary of clients, name->address.
			
		Preconditions:
			The client manager is loaded.
			
		Postconditions:
			None.
		"""
		res = {}
		for key in self._aliases.keys():
			res[key] = self._aliases[key]
		return res