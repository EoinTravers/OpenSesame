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

class save_to_sd(item):

	"""
	This class (the class with the same name as the module) handles the basic
	functionality of the item. It does not deal with GUI stuff.
	"""

	# Provide an informative description for your plug-in.
	description = u'Save data to phone\'s memory'

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
		print eval(self.compile_cond(self._runif))
		if eval(self.compile_cond(self._runif)):
			print 'Saving to sd card'
			sdcard_folders = ['/sdcard/', '/mnt/sdcard/']
			for path in sdcard_folders:
				if os.path.isdir(path):
					break
			try:
				save_as = os.path.join(path, 'datafile.txt') 
				f = open(save, 'w')
				print 'Data saved as %s' % save_as
			except:
				print 'Failed to create %s' % path
				save_as = 'datafile.txt'
				f = open('datafile.txt', 'w')
				print 'Data saved as %s' % os.path.join(os.curdir, save_as)
			f.truncate()
			#f.write( 'log_list = ' + repr(data_list)+'\n')
			#f.write(repr(data_list)+'\n')
			data_list = self.experiment.log_list
			pickle.dump(data_list, f)
			f.close()
			self.experiment.set('data_saved', 1)

		
class qtsave_to_sd(save_to_sd, qtautoplugin):
	
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
		save_to_sd.__init__(self, name, experiment, script)
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
