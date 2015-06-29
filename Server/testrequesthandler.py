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
					{'uuid':'x', 'query':'Research Room'},
					{'uuid':'x', 'query':'Research'},
					{'uuid':'x', 'query':'Rese'},
					{'uuid':'x', 'query':'Ceiling'},
					{'uuid':'x', 'query':'Under Countertop'},
					{'uuid':'x', 'query':'Under'},
					{'uuid':'x', 'query':'Unde'},
					{'uuid':'x', 'query':'127.0.0'},
					# Test bad queries from a non-privileged user.
					{'uuid':'1', 'query':'not a valid query'}

stateQueries = [
					{'uuid':'1', 'id': "100001"}
					{'uuid':'1', 'id': "100001"}
					{'uuid':'1', 'id': "100001"}
				]

if __name__ == '__main__':
	rh = RequestHandler.Instance()
	# Make all the test queries.
	for q in lightQueries:
		printme = []
		for light in rh.lightQuery(q)['lights']:
			printme.append(light['name'])
		print(printme)
		
	# Make all the test state queries.
	for q in stateQueries:
		print(rh.stateQuery(q))