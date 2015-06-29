"""
Tests the RequestHandler module.
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
					{'uuid':'1', 'query':'not a valid query'}
				]

stateQueries = [	# Test valid state queries from a privileged user.
					{'uuid':'1', 'id': "100001"},
					{'uuid':'1', 'id': "100004"},
					# Test invalid state queries from a privileged user.
					{'uuid':'1', 'id': "10000X"},
					# Test valid state queries from a non-privileged user.
					{'uuid':'X', 'id': "100001"},
					{'uuid':'X', 'id': "100004"},
					# Test invalid state queries from a non-privileged user.
					{'uuid':'X', 'id': "10000X"}
				]

if __name__ == '__main__':
	rh = RequestHandler.Instance()
	# Make all the test light queries.
	for q in lightQueries:
		for light in rh.lightQuery(q)['lights']:
			print(light)
	
	# Make all the test state queries.
	for q in stateQueries:
		print(rh.stateQuery(q))
	