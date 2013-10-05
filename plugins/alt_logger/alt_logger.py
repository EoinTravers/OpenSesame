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
from libqtopensesame.items.qtautoplugin import qtautoplugin
from libqtopensesame.items import qtitem
from openexp.canvas import canvas
from PyQt4 import QtCore, QtGui
from libqtopensesame.misc import _
from libopensesame import exceptions, debug

class alt_logger(item):

	"""
	This class (the class with the same name as the module) handles the basic
	functionality of the item. It does not deal with GUI stuff.
	"""

	# Provide an informative description for your plug-in.
	description = u'A plug-in to record data in a more Python-compatible way.'

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
		#self._log_all = u'yes' # yes = checked, no = unchecked
		self._vars_string = u''
		self.ignore_missing = u'yes'
		self.auto_log = u'yes'
		self.logvars = []
		# Then call the parent constructor
		item.__init__(self, name, experiment, script)

	def run(self):

		"""The run phase of the plug-in goes here."""
		if self.get(u'auto_log') == u'yes':
			# Log everything
			self.logvars = []
			for logvar, val, item in self.experiment.var_list():
				if (self.has(logvar) or self.get(u'ignore_missing') == u'yes') and logvar not in self.logvars:
					self.logvars.append(logvar)
					debug.msg(u'auto-logging "%s"' % logvar)
		else:
			# Parse variable to log from user input (stopgap function, until
			# proper UI can be used.
			self.logvars = self._vars_string.strip(' ').split(',')
			
		trial_data = dict()
		for var in self.logvars:
			try:
				val = self.experiment.get(var)
			except exceptions.runtime_error as e:
				if self.get(u'ignore_missing') == u'yes':
					val = u'NA'
				else:
					raise exceptions.runtime_error( \
						u"Logger '%s' tries to log the variable '%s', but this variable is not available. Please deselect '%s' in logger '%s' or enable the 'Use NA for variables that have not been set' option." \
						% (self.name, var, var, self.name))
			trial_data[var] = val

		self.experiment.log_list.append(trial_data)
			

class qtalt_logger(alt_logger, qtautoplugin):
	
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
		alt_logger.__init__(self, name, experiment, script)
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
		self.checkbox_log_all.stateChanged.connect( \
			self.line_vars_string.setDisabled)


