# pyui2
# Copyright (C) 2001-2002 Sean C. Riley
# Portions Copyright (C) 2005 John Judd
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

import string
import math
import pyui2
import pyui2.system

from pygame.locals import *

import OpenGL
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

class OpenGLGraphics:

    fontMap = {}

    def __init__(self, size, flags=None, screen = None):
        self.size = size;
        self.flags = flags
        self.screen = screen

    def clearScreen(self, color=None):
        if color:
            glClearColor( color[0], color[1], color[2], color[3] )

        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

    def createSurface(self, size):
        displayList = glGenLists(1)
        #print "createSurface returns", displayList
        return displayList

    def beginDraw(self, displayList):
        #print "BEGINDRAW"
        if displayList:
            #print "The displayList =", displayList
            if glIsList(displayList):
                #print "displayList", displayList, "is a valid list"
                glDeleteLists(displayList, 1)

        displayList = glGenLists(1)
        glNewList(displayList, GL_COMPILE)
        #print "New displayList =", displayList
        return displayList

    def endDraw(self):
        #print "ENDDRAW"
        glEndList()

    def render(self, displayList, destPos, srcRect=None):
        self.setWindowOrigin(destPos)
        # draw the surface display list
        glCallList(displayList)

    def createFont(self, font):
        import types
        if isinstance(font, types.StringTypes):
            gFont = GLUTFont(font)
        else:
            gFont = GLFont(font)

        return gFont

    def drawLine(self, displayList, color, thickness, pointList):
        glBegin(GL_LINE_STRIP)
        glColor4ub( color[0], color[1], color[2], color[3] )
        for point in pointList:
            glVertex2i(point[0], point[1])
        glEnd()

    def drawRect(self, displayList, color, thickness, rect):
        pointList = ((rect[0], rect[1]),
                     (rect[0] + rect[2], rect[1]),
                     (rect[0] + rect[2], rect[1] + rect[3]),
                     (rect[0], rect[1] + rect[3]),
                     (rect[0], rect[1]))

        self.drawLine(displayList, color, thickness, pointList)

    def drawFilledRect(self, displayList, color, rect):
        (x,y,w,h) = (int(rect[0]), int(rect[1]), int(rect[2]), int(rect[3]))
        glDisable(GL_TEXTURE_2D)
        glBegin(GL_QUADS)
        glColor4ub( color[0], color[1], color[2], color[3] )
        glVertex2i(x, y)
        glVertex2i(x + w, y)
        glVertex2i(x + w, y + h)
        glVertex2i(x, y + h)
        glEnd()

    def drawCircle(self, displayList, color, width, pos, radius):
        if width == 0: # Filled Circle
            glBegin(GL_POLYGON)
        else:
            glBegin(GL_LINE_LOOP)

        i = 0
        numLines = 16
        while  i < numLines:
            # M_PI defined in cmath.h
            angle = (i * 2 * math.pi) / numLines;
            # we use vertex2f since we are currently in working
            # in 2d.
            x = pos[0] + (radius * math.cos(angle))
            y = pos[1] + (radius * math.sin(angle))
            glVertex2f(x, y);
            i += 1

        glEnd();

    def drawPolygon(self, displayList, color, pointList, width):
        glBegin(GL_LINE_LOOP)
        glColor4ub( color[0], color[1], color[2], color[3] )
        for point in pointList:
            glVertex2i(point[0], point[1])
        glEnd()

    def drawFilledPolygon(self, displayList, color, pointList):
        glDisable(GL_TEXTURE_2D)
        glBegin(GL_POLYGON)
        glColor4ub( color[0], color[1], color[2], color[3] )
        for point in pointList:
            glVertex2i(point[0], point[1])
        glEnd()

    def drawText(self, displayList, text, pos, font, color):
        font.drawText(text, pos, color)

    def drawImage(self, displayList, image, destRect, srcRect=None):
        textureCoords = [[0.0,1.0],[1.0,1.0],[1.0,0.0],[0.0,0.0]]

        #print "drawImage at", destRect
        texture, w, h = self.createTexture(image)

        glColor4ub( 255, 255, 255, 255 )
        glEnable(GL_TEXTURE_2D)
        glBindTexture( GL_TEXTURE_2D, texture)

        glBegin(GL_QUADS)
        glTexCoord2f(textureCoords[0][0], textureCoords[0][1])
        glVertex2i( destRect[0], destRect[1])
        glTexCoord2f(textureCoords[1][0], textureCoords[1][1])
        glVertex2i( destRect[0] + destRect[2], destRect[1])
        glTexCoord2f(textureCoords[2][0], textureCoords[2][1])
        glVertex2i( destRect[0] + destRect[2], destRect[1] + destRect[3])
        glTexCoord2f(textureCoords[3][0], textureCoords[3][1])
        glVertex2i( destRect[0], destRect[1] + destRect[3])
        glEnd()
        glDisable(GL_TEXTURE_2D)

    def blit(self, surface, destPos, srcRect=None):
        pass

    def prepare(self):
        self.setup2D()

    def present(self, updateRegions=None):
        # When finished, teardown
        self.teardown2D()

    def postPresent(self, callback):
        if callback != None:
            callback()

    def setup2D(self):
        """Setup everything on the opengl Stack to draw in 2D in a way that can be torn down later.
        """
        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()
        glOrtho( 0, self.size[0], self.size[1], 0, -1, 1 )

        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()

        glDisable(GL_DEPTH_TEST)
        glEnable(GL_SCISSOR_TEST)

        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    def teardown2D(self):
        """tear down the 2D stuff to revert to the previous state.
        """
        # pop off 2D state matrices
        glMatrixMode(GL_MODELVIEW)
        glPopMatrix()
        glMatrixMode(GL_PROJECTION)
        glPopMatrix()
        # leave in model view mode
        glMatrixMode(GL_MODELVIEW)

    def setWindowOrigin(self, pos ):
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glTranslatef(pos[0], pos[1], 0)

    def createTexture(self, image):
        #print "createTexture.image:", image, image.get_size()
        adjImg = pyui2.system.getDeviceContext().makePowersOfTwo(image)
        (data, w, h) = pyui2.system.getDeviceContext().convertToImageString(adjImg)
        #print "createTexture:", w, h, len(data)
        # Create Texture
        texture = glGenTextures(1)
        #print "Texture =", texture
        glBindTexture(GL_TEXTURE_2D, texture)   # 2d texture (x and y size)
        glPixelStorei(GL_UNPACK_ALIGNMENT,1)
        glTexImage2D(GL_TEXTURE_2D, 0, 4, w, h, 0, GL_RGBA, GL_UNSIGNED_BYTE, data)

        glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_MODULATE)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)

        return texture, w, h


