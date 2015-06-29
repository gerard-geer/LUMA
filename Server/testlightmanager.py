"""
Tests the LightManager module.
"""
from lightmanager import LightManager
uuid = '6'
	
if __name__ == '__main__':
	lm = LightManager.Instance()
	lm.load()
	
	# Make sure all lights were loaded.
	print("LIGHT MANAGER UNIT TESTING")
	for id in ['100001','100002','100003', \
			'100004','100005']:
		print(str(lm.getLight(id) != None)+' (Light id='+id+' loaded.)')
	
	# Test name changing and permissions.
	print(str(lm.changeLightName('100001', 'lol'))+' (Change light name.)')
	print(str(lm.getLight('100001')['name']=='lol')+' (Verify change.)')
	print(str(lm.changeLightClient('100001', 'new client'))+' (Change light client.)')
	print(str(lm.getLight('100001',)['client']=='new client')+' (Verify change.)')
	print(str(lm.lightExists('100001'))+' (Verify existence testing.)')
	print(str(not lm.lightExists('fake ID'))+' (Verify existence testing.)')
	print(str(not lm.deleteLight('fake ID'))+' (Delete fake light.)')
	print(str(lm.deleteLight('100001'))+' (Delete real light.)')
	print(str(not lm.getLight('100001'))+' (Verify deletion.)')
	print(str(not lm.deleteLight('100001'))+' (Check double delete.)')
	print(str(not lm.isAllowed('3', '100002'))+' (Check light whitelisting.)')
	print(str(lm.isAllowed('6', '100002'))+' (Check light whitelisting.)')
	print(str(lm.isAllowed('3', '100003'))+' (Check light whitelisting.)')
	print(str(not lm.isAllowed('999', '100003'))+' (Check light whitelisting.)')
	
	result = lm.addUUIDtoSubset('new UUID', ['100002', '100003','100004'])
	test = True
	for light in result.values():
		test = test and light['success']
		
	print(str(test)+' (Test adding UUID to multiple lights.')
	print(str(lm.isAllowed('new UUID', '100002'))+' (Verify add.)')
	print(str(not lm.isAllowed('new UUID', '100005'))+' (Verify add.)')
	
	result = lm.removeUUIDfromSubset('new UUID', ['100002', '100003','100004'])
	test = True
	for light in result.values():
		test = test and light['success']
		
	print(str(test)+' (Test removing UUID from multiple lights.')
	print(str(not lm.isAllowed('new UUID', '100002'))+' (Verify removal.)')
	print(str(not lm.isAllowed('new UUID', '100005'))+' (Verify removal.)')
