import os

class ExternalFiles:
	'''
		The ExternalFiles class is used to handle working with both externalizing files, 
		as well as ingesting files that were previously externalized. This helps
		to minimize the amount of manual work that might need to otherise be used
		for handling external files. 
	'''
	def __init__(self, my_op):
		'''
			Stands in place of an execute dat - ensures all elements start-up correctly

			Notes
			---------

			Args
			---------
			myOp (touchDesignerOperator):
			> the operator that is loading the current extension
					
			Returns
			---------
			none		
		'''

		self.my_op 				= my_op
		self.Flash_duration 	= 10

		init_msg 				= "Save init from {}".format(my_op)
		self.Defaultcolor		= parent().pars('Defaultcolor*')
		self.Op_finder 			= op('opfind1')

		print(init_msg)

		return
	
	@property
	def get_current_location(self):
		return ui.panes.current.owner

	def Prompt_to_save(self):
		'''
			The method used to save an external TOX to file

			Notes
			---------

			Args
			---------
			current_loc (str):
			> the operator that's related to the currently focused 
			> pane object. This is required to ensure that we correctly
			> grab the appropriate COMP and check to see if needs to be saved
					
			Returns
			---------
			none		
		'''
		current_loc = self.get_current_location

		ext_color 						= parent().pars("Extcolor*")
		msg_box_title 					= "TOX Save"
		msg_box_msg 					= "Replacing External\n\nYou are about to overwrite an exnteral TOX"
		msg_box_buttons 				= ["Cancel", "Continue"]

		sav_msg_box_title 				= "Externalize Tox"
		sav_msg_box_msg 				= "This TOX is not yet externalized\n\nWould you like to externalize this TOX?"
		sav_msg_box_buttons 			= ["No", "Yes"]

		save_msg_buttons_parent_too 	= ["No", "This COMP Only", "This COMP and the Parent"]


		# check if location is the root of the project 
		if current_loc == '/':
			# skip if we're at the root of the project
			pass

		else:
			# if we're not at the root of the project 
			
			# check if external
			if current_loc.par.externaltox != '':
				confirmation 				=  ui.messageBox(msg_box_title, msg_box_msg, buttons = msg_box_buttons)

				if confirmation:

					# save external file
					self.Save_over_tox(current_loc)
				
				else:
					# if the user presses "cancel" we pass
					pass
			
			# in this case we are not external, so let's ask if we want to externalize the file
			else:

				# check if the parent is externalized
				if current_loc.parent().par.externaltox != '':
					save_ext = ui.messageBox(sav_msg_box_title, sav_msg_box_msg, 
					buttons = save_msg_buttons_parent_too)

					# save this comp only
					if save_ext == 1:
						self.Save_tox(current_loc)

					# save this comp and the parent
					elif save_ext == 2:
						self.Save_tox(current_loc)
						print("save this tox")

						# save parent() COMP
						self.Save_over_tox(current_loc.parent())
						print("Save the parent too!")

					# user selected 'No'
					else:
						pass

				# the parent is not external, so let's ask about externalizing the tox
				else:
					save_ext 			= ui.messageBox(sav_msg_box_title, sav_msg_box_msg, buttons = sav_msg_box_buttons)
					
					if save_ext:
						self.Save_tox(current_loc)

					else:
						# the user selected "No"
						pass

		
		return

	def Save_over_tox(self, current_loc):
		ext_color 				= parent().pars("Extcolor*")
		external_path 			= current_loc.par.externaltox

		# update custom pars
		self.update_version_pars(current_loc)

		#save tox
		current_loc.save(external_path)

		# set color for COMP
		current_loc.color 		= (ext_color[0], ext_color[1], ext_color[2])

		# flash color
		self.Flash_bg("Bgcolor")

		# set external file colors
		self.Set_external_file_colors()

		# create and print log message
		log_msg 		= "{} saved to {}/{}".format(current_loc, 
													project.folder, 
													external_path)
		
		self.Logtotextport(log_msg)

		return

	def Save_tox(self, current_loc):
		ext_color 		= parent().pars("Extcolor*")

		# ask user for a save location
		save_loc 		= ui.chooseFolder(title="TOX Location", start=project.folder)
		
		# construct a relative path and relative loaction for our elements
		print(save_loc)
		rel_path 		= tdu.collapsePath(save_loc)
		
		# check to see if the location is at the root of the project folder structure
		if rel_path == "$TOUCH":
			rel_loc 	= '{new_tox}/{new_tox}.tox'.format(new_tox = current_loc.name)
		
		# save path is not in the root of the project
		else:
			rel_loc 	= '{new_module}/{new_tox}/{new_tox}.tox'.format(new_module = rel_path, new_tox = current_loc.name)

		# create path and directory in the OS
		new_path 		= '{selected_path}/{new_module}'.format(selected_path = save_loc, new_module = current_loc.name)
		try:
			os.mkdir(new_path)
			valid_external_path = True
		except:
			self.alert_failed_dir_creation()
			valid_external_path = False

		if valid_external_path:
			# format our tox path
			tox_path 		= '{dir_path}/{tox}.tox'.format(dir_path = new_path, tox = current_loc.name)

			# setup our module correctly
			current_loc.par.externaltox 		= rel_loc
			current_loc.par.savebackup 			= False

			# set color for COMP
			current_loc.color 		= (ext_color[0], ext_color[1], ext_color[2])

			# setup about page
			self.custom_page_setup(current_loc)

			# save our tox
			current_loc.save(tox_path)

			# flash color
			self.Flash_bg("Bgcolor")

			# set external file colors
			self.Set_external_file_colors()

			# create and print log message
			log_msg 		= "{} saved to {}/{}".format(current_loc, 
														project.folder, 
														tox_path)
			self.Logtotextport(log_msg)
		else:
			pass

		return

	def alert_failed_dir_creation(self):
		op.TDResources.op('popDialog').Open(
			title="Failed to Save TOX",
			text='''It looks like there is an existing
TOX in this directory. 

Please check your to make sure
this TOX does not already exist.
''',
			buttons=["Okay"]
		)

	def update_custom_str_par(self, targetOp, par, value, par_label="Temp"):
		if targetOp.par[par] != None:
			targetOp.par[par] = value
		else:
			about_page = targetOp.appendCustomPage("About")
			about_page.appendStr(par, label=par_label)
			targetOp.par[par] = value
			targetOp.par[par].readOnly = True

	def update_version_pars(self, target_op):
		if target_op.par['Toxversion'] == None:
			self.update_custom_str_par(target_op, "Toxversion", "0.0.0", "Tox Version")
		else:
			version = target_op.par['Toxversion'].eval()
			digits = version.split('.')
			update_val = int(digits[2]) + 1
			digits[2] = str(update_val)
			new_version = ".".join(digits)
			self.update_custom_str_par(target_op, "Toxversion", new_version, "Tox Version")
		self.update_custom_str_par(target_op, "Tdversion", app.version, "TD Version")
		self.update_custom_str_par(target_op, "Tdbuild", app.build, "TD Build")		

	def custom_page_setup(self, target_op):
		self.update_custom_str_par(target_op, "Toxversion", "0.0.0", "Tox Version")
		self.update_custom_str_par(target_op, "Tdversion", app.version, "TD Version")
		self.update_custom_str_par(target_op, "Tdbuild", app.build, "TD Build")

	def Flash_bg(self, parColors):
		'''
			Used to flash the background of the TD network. 

			Notes
			---------
			This is a simple tool to flash indicator colors in the
			background to help you have some visual confirmation that
			you have in fact externalized a file.

			Args
			---------
			parColors (str):
			> this is the string name to match against the parent's pars()
			> for to pull colors to use for changing the background
					
			Returns
			---------
			none		
		'''
		par_color 			= '{}*'.format(parColors)
		over_ride_color 	= parent().pars(par_color)

		# change background color (0.1, 0.105, 0.12)
		ui.colors['worksheet.bg'] 	= over_ride_color
		delay_script 				= "ui.colors['worksheet.bg'] = args[0]"
		
		# want to change the background color back
		run(delay_script, self.Defaultcolor, delayFrames = self.Flash_duration)		

		return

	def Logtotextport(self, logMsg):
		if parent().par.Logtotextport:
			print(logMsg)
		else:
			pass
		return

	def find_all_dats(self):
		external_dats = []
		exclude_list = [
			'eval', 
			'keyboardin', 
			'opfind', 
			'folder', 
			'examine', 
			'select',
			'udpout',
			'udpin',
			'script',
			'null',
			'info']
		for eachOp in root.findChildren(type=DAT):
			if eachOp.type in exclude_list:
				pass
			
			else:
				if eachOp.par['file'] != '':
					external_dats.append(eachOp)
				else:
					pass
		return external_dats

	def Set_ext_tox_colors(self):
		externalChildren = self.find_external_ops()
		colors = [par.eval() for par in parent().pars('Extcolor*')]
		for eachOp in externalChildren:
			eachOp.color = (colors[0], colors[1], colors[2])
		pass

	def Set_external_file_colors(self):
		'''Sets colors for external files
		'''
		colors = [par.eval() for par in parent().pars('Filecolor*')]

		external_dats = self.find_all_dats()
		for eachDat in external_dats:
			eachDat.color = (colors[0], colors[1], colors[2])
		pass

	def find_external_ops(self):
		'''Returns a list of all external comps
		'''
		children = root.findChildren(type=COMP)
		external_ops = [eachChild for eachChild in children if eachChild.par.externaltox != '']
		return external_ops

	def Update_dirty_table(self):
		'''Updates table of dirty tox files
		'''
		op('table_dirty_ops').clear(keepFirstRow=True)
		children = root.findChildren(type=COMP)
		for each in children:
			if each.dirty:
				op('table_dirty_ops').appendRow([each.name, each.path])
		return children

	def Find_dirty_tox(self):
		'''Finds all dirty comps
		'''
		op('table_dirty_ops').clear(keepFirstRow=True)
		children = self.Update_dirty_table()

		if len(children) > 0:
			op('window1').par.winopen.pulse()

		else:
			return None

	def Open_network_location(self, network_location):
		''' Moves network to save location
		'''
		ui.panes.current.owner = network_location
		ui.panes.current.home()
		print(type(ui.panes.current))

	def Keyboard_input(self, shortcut):
		'''Keyboard input handler
		'''
		shortcut_lookup = {
			'ctrl.w' : self.Prompt_to_save,
			'ctrl.shift.w' : self.Find_dirty_tox
		}

		func = shortcut_lookup.get(shortcut)

		try:
			func()
		except Exception as e:
			print(e)