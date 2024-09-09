class par_helper:
	'''A generalized parameter helper for simple par callbacks
 
	The intention of this extension is to provide a slim interface
	for easily scritable actions intended to be connected to custom
	changes. The model assumes that the developer would like to 
	call a scriptable action whose function name matches the parameter
	name.
	'''
	def __init__(self, my_op, actionsMOD, debug=False):
		self.My_op = my_op
		self.actions = actionsMOD
		self.Debug = debug
 
	def Par_functions(self, par):
		'''Attempts to match parameters to appropriatly scoped
		functions.
		'''
		if par.isPulse:
			self.pulse_function(par)
		
		elif len(par.tuplet) > 1:
			self.tuplet_function(par)
		
		else:
			self.general_function(par)
 
	def pulse_function(self, par):
		'''Pulse functions are only one frame long, and are
		considered "instant" to touchdesigner. They do not offer
		any additional information, they're only an event.
		'''
		try:
			func = getattr(self.actions, par.name)
			func()
		except Exception as e:
			if self.Debug:
				debug(e)
				print("This par has no matching function")
 
	def tuplet_function(self, par):
		'''TouchDesigner tuplets have a slight variation
		in their parameter pattern. An RGB parameter, for example
		will have r g and b appended to the end of the user's
		descriptive parameter name. A tuplet_function allows us
		to target by Tuplet name, retrieving all pars in the tuplet.
		'''
		try:
			func = getattr(self.actions, par.tupletName)
			func(par.tuplet, par)
		except Exception as e:
			if self.Debug:
				debug(e)
				print("This par has no matching function")
 
	def general_function(self, par):
		'''Other TouchDesigner parameters follow a consistent enough
		pattern, that we safely map the parameter name and argument
		to a set of provided actions.
		'''
		try:
			func = getattr(self.actions, par.name)
			func(par)
		except Exception as e:
			if self.Debug:
				debug(e)
				print("This par has no matching function")