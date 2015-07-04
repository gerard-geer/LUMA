#! /usr/bin/env python

# LUMA copyright (C) Gerard Geer 2014-2015

from json import dumps
from flask import Flask, send_from_directory, request
from requesthandler import RequestHandler
from datetime import datetime

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
rh = RequestHandler.Instance()
	
# Draw the start-up message.
def printStartupHeader():
	print('*******************************************************************************')
	print(" You're now running the LUMA Server!")
	rh.printInfo()
	print('*******************************************************************************')

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
	
if __name__ == '__main__':
	printStartupHeader()
	app.run(host='0.0.0.0')