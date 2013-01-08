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

import pygame
import pygame.draw



class PygameGraphics:

    def __init__(self, size, flags):
        self.size = size
        self.flags = flags
        self.screen = pygame.display.set_mode(size, flags)

    def clearScreen(self, color=None):
        if color == None:
            color = (0,0,0, 255)

        self.screen.fill(color)

    def createSurface(self, size):
        return pygame.Surface(size)

    def beginDraw(self, surface):
        # No implementation necessary here
        return surface

    def endDraw(self):
        pass # No implementation necessary here

    def createFont(self, font):
        return PGFont(font)

    def drawLine(self, surface, color, thickness, pointList):
        pygame.draw.lines(surface, color, False, pointList, thickness)

    def drawRect(self, surface, color, thickness, rect):
        pygame.draw.rect(surface, color, rect, thickness)

    def drawFilledRect(self, surface, color, rect):
        rv = surface.fill(color, rect)

    def drawCircle(self, surface, color, width, pos, radius):
        pygame.draw.circle(surface, color, pos, radius, width)

    def drawPolygon(self, surface, color, pointList, width):
        pygame.draw.polygon(surface, color, pointList, width)

    def drawFilledPolygon(self, surface, color, pointList):
        pygame.draw.polygon(surface, color, pointList, 1)

    def drawText(self, text, pos, font, color, surface):
        #print font
        font.drawText(text, pos, color, surface)

    def render(self, surface, destPos, srcRect=None):
        self.screen.blit(surface, destPos)

    def drawImage(self, surface, image, destPos, srcRect=None):
        surface.blit(image, destPos)

    def blit(self, surface, destPos, srcRect=None):
        self.screen.blit(surface, destPos)

    def prepare(self):
        pass

    def present(self, updateRegions=None):
        if updateRegions == None:
            pygame.display.update()
        else:
            pygame.display.update(updateRegions)

    def postPresent(self, callback):
        pass


class PGFont:
    def __init__(self, font):
        self.font = font

    def drawText(self, text, pos, color, surface):
        if text != None and text != "":
            textSurface = self.font.render(text, 0, color, (0,0,0,255))
            textSurface.set_colorkey( (0,0,0,255))
            surface.blit(textSurface, pos)

    def getTextSize(self, text):
        return self.font.size(text)











