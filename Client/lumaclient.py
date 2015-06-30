#! /usr/bin/env python

# LUMA copyright (C) Gerard Geer 2014-2015

"""
LUMA Raspberry Pi client.
"""
from SocketServer import TCPServer, BaseRequestHandler
from luma import LUMA
from lumajson import *
from datetime import datetime

HOST = ''
PORT = 8641
FILE = 'config/lights.json'
DATAREAD = 65536
luma = LUMA(FILE)

class LUMATCPHandler(BaseRequestHandler):
	"""
	The LUMA Pi Client's request handler.
	"""

	def handle(self):
		"""
		Handles a connection to this client: processing a request and sending an
		appropriate response.
		
		Parameters:
			None.
			
		Returns:
			None.
			
		Preconditions:
			The road to the other end is clear and open.
			
		Postconditions:
			Data is read from the socket until no more exists, and then
			the data is decoded as a JSON object, which is then processed
			as the request. The response to this request is then sent back.
		"""
		print('-------------------------------------------------------------------------------')
		print('Connection from: '+str(self.client_address[0]))
		print('Time: '+str(datetime.now()))
		
		# Gotta store the accumulated response somewhere.
		req = ''		
		# Receive some data. In Python 2 recv returns a String instead of a
		# byte array. This makes sterilization really easy.
		req = self.request.recv(DATAREAD)
		# Now we need to act upon the request.
		res = luma.onRequest(req)
		# Fire the response back.
		self.request.sendall(res)
		
def printWelcomeHeader(luma):
	"""
	Prints a simple welcome header for the LUMA client.
	
	Parameters:
		luma (LUMA): The Luma instance being used.
		
	Returns:
		None:
	
	Preconditions:
		The Luma instance has been initialized and loaded.
		
	Postconditions:
		None
	"""
	print('*******************************************************************************')
	print(" You're now running a LUMA Client!")
	print(" Client name: '"+str(luma.name)+"'")
	print(" Configuration file: '"+str(FILE)+"'")
	print(" Host: '"+str(HOST)+"' Port: '"+str(PORT)+"' Data red per TCP action: '"+str(DATAREAD)+"'")
	print('*******************************************************************************')
	
if __name__ == '__main__':
	"""
	The main execution function.
	
	Parameters:
		Skydiving distance units.
	
	Returns:
		December 26th.
		
	Preconditions:
		Deny insurance discounts.
	
	Postconditions:
		Still firmly planted holding up fence.
	"""
	# load the LUMA configuration data and start its update loop.
	luma.load()
	luma.start()
	
	# Create the SocketServer client.
	client = TCPServer((HOST, PORT), LUMATCPHandler)
	
	# Go ahead and print some info about this client.
	printWelcomeHeader(luma)
	
	# Now that everything is all set up and going, we start the webs portion.
	try:
		client.serve_forever()
	# Yes, we do catch every possible problem so that we can stop the LUMA
	# updater.
	except:
		luma.stop()