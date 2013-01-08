# pyui2
# Copyright (C) 2001-2002 Sean C. Riley
# 
# This library is free software; you can redistribute it and/or
# modify it under the terms of version 2.1 of the GNU Lesser General Public
# License as published by the Free Software Foundation.
# 
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
# 
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

"""pyui2 Themes.
Themes are a method of customizing the drawing of widgets in a pyui2 GUI.

This modules keeps NO state for the drable objects - it just draws them on demand
from the widgets themselves which hold all the state.

The constants for the theme objects live in pyui2/locals.py

Themes have a default font that is used for any widgets that dont specify a font.
"""

from theme import Theme

class FutureTheme(Theme):
	""" Futuristic looking theme.
	"""

	def __init__(self):
		Theme.__init__(self)


	def setupTheme(self):
		Theme.setupTheme(self)


	
