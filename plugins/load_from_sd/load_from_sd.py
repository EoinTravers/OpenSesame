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
from libopensesame import debug
from libqtopensesame.items.qtautoplugin import qtautoplugin
from openexp.canvas import canvas
from openexp.mouse import mouse
import urllib
import os
try:
    import android
except ImportError:
    android = None
import pickle
   

class LoadError(Exception):
    pass

class load_from_sd(item):

	"""
	This class (the class with the same name as the module) handles the basic
	functionality of the item. It does not deal with GUI stuff.
	"""

	# Provide an informative description for your plug-in.
	description = u'Loads saved results from the phone\'s memory'

	def __init__(self, name, experiment, script=None):

		"""
		Constructor.
		
		Arguments:
		name		--	The name of the plug-in.
		experiment	--	The experiment object.
		
		Keyword arguments:
		script		--	A definition script. (default=None)
		"""
		self._runif = u'always'
		item.__init__(self, name, experiment, script)

	def run(self):
		# Run this now?
		# TODO: See issue on line 80 of /plugins/send_to_server/send_to_server.py
		if eval(self.compile_cond(self._runif)):
			print 'Loading from sd card'
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
			else:
				print 'No data found on sd card'
				debug.msg('No data found on sd card')
				self.experiment.set('data_loaded', 0)
				return False
			print 'Loading data from %s' % data_path
			try:
				f = open(data_path)
				data_list = pickle.load(f)
				f.close()
				self.experiment.set('data_loaded', 1)
				for trial in data_list:
					self.experiment.log_list.append(trial)
				print 'Data loaded from sd card (%i trials)' % len(data_list)
				debug.msg('Data loaded from sd card (%i trials)' % len(data_list))
			except:
				debug.msg('Error occured while loading data. Skipping...')
				self.experiment.set('data_loaded', 0)
			return True
	
		
class qtload_from_sd(load_from_sd, qtautoplugin):
	
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
		load_from_sd.__init__(self, name, experiment, script)
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