class GLUTFont:
    def __init__(self, font):
        self.font = font

    def drawText(self, text, pos, color, surface):
        glColor4ub( color[0], color[1], color[2], color[3] )
        glRasterPos2f(pos[0], pos[1]+13)
        if self.font == 'fixed':
            self.font = GLUT_BITMAP_8_BY_13
        else:
            self.font = GLUT_BITMAP_HELVETICA_12
        for char in text:
            glutBitmapCharacter(self.font, ord(char))

    def getTextSize(self, text):
        if self.font == 'fixed':
            w, h = ( 8 * len( text ), 13 )
        else:
            w = 0
            h = pyui2.locals.TEXT_HEIGHT
            for c in text:
                w += glutBitmapWidth(GLUT_BITMAP_HELVETICA_12, ord(c))

        return (w, h)


import pygame
class GLFont:
    def __init__(self, font):
        self.font = font
        self.charInfo = []  # tuples of (width, height, texture coordinates) for each character
        self.createGlyphs()

    def createGlyphs(self ):
        testSurface = self.font.render("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRTSUTWXYZ", 1, (255,255,255,255))
        charWidth = testSurface.get_width()
        charHeight = testSurface.get_height()
        charSurfaces = []

        # create the character surfaces
        totalWidth = 0
        for i in range(0,128):
            try:
                charSurface = self.font.render( chr(i), 1, (255,255,255,255))
            except:
                charSurfaces.append( None )
            else:
                charSurfaces.append(charSurface)
                totalWidth += charSurface.get_width()

        # TODO: calculate this properly
        if totalWidth > 1300:
            SZ = 512
        else:
            SZ = 256
        totalWidth = SZ
        totalHeight = SZ

        # pack the surfaces into a single texture
        x = pygame.surface.Surface((totalWidth, totalHeight),
                                   flags=pygame.HWSURFACE |pygame.SRCALPHA,
                                   depth=32,
                                   masks=(0,0,0,0))
        self.packedSurface = x.convert_alpha()
        self.packedSurface.fill((0,0,0,0))
        positionX = 0
        positionY = 0
        c = 0
        for charSurf in charSurfaces:
            if not charSurf:
                self.charInfo.append( (0,0, (0,0,0,0)) )
                continue

            if positionX + charSurf.get_width() > SZ:
                positionX = 0
                positionY += charSurf.get_height()

            self.packedSurface.blit(charSurf, (positionX, positionY) )

            # calculate texture coords
            left = positionX/(float)(totalWidth)
            top = 1- positionY/(float)(totalHeight)
            right = (positionX+charSurf.get_width()) / (float)(totalWidth)
            bottom = 1 - ((positionY+charSurf.get_height()) / (float)(totalHeight))
            texCoords = (left, top, right, bottom)

            self.charInfo.append( (charSurf.get_width(), charSurf.get_height(), texCoords) )
            positionX += charSurf.get_width()
            c += 1

        # create GL texture from surface
        self.texture = glGenTextures(1)
        data = pygame.image.tostring(self.packedSurface, "RGBA", 1)
        glBindTexture(GL_TEXTURE_2D, self.texture)
        glPixelStorei(GL_UNPACK_ALIGNMENT,1)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, totalWidth, totalHeight, 0, GL_RGBA, GL_UNSIGNED_BYTE, data)

        glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_MODULATE)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)

        # create display lists for each of the characters
        top = 1
        bottom = 3
        self.displayLists = []
        for (width, height, coords) in self.charInfo:
            if not width and not height:
                self.displayLists.append(0)
                continue
            newList = glGenLists(1)
            glNewList(newList, GL_COMPILE)
            glBegin(GL_QUADS)
            glTexCoord2f(coords[0], coords[top])
            glVertex2i(0, 0)
            glTexCoord2f(coords[2], coords[top])
            glVertex2i(width, 0)
            glTexCoord2f(coords[2], coords[bottom])
            glVertex2i(width, height)
            glTexCoord2f(coords[0], coords[bottom])
            glVertex2i(0, height)
            glEnd()
            glEndList()
            self.displayLists.append(newList)

    def drawText(self, text, pos, color, surface):
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, self.texture)
        glColorub(color)
        xPos = pos[0]
        yPos = pos[1]-5
        glPushMatrix()
        glTranslate(xPos,yPos,0)
        for c in text:
            width = self.charInfo[ord(c)][0]
            glCallList( self.displayLists[ord(c)])
            glTranslate(width,0,0)
        glPopMatrix()
        glDisable(GL_TEXTURE_2D)

    def getTextSize(self, text):
        w = 0
        h = 0
        for c in text:
            (width, height, coords) = self.charInfo[ord(c)]
            w += width
            h = max(height,h)
        return (w,h/1.4)






