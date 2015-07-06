#! /usr/bin/env python

# LUMA copyright (C) Gerard Geer 2014-2015

from json import dumps
from flask import Flask, send_from_directory, request
from requesthandler import RequestHandler
from datetime import datetime
import logging

"""
The LUMA central server. It's a Flask app. All non-file requests are handled
by an instance of RequestHandler from requesthandler.py.

The server works by maintaining an understanding of available lights
and clients, and upon requests from the web interface sanitizes and translates
those requests and sends them out to the Pis. The response from the Pi is then
sent back to the web interface as confirmation. Timely? About as can be.
Responsive? If it's your lucky day.
"""
app = Flask(__name__)
	
# Index page.
@app.route('/', methods=['GET'])
def fetchHTML():
	print('-------------------------------------------------------------------------------')
	print(' HTML Request from: '+request.remote_addr)
	print(' Time: '+str(datetime.now())+' For: '+request.path)
	return send_from_directory('webs/', 'index.html')
# CSS
@app.route('/css/<path:filename>', methods=['GET'])
def fetchCSS(filename):
	print('-------------------------------------------------------------------------------')
	print(' CSS Request from: '+request.remote_addr)
	print(' Time: '+str(datetime.now()) + ' For: '+request.path)
	return send_from_directory('webs/css/', filename)
	
# JavaScript
@app.route('/js/<path:filename>', methods=['GET'])
def fetchJS(filename):
	print('-------------------------------------------------------------------------------')
	print(' JS Request from: '+request.remote_addr)
	print(' Time: '+str(datetime.now()) +' For: '+request.path)
	return send_from_directory('webs/js/', filename)
	
# Light queries.
@app.route('/resources/lights/<light_query>', methods=['GET'])
def lightQueries(light_query):
	print('-------------------------------------------------------------------------------')
	print(' Light Query from: '+request.remote_addr)
	print(' Time: '+str(datetime.now()))
	return dumps(rh.lightQuery(light_query))

# Get light state.
@app.route('/resources/lights/state/<light_state_query>', methods=['GET'])
def stateQuery(light_state_query):
	print('-------------------------------------------------------------------------------')
	print(' Light State Query from: '+request.remote_addr)
	print(' Time: '+str(datetime.now()))
	return dumps(rh.stateQuery(light_state_query))
	
# Set light state.
@app.route('/resources/lights/state/', methods=['POST'])
def stateUpdate():
	print('-------------------------------------------------------------------------------')
	print(' Light State Update from: '+request.remote_addr)
	print(' Time: '+str(datetime.now()))
	return dumps(rh.lightUpdate(request.get_json()))

def printInitialSetupHeader():
	print('*******************************************************************************')
	print(" Welcome to the LUMA server!")
	print(" Sadly, there have been problems during startup.")
	print(" This may only be first-time jitters.")
	print('-------------------------------------------------------------------------------')
	
# Draw the start-up message.
def printStartupHeader():
	print('*******************************************************************************')
	print(" You're now running the LUMA Server!")
	rh.printInfo()
	print('*******************************************************************************')

	
def createAliasConfigFile():
	"""
	A utility function for first time or error time startup. If the alias manager
	fails to open its config file, this function should be called to create one.
	
	Parameters:
		None.
		
	Returns:
		None.
		
	Preconditions:
		config/aliases.json either doesn't exist or is ready to get nuked.
		
	Postconditions:
		A new config file is born.
	"""
	print(" The alias configuration file doesn't seem to exist. Let's specify")
	print(" some client names and their IP addresses and make one.\n")
	resp = 'y'
	clients = {}
	while resp.lower() == 'y':
		print(" Client #"+str(len(clients.keys())+1))
		name = raw_input('   Client name: ')
		addr = raw_input('   Client address: ')
		clients[name] = addr
		resp = raw_input(" Another? (Y/n): ")
	print(" Clients created...")
	print(" Creating new config file...")
	f = open('config/aliases.json', 'w')
	print(" Dumping client-->address table to file...")
	f.write(dumps(clients, indent=2))
	print(" Done.")
	print('-------------------------------------------------------------------------------')
	
def createLightConfigFile():
	"""
	A utility function for first time or error time startup. If the light manager
	fails to open its config file, this function should be called to create one.
	
	Parameters:
		None.
		
	Returns:
		None.
		
	Preconditions:
		config/lights.json either doesn't exist or is ready to get nuked.
		
	Postconditions:
		A new config file is born.
	"""
	print(" The lights configuration file doesn't seem to exist. Let's create an empty")
	print(' one to get running. You can add lights later.\n')
	raw_input(' ## Press enter to create a new light configuration file. ##')
	print(' Creating document structure...')
	lights = {}
	print(' Creating new config file...')
	f = open('config/lights.json','w')
	print(' Dumping light structure to file...')
	f.write(dumps(lights, indent = 2))
	print(' Done.')
	print('-------------------------------------------------------------------------------')
	
	
	
def main():
	"""
	The main execution function of the LUMA server. Initializes and loads the
	managers, then starts Flask.
	If the loading of any manager fails, an initial setup dialog for the manager
	is run.
	
	Parameters:
		None.
	
	Returns:
		None.
		
	Preconditions:
		None.
		
	Postconditions:
		The program is running.
	"""
	# Disable normal logging so that we don't clutter up things.
	log = logging.getLogger('werkzeug')
	log.setLevel(logging.WARNING)
	
	# Create the request handler.
	rh = RequestHandler.Instance()
	
	# Try to load the components of the request handler.
	am, lm = rh.load()
	
	# If either fail we have to act.
	if not (am and lm):
		printInitialSetupHeader()
		if not am:
			try:
				createAliasConfigFile()
			except KeyboardInterrupt:
				print('\n\n Keyboard interrupt. Cancelling.')
				print('-------------------------------------------------------------------------------')
		if not lm:
			try:
				createLightConfigFile()
			except KeyboardInterrupt:
				print('\n\n Keyboard interrupt. Cancelling.')
				print('-------------------------------------------------------------------------------')
		print('*******************************************************************************')
		return
	
	
	# Print the startup header.
	printStartupHeader()
	# Start the server.
	app.run(host='0.0.0.0')
	
if __name__ == '__main__':
	main()