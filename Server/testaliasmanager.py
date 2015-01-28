"""
Tests the AliasManager Module.
"""

from aliasmanager import AliasManager
	
if __name__ == '__main__':
	am = AliasManager.Instance()
	am.load()
	
	# Test getting an existent and non-existent address.
	print(am.getAddress("Gerard's Room")=='1.2.3.4')
	print(am.getAddress("Gerard's Hoom")==None)
	
	# Test getting aliases from parts of addresses.
	print(len(am.getPossibleAliases('2'))==2)
	print(len(am.getPossibleAliases('3'))==3)
	print(len(am.getPossibleAliases('1'))==1)
	
	# Test adding an alias, if it doesn't already exist
	# and if it does.
	print(am.addAlias('added', '7.7.7.7'))
	print(not am.addAlias('added', '7.7.7.7'))
	
	# Test to see if we can get the newly added alias.
	print(am.getPossibleAliases('7'))
	
	# Try to get the new alias' address.
	print(am.getAddress('added'))
	
	# Try to delete that alias.
	print(am.deleteAlias('added'))
	
	# Make sure we don't double-delete.
	print(not am.deleteAlias('added'))
	
	# Is it still there?
	print(am.getPossibleAliases('7'))