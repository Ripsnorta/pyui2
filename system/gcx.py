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

import pyui2.system

class GCX:
    """The Graphics Context class provides a context for a parent to draw
        into. for Pygame this is a surface, while for OpenGL it is a display
        list.
    """

    TEXT_LEFT = 0
    TEXT_CENTER = 1
    TEXT_RIGHT = 2

    def __init__(self, size, graphicsDevice):
        self.size = size
        self.graphicsDevice = graphicsDevice
        self.surface = graphicsDevice.createSurface(size)

    def release(self):
        if self.surface != None:
            self.surface = None

    def beginDraw(self, posX, posY):
        self.surface = self.graphicsDevice.beginDraw(self.surface)

    def endDraw(self):
        self.graphicsDevice.endDraw()

    def render(self, pos, srcRect=None):
        self.graphicsDevice.render(self.surface, pos, srcRect)

    def getSize(self):
        return self.size

    def resize(self, size):
        self.release()
        self.size = size
        self.surface = self.graphicsDevice.createSurface(size)

    def createFont(self, face, size, flags):
        return self.graphicsDevice.createFont(face, size, flags)

    def drawGraphicObject(self, grob):
        grob.draw(self)

    def drawLine(self, pointList, pen):
        self.graphicsDevice.drawLine(self.surface, pen.color, pen.thickness, pointList)

    def drawRect(self, rect, pen):
        self.graphicsDevice.drawRect(self.surface, pen.color, pen.thickness, rect)

    def drawFilledRect(self, rect, brush):
        self.graphicsDevice.drawFilledRect(self.surface, brush.color, rect)

    def drawCircle(self, pos, radius, pen):
        width = pen.thickness
        if width == 0:
            width = 1

        self.graphicsDevice.drawCircle(self.surface, pen.color, width, pos, radius)

    def drawFilledCircle(self, pos, radius, brush):
        self.graphicsDevice.drawCircle(self.surface, brush.color, 0, pos, radius)

    def drawPolygon(self, pointList, pen):
        width = pen.thickness
        if width == 0:
            width = 1

        self.graphicsDevice.drawPolygon(self.surface, pen.color, pointList, width)

    def drawFilledPolygon(self, pointList, brush):
        self.graphicsDevice.drawFilledPolygon(self.surface, brush.color, pointList)

    def drawImage(self, image, rect, scale=True):
        #print "GCX.drawImage before scaling:", image, image.get_size()
        if scale == True:
            (w,h) = image.get_size()
            if (w,h) != (rect[2], rect[3]):
                postimage = pyui2.system.getDeviceContext().scaleImage(image, (rect[2], rect[3]))
                #print "postimage =", postimage
                if postimage != None:
                    image = postimage

        #print "GCX.drawImage after scaling:", image, image.get_size()
        self.graphicsDevice.drawImage(self.surface, image, rect)

    def drawText(self, text, rect, font, color, justification=TEXT_LEFT):
        # Need to work out if the text will fit inside the rectangle and truncate it if it won't
        textSize = font.getTextSize(text)
        pos = (rect[0], rect[1])
        width = rect[2]

        if justification == GCX.TEXT_LEFT:
            pos = (rect[0], rect[1])

            if textSize[0] > width:
                # if we're justifying left, we truncate the right side
                dText = text
                while textSize[0] > width:
                    textLen = len(dText)
                    if textLen > 0:
                        dText = dText[0:textLen - 1]
                        textSize = font.getTextSize(dText)
                    else:
                        break

                text = dText

        elif justification == GCX.TEXT_RIGHT:
            if textSize[0] > width:
                #if we're justifying right, we trucate the left side
                dText = text
                while textSize[0] > width:
                    textLen = len(dText)
                    if textLen > 0:
                        dText = dText[1:textLen]
                        textSize = font.getTextSize(dText)
                    else:
                        break

                text = dText

            textSize = font.getTextSize(text)
            gap = width - textSize[0]
            pos = (rect[0] + gap, rect[1])


        elif justification == GCX.TEXT_CENTER:
            if textSize[0] > width:
                #if we're justifying centered, we truncate both ends, starting
                # with the front
                dText = text

                trimFront = True

                while textSize[0] > width:
                    textLen = len(dText)
                    if textLen > 0:
                        if trimFront == True:
                            dText = dText[1:textLen]
                            trimFront = False
                        else:
                            dText = dText[0:textLen - 1]
                            trimFront = True

                        textSize = font.getTextSize(dText)
                    else:
                        break

                text = dText

            textSize = font.getTextSize(text)
            s = rect[0] + ((width / 2) - (textSize[0] / 2))
            pos = (s , rect[1])

        font.font.drawText(text, pos, color, self.surface)
        #self.graphicsDevice.drawText(text, pos, font, color, self.surface)





