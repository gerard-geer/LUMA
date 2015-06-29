#module: luma.py

from threading import Lock, Thread, Timer
from lumajson import *
from light import Light
from colorchannel import ColorChannel
from time import sleep

# from Adafruit_PWM_Servo_Driver import PWM

SANITIZE_ERR = {'type': 'error',
				'message': 'Request failed sanitation.',
				'data': None}

class LUMA(object):
	"""
	The LUMA device class. This manages all lighting instances; loading and
	saving their state from and to file, and updating them in their own thread.
	
	Slots:
		name (String): The name of this client.
		lights (Dictionary): A dictionary of all Light instances. Mapped as:
			Light.name -> Light
		file (String): The most recent filename used as the lighting state JSON
		file.
		pwm (Adafruit PWM): The PWM instance used to control the PCA9685.
		thread (Thread): The update loop thread.
		lightLock (Lock): The lock object used to secure exclusive 
		access to the Lights.
		runLock (Lock): The lock object used to secure exclusive
		access to the running variable.
		running (Boolean): The update loop continue flag.
	"""
	__slots__ = ('name', 'lights', 'file', 'pwm', 'updateThread', 'lightLock',\
				'runLock', 'running')
	
	def __init__(self, filename):
		"""
		Initializes this LUMA instance.
		
		Parameters:
			filename (String): The name of the lighting state JSON file.
			
		Returns:
			None.
			
		Preconditions:
			None.
			
		Postconditions:
			None.
		"""
		self.name = 'default_client_name'
		self.file = filename
		self.running = False
	
		# Create the PWM instance, and set the frequency to 10kHz.
		# self.pwm = PWM()
		# self.pwm.setPWMFreq(10000.0)
		
		# Create the lock object.
		self.lightLock = Lock()
		self.runLock = Lock()
		
	def load(self):
		"""
		Loads lighting state from file.
		
		Parameters:
			filename (String): The name of the lighting state JSON file.
			
		Returns:
			None.
			
		Preconditions:
			The file is good.
			
		Postconditions:
			The file is temporarily opened and closed, and the state it contains
			is loaded.
		"""
		# We don't know if the json is a single line or not, so we go through
		# potentially multiple lines in reading the file.
		s = ''
		f = open(self.file, 'r')
		for line in f:
			s+=line
		# Close the file.
		f.close()
		
		self.lightLock.acquire(True)
		self.name, self.lights = decodeState(s)
		self.lightLock.release()
		
	def save(self):
		"""
		Saves the lighting state to file.
		
		Parameters:
			None.
			
		Returns:
			None.
			
		Preconditions:
			None.
			
		Postconditions:
			The current state of this client is saved.
		"""
		self.lightLock.acquire(True)
		s = encodeState(self.name, self.lights)
		self.lightLock.release()
		f = open(self.file, 'w')
		f.write(s)
		f.close()
		
	def _isRunning(self):
		"""
		A thread safe way to check if the update loop continue flag is still
		set to "Go!".
		
		Parameters:
			None.
			
		Returns:
			None.
			
		Preconditions:
			None.
			
		Postconditions:
			None.
		"""
		self.runLock.acquire(True)
		r = self.running
		self.runLock.release()
		return r
		
	def start(self):
		"""
		Starts the update loop.
		
		Parameters:
			None.
			
		Returns:
			None.
			
		Preconditions:
			None.
			
		Postconditions:
			None.
		"""
		self.updateThread = Thread(target=self._updateLoop,\
		name='LUMA CLIENT UPDATE THREAD')
		if not self._isRunning():
			self.runLock.acquire(True)
			self.running = True
			self.runLock.release()
			self.updateThread.start()
			
	def stop(self):
		"""
		Terminates the update loop.
		
		Parameters:
			None.
			
		Returns:
			None.
			
		Preconditions:
			None.
			
		Postconditions:
			None.
		"""
		if self.updateThread and self._isRunning():
			self.runLock.acquire(True)
			self.running = False
			self.runLock.release()
			
	def _exists(self, lightID):
		"""
		A thread safe way to check if a light is present.
		
		Parameters:
			lightID (String): The ID of the Light to question.
			
		Returns:
			Whether or not the Light is present.
			
		Preconditions:
			None.
			
		Postconditions:
			None.
		"""
		self.lightLock.acquire(True)
		e = ( lightID in self.lights.keys() )
		self.lightLock.release()
		return e
	
	def _getLight(self, lightID=None):
		"""
		A thread safe way to get one or all lights.
		
		Parameters:
			lightID (String, default=None): The ID of the Light to get. If
			omitted, a list of copies of all lights are returned.
			
		Returns:
			Either a copy of the requested Light or a list of copies of
			all Lights.
			
		Preconditions:
			If specified the Light must be present.
			
		Postconditions:
			Copies are made of one or all Lights.
		"""
		
		# Return all lights if the ID given is None.
		if lightID == None:
			l = []
			self.lightLock.acquire(True)
			for light in self.lights.values():
				l.append(light)
			self.lightLock.release()
			return l
		
		# Otherwise we return the specific light.
		self.lightLock.acquire(True)
		l = self.lights[lightID]
		self.lightLock.release()
		return l
		
		
	def _changeLight(self, id, rtimes, rvals, gtimes, gvals, btimes, bvals):
		"""
		Change the state of a Light instance by ID.
		
		Parameters:
			id (String): The ID of the light to change.
			rtimes (List): The list of transition durations for the red channel.
			rvals (List): The list of brightness values for the red channel.
			gtimes (List): The list of transition durations for the 
			gvals (List): The list of brightness values for the green channel.
			green channel.
			btimes (List): The list of transition durations for the 
			bvals (List): The list of brightness values for the blue channel.
			blue channel.
			
		Returns:
			None.
		
		Preconditions:
			The Light exists.
			
		Postconditions:
			A lock is acquired to update each of the brightness curves and
			transition timings of the ColorChannels of the requested light.
		"""
		# Acquire the lock so that we can access the lights.
		self.lightLock.acquire(True)
		self.lights[id].change(rtimes, rvals, gtimes, gvals, btimes, bvals)
		self.lightLock.release()
		
	def _updateLights(self):
		"""
		Updates the lighting state of each Light.
		
		Parameters:
			None.
		
		Returns:
			None.
			
		Preconditions:
			None.
			
		Postconditions:
			A lock is acquired to block on updating the lighting state of each
			Light then release.
		"""
		self.lightLock.acquire(True)
		for i in self.lights.values():
			i.update('')#self.pwm)
		self.lightLock.release()
			
	def _updateLoop(self):
		"""
		The main lighting update loop. If no lock is present on the Lights,
		it spawns a Timer to update the light.
		
		Parameters:
			None.
			
		Returns:
			None.
			
		Preconditions:
			None.
			
		Postconditions:
			None.
		"""
		while self._isRunning():
			# Acquire the lock, since we don't want to spawn a new update thread
			# when the lights are being accessed. This would cause Timers to
			# compete over the lights and would lead to less consistent updates.
			if self.lightLock.acquire(False):
				# Create a timer to update the lights 1/100th of a second into the
				# future.
				t = Timer(.0, self._updateLights)
				# Release the lock.
				self.lightLock.release()
				# Start the timer.
				t.start()
			# Have the update thread sleep.
			sleep(.001)
			
	def _inspectDiff(self, req):
		"""
		Upon a change request one should inspect the changes being made.
		This function takes the request, the current state of the light
		to be changed, and prints the changes.
		
		Parameters:
			req (JSON): The dictionary containing the change request.
		
		Returns:
			None.
			
		Preconditions:
			The request must be a change request, and the change request
			changes a light that exists.
			
		Postconditions:
			The elements to be changed are logged to output.
		"""
		print('Items changed:')
		changed = req['data']
		current = self._getLight(changed['id'])
		
		# Test the red channel. Overflowing the light's lists doesn't matter
		# since they're FloatLists and circular.
		for i in range(len(changed['r_v'])):
			if(changed['r_v'][i] != current.r.vals[i]):
				print('Red values.')
				break
		for i in range(len(changed['r_t'])):
			if(changed['r_t'][i] != current.r.times[i]):
				print('Red timings.')
				break
				
		# Now for the green channel.
		for i in range(len(changed['r_v'])):
			if(changed['g_v'][i] != current.g.vals[i]):
				print('Green values.')
				break
		for i in range(len(changed['r_t'])):
			if(changed['g_t'][i] != current.g.times[i]):
				print('Green timings.')
				break
				
		# And the blue.
		for i in range(len(changed['r_v'])):
			if(changed['b_v'][i] != current.b.vals[i]):
				print('Blue values.')
				break
		for i in range(len(changed['r_t'])):
			if(changed['b_t'][i] != current.b.times[i]):
				print('Blue timings.')
				break
			
	def _onStatusRequest(self, req):
		"""
		Defines behaviour when given a status request.
		
		Parameters:
			req (Dictionary): The decoded request Dictionary.
			
		Returns:
			A JSON String encoding the response to this request.
			
		Preconditions:
			The request is valid.
			
		Postconditions:
			None.
		"""
		# Log some info. 
		print('for light id='+req['data'])
		
		# If the light name is None, then all lights are sought.
		if req['data'] == None:
			return encodeResponse('status', self._getLight(),	\
			'Status returned.')
		
		# OH MAN WHOA GET GOT A ID THAT MATCHES LET'S DO OUR BEST!
		if self._exists(req['data']):
			return encodeResponse('status', self._getLight(req['data']),	\
			'Status returned.')
		
		# If data does contains a name but that name does not exist, then we
		# have to return an error.
		else:
			return encodeResponse('error', None,	\
			'Light '+str(req['data'])+' does not exist on client '+\
			str(self.name))
		
	def _onChangeRequest(self, req):
		"""
		Defines behaviour when given a status request.
		
		Parameters:
			req (Dictionary): The decoded request Dictionary.
			
		Returns:
			A JSON String encoding the response to this request.
			
		Preconditions:
			The request is valid.
			
		Postconditions:
			None.
		"""
		# Similarly log some info.
		print(	'for light id='+str(req['data']['id'])+	\
				' name='+str(req['data']['name'])+		\
				'('+str(type(req['data']['name']))+')'	)

		# OH MAN THIS LIGHT UPDATE MATCHES ONE OF MY LIGHTS I'M SO HAPPY
		if self._exists(req['data']['id']):
			
			# Print the differential.
			self._inspectDiff(req)
			
			# Change the light.
			self._changeLight( req['data']['id'], \
			req['data']['r_t'], req['data']['r_v'],	\
			req['data']['g_t'], req['data']['g_v'],	\
			req['data']['b_t'], req['data']['b_v'] )
			
			# Return a response to this request.
			return encodeResponse('success',\
					self._getLight(req['data']['id']),\
					'State updated.')
			
		# Whelp the requested Light off and skedaddled.
		else:
			return encodeResponse('error', None,	\
			'Light '+str(req['data']['id'])+' does not exist on client '+	\
			str(self.name))
		
	def onRequest(self, s):
		"""
		Acts upon a request.
		
		Parameters:
			s (String): The request still an encoded JSON String.
			
		Returns:
			A JSON String for direct response.
			
		Preconditions:
			None.
			
		Postconditions:
			If the command was valid, it was obeyed.
		"""
		# Create a String to build our response in.
		res = ''
		
		# Try to decode the request.
		try:
			r = decodeRequest(s)
		except Exception as e:
			return encodeResponse('error', None, 'Request sent to '+
				'client '+str(self.name)+' could not be decoded. Error: '+str(e))
				
		# Sanitize the request.
		e = sanitizeRequest(r)
		if e != None:
			print('Request Failed sanitization. Error: '+e)
			return encodeResponse('error', None, 'Request sent to '+
				'client '+str(self.name)+' failed sanitation. Error: '+str(e))
		
		# Log the request type.
		print('Request type: '+r['type'])
				
		# Act appropriately for the request.
		if r['type'] == 'status':
			return self._onStatusRequest(r)
		elif r['type'] == 'change':
			return self._onChangeRequest(r)
		else:
			return encodeResponse('error', None, 'Invalid request type sent to '+
				'client '+str(self.name)+'.')