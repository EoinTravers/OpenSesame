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

from libopensesame import item
from libqtopensesame.items.qtautoplugin import qtautoplugin
from openexp.canvas import canvas
from PyQt4 import QtCore, QtGui
from libqtopensesame.misc import _

from libopensesame import logger
from libqtopensesame.items import qtitem
from libqtopensesame.items import logger as qtlogger


class alt_logger(item.item):

	"""
	This class (the class with the same name as the module) handles the basic
	functionality of the item. It does not deal with GUI stuff.
	"""

	# Provide an informative description for your plug-in.
	description = u'A plug-in to record data in a more Python-compatible way.'

	def __init__(self, name, experiment, string=None):

		"""
		Constructor.
		
		Arguments:
		name		--	The name of the item.
		experiment 	--	The experiment.

		Keyword arguments:
		string		--	An item definition string (default=None).
		"""

		self.logvars = []
		self.log_started = False
		self.use_quotes = u'yes'
		self.auto_log = u'yes'
		self.ignore_missing = u'yes' # This means that missing variables should
									# be ignored in the sense that they are
									# assigned the value 'NA'. They are included
									# in the logfile.
		item.item.__init__(self, name, experiment, string)
		
	def run(self):

		"""Log the selected variables"""

		if not self.log_started:
			self.log_started = True
			# If auto logging is enabled, collect all variables
			if self.get(u'auto_log') == u'yes':
				self.logvars = []
				for logvar, val, item in self.experiment.var_list():
					if (self.has(logvar) or self.get(u'ignore_missing') == \
						u'yes') and logvar not in self.logvars:
						self.logvars.append(logvar)
						debug.msg(u'auto-logging "%s" foo' % logvar)
			# Sort the logvars to ascertain a consistent ordering
			self.logvars.sort()
			# Draw the first line with variables
			#self.log(u','.join(self.logvars))

		l = []
		for var in self.logvars:
			try:
				val = self.unistr(self.get(var))
			except exceptions.runtime_error as e:
				if self.get(u'ignore_missing') == u'yes':
					val = u'NA'
				else:
					raise exceptions.runtime_error( \
						u"Logger '%s' tries to log the variable '%s', but this variable is not available. Please deselect '%s' in logger '%s' or enable the 'Use NA for variables that have not been set' option." \
						% (self.name, var, var, self.name))
			l.append(val)

		trial_log = dict()
		for i in range(len(self.logvars)):
			label = str(self.logvars[i])
			value = l[i]
			trial_log[label] = value
		self.experiment.log_list.append(trial_log)

class qtalt_logger(alt_logger, qtlogger.logger):
	
	"""
	This class handles the GUI aspect of the plug-in. By using qtautoplugin, we
	usually need to do hardly anything, because the GUI is defined in info.json.
	"""

	def __init__(self, name, experiment, string = None):

		"""
		Constructor

		Arguments:
		name -- the name of the item
		experiment -- the experiment

		Keyword arguments:
		string -- the definition string for the item (default = None)
		"""

		alt_logger.__init__(self, name, experiment, string)
		qtitem.qtitem.__init__(self)


