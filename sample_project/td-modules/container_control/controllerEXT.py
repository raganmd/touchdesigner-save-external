class MyController:

	def __init__(self, my_op):
	
		self.Myop 		= my_op

		log_msg 		= 'MyController init from op({})'.format(my_op)
		print(log_msg)

		return