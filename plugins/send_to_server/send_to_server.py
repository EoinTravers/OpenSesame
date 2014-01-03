#-*- coding:utf-8 -*-

"""
This file is part of OpenSesame.

OpenSesame is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

OpenSesame is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with OpenSesame.  If not, see <http://www.gnu.org/licenses/>.
"""

from libopensesame.item import item
from libopensesame import debug, widgets
from libqtopensesame.items.qtautoplugin import qtautoplugin
from openexp.canvas import canvas
from openexp.mouse import mouse
import urllib
import os

class send_to_server(item):

	"""
	This class (the class with the same name as the module) handles the basic
	functionality of the item. It does not deal with GUI stuff.
	"""

	# Provide an informative description for your plug-in.
	description = u'An example new-style plug-in'

	def __init__(self, name, experiment, script=None):

		"""
		Constructor.
		
		Arguments:
		name		--	The name of the plug-in.
		experiment	--	The experiment object.
		
		Keyword arguments:
		script		--	A definition script. (default=None)
		"""

		# Here we provide default values for the variables that are specified
		# in info.json. If you do not provide default values, the plug-in will
		# work, but the variables will be undefined when they are not explicitly
		# set in the GUI.
		self._runif = u'always'
		self._address = u''
		# UI
		self._question = u'Submit data now?'
		self._yes = u'Yes'
		self._no = u'No'
		#self._variable = u'menu_choice'
		# Then call the parent constructor
		item.__init__(self, name, experiment, script)

	def prepare(self):

		"""The preparation phase of the plug-in goes here."""

		# Call the parent constructor.
		item.prepare(self)
		# User input
		self.responses = [self._yes, self._no]
		self.rows = [2] + [1]*len(self.responses)
		self.m = mouse(self.experiment)
		self.c = canvas(self.experiment)

		
	def run(self):
		# Check if we should run this at all
		# TODO: For some reason, this works fine, as
		# [data_loaded]
		# [data_loaded] = 1
		# , etc, but not
		# [data_loaded] = true, or '= True', or '== true', or '== True'.
		print self._runif
		print self.compile_cond(self._runif)
		if eval(self.compile_cond(self._runif)):
			# Run the itemf
			# User input
			form = widgets.form(self.experiment, cols=[1,5,1], rows=self.rows, margins=[32,32,32,32])
			label_title = widgets.label(form, text=self._question)
			form.set_widget(label_title, (0,0), colspan=3)
			for i in range(len(self.responses)):
				resp = self.responses[i]
				button = widgets.button(form, text=resp)
				form.set_widget(button, (1, i+1))
			button_clicked = form._exec()
			# Check input
			if button_clicked == self._yes:
				# Send data
				data = self.experiment.log_list
				self.c.clear()
				self.c.text('Connecting to server...')
				self.c.show()
				
				# Try to open the connection
				#address = 'http://cogsci.nl/etravers/androidsql.php'
				address = self._address
				try:
					page = urllib.urlopen(address)#, data='position=OpeningConnection')
					page.close()
					# Connection works. Send data.
					debug.msg('Connection to server  at %s succesful...' % address)
					t = 0
					for trial in data:
						progress = int(float(t)/len(data)*680)
						#print t, len(data), progress
						self.c.clear()
						self.c.text('Sending...')
						self.c.rect(300, 600, 680, 72, False, 'grey')
						self.c.rect(303, 601, progress, 70, True, 'red')
						self.c.show()
						encode_data = urllib.urlencode(trial)
						debug.msg(encode_data)
						for i in range(5):
							# Try to send data 5 times.
							try:
								page = urllib.urlopen(address, encode_data)
								page.close()
								print 'Sent!', t
							except IOError as e:
									print str(e)
							else:
								break
						t += 1
					result = 'Data sent!'
					self.experiment.set('data_sent', 1)
					# Delete sent datafile
					# Find the saved data
					sdcard_folders = ['/sdcard/', '/mnt/sdcard/']
					for path in sdcard_folders:
						if os.path.isdir(path):
							print path
							break
					if os.path.exists(os.path.join(path, 'datafile.txt')):
						data_path = os.path.join(path, 'datafile.txt')
					elif os.path.exists('datafile.txt'):
						data_path = 'datafile.txt'
					# Delete it
					if os.path.isfile(data_path):
						os.remove(data_path)
				except IOError as e:
					result = 'Unable to connect.\nPlease try again when connected to the internet.'
					print str(e)
					self.experiment.set('data_sent', 0)
				debug.msg(result)
				self.c.clear()
				self.c.text(result)
				self.c.text('Tap to continue.', y = 500)
				self.c.show()
				self.m.get_click()
			else:
				# Don't send data
				self.experiment.set('data_sent', 0)
		
class qtsend_to_server(send_to_server, qtautoplugin):
	
	"""
	This class handles the GUI aspect of the plug-in. By using qtautoplugin, we
	usually need to do hardly anything, because the GUI is defined in info.json.
	"""

	def __init__(self, name, experiment, script=None):

		"""
		Constructor.
		
		Arguments:
		name		--	The name of the plug-in.
		experiment	--	The experiment object.
		
		Keyword arguments:
		script		--	A definition script. (default=None)
		"""

		# We don't need to do anything here, except call the parent
		# constructors.
		send_to_server.__init__(self, name, experiment, script)
		qtautoplugin.__init__(self, __file__)

	def init_edit_widget(self):

		"""
		Constructs the GUI controls. Usually, you can omit this function
		altogether, but if you want to implement more advanced functionality,
		such as controls that are grayed out under certain conditions, you need
		to implement this here.
		"""

		# First, call the parent constructor, which constructs the GUI controls
		# based on info.json.
		qtautoplugin.init_edit_widget(self)
		# If you specify a 'name' for a control in info.json, this control will
		# be available self.[name]. The type of the object depends on the
		# control. A checkbox will be a QCheckBox, a line_edit will be a
		# QLineEdit. Here we connect the stateChanged signal of the QCheckBox,
		# to the setEnabled() slot of the QLineEdit. This has the effect of
		# disabling the QLineEdit when the QCheckBox is uncheckhed.
		#self.checkbox_widget.stateChanged.connect( \
		#	self.line_edit_widget.setEnabled)
		pass


