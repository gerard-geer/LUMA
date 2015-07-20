#module: colorchannel.py
# LUMA copyright (C) Gerard Geer 2014-2015

from floatlist import FloatList
# from Adafruit_PWM_Servo_Driver import PWM

class ColorChannel(object):
	"""
	Represents a single channel of a lighting instance.
	
	Slots:
		times (FloatList):The durations of the transitions between brightness 
		levels. (In hundredths of a second.)
		vals (FloatList): The brightness levels of the channel over time.
		cur (Float): The current index into the timing and value lists.
		chan (Integer): The PWM channel to which this color channel is assigned.
	"""
	__slots__ = ('times', 'vals', 'cur', 'chan')
	
	def __init__(self, timings, values, channel):
		"""
		Initializes this ColorChannel.
		
		Parameters:
			timings (List): A list of the durations of the transitions between
			brightnesses in the brightness values list.
			vals (List): A list of the brightness levels of this color channel
			over time.
			channel (Integer): The PWM channel that this ColorChannel is
			assigned to.
			
		Returns:
			None.
			
		Preconditions:
			The timings list must store durations in hundredths of a second.
			
		Postconditions:
			Two FloatLists are created.
		"""
		# Create a FloatList to store the timing values, but we disable
		# interpolation for consistent samples per index.
		self.times = FloatList(timings, False)
		# Create another FloatList to store the lighting levels.
		self.vals = FloatList(values)
		
		self.chan = channel
		self.cur = 0.0
		
	def clone(self):
		"""
		Returns a copy of this ColorChannel.
		
		Parameters:
			None.
		
		Returns:
			A copy of this ColorChannel.
			
		Preconditions:
			None.
			
		Postconditions:
			None.
		"""
		fresh = ColorChannel(self.times.aslist(), self.vals.aslist(), self.chan)
		fresh.cur = self.cur
		return fresh
		
	def update(self, pwm):
		"""
		Performs a per-"frame" update of the lighting channel, by incrementing
		its current index and setting the assigned PWM channel to the new 
		brightness pulled from the brightness list.
		
		*THIS FUNCTION MUST BE CALLED EVERY 1/100th OF A SECOND. 100Hz!*
		
		Parameters:
			pwm (PWM instance): The global PWM instance used to control the 
			PCA9685 over i2c.
			
		Returns:
			None.
			
		Preconditions:
			This function is registered to be called at 100Hz.
		
		Postconditions:
			The PWM channel is set to the current brightness level.
		"""
		# Pull a value out of the timings array.
		self.cur += 1.0/self.times[self.cur]
		# pwm.setPWM(self.chan, 0, 4096*self.vals[self.cur])
		
	def change(self, timings, values):
		"""
		Updates the brightness values and transition timings of this
		ColorChannel.
		
		Parameters:
			timings(List): The new transition timings.
			values(List): The new brightness values.
			
		Returns:
			None.
			
		Preconditions:
			None.
		
		Postconditions:
			The brightness values and transition timings of this ColorChannel
			are updated.
		"""
		self.times = FloatList(timings, False)
		self.vals = FloatList(values)
	
	def getMaximumD1(self):
		"""
		Returns the maximum rate of change for this color channel.
		
		Parameters:
			None.
		
		Returns:
			the maximum rate of change for this color channel.
		
		Preconditions:
			None.
		
		Postconditions:
			None.
		"""
		maxRate = 0
		for i in range(len(self.vals)):
			# We have to account for zero-length times.
			rate = ( self.vals[i+1]-self.vals[i] ) / (self.times[i]+.0001)
			# Update the maximum rate should we need to.
			maxRate = max(rate, maxRate)
				
		return maxRate
