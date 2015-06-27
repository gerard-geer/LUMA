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

cr = {	\
			'name': None,	\
			'id': None,
			'r_t': [9, 6],	\
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
	print('STATUS TESTING')
	print(cm.sendStatusRequest(good_addr, '200001'))
	print(cm.sendStatusRequest(good_addr, '200002'))
	print(cm.sendStatusRequest(good_addr, 'doesntexist'))
	print(cm.sendStatusRequest('bad addr', '200001'))
	
	# Try every thing that can happen when changing a light.
	print('CHANGE TESTING')
	print(cm.sendChangeRequest(good_addr, cr))
	cr['id'] = '200001'
	print(cm.sendChangeRequest(good_addr, cr))
	cr['id'] = '200002'
	print(cm.sendChangeRequest(good_addr, cr))
	cr['name'] = 'testB'
	print(cm.sendChangeRequest(good_addr, cr))
	cr['name'] = 'testA'
	print(cm.sendChangeRequest(good_addr, cr))
	cr['id'] = 'nonexistent id'
	print(cm.sendChangeRequest(good_addr, cr))
	print(cm.sendChangeRequest(bad_addr, cr))
	
	# Test light validation.
	print(lm.validateLight(validLight) == None)
	print(lm.validateLight(invalidLightA) == 'r_t does not contain only numbers.')
	print(lm.validateLight(invalidLightB) == 'Light not in server.')
	print(lm.validateLight(invalidLightC) == 'Incorrect number of keys.')
	print(lm.validateLight(invalidLightD) == 'g_t is not a list.')
	print(lm.validateLight(invalidLightE) == 'Light does not contain a r_t key.')
	print(lm.validateLight(invalidLightF) == 'name not a string.')
	print(lm.validateLight(invalidLightG))# == 'name not a string.')
	print(lm.validateLight(invalidLightH))# == 'name not a string.')
	print(lm.validateLight(invalidLightI))# == 'name not a string.')