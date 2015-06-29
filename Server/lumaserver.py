# LUMA copyright (C) Gerard Geer 2014-2015

from flask import Flask, send_from_directory
from requesthandler import RequestHandler

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
indexPage = ''
f = open("webs/test/index.html")
for line in f:
	indexPage += line

# Index page.
@app.route('/')
def fetchHTML():
	return send_from_directory('webs/test/', 'index.html')
# CSS
@app.route('/css/<path:filename>')
def fetchCSS(filename):
	return send_from_directory('webs/test/css/', filename)
	
# JavaScript
@app.route('/js/<path:filename>')
def fetchJS(filename):
	return send_from_directory('webs/test/js/', filename)
	
# Light queries.
@app.route('/resources/lights/<light_query>', methods=['GET'])
def lightQueries():
    return rh.lightQuery(request.get_json(light_query))

# Get light state.
@app.route('/resources/lights/state/<light_state_query>', methods=['GET'])
def stateQuery(light_state_query):
    return rh.stateQuery(request.get_json(light_state_query))
	
# Set light state.
@app.route('/resources/lights/state/<light_state_query>', methods=['POST'])
def stateUpdate(light_state_query):
    return rh.lightUpdate(request.get_json(light_state_query))
	
if __name__ == '__main__':
    app.run(debug=True)