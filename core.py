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

# system imports
import sys
import string
import os
import time

# library imports
import pyui2.locals
import colors

from desktop import Desktop, readTimer
from themes import theme

###########################################################
# Section: Globals
##########################################################

gRenderer = None
gDesktop = None
gVersion = 0.2
gFrameCounter = 0
gLastTime = time.time()

#########################################################
# Section: external/public functions
#
# External/Public Module level functions
#########################################################

def init(w, h, deviceName = "p3d", fullscreen = 0, title=""):
    """Initialize pyui2. Will set to fullscreen if specified. default is to run in a window.
    This will return a Desktop Object.
    (public)
    """
    print "init"
    global gDesktop
    # create the theme and desktop
    gDesktop = Desktop(w, h, fullscreen, theme.Theme, deviceName)
    pyui2.system.getDeviceContext().setWindowTitle(title)
    colors.init()
    return gDesktop

def quit():
    """Sets the running flag so that the application knows to quit.
    (public)
    """
    global gDesktop
    gDesktop.quit()

def update():
    """Process events from the renderer, and events posted by users or widgets.
    Will return 1 if execution should continue, 0 if we should exit.
    (public)
    """
    global gDesktop
    return gDesktop.update()

def draw():
    """
    fills the background and draws the widgets.
    (public)
    """
    global gDesktop
    gDesktop.draw()


def version():
    """return the version number of pyui2"""
    global gVersion
    return gVersion


def run(callback=None, trackFPS=True):
    """This is a default way of _running_ an application using
    the current renderer.
    """
    pyui2.system.getDeviceContext().run(callback)


def isRunning():
    global gDesktop
    return gDesktop.running


def loadpyui2Image(filename):
    """This loads an image file from the images directory in the pyui2 install.
    The directory pyui2/images holds general images used in pyui2 that are not
    application specific.
    """
    path = pyui2.__path__[0]
    pathElements = list(os.path.split(path)) # string.split(path, "\\")
    pathElements.pop( len(pathElements) -1)
    realName = string.join( pathElements, "/") + "/images/" + filename
    getPresenter().loadImage(realName, filename)

