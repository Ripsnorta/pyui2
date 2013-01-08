###################################################################################
# pyui2
# Copyright (C) 2005 John Judd
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
###################################################################################

from pyui2.panel import Panel





class Group(Panel):
    widgetLabel = "GROUP"

    def __init__(self):
        Panel.__init__(self)


    def present(self, presenter, graphicsContext):
        """Performs the rendering of the panel and it's children to the windows graphic context.
        """
        # Draw the panel first
        presenter.drawWidget("GROUP", self, graphicsContext)

        # Draw each of the children on to the graphics context using the theme supplied through
        # the presenter
        for child in self.children:
            child.present(presenter, graphicsContext)
