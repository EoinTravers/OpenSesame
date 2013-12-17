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
from libopensesame import widgets
from libqtopensesame.items.qtautoplugin import qtautoplugin
from openexp.canvas import canvas

# TODO: Facilitate more than 2 response options

class mobile_menu(item):

	"""
	This class (the class with the same name as the module) handles the basic
	functionality of the item. It does not deal with GUI stuff.
	"""

	# Provide an informative description for your plug-in.
	description = u'Simple plug-in for multiple choice on touchscreens.'

	def __init__(self, name, experiment, script=None):

		"""
		Constructor.
		
		Arguments:
		name		--	The name of the plug-in.
		experiment	--	The experiment object.
		
		Keyword arguments:
		script		--	A definition script. (default=None)
		"""

		self._question = u'Your question?'
		self._resp1 = u'Response 1'
		self._resp2 = u'Response 2'
		self._responses = u'Response 1\nResponse2'
		self._variable = u'menu_choice'
		# Then call the parent constructor
		item.__init__(self, name, experiment, script)

	def prepare(self):

		"""The preparation phase of the plug-in goes here."""
		self.responses = self._responses.split('\n')
		while self.responses.count('') > 0:
			self.responses.remove('')
		self.rows = [2] + [1]*len(self.responses)
		pass

	def run(self):

		"""The run phase of the plug-in goes here."""
		form = widgets.form(self.experiment, cols=[1,5,1], rows=self.rows, margins=[32,32,32,32])
		label_title = widgets.label(form, text=self._question)
		form.set_widget(label_title, (0,0), colspan=3)
		for i in range(len(self.responses)):
			resp = self.responses[i]
			button = widgets.button(form, text=resp)
			form.set_widget(button, (1, i+1))
		button_clicked = form._exec()
		self.experiment.set(self._variable, button_clicked)		

class qtmobile_menu(mobile_menu, qtautoplugin):
	
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
		mobile_menu.__init__(self, name, experiment, script)
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