class Pen:
    STYLE_SOLID = 0

    def __init__(self, thickness, color, style):
        self.thickness = thickness
        self.color = color
        self.style = style



class Brush:
    STYLE_SOLID = 0

    def __init__(self, color, style):
        self.color = color
        self.style = style


class GraphicObject:
    def __init__(self, position):
        if position == None:
            self.position = (0, 0)
        else:
            self.position = position

    def setPosition(self, position):
        self.position = position

    def getPosition(self):
        return self.position


class Rectangle(GraphicObject):
    def __init__(self, rect=None, pen=None, brush=None):
        self.rect = rect
        if self.rect == None:
            self.rect = (0, 0, 0, 0)

        GraphicObject.__init__(self, (self.rect[0], self.rect[1]))
        self.pen = pen
        self.brush = brush

    def setPosition(self, (x, y)):
        self.position = (x, y)
        self.rect[0] = x
        self.rect[1] = y

    def setRectangle(self, rect):
        self.rect = rect

    def draw(self, gcx):
        if self.rect != None:
            if self.brush != None:
                gcx.drawFilledRect(self.rect, self.brush)

            if self.pen != None:
                gcx.drawRect(self.rect, self.pen)


class Square(Rectangle):
    def __init__(self, position=None, length=None, pen=None, brush=None):
        rect = None
        if position != None and length != None:
            rect = (position[0], position[1], length, length)

        Rectangle.__init__(self, rect, pen, brush)

    def setSideLength(self, length):
        self.rect[2] = length
        self.rect[3] = length


class Circle(GraphicObject):
    def __init__(self, position=None, radius=None, pen=None, brush=None):
        GraphicObject.__init__(self, position)
        self.radius = radius
        self.pen = pen
        self.brush = brush

    def setRadius(self, radius):
        self.radius = radius

    def getRadius(self):
        return self.radius

    def setRectangle(self, rect):
        w = rect[2]
        h = rect[3]
        if w > h:
            radius = h / 2
        else:
            radius = w / 2

        self.radius = radius
        self.setPosition((rect[0] + radius, rect[1] + radius))
        #print self.radius, self.position

    def draw(self, gcx):
        if self.position != None and self.radius != None:
            if self.brush != None:
                gcx.drawFilledCircle(self.position, self.radius, self.brush)

            if self.pen != None:
                gcx.drawCircle(self.position, self.radius, self.pen)


class Line(GraphicObject):
    def __init__(self, pointList=None, pen=None, position=None):
        GraphicObject.__init__(self, position)
        self.pointList = pointList
        self.pen = pen

    def setPoints(self, pointList):
        self.pointList = pointList

    def setPosition(self, position):
        deltaX = self.position[0] - position[0]
        deltaY = self.position[1] - position[1]
        #print "deltaX =", deltaX, "deltaY =", deltaY

        if deltaX != 0 and deltaY != 0:
            self.position = position

            newPointList = []
            for index in range(len(self.pointList)):
                point = self.pointList[index]
                newPointList.append((point[0] - deltaX, point[1] - deltaY))

            self.setPoints(newPointList)

    def setRectangle(self, rect):
        self.setPosition((rect[0], rect[1]))

    def draw(self, gcx):
        if self.pointList != None:
            if self.pen != None:
                #print "drawLine:", self.pointList
                gcx.drawLine(self.pointList, self.pen)


class Polygon(Line):
    def __init__(self, pointList=None, pen=None, brush=None, position=(0,0)):
        Line.__init__(self, pointList, pen, position)
        self.brush = brush

    def draw(self, gcx):
        if self.pointList != None:
            if self.brush != None:
                gcx.drawFilledPolygon(self.pointList, self.brush)

            if self.pen != None:
                gcx.drawPolygon(self.pointList, self.pen)


class Font:
    def __init__(self, face, size, flags):
        self.face = face
        self.size = size
        self.flags = flags
        self.font = pyui2.system.getDeviceContext().createFont(face, size, flags)

    def getTextSize(self, text):
        return self.font.getTextSize(text)

    def drawText(self, text, pos, color):
        self.font.drawText(text, pos, color)


class Text(GraphicObject):
    def __init__(self, text=None, rect=None, font=None, color=None, justification=GCX.TEXT_LEFT):
        if rect == None:
            pos = (0, 0)
        else:
            pos = (rect[0], rect[1])

        GraphicObject.__init__(self, pos)
        self.rect = rect
        self.text = text
        self.font = font
        self.justification = justification

        if color == None:
            self.color = (255, 255, 255, 255)
        else:
            self.color = color

    def setText(self, text):
        self.text = text

    def setRectangle(self, rect):
        self.rect = rect

    def setColor(self, color):
        self.color = color

    def setJustification(self, justification):
        self.justification = justification

    def draw(self, gcx):
        if self.text != None and self.rect != None and self.font != None:
            gcx.drawText(self.text, self.rect, self.font, self.color, self.justification)



