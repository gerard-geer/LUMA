"""
LUMA Raspberry Pi client.
"""
from SocketServer import TCPServer, BaseRequestHandler
from luma import LUMA
from lumajson import *

HOST = ''
PORT = 8641
FILE = 'config/lights.json'

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
		print('Connection from '+str(self.client_address[0])+'.')
		
		# Gotta store the accumulated response somewhere.
		req = ''
		# We loop on reading data until having no data received breaks us out.
		
		# Receive some data. In Python 2 recv returns a String instead of a
		# byte array. This makes sterilization really easy.
		req = self.request.recv(4096)
		print("request: "+req)
		# Now we need to act upon the request.
		res = luma.onRequest(req)
		# Fire the response back.
		self.request.sendall(res)
	
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
	
	# Now that everything is all set up and going, we start the webs portion.
	try:
		client.serve_forever()
	# Yes, we do catch every possible problem so that we can stop the LUMA
	# updater.
	except:
		luma.stop()