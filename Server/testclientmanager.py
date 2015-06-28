"""
Tests the ClientManager module.

This requires a running client on the local machine, or if
one wants to test another connection, one can change the
[good_addr] variable. That client should also be using the
test configuration.
"""
from clientmanager import ClientManager

good_addr = '127.0.0.1'
bad_addr = 'not a good address'


validLight = {
	'id': '1234',
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
	'id': '1234',
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
	'id': '1234',
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
	'id': '1234',
	'r_t':[1,1.0],
	'r_v':[1,1.0],
	'g_v':[1,1.0],
	'b_t':[1,1.0],
	'b_v':[1,1.0],
	'name': 'Ceiling',
	'client': 'client'
	}
invalidLightD = {
	'id': '1234',
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
	'id': '1234',
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
	'id': '1234',
	'r_t':[1,1.0],
	'r_v':[1,1.0],
	'g_t':[1,1.0],
	'g_v':[1,1.0],
	'b_t':[1,1.0],
	'b_v':[1,1.0],
	'name': [1.0],
	'client': 'client'
	}
invalidLightG = {
	'id': [1, 1],
	'r_t':[1,1.0],
	'r_v':[1,1.0],
	'g_t':[1,1.0],
	'g_v':[1,1.0],
	'b_t':[1,1.0],
	'b_v':[1,1.0],
	'name': 'Ceiling',
	'client': 'client'
	}
invalidLightH = {
	'id': 1,
	'r_t':[1,1.0],
	'r_v':[1,1.0],
	'g_t':[1,1.0],
	'g_v':[1,1.0],
	'b_t':[1,1.0],
	'b_v':[1,1.0],
	'name': 'Ceiling',
	'client': 'client'
	}
invalidLightI = {
	'r_t':[1,1.0],
	'r_v':[1,1.0],
	'g_t':[1,1.0],
	'g_v':[1,1.0],
	'b_t':[1,1.0],
	'b_v':[1,1.0],
	'name': 'Ceiling',
	'client': 'client'
	}

base = {	\
			'name': None,	\
			'id': 'testA',
			'r_t': [9, 6],	\
			'r_v': [8, 6],	\
			'g_t': [9, 6],	\
			'g_v': [8, 6],	\
			'b_t': [9, 6],	\
			'b_v': [8, 6]	\
	}
change = {	\
			'name': None,	\
			'id': 'testA',
			'r_t': [10, 6],	\
			'r_v': [8, 6],	\
			'g_t': [9, 6],	\
			'g_v': [8, 6],	\
			'b_t': [9, 6],	\
			'b_v': [8, 6]	\
	}
if __name__ == '__main__':
	cm = ClientManager.Instance()
	
	# Test getting the status of multiple lights, and
	# lights that don't exist, and ones on bad clients.
	status = None
	print('STATUS TESTING')
	status = cm.sendStatusRequest(good_addr, '200001')
	print(status['type']=='status')
	status = cm.sendStatusRequest(good_addr, '200002')
	print(status['type']=='status')
	status = cm.sendStatusRequest(good_addr, 'doesntexist')
	print(status['type']=='error' and 'does not exist on client' in status['message'])
	status = cm.sendStatusRequest(bad_addr, 'doesntexist')
	print(status['type']=='error' and  'Could not connect' in status['message'])
	status = cm.sendStatusRequest(bad_addr, '200001')
	print(status['type']=='error' and 'Could not connect' in status['message'])
	
	# Try every thing that can happen when changing a light.
	print('CHANGE TESTING')
	# Objects to store the before and after states of a change.
	a = None
	b = None
	
	
	# The ID is still none, so a change request should error out.
	a = cm.sendChangeRequest(good_addr, base)
	print(a['type']=='error' and 'does not exist' in a['message'])
	
	# Change all lights to the base light and verify.
	base['id'] = '200001'
	a = cm.sendChangeRequest(good_addr, base)['data']
	base['name'] = a['name'] # Names are not changed.
	print(a==base)
	base['id'] = '200002'
	a = cm.sendChangeRequest(good_addr, base)['data']
	base['name'] = a['name'] # Names are not changed.
	print(a==base)
	
	# Go to the first object and try changing it.
	base['id'] = '200001'
	change['id'] = '200001'
	b = cm.sendChangeRequest(good_addr, change)['data']
	print(b['r_t'][0]!=base['r_t'][0])
	
	# Moving over to the other object.
	base['id'] = '200001'
	change['id'] = '200001'
	b = cm.sendChangeRequest(good_addr, change)['data']
	print(b['r_t'][0]!=base['r_t'][0])
	
	# Make sure we can make a non-change change.
	a = cm.sendStatusRequest(good_addr, change['id'])
	b = cm.sendChangeRequest(good_addr, change)['data']
	print(b['r_t'][0]!=base['r_t'][0])
	
	# Check bad IDs and disconnected clients.
	base['id'] = 'nonexistent id'
	print('does not exist' in cm.sendChangeRequest(good_addr, base)['message'])
	print('Could not connect' in cm.sendChangeRequest(bad_addr, base)['message'])
	
	# Test light validation.
	print('LIGHT VALIDATION TESTING')
	print(cm.validateLight(validLight) == None)
	print(cm.validateLight(invalidLightA) == 'r_t does not contain only numbers.')
	print(cm.validateLight(invalidLightC) == 'Incorrect number of keys.')
	print(cm.validateLight(invalidLightD) == 'g_t is not a list.')
	print(cm.validateLight(invalidLightE) == 'Light does not contain a r_t key.')
	print(cm.validateLight(invalidLightF) == 'name is not a string.')
	print(cm.validateLight(invalidLightG) == 'id is not a string.')
	print(cm.validateLight(invalidLightH) == 'id is not a string.')
	print(cm.validateLight(invalidLightI) == 'Incorrect number of keys.')