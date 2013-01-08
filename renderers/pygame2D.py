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

import sys
import pygame
import pygame.font
import pygame.image
import pygame.key
import pygame.draw
import pyui2.core
import pygame.transform

from pygame.locals import *

from pyui2.desktop import getDesktop, getTheme, getPresenter

class Pygame2D(pyui2.core.RendererBase):
    """Pygame 2D renderer.
    """
    name = "2D"

    def __init__(self, w, h, fullscreen, title):
        pyui2.core.RendererBase.__init__(self, w, h, fullscreen, title)
        pygame.init()
        if fullscreen:
            self.screen = pygame.display.set_mode((w, h), FULLSCREEN | SWSURFACE)
        else:
            self.screen = pygame.display.set_mode((w, h))

        pygame.display.set_caption(title)

        self.screen.set_alpha(255)

        pygame.key.set_mods(KMOD_NONE)
        pygame.mouse.set_visible(0)

        pyui2.locals.K_SHIFT     = 304
        pyui2.locals.K_CONTROL   = 306
        pyui2.locals.K_ALT       = 308

        pyui2.locals.K_PAGEUP    = 280
        pyui2.locals.K_PAGEDOWN  = 281
        pyui2.locals.K_END       = 279
        pyui2.locals.K_HOME      = 278

        pyui2.locals.K_LEFT      = 276
        pyui2.locals.K_UP        = 273
        pyui2.locals.K_RIGHT     = 275
        pyui2.locals.K_DOWN      = 274

        pyui2.locals.K_INSERT    = 277
        pyui2.locals.K_DELETE    = 127

        pyui2.locals.K_F1        = 282
        pyui2.locals.K_F2        = 283
        pyui2.locals.K_F3        = 284
        pyui2.locals.K_F4        = 285
        pyui2.locals.K_F5        = 286
        pyui2.locals.K_F6        = 287
        pyui2.locals.K_F7        = 288
        pyui2.locals.K_F8        = 289
        pyui2.locals.K_F9        = 290
        pyui2.locals.K_F10       = 291
        pyui2.locals.K_F11       = 292
        pyui2.locals.K_F12       = 293

        self.lastID = 1000
        self.windows = {}
        self.images = {}

        self.drawBackMethod = self.clear

    def doesDirtyRects(self):
        return 1

    def createFont(self, face, size, flags):
        try:
            newFont = pygame.font.SysFont(face, size)
            #newFont = pygame.font.Font(face, size)
        except:
            print "Exception: ", sys.exc_info()[0]
            print "Couldn't find " + face + " - attempting to load as system font"
            newFont = pygame.font.SysFont(face, size)

        pyui2.locals.TEXT_HEIGHT = newFont.get_height()

        return newFont;

    def clear(self):
        self.screen.fill((0,0,0, 255))

    def draw(self, windows):
        # draw back if required
        if self.drawBackMethod:
            self.windowPos = (0,0)
            self.drawList = []
            apply(self.drawBackMethod, self.drawBackArgs)
            for command in self.drawList:
                self.doDrawCommand(command)
            self.drawList = []

        for i in xrange(len(windows)-1, -1, -1):
            w = windows[i]
            w.setDirty(1)
            n =  w.drawWindow(self)
            if n:
                self.windowPos = (w.posX, w.posY)
                for command in w.drawCommands:
                    self.doDrawCommand(command)

        self.drawMouseCursor()
        if self.mustFill:
            pygame.display.flip()
        else:
            pygame.display.update()#self.dirtyRects)

        self.mustFill = 0
        self.dirtyRects = []


    ###############################################################################
    ### Draw Primitives functions
    ###############################################################################

    def drawRect(self, color, rect):
        """Fills a rectangle with the specified color."""
        self.drawList.append( (pyui2.locals.RECT, rect, color) )

    def drawText(self, text, pos, color, font = None):
        """Draws the text on the screen in the specified position"""
        self.drawList.append( (pyui2.locals.TEXT, text, pos, color, font) )

    def drawGradient(self, rect, c1, c2, c3, c4):
        """Draws a gradient rectangle"""
        self.drawList.append( (pyui2.locals.GRADIENT, rect, c1, c2, c3, c4 ) )

    def drawImage(self, rect, filename, pieceRect = None):
        """Draws an image at a position"""
        if not self.images.has_key(filename):
            self.loadImage(filename)
        self.drawList.append( (pyui2.locals.IMAGE, rect, filename) )

    def drawLine(self, x1, y1, x2, y2, color):
        """Draws a line"""
        self.drawList.append( (pyui2.locals.LINE, x1, y1, x2, y2, color) )

    def loadImage(self, filename, label = None):
        if label:
            realName = label
        else:
            realName = filename

        try:
            img = pygame.image.load(filename)
        except:
            img = pygame.image.load(  pyui2.__path__[0] + "/images/" + filename )

        self.images[realName] = img


    def setClipping(self, rect = None):
        """set the clipping rectangle for the main screen. defaults to clearing the clipping rectangle."""
        self.drawList.append( (pyui2.locals.CLIP, rect) )

    ###############################################################################
    ### actual drawing functions
    ###############################################################################

    def doDrawCommand(self, command):
        cmd = command[0]
        if cmd == pyui2.locals.RECT:
            (cmd, rect, color) = command
            rect = (self.windowPos[0]+rect[0], self.windowPos[1]+rect[1], rect[2], rect[3])
            self.screen.fill(color, rect)
            return 2
        elif cmd == pyui2.locals.TEXT:
            (cmd, text, pos, color, font) = command
            if not text:
                return
            pos = (self.windowPos[0]+pos[0], self.windowPos[1]+pos[1])
            if font == None:
                font = getTheme().defaultFont

            surf = font.render(text, 0, color, (0,0,0,255))
            surf.set_colorkey( (0,0,0,255))
            self.screen.blit(surf, pos)
            return len(text)
        elif cmd == pyui2.locals.IMAGE:
            (cmd, rect, filename) = command
            rect = (self.windowPos[0]+rect[0], self.windowPos[1]+rect[1], rect[2], rect[3])
            img = self.images[filename]
            (w,h) = img.get_size()
            if (w,h) != (rect[2], rect[3]):
                img = pygame.transform.scale(img, (rect[2], rect[3]) )
            self.screen.blit(img, (rect[0], rect[1]) )
            return 2
        elif cmd == pyui2.locals.GRADIENT:
            (cmd, rect, c1, c2, c3, c4 ) = command
            rect = (self.windowPos[0]+rect[0], self.windowPos[1]+rect[1], rect[2], rect[3])
            self.screen.fill(c3, rect)
            return 2
        elif cmd == pyui2.locals.CLIP:
            #(cmd, rect) = command
            #rect = (self.windowPos[0]+rect[0], self.windowPos[1]+rect[1], rect[2], rect[3])
            #self.screen.set_clip(rect)
            pass
        elif cmd == pyui2.locals.LINE:
            (pyui2.locals.LINE, x1, y1, x2, y2, color) = command
            pos1 = (self.windowPos[0] + x1, self.windowPos[1] + y1)
            pos2 = (self.windowPos[0] + x2, self.windowPos[1] + y2)
            pygame.draw.line(self.screen, color, pos1, pos2)
        return 0

    def setMouseCursor(self, cursor, offsetX=0, offsetY=0):
        self.mouseCursor = cursor
        self.mouseOffset = (offsetX, offsetY)
        self.loadImage(cursor)

    def drawMouseCursor(self):
        image = self.images[self.mouseCursor]
        self.screen.blit(image, (self.mousePosition[0]-self.mouseOffset[0], self.mousePosition[1]-self.mouseOffset[1]) )

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


    def quit(self):
        pygame.quit()


    def packColor(self, r, g, b, a = 255):
        """pack the rgba triplet into a color
        """
        return (r, g, b, a)

    def getTextSize(self, text, font = None):
        if not font:
            font = getTheme().defaultFont

        return font.size(text)

    def getImageSize(self, filename):
        if not self.images.has_key(filename):
            self.loadImage(filename)

        return self.images[filename].get_size()
