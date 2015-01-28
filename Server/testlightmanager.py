"""
Tests the LightManager module.
"""
from lightmanager import LightManager
uuid = '6'
validLight = {
	'r_t':[1,1.0],
	'r_v':[1,1.0],
	'g_t':[1,1.0],
	'g_v':[1,1.0],
	'b_t':[1,1.0],
	'b_v':[1,1.0],
	'name': 'Ceiling',
	'client': 'client'
	}
invalidLightA = {
	'r_t':['a', 'a'],
	'r_v':[1,1.0],
	'g_t':[1,1.0],
	'g_v':[1,1.0],
	'b_t':[1,1.0],
	'b_v':[1,1.0],
	'name': 'Ceiling',
	'client': 'client'
	}
invalidLightB = {
	'r_t':[1,1.0],
	'r_v':[1,1.0],
	'g_t':[1,1.0],
	'g_v':[1,1.0],
	'b_t':[1,1.0],
	'b_v':[1,1.0],
	'name': 'not in server',
	'client': 'client'
	}
invalidLightC = {
	'r_t':[1,1.0],
	'r_v':[1,1.0],
	'g_v':[1,1.0],
	'b_t':[1,1.0],
	'b_v':[1,1.0],
	'name': 'Ceiling',
	'client': 'client'
	}
invalidLightD = {
	'r_t':[1,1.0],
	'r_v':[1,1.0],
	'g_t':'a',
	'g_v':[1,1.0],
	'b_t':[1,1.0],
	'b_v':[1,1.0],
	'name': 'Ceiling',
	'client': 'client'
	}
invalidLightE = {
	'r_x':[1,1.0],
	'r_v':[1,1.0],
	'g_t':[1,1.0],
	'g_v':[1,1.0],
	'b_t':[1,1.0],
	'b_v':[1,1.0],
	'name': 'Ceiling',
	'client': 'client'
	}
invalidLightF = {
	'r_t':[1,1.0],
	'r_v':[1,1.0],
	'g_t':[1,1.0],
	'g_v':[1,1.0],
	'b_t':[1,1.0],
	'b_v':[1,1.0],
	'name': [1.0],
	'client': 'client'
	}
	
if __name__ == '__main__':
	lm = LightManager.Instance()
	lm.load()
	
	# Make sure all lights were loaded.
	for light in lm.getAllowedSubset('6'):
		print(light['name'] in ['Ceiling',"Gerard's Desk", "Shelves", \
			"Under Countertop"])
	
	# Test name changing and permissions.
	print(lm.changeLightName("Gerard's Desk", "lol"))
	print(lm.lightExists('lol'))
	print(not lm.lightExists('loll'))
	print(not lm.isAllowed('3', 'lol'))
	print(lm.isAllowed('6', 'lol'))
	print(lm.isAllowed('3', "Max's Couch"))
	print(not lm.isAllowed('999', "Max's Couch"))
	
	# Test light validation.
	print(lm.validateLight(validLight) == None)
	print(lm.validateLight(invalidLightA) == 'r_t does not contain only numbers.')
	print(lm.validateLight(invalidLightB) == 'Light not in server.')
	print(lm.validateLight(invalidLightC) == 'Incorrect number of keys.')
	print(lm.validateLight(invalidLightD) == 'g_t is not a list.')
	print(lm.validateLight(invalidLightE) == 'Light does not contain a r_t key.')
	print(lm.validateLight(invalidLightF) == 'name not a string.')
