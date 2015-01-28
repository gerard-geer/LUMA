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
	print(cm.sendStatusRequest(good_addr, 'testA'))
	print(cm.sendStatusRequest(good_addr, 'testB'))
	print(cm.sendStatusRequest(good_addr, 'doesntexist'))
	print(cm.sendStatusRequest('bad addr', 'testA'))
	
	# Try every thing that can happen when changing a light.
	print('CHANGE TESTING')
	print(cm.sendChangeRequest(good_addr, cr))
	cr['name'] = 'testA'
	print(cm.sendChangeRequest(good_addr, cr))
	cr['name'] = 'testB'
	print(cm.sendChangeRequest(good_addr, cr))
	cr['name'] = 'nonexistent light'
	print(cm.sendChangeRequest(good_addr, cr))
	print(cm.sendChangeRequest(bad_addr, cr))