#! /usr/bin/env python

# LUMA copyright (C) Gerard Geer 2014-2015

"""
LUMA Raspberry Pi client.
"""
from SocketServer import TCPServer, StreamRequestHandler
from socket import SOL_SOCKET, SO_REUSEADDR
from luma import LUMA
from select import select
from lumajson import *
from datetime import datetime

HOST = ''
PORT = 8641
FILE = 'config/lights.json'
TIMEOUT = 3.0
luma = LUMA(FILE)

class LUMATCPHandler(StreamRequestHandler):
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
		# Print some info.
		print('-------------------------------------------------------------------------------')
		print('Connection from: '+str(self.client_address[0]))
		print('Time: '+str(datetime.now()))
		
		# Receive some data. 
		req = self.rfile.readline()
		
		# Print some more info.
		print('Request:')
		print('  Length: '+str(len(req)))
		
		# Now we need to act upon the request.
		res = luma.onRequest(req)
		
		# Fire the response back.
		self.wfile.write(res)
		
def printWelcomeHeader(luma):
	"""
	Prints a simple welcome header for the LUMA client.
	
	Parameters:
		luma (LUMA): The Luma instance being used.
		
	Returns:
		None.
	
	Preconditions:
		The Luma instance has been initialized and loaded.
		
	Postconditions:
		None.
	"""
	lights = luma.getLights()
	print('*******************************************************************************')
	print(" You're now running a LUMA Client!\n")
	
	print(" Client name: '"+str(luma.name)+"'")
	print(" Configuration file: '"+str(FILE)+"'")
	print(" Host: '"+str(HOST)+"' Port: '"+str(PORT)+'\n')
	
	print(" Lights: ("+str(len(lights))+")")
	for light in lights:
		print("   %-20s : "%str(light.id)+str(light.name))
	print('*******************************************************************************')
	
def firstTimeStartup():
	"""
	If the file config file doesn't exist, this function is called
	in order to initialize the new client.
	It asks for a name, and creates an empty configuration file 
	with it.
	
	Parameters:
		None.
	
	Returns:
		None.
		
	Preconditions:
		None.
		
	Postconditions:
		A fresh empty configuration file is stored in 'config/'.
	"""
	print('*******************************************************************************')
	print(" Welcome to your LUMA Client!\n")
	print(" It appears this is the first time you've run the client, or your configuration")
	print(" is corrupted.\n")
	print(" Let's do some initial setup.\n")
	name = raw_input(" What would you like your client's name to be?\n -->")
	print(" Thanks, that's all we need for now.")
	
	print(" Creating configuration...")
	s = encodeState(name, {})
	
	print(" Creating config file...")
	f = open(FILE, 'w')
	
	print(" Saving...")
	f.write(s)
	print(" Done.")
	print('*******************************************************************************')
	
def main():
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
	luma = LUMA(FILE)
	
	# load the LUMA configuration data and start its update loop.
	success = luma.load()
	if not success:
		try:
			firstTimeStartup()
		except:
			print('\n\n Keyboard interrupt. Cancelling.')
			print('*******************************************************************************')
		return
		
	luma.start()
	
	# Create the SocketServer client.
	client = TCPServer((HOST, PORT), LUMATCPHandler)
	
	# Set the client's time-out.
	client.timeout = TIMEOUT

	# Set the client's maximum request queue length so peeeeps don't get peeeeeeepy.
	client.request_queue_size = 1
	
	# Go ahead and print some info about this client.
	printWelcomeHeader(luma)
	
	# Now that everything is all set up and going, we start the webs portion.
	try:
		client.serve_forever()
	# Yes, we do catch every possible problem so that we can stop the LUMA
	# updater.
	except:
		luma.stop()
	
if __name__ == '__main__':
	main()