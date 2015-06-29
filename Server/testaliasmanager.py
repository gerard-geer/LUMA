#module testaliasmanager.py
# LUMA copyright (C) Gerard Geer 2014-2015

"""
Tests the AliasManager Module.

This requires that the server is using the test configuration files.
"""

from aliasmanager import AliasManager

def testAliasManager():
	am = AliasManager.Instance()
	am.load()
	print('ALIAS MANAGER UNIT TESTING')
	# Test getting an existent and non-existent address.
	print(str(am.getAddress("Gerard's Room")=='1.2.3.4')+' (Get address for existent client.)')
	print(str(am.getAddress("Gerard's Hoom")==None)+' (Get null address for non-existend client.)')
	
	# Test getting aliases from parts of addresses.
	print(str(len(am.getPossibleAliases('2'))==3)+' (Two aliases have addrs with "3" in them.)')
	print(str(len(am.getPossibleAliases('3'))==2)+' (Three aliases have addrs with "2" in them.)')
	print(str(len(am.getPossibleAliases('127'))==1)+' (One possible alias with "127")')
	
	# Test adding an alias, if it doesn't already exist
	# and if it does.
	print(str(am.addAlias('added', '7.7.7.7'))+' (Light successfully added.)')
	print(str(not am.addAlias('added', '7.7.7.7'))+' (Duplicate rejected)')
	
	# Test to see if we can get the newly added alias.
	print(str(am.getAddress('added')=='7.7.7.7')+' (Retrieve added alias.)')
	
	# Try to get the new alias' address.
	print(str(am.getAddress('added')=='7.7.7.7')+" (Get added alias' address.)")
	
	# Try to delete that alias.
	print(str(am.deleteAlias('added'))+' (Delete added alias.)')
	
	# Make sure we don't double-delete.
	print(str(not am.deleteAlias('added'))+' (Cannot double delete.)')
	
	# It better not still be there.
	print(str(am.getAddress('added')==None)+' (Verify deletion.)')
	
if __name__ == '__main__':
	testAliasManager()