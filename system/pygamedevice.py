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

import pygame
import pygame.font
import pygame.image
import pygame.key
import pygame.draw
import pygame.transform

from pygame.locals import *

import pyui2.core
from pyui2.desktop import getDesktop, getPresenter

from device import Device
from pygamegraphics import PygameGraphics
from gcx import GCX



class PygameDevice(Device):
    P2D = 0
    OGL = 1

    def __init__(self, width, height, fullscreen, mode=P2D):
        Device.__init__(self)

        self.mode = mode
        self.size = (width, height)

        pygame.init()
        pygame.key.set_mods(KMOD_NONE)
        pygame.mouse.set_visible(0)

        if mode == PygameDevice.P2D:
            flags = 0
            if fullscreen:
                flags = flags | pygame.locals.FULLSCREEN | pygame.locals.SWSURFACE

            self.graphicsDevice = PygameGraphics(self.size, flags)

        elif mode == PygameDevice.OGL:
            from openglgraphics import OpenGLGraphics
            
            flags = pygame.locals.OPENGL | pygame.locals.DOUBLEBUF
            if fullscreen:
                flags = flags | pygame.locals.FULLSCREEN

            self.graphicsDevice = OpenGLGraphics(self.size, flags, pygame.display.set_mode(self.size, flags))

        else:
            raise device.DeviceException("Invalid Graphics Mode Specified")

    def setWindowTitle(self, title):
        pygame.display.set_caption(title)


    def update(self):
        """PyGame event handling.
        """
        desktop = getDesktop()

        if pygame.mouse.get_focused() == False:
            # The mouse is no longer over the application
            getPresenter().setMousePosition(None)

        ## process all pending system events.
        event = pygame.event.poll()
        while event.type != NOEVENT:

            if event.type == pygame.QUIT:
                desktop.postUserEvent(pyui2.locals.QUIT)

            # special case to handle multiple mouse buttons!
            elif event.type == MOUSEBUTTONDOWN:
                if event.dict['button'] == 1:
                    desktop.postUserEvent(pyui2.locals.LMOUSEBUTTONDOWN, event.pos[0], event.pos[1])
                elif event.dict['button'] == 3:
                    desktop.postUserEvent(pyui2.locals.RMOUSEBUTTONDOWN, event.pos[0], event.pos[1])

            elif event.type == MOUSEBUTTONUP:
                if event.dict['button'] == 1:
                    desktop.postUserEvent(pyui2.locals.LMOUSEBUTTONUP, event.pos[0], event.pos[1])
                elif event.dict['button'] == 3:
                    desktop.postUserEvent(pyui2.locals.RMOUSEBUTTONUP, event.pos[0], event.pos[1])

            elif event.type == MOUSEMOTION:
                desktop.postUserEvent(pyui2.locals.MOUSEMOVE, event.pos[0], event.pos[1])
                self.mousePosition = event.pos
                getPresenter().setMousePosition(event.pos)

            elif event.type == KEYDOWN:
                character = event.unicode
                code = 0
                if len(character) > 0:
                    code = ord(character)
                else:
                    code = event.key
                desktop.postUserEvent(pyui2.locals.KEYDOWN, 0, 0, code, pygame.key.get_mods())
                if code >= 32 and code < 128:
                    desktop.postUserEvent(pyui2.locals.CHAR, 0, 0, character.encode(), pygame.key.get_mods())

            elif event.type == KEYUP:
                code = event.key
                desktop.postUserEvent(pyui2.locals.KEYUP, 0, 0, code, pygame.key.get_mods())
            else:
                try:
                    desktop.postUserEvent(event.type)
                except:
                    print "Error handling event %s" % repr(event)
            event = pygame.event.poll()


    def run(self, callback=None, trackFPS=True):
        lastTime = 0
        frameCounter = 0
        desktop = getDesktop()

        while desktop and desktop.running:
            if trackFPS == True:
                frameCounter = frameCounter + 1
                now = time.time()
                if now - lastTime >= 1:
                   lastTime = now
                   print "FPS: %d" % frameCounter
                   frameCounter = 0

            if callback:
                callback()

            desktop.update()
            desktop.draw()

    def quit(self):
        pygame.quit()

    def createGraphicsContext(self, size):
        graphicsContext = GCX(size, self.graphicsDevice)
        return graphicsContext

    def createFont(self, face, size, flags):
        try:
            newFont = pygame.font.SysFont(face, size)
            #newFont = pygame.font.Font(face, size)
        except:
            print "Exception: ", sys.exc_info()[0]
            print "Couldn't find " + face + " - attempting to load as system font"
            newFont = pygame.font.SysFont(face, size)

        return self.graphicsDevice.createFont(newFont)

    def render(self, graphicsContext, pos):
        graphicsContext.render(pos)

    def clearScreen(self):
        self.graphicsDevice.clearScreen()

    def getScreenSize(self):
        return self.size

    def prepare(self):
        self.graphicsDevice.prepare()

    def present(self):
        desktop = getDesktop()
        if desktop and desktop.running:
            self.graphicsDevice.present()
            self.graphicsDevice.postPresent(pygame.display.flip())

    def loadImage(self, filename):
        return pygame.image.load(filename)

    def drawImage(self, image, pos):
        #print "drawImage:", self.graphicsDevice.screen, image, pos
        rect = (pos[0], pos[1], image.get_width(), image.get_height())
        self.graphicsDevice.drawImage(self.graphicsDevice.screen, image, rect)

    def convertToImageString(self, image):
        #print "PygameDevice.convertToImageString:", image
        ix = image.get_width()
        iy = image.get_height()
        data = pygame.image.tostring(image, "RGBA", 1)
        #print data
        return (data, ix, iy)

    def scaleImage(self, image, newSize):
        return pygame.transform.scale(image, newSize)


















