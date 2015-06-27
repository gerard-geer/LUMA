"""
Tests the LightManager module.
"""
from lightmanager import LightManager
uuid = '6'
	
if __name__ == '__main__':
	lm = LightManager.Instance()
	lm.load()
	
	# Make sure all lights were loaded.
	for light in lm.getAllowedSubset('6'):
		print(light['name'] in ['Ceiling',"Gerard's Desk", "Shelves", \
			"Under Countertop"])
	
	# Test name changing and permissions.
	print(lm.changeLightName("100001", "lol"))
	print(lm.lightExists('100001'))
	print(not lm.lightExists('300001'))
	print(not lm.isAllowed('3', '100002'))
	print(lm.isAllowed('6', '100002'))
	print(lm.isAllowed('3', "100003"))
	print(not lm.isAllowed('999', "100003"))
