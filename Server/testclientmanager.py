#module testclientmanager.py

"""
Tests the ClientManager module.

This requires a running client on the local machine, or if
one wants to test another connection, one can change the
[good_addr] variable. 
This also requires that the client and server are using
the test configuration files, stored in "LUMA/Test Configs/"
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
	
def testClientManager():
	cm = ClientManager.Instance()
	
	# Test getting the status of multiple lights, and
	# lights that don't exist, and ones on bad clients.
	status = None
	print('SERVER TO CLIENT SYSTEM TESTING (REQUESTING)')
	status = cm.sendStatusRequest(good_addr, '100001')
	print(str(status['type']=='status')+' (Make sure we got a status on valid.)')
	status = cm.sendStatusRequest(good_addr, 'doesntexist')
	print(str(status['type']=='error' and 'does not exist on client' in status['message'])+' (non-existent light.)')
	status = cm.sendStatusRequest(bad_addr, 'doesntexist')
	print(str(status['type']=='error' and  'Could not connect' in status['message'])+' (non-existent client and light.)')
	status = cm.sendStatusRequest(bad_addr, '100001')
	print(str(status['type']=='error' and 'Could not connect' in status['message'])+' (non-existent client.)')
	
	# Try every thing that can happen when changing a light.
	print('SERVER TO CLIENT SYSTEM TESTING (EDITING)')
	# Objects to store the before and after states of a change.
	a = None
	b = None
	
	
	# The ID is still none, so a change request should error out.
	a = cm.sendChangeRequest(good_addr, base)
	print(str(a['type']=='error' and 'does not exist' in a['message'])+' (Null ID)')
	
	# Change all lights to the base light and verify.
	base['id'] = '100001'
	a = cm.sendChangeRequest(good_addr, base)['data']
	if a != None:
		base['name'] = a['name'] # Names are not changed.
	print(str(a==base) + ' (change 20001 to base.)')
	base['id'] = '100004'
	a = cm.sendChangeRequest(good_addr, base)['data']
	if a != None:
		base['name'] = a['name'] # Names are not changed.
	print(str(a==base) + ' (change 20002 to base.)')
	
	# Go to the first object and try changing it.
	base['id'] = '100001'
	change['id'] = '100001'
	b = cm.sendChangeRequest(good_addr, change)['data']
	if b == None:
		print(str(False) + ' (change 10001 and verify change.)')
	else:
		print(str(b['r_t'][0]!=base['r_t'][0]) + ' (change 10001 and verify change.)')
	
	# Moving over to the other object.
	base['id'] = '100004'
	change['id'] = '100004'
	b = cm.sendChangeRequest(good_addr, change)['data']
	if b == None:
		print(str(False) + ' (change 100004 and verify change.)')
	else:
		print(str(b['r_t'][0]!=base['r_t'][0]) + ' (change 10004 and verify change.)')
	
	# Make sure we can make a non-change change.
	a = cm.sendStatusRequest(good_addr, change['id'])
	b = cm.sendChangeRequest(good_addr, change)['data']
	if b == None:
		print(str(False) + " (change 10004 to itself and verify that it hasn't changed'.)")
	else:
		print(str(b['r_t'][0]!=base['r_t'][0]) + " (change 10004 to itself and verify that it hasn't changed'.)")
	
	# Check bad IDs and disconnected clients.
	base['id'] = 'nonexistent id'
	a = cm.sendChangeRequest(good_addr, base)['message']
	print(str('does not exist' in a) + ' (non-existent light)')	
	a = cm.sendChangeRequest(bad_addr, base)['message']
	print(str('Could not connect' in a) + ' (non-existent client)')
	
	# Test light validation.
	print('LIGHT VALIDATION UNIT TESTING')
	print(str(cm.validateLight(validLight) == None)+' (valid light.)')
	print(str(cm.validateLight(invalidLightA) == 'r_t does not contain only numbers.')+' (Bad timing values.)')
	print(str(cm.validateLight(invalidLightC) == 'Incorrect number of keys.')+' (No green channel timings.)')
	print(str(cm.validateLight(invalidLightD) == 'g_t is not a list.')+' (g_t is not a list.)')
	print(str(cm.validateLight(invalidLightE) == 'Light does not contain a r_t key.')+' (No r_t key.)')
	print(str(cm.validateLight(invalidLightF) == 'name is not a string.')+' (name is not a string.)')
	print(str(cm.validateLight(invalidLightG) == 'id is not a string.')+' (id is an integer list.)')
	print(str(cm.validateLight(invalidLightH) == 'id is not a string.')+' (id is an integer.)')
	print(str(cm.validateLight(invalidLightI) == 'Incorrect number of keys.')+' (No client key.)')

if __name__ == '__main__':
	testClientManager()