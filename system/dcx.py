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

import time
import math

deviceContext = None



def setDeviceContext(device):
    global deviceContext
    deviceContext = DCX(device);


def getDeviceContext():
    global deviceContext
    return deviceContext




class DCX:
    """The Device Context (DCX) class manages a single device and
        provides the interface to that device for the rest of the
        PyUI2 system.
    """

    def __init__(self, device):
        self.device = device
        self.images = {}

    def setWindowTitle(self, title):
        self.device.setWindowTitle(title)

    def update(self):
        self.device.update()

    def run(self, callback=None, trackFPS=True):
        self.device.run(callback, trackFPS)

    def quit(self):
        self.device.quit()

    def readTimer(self):
        return time.time()

    def createGraphicsContext(self, size):
        return self.device.createGraphicsContext(size)

    def createFont(self, face, size, flags):
        return self.device.createFont(face, size, flags)

    def loadImage(self, filename, label = None):
        realName = filename
        if label:
            realName = label

        img = self.device.loadImage(filename)
        self.images[realName] = img

        return img

    def getImage(self, filename, label = None, reloadImage=False):
        realName = filename
        if label:
            realName = label

        if self.images.has_key(realName) and reloadImage == False:
            img = self.images[realName]
        else:
            img = self.device.loadImage(filename)
            self.images[realName] = img

        return img

    def getImageSize(self, filename, label = None):
        realName = filename
        if label:
            realName = label

        if self.images.has_key(realName):
            img = self.images[realName]
        else:
            img = self.loadImage(filename, label)

        return img.get_size()

    def drawImage(self, image, pos):
        #print "drawImage:", pos, image
        self.device.drawImage(image, pos)

    def convertToImageString(self, image):
        return self.device.convertToImageString(image)

    def scaleImage(self, image, newSize):
        return self.device.scaleImage(image, newSize)

    def makePowersOfTwo(self, image):
        size = image.get_size()
        w = pow(2, math.ceil(math.log(size[0], 2)))
        h = pow(2, math.ceil(math.log(size[1], 2)))
        return self.device.scaleImage(image, (w, h))

    def clearScreen(self):
        self.device.clearScreen()

    def getScreenSize(self):
        return self.device.getScreenSize()

    def prepare(self):
        self.device.prepare()

    def present(self):
        """Update the display.
        """
        self.device.present()

