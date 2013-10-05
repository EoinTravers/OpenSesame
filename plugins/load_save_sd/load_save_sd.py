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

class load_save_sd(item):

	"""
	This class (the class with the same name as the module) handles the basic
	functionality of the item. It does not deal with GUI stuff.
	"""

	# Provide an informative description for your plug-in.
	description = u'Load/save data from/to phone\'s memory'

	def __init__(self, name, experiment, script=None):

		"""
		Constructor.
		
		Arguments:
		name		--	The name of the plug-in.
		experiment	--	The experiment object.
		
		Keyword arguments:
		script		--	A definition script. (default=None)
		"""

		self._mode = u'Save'
		self._skip = u'yes'
		# Then call the parent constructor
		item.__init__(self, name, experiment, script)

	def save_data(self, data_list):
		sdcard_folders = ['/sdcard/', '/mnt/sdcard/']
		for path in sdcard_folders:
			if os.path.isdir(path):
				break
		try:
			f = open(os.path.join(path, 'datafile.txt'), 'w')
		except:
			print 'Failed to create %s' % path
			f = open('datafile.txt', 'w')
		f.truncate()
		#f.write( 'log_list = ' + repr(data_list)+'\n')
		#f.write(repr(data_list)+'\n')
		pickle.dump(data_list, f)
		f.close()
	
	def load_data(self):
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
			if self._skip == 'no':
				raise LoadError("Data not found")
			self.experiment.set('data_found', False)
			return False
		#data_list = execfile(data_path)
		f = open(data_path)
		data_list = pickle.load(f)
		f.close()
		self.experiment.set('data_found', True)
		for trial in data_list:
			self.experiment.log_list.append(trial)
		return True


	def run(self):

		"""The run phase of the plug-in goes here."""

		if self._mode == 'Save':
			self.save_data(self.experiment.log_list)
		elif self._mode == 'Load':
			self.load_data()
		
class qtload_save_sd(load_save_sd, qtautoplugin):
	
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
		load_save_sd.__init__(self, name, experiment, script)
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
