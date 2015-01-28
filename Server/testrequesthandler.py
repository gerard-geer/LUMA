"""
Tests the RequestHandler module.
"""

from requesthandler import RequestHandler

lightQueries = [	{'uuid':'1', 'query':''},
					{'uuid':'1', 'query':'Research'},
					{'uuid':'1', 'query':'Research Room'},
					{'uuid':'1', 'query':'Ceiling'},
					{'uuid':'1', 'query':'Gerard'},
					{'uuid':'6', 'query':''},
					{'uuid':'3', 'query':'Max'},
					{'uuid':'3', 'query':"Gerard's Desk"},
					{'uuid':'3', 'query':'Shelves'},
					{'uuid':'6', 'query':'.3'}
				]

stateQueries = [
					{'uuid':'3', 'name': "Max's Couch"}
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