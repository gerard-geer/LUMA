from flask import Flask
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
	return indexPage
# CSS
@app.route('/css/<path:filename>')
def fetchCSS():
	return app.send_static_file(filename)
	
# JavaScript
@app.route('/js/<path:filename>')
def fetchJS():
	return app.send_static_file(filename)
	
# Light queries.
@app.route('/resources/lights', methods=['GET'])
def lightQueries():
    return rh.lightQuery(request.get_json())

# Get light state.
@app.route('/resources/lights/state', methods=['GET'])
def stateQuery():
    return rh.stateQuery(request.get_json())
	
# Set light state.
@app.route('/resources/lights/state', methods=['POST'])
def stateUpdate():
    return rh.lightUpdate(request.get_json())
	
if __name__ == '__main__':
    app.run()