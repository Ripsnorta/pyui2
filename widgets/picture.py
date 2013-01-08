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

import pyui2

from pyui2.desktop import getDesktop, getTheme, getPresenter
from pyui2.base import Base
from pyui2.layouts import Much


class Picture(Base):
	"""Picture/Image object. warning: this does not clip to it's resized psize by default.

	The pieceRect arg is used to draw portions of images. This can be
	useful for flipbook style animations. The PieceRect is a tuple of
	(x position, y position, width, height). When the image is divided
	into pieces (width * height) and the single piece at (x,y) is
	drawn.
	"""

	widgetLabel = "PICTURE"

	def __init__(self, filename, pieceRect = (0,0,1,1)):
		Base.__init__(self)
		self.setFilename(filename)
		self.tooltipText = self.filename
		self.pieceRect = pieceRect

	def setRotation(self, irotationDeg):
		self.irotationDegrees = irotationDeg

	def getPreferredSize(self):
		size = getPresenter().getImageSize(self.filename)
		return (int(size[0]), int(size[1]))

	getMaximumSize = getPreferredSize

	def setFilename(self, filename):
		self.filename = filename
		self.setDirty(1)

	def setPiece(self, x, y, w, h):
		self.pieceRect = (x, y, w, h)
		self.setDirty(1)
