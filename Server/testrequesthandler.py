#module testrequesthandler.py

"""
Tests the RequestHandler module. Like the other test suites,
this requires that the client and manager are using the test
configuration files.
"""

from requesthandler import RequestHandler

lightQueries = [	# Test good queries from a privileged user.
					{'uuid':'1', 'query':'Research Room'},
					{'uuid':'1', 'query':'Research'},
					{'uuid':'1', 'query':'Rese'},
					{'uuid':'1', 'query':'Ceiling'},
					{'uuid':'1', 'query':'Under Countertop'},
					{'uuid':'1', 'query':'Under'},
					{'uuid':'1', 'query':'Unde'},
					{'uuid':'1', 'query':'127.0.0'},
					# Test bad queries from a valid user.
					{'uuid':'1', 'query':'not a worthwhile query'},
					# Test good queries from a non-privileged user.
					{'uuid':'X', 'query':'Research Room'},
					{'uuid':'X', 'query':'Research'},
					{'uuid':'X', 'query':'Rese'},
					{'uuid':'X', 'query':'Ceiling'},
					{'uuid':'X', 'query':'Under Countertop'},
					{'uuid':'X', 'query':'Under'},
					{'uuid':'X', 'query':'Unde'},
					{'uuid':'X', 'query':'127.0.0'},
					# Test bad queries from a non-privileged user.
					{'uuid':'X', 'query':'not a valid query'},
					# Test badly formed query objects.
					{},
					{'asdfasd':'asdfasfd'},
					{'uuid':'1'},
					{'uuid':'x'},
					{'uuid':1},
					{'query':'ohno'},
					{'query':5}
				]
lightQueryComments = [
					' (Good query from a privileged user.)',
					' (Good query from a privileged user.)',
					' (Good query from a privileged user.)',
					' (Good query from a privileged user.)',
					' (Good query from a privileged user.)',
					' (Good query from a privileged user.)',
					' (Good query from a privileged user.)',
					' (Good query from a privileged user.)',
					' (Bad query from a privileged user.)',
					' (Good query from a non-privileged user.)',
					' (Good query from a non-privileged user.)',
					' (Good query from a non-privileged user.)',
					' (Good query from a non-privileged user.)',
					' (Good query from a non-privileged user.)',
					' (Good query from a non-privileged user.)',
					' (Good query from a non-privileged user.)',
					' (Good query from a non-privileged user.)',
					' (Bad query from a non-privileged user.)',
					' (Badly formed object.)',
					' (Badly formed object.)',
					' (Badly formed object.)',
					' (Badly formed object.)',
					' (Badly formed object.)',
					' (Badly formed object.)',
					' (Badly formed object.)'
				]
				
lightQueryExpectedLengths = [
					3,
					3,
					3,
					1,
					1,
					1,
					1,
					3,
					0,
					0,
					0, 
					0, 
					0, 
					0, 
					0, 
					0, 
					0, 
					0, 
					0, 
					0, 
					0, 
					0, 
					0, 
					0, 
					0
				]
					

stateQueries = [	# Test valid state queries from a privileged user.
					{'uuid':'1', 'id': "100001"},
					{'uuid':'1', 'id': "100004"},
					# Test valid state queries for a client that isn't accessible.
					# (privileged user)
					{'uuid':'3', 'id': "100003"},
					# Test invalid state queries from a privileged user.
					{'uuid':'1', 'id': "10000X"},
					# Test state queries for a light that exists but the client
					# isn't in the alias manager from a privileged user.
					{'uuid':'1', 'id': "100006"},
					# Test valid state queries from a non-privileged user.
					{'uuid':'X', 'id': "100001"},
					{'uuid':'X', 'id': "100004"},
					# Test invalid state queries from a non-privileged user.
					{'uuid':'X', 'id': "10000X"},
					# Test valid state queries for a client that isn't accessible.
					# (non-privileged user)
					{'uuid':'X', 'id': "100003"},
					# Test state queries for a light that exists but the client
					# isn't in the alias manager from a privileged user.
					{'uuid':'X', 'id': "100006"},
					# Test badly formed state query objects.
					{},
					{'astf':'asdf'},
					{'uuid':'1'},
					{'uuid':'x'},
					{'uuid':1},
					{'id':'ohno'},
					{'id':5}	
				]
				
stateQueryComments = [
					' (Valid state query from privileged user.)',
					' (Valid state query from privileged user.)',
					' (Valid state query from privileged user--inaccessible client.)',
					' (Invalid state query from privileged user.)',
					' (Valid state query from privileged user--light not in alias manager.)',
					' (Valid state query from non-privileged user.)',
					' (Valid state query from non-privileged user.)',
					' (Invalid state query from non-privileged user.)',
					' (Valid state query from non-privileged user--inaccessible client.)',
					' (Valid state query from non-privileged user--light not in alias manager.)',
					' (Badly formed query object.)',
					' (Badly formed query object.)',
					' (Badly formed query object.)',
					' (Badly formed query object.)',
					' (Badly formed query object.)',
					' (Badly formed query object.)',
					' (Badly formed query object.)',
					' (Badly formed query object.)'
				]
stateQueryExpectedMessages = [
					'Status returned.',
					'Status returned.',
					'Could not connect to client.',
					'Light does not exist.',
					'Client alias not recognized.',
					'User not allowed to access light.',
					'User not allowed to access light.',
					'Light does not exist.',
					'User not allowed to access light.',
					'User not allowed to access light.',
					'Invalid query.',
					'Invalid query.',
					'Invalid query.',
					'Invalid query.',
					'Invalid query.',
					'Invalid query.',
					'Invalid query.'
				]
				
if __name__ == '__main__':
	rh = RequestHandler.Instance()
	
	# Light query testing.
	print('LIGHT QUERY TESTING')
	for i in range(len(lightQueries)):
		q = lightQueries[i]
		e = lightQueryExpectedLengths[i]
		c = lightQueryComments[i]
		print(str(len(rh.lightQuery(q)['lights'])==e)+c)
	
	# Make all the test state queries.
	print('STATE QUERY TESTING')
	for i in range(len(stateQueries)):
		q = stateQueries[i]
		e = stateQueryExpectedMessages[i]
		c = stateQueryComments[i]
		print(str(rh.stateQuery(q)['message']==e)+c)
	