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

import sys
import time

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

from pygame.locals import *
from pyui2.desktop import getDesktop, getPresenter

from device import Device
from openglgraphics import OpenGLGraphics
from gcx import GCX



class GLUTDevice(Device):
    def __init__(self, width, height, fullscreen):
        print "glut::__init__()"
        Device.__init__(self)

        self.size = (width, height)
        self.fullscreen = fullscreen

        glutInit(sys.argv)
        glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)

        if self.fullscreen:
            glutGameModeString("%dx%d:32@70" % self.size )
            self.windowID = glutEnterGameMode()
        else:
            glutInitWindowSize(self.size[0], self.size[1])
            glutInitWindowPosition(0,0)
            self.windowID = glutCreateWindow("")

        glutSetWindow(self.windowID)

        glutReshapeFunc(self.reSizeGLScene)
        glutMouseFunc(self.onMouse)
        glutMotionFunc(self.onMotion)
        glutPassiveMotionFunc(self.onMotion)
        glutKeyboardFunc(self.onKeyDown)
        glutKeyboardUpFunc(self.onKeyUp)
        glutSpecialFunc(self.onSpecialDown)
        glutSpecialUpFunc(self.onSpecialUp)

        self.graphicsDevice = OpenGLGraphics(self.size)

    def setWindowTitle(self, title):
        if not self.fullscreen:
            glutSetWindowTitle(title)

    def update(self):
        pass

    def run(self, callback=None, trackFPS=True):
        print "glut::run"
        self.trackFPS = trackFPS

        self.callback = callback
        glutDisplayFunc(self.runMe)
        #glutIdleFunc(self.runMe)

        glutMainLoop()

    def runMe(self):
        print "glut::runMe"
        lastTime = 0
        frameCounter = 0
        desktop = getDesktop()

        while desktop and desktop.running:
            if self.trackFPS == True:
                frameCounter = frameCounter + 1
                now = time.time()
                if now - lastTime >= 1:
                   lastTime = now
                   print "FPS: %d" % frameCounter
                   frameCounter = 0

            if self.callback:
                self.callback()

            desktop.update()
            desktop.draw()

        sys.exit()

    def quit(self):
        if self.fullscreen:
            glutLeaveGameMode()
        self.done = 1

    def onMouse(self, button, state, x, y):
        print "glut::onMouse"
        if button==1:
            return
        if state==0:
            #mouse button down
            if button==0:
                getDesktop().postUserEvent(pyui2.locals.LMOUSEBUTTONDOWN,x,y)
            else:
                getDesktop().postUserEvent(pyui2.locals.RMOUSEBUTTONDOWN,x,y)
        else:
            #mouse button up
            if button==0:
                getDesktop().postUserEvent(pyui2.locals.LMOUSEBUTTONUP  ,x,y)
            else:
                getDesktop().postUserEvent(pyui2.locals.RMOUSEBUTTONUP  ,x,y)

    def onMotion(self, x, y):
        print "glut::onMotion"
        getDesktop().postUserEvent(pyui2.locals.MOUSEMOVE, x,y)
        self.mousePosition = (x,y)

    def getModifiers(self):
        """NOTE: GLUT does not detect the CONTROL key!!!! BUG!!
        """
        mod = glutGetModifiers()
        realmod = 0
        if mod & GLUT_ACTIVE_SHIFT:
            realmod |= pyui2.locals.MOD_SHIFT
        if mod & GLUT_ACTIVE_CTRL:
            realmod |= pyui2.locals.MOD_CONTROL
        if mod & GLUT_ACTIVE_ALT:
            realmod |= pyui2.locals.MOD_ALT
        return realmod

    def onSpecialDown(self, key, x, y):
        k = self.keyMap.get(key, key)
        print "down: ", k, key
        getDesktop().postUserEvent(pyui2.locals.KEYDOWN, 0, 0, k, self.getModifiers() )

    def onSpecialUp(self, key, x, y):
        k = self.keyMap.get(key, key)
        getDesktop().postUserEvent(pyui2.locals.KEYUP, 0, 0, k, self.getModifiers() )

    def onKeyDown(self,key,x,y):
        if ord(key) < 128:
            getDesktop().postUserEvent(pyui2.locals.CHAR, 0, 0, key, self.getModifiers() )

        getDesktop().postUserEvent(pyui2.locals.KEYDOWN, 0, 0, ord(key), self.getModifiers() )

    def onKeyUp(self,key,x,y):
        getDesktop().postUserEvent(pyui2.locals.KEYUP  , 0, 0, ord(key), self.getModifiers() )

    def reSizeGLScene(self, Width, Height):
        print "glut::reSizeGLScene"
        # Prevent A Divide By Zero If The Window Is Too Small
        if Height == 0:
            Height = 1

        # Reset The Current Viewport And Perspective Transformation
        glViewport(0, 0, Width, Height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45.0, float(Width)/float(Height), 0.1, 100.0)
        glMatrixMode(GL_MODELVIEW)
        self.width = Width
        self.height = Height

    def createGraphicsContext(self, size):
        graphicsContext = GCX(size, self.graphicsDevice)
        return graphicsContext

    def createFont(self, face, size, flags):
        #TO DO: Work out the appropriate glut font from the requested parameters
        fontName = "fixed"
        return self.graphicsDevice.createFont(fontName)

    def render(self, graphicsContext, pos):
        pass

    def clearScreen(self):
        self.graphicsDevice.clearScreen()

    def getScreenSize(self):
        return self.size

    def prepare(self):
        self.graphicsDevice.prepare()

    def present(self):
        self.graphicsDevice.present()
        glutSwapBuffers()

    def loadImage(self, filename):
        try:
            image = open(filename)
        except:
            print "Unable to open the image file"
        return image

    def drawImage(self, image, pos):
        rect = (pos[0], pos[1], image.get_width(), image.get_height())
        self.graphicsDevice.drawImage(image, rect)

    def convertToImageString(self, image):
        ix = image.size[0]
        iy = image.size[1]
        seq = 0
        for mode, seq in [('RGBA', 4), ('RGBX', 4), ('RGB', 3)]:
            try:
                data = image.tostring("raw", mode, 0, -1)
            except (IOError, SystemError):
                print "Unable to load %s with encoder %s" % (filename, mode)
                failed = 1
            else:
                failed = 0
                break
        if failed:
            raise IOError("All three encoders failed.")

        return (data, ix, iy)







