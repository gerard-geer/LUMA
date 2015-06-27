#module: light.py

from colorchannel import ColorChannel
class Light(object):
	"""
	Encapsulates the red, green, and blue ColorChannels into a Light, with
	a name and ID field as a well.
	
	Slots:
		r (ColorChannel): The red ColorChannel.
		g (ColorChannel): The green ColorChannel.
		b (ColorChannel): The blue ColorChannel.
		name (String): The name of this Light.
		id (String): The ID number of this light.
	"""
	__slots__ = ('r', 'g', 'b', 'name', 'id')

	def __init__(self, r, g, b, name, id):
		"""
		Initializes this Light.
		
		Parameters:
			r (ColorChannel): The red ColorChannel.
			g (ColorChannel): The green ColorChannel.
			b (ColorChannel): The blue ColorChannel.
			name (String): The name of this Light.
			id (String): This light's ID.
		
		Returns:
			None.
			
		Preconditions:
			The ColorChannels must be properly initialized.
			
		Postconditions:
			None.
		"""
		self.r = r
		self.g = g
		self.b = b
		self.name = name
		self.id = id

	def update(self, pwm):
		"""
		Updates the three ColorChannels of this Light.
		
		*THIS FUNCTION MUST BE CALLED EVERY 100TH OF A SECOND. 100Hz.*

		Parameters:
			pwm (PWM): The global PWM instance used to control the external
			PWM controller over i2c.
			
		Returns:
			None.
		
		Preconditions:
			The PWM instance is kosher and ready to be used.
			
		Postconditions:
			All three ColorChannels are updated to their next value.
		"""
		self.r.update(pwm)
		self.g.update(pwm)
		self.b.update(pwm)

	def change(self, rtimes, rvals, gtimes, gvals, btimes, bvals):
		"""
		Update the transition timings and brightness values of each ColorChannel
		of this Light.
		
		Parameters:
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
			None.
			
		Postconditions:
			The ColorChannels of this Light walk away with different brightness
			curves and transition timings.
		"""
		self.r.change(rtimes, rvals)
		self.g.change(gtimes, gvals)
		self.b.change(btimes, bvals)
