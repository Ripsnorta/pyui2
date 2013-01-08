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

import copy
import pyui2

import pyui2.system
from pyui2.system import GCX
from pyui2.system import Brush
from pyui2.system import Pen
from pyui2.system import Font

from pyui2.config import getImagePath


#############################################################################################################
##
#############################################################################################################
class PropertyList:

    #########################################################################################################
    ##
    #########################################################################################################
    def __init__(self):
        self.properties = {}

    #########################################################################################################
    ##
    #########################################################################################################
    def getProperty(self, propName):
        try:
            return self.properties[propName]
        except:
            return None

    #########################################################################################################
    ##
    #########################################################################################################
    def setProperty(self, propName, value=None):
        if value == None:
            self.properties[propName] = PropertyList()
        else:
            self.properties[propName] = value

        return self.properties[propName]




#############################################################################################################
##
#############################################################################################################
class ThemeBase(PropertyList):
    styles = {}
    themeStyles = {}

    #########################################################################################################
    ##
    #########################################################################################################
    def __init__(self):
        PropertyList.__init__(self)

        self.nextID = 0
        self.defaultFont = pyui2.system.Font("tahoma", 14, 0)

        # setup widget offsets
        (w, h) = self.defaultFont.getTextSize("Wp")
        self.tabsHeight = int(h * 1.3)

    #########################################################################################################
    ##
    #########################################################################################################
    def setPresenter(self, presenter):
        self.presenter = presenter
        #self.renderer = presenter.renderer

    #########################################################################################################
    ##
    #########################################################################################################
    def printPropertyTree(self, propList, indent=0):
        for key, value in  propList.iteritems():
            text = ' ' * (indent * 4) + repr(key)
            dots = 35 - len(text)
            print text, '.' * dots, value
            if isinstance(value, PropertyList):
                self.printPropertyTree(value.properties, indent+1)

    #########################################################################################################
    ##
    #########################################################################################################
    def findProp(self, aggProperty, propList):
        for testKey in aggProperty:
            value = propList[testKey]
            if isinstance(value, PropertyList):
                propList = value.properties

        return value

    #########################################################################################################
    ##
    #########################################################################################################
    def getAggProperty(self, aggProperty):
        try:
            return self.findProp(aggProperty, self.properties)
        except KeyError:
            return None

    #########################################################################################################
    ##
    #########################################################################################################
    def determineProp(self, propList, propertyName, defaultValue):
        pval = propList.getProperty(propertyName)
        if pval == None:
            pval = defaultValue

        return pval

    #########################################################################################################
    ##
    #########################################################################################################
    def loadMouseCursor(self, mouseCursor, offset, cursorName):
        self.presenter.loadMouseCursor(mouseCursor, offset, cursorName)

    #########################################################################################################
    ##
    #########################################################################################################
    def getDefaultFont(self):
        return self.getProperty("DEFAULT FONT")

    #########################################################################################################
    ##
    #########################################################################################################
    def setupTheme(self):
        #print "Setting up the theme"

        self.loadMouseCursor(getImagePath("cursor_pointer.png"), (11, 7), "pointer")
        self.loadMouseCursor(getImagePath("cursor_hand.png"), (11, 7), "hand")
        self.loadMouseCursor(getImagePath("cursor_drag.png"), (11, 7), "drag")
        self.loadMouseCursor(getImagePath("cursor_resize.png"), (15, 15), "resize")
        self.loadMouseCursor(getImagePath("cursor_text.png"), (11, 7), "text")
        self.loadMouseCursor(getImagePath("cursor_wait.png"), (11, 7), "wait")

        self.presenter.setCurrentMouseCursor("pointer")

        self.setProperty("DEFAULT FONT", self.defaultFont)

        windowProp = self.setProperty("WINDOW")
        windowProp.setProperty("function", self.drawWindow)

        panelProp = self.setProperty("PANEL")
        panelProp.setProperty("function", self.drawPanel)

        gridPanelProp = self.setProperty("GRIDPANEL")
        gridPanelProp.setProperty("function", self.drawGridPanel)

        frameProp = self.setProperty("FRAME")
        frameProp.setProperty("function", self.drawFrame)

        borderProp = frameProp.setProperty("BORDER")

        captionBarProp = self.setProperty("CAPTIONBAR")
        captionBarProp.setProperty("function", self.drawCaptionBar)

        titleProp = captionBarProp.setProperty("TITLE")

        buttonProp = captionBarProp.setProperty("BUTTONS")

        closeButtonProp = self.setProperty("CLOSEBUTTON")
        closeButtonProp.setProperty("function", self.drawCloseButton)

        minButtonProp = self.setProperty("MINBUTTON")
        minButtonProp.setProperty("function", self.drawMinimizeButton)

        maxButtonProp = self.setProperty("MAXBUTTON")
        maxButtonProp.setProperty("function", self.drawMaximizeButton)

        labelProp = self.setProperty("LABEL")
        labelProp.setProperty("function", self.drawLabel)

        buttonProp = self.setProperty("BUTTON")
        buttonProp.setProperty("function", self.drawButton)

        imgBtnProp = self.setProperty("IMAGEBUTTON")
        imgBtnProp.setProperty("function", self.drawImageButton)

        checkProp = self.setProperty("CHECKBOX")
        checkProp.setProperty("function", self.drawCheckBox)

        radioProp = self.setProperty("RADIOBUTTON")
        radioProp.setProperty("function", self.drawRadioButton)

        editProp = self.setProperty("EDIT")
        editProp.setProperty("function", self.drawEdit)

        sliderProp = self.setProperty("SLIDERBAR")
        sliderProp.setProperty("function", self.drawSliderBar)

        scrollProp = self.setProperty("SCROLLBAR")
        scrollProp.setProperty("function", self.drawScrollBar)

        tabPanelProp = self.setProperty("TABBEDPANEL")
        tabPanelProp.setProperty("function", self.drawTabbedPanel)

        tabBarProp = self.setProperty("TABBAR")
        tabBarProp.setProperty("function", self.drawTabBar)

        tabButtonProp = self.setProperty("TABBUTTON")
        tabButtonProp.setProperty("function", self.drawTabButton)

        tabScrollButtonProp = self.setProperty("TABSCROLLBUTTON")
        tabScrollButtonProp.setProperty("function", self.drawTabScrollButton)

        menuBarProp = self.setProperty("MENUBAR")
        menuBarProp.setProperty("function", self.drawMenuBar)

        menuProp = self.setProperty("MENU")
        menuProp.setProperty("function", self.drawMenu)

        listboxProp = self.setProperty("LISTBOX")
        listboxProp.setProperty("function", self.drawListBox)

        dropdownProp = self.setProperty("DROPDOWN")
        dropdownProp.setProperty("function", self.drawDropDown)

        splitterProp = self.setProperty("SPLITTER")
        splitterProp.setProperty("function", self.drawSplitter)

        tooltipProp = self.setProperty("TOOLTIP")
        tooltipProp.setProperty("function", self.drawToolTip)

        pictureProp = self.setProperty("PICTURE")
        pictureProp.setProperty("function", self.drawPicture)

        groupProp = self.setProperty("GROUP")
        groupProp.setProperty("function", self.drawGroup)

        treeProp = self.setProperty("TREE")
        treeProp.setProperty("function", self.drawTree)

        sheetProp = self.setProperty("SHEET")
        sheetProp.setProperty("function", self.drawSheet)

    #########################################################################################################
    ###
    ### Information about the theme..
    ###
    #########################################################################################################
    #########################################################################################################
    ##
    #########################################################################################################
    def getFrameBorderTop(self):
        borderWidth = self.getAggProperty(("FRAME", "BORDER", "width"))
        if borderWidth == None:
            borderWidth = 0
        return borderWidth

    #########################################################################################################
    ##
    #########################################################################################################
    def getFrameBorderLeft(self):
        borderWidth = self.getAggProperty(("FRAME", "BORDER", "width"))
        if borderWidth == None:
            borderWidth = 0
        return borderWidth

    #########################################################################################################
    ##
    #########################################################################################################
    def getFrameBorderRight(self):
        borderWidth = self.getAggProperty(("FRAME", "BORDER", "width"))
        if borderWidth == None:
            borderWidth = 0
        return borderWidth

    #########################################################################################################
    ##
    #########################################################################################################
    def getFrameBorderBottom(self):
        borderWidth = self.getAggProperty(("FRAME", "BORDER", "width"))
        if borderWidth == None:
            borderWidth = 0
        return borderWidth

    #########################################################################################################
    ##
    #########################################################################################################
    def getTabsHeight(self):
        return self.tabsHeight

    #########################################################################################################
    ##
    #########################################################################################################
    def getScrollerSize(self):
        scrollerSize = self.getAggProperty(("SCROLLBAR","scrollersize"))
        if scrollerSize == None:
            scrollerSize = 14
        return scrollerSize

        ### mouse cursor functions
    #########################################################################################################
    ##
    #########################################################################################################
    def setArrowCursor(self):
        self.presenter.setCurrentMouseCursor("pointer")

    #########################################################################################################
    ##
    #########################################################################################################
    def setResizeCursor(self):
        self.presenter.setCurrentMouseCursor("resize")

    #########################################################################################################
    ##
    #########################################################################################################
    def setButtonCursor(self):
        self.presenter.setCurrentMouseCursor("hand")

    #########################################################################################################
    ##
    #########################################################################################################
    def setWaitCursor(self):
        self.presenter.setCurrentMouseCursor("wait")

    #########################################################################################################
    ##
    #########################################################################################################
    def setMovingCursor(self):
        self.presenter.setCurrentMouseCursor("drag")


    #########################################################################################################
    ###
    ###   Utility drawing functions not specific to any widgets
    ###
    #########################################################################################################
    #########################################################################################################
    ##
    #########################################################################################################
    def draw(self, widgetName, widget, graphicsContext, parentRect=None):
        widgetProperties = self.getProperty(widgetName)

        drawingFunction = None

        if widgetProperties != None:
            drawingFunction = widgetProperties.getProperty("function")

        if drawingFunction != None:
            drawingFunction(widget, graphicsContext, widgetProperties, parentRect)
        else:
            self.drawUnknown(widget, graphicsContext, widgetProperties, parentRect)


    #########################################################################################################
    ##
    #########################################################################################################
    def getDrawingArea(self, widget, widgetProperties):
        topMargin = widgetProperties.getProperty("topMargin")
        leftMargin = widgetProperties.getProperty("leftMargin")
        bottomMargin = widgetProperties.getProperty("bottomMargin")
        rightMargin = widgetProperties.getProperty("rightMargin")
        rect = (widget.posX + leftMargin,
                widget.posY + topMargin,
                widget.width - rightMargin,
                widget.height - bottomMargin)

        return rect


    #########################################################################################################
    ##
    #########################################################################################################
    def calcWidgetRect(self, widget, parentRect):
        offsetX = 0
        offsetY = 0
        #if parentRect != None:
        #    offsetX = parentRect[0]
        #    offsetY = parentRect[1]

        rect = (int(widget.posX+offsetX), int(widget.posY+offsetY), int(widget.width), int(widget.height))
        return rect


    #########################################################################################################
    ##
    #########################################################################################################
    def draw3DRect(self, graphicsContext, rect, color, reverse=0, thick=1, filled=False):
        """Draw a 3D rectangle
        """
        (r,g,b,a) = color
        penLo = pyui2.system.Pen(thick, (0,0,0,255), pyui2.system.Pen.STYLE_SOLID)
        penHi = pyui2.system.Pen(thick, (255- r/4, 255-g/4, 255-b/4, 255), pyui2.system.Pen.STYLE_SOLID)
        brush = pyui2.system.Brush(color, pyui2.system.Brush.STYLE_SOLID)
        if reverse:
            (penLo, penHi) = (penHi, penLo)

        (x,y,w,h) = (int(rect[0]), int(rect[1]), int(rect[2]), int(rect[3]))
        if w < 2 or h < 2:
            return

        if filled == True:
            graphicsContext.drawFilledRect(rect, brush)

        graphicsContext.drawRect((x, y, w-thick, thick), penHi)
        graphicsContext.drawRect((x, y+thick, thick, h-thick), penHi)
        if w > 2 and h > 2:
            graphicsContext.drawRect((x+thick, y+thick, w-thick*2, h-thick*2), penLo)
        graphicsContext.drawRect((x+thick, y+h-thick, w-thick, thick), penLo)
        graphicsContext.drawRect((x+w-thick, y+thick, thick, h-thick*2), penLo)


    #########################################################################################################
    ##
    #########################################################################################################
    def getNextID(self):
        self.nextID = self.nextID + 1
        return self.nextID

    def createDefaultFont(self, face, size, flags):
        #self.defaultFont = getRenderer().createFont(face, size, flags)
        pass

    #########################################################################################################
    ###
    ### Widgets specific drawing functions.
    ### These are the methods for actual themes to implement.
    ###
    #########################################################################################################
    #########################################################################################################
    ##
    #########################################################################################################
    def drawUnknown(self, widget, graphicsContext, widgetProperties, parentRect=None):
        rect = self.calcWidgetRect(widget, parentRect)
        graphicsContext.drawRect(rect, pyui2.system.Pen(1, (0, 0, 0, 255), pyui2.system.Pen.STYLE_SOLID))

    #########################################################################################################
    ##
    #########################################################################################################
    def drawWindow(self, widget, graphicsContext, widgetProperties, parentRect=None):
        rect = (0, 0, widget.width, widget.height)
        backgroundBrush = self.determineProp(widgetProperties, "background", Brush((255, 255, 255, 255), Brush.STYLE_SOLID))
        graphicsContext.drawFilledRect(rect, backgroundBrush)

    #########################################################################################################
    ##
    #########################################################################################################
    def drawPanel(self, widget, graphicsContext, widgetProperties, parentRect=None):
        rect = self.calcWidgetRect(widget, parentRect)
        backgroundBrush = self.determineProp(widgetProperties, "background", Brush((180, 180, 180, 255), Brush.STYLE_SOLID))
        graphicsContext.drawFilledRect(rect, backgroundBrush)

    #########################################################################################################
    ##
    #########################################################################################################
    def drawGridPanel(self, widget, graphicsContext, widgetProperties, parentRect=None):
        rect = self.calcWidgetRect(widget, parentRect)
        backgroundBrush = self.determineProp(widgetProperties, "background", Brush((255, 255, 255, 255), Brush.STYLE_SOLID))
        gridPen = self.determineProp(widgetProperties, "button", Pen(1, (0, 0, 0, 255), pyui2.system.Pen.STYLE_SOLID))

        rectObj = pyui2.system.Rectangle(rect, gridPen, backgroundBrush)
        graphicsContext.drawGraphicObject(rectObj)

        xpos = rect[0]
        ypos = rect[1]
        w = rect[2]
        h = rect[3]
        cellw = w / widget.vWidth
        cellh = h / widget.vHeight

        lineObj = pyui2.system.Line(None, gridPen)
        for x in range(0, widget.vWidth+1):
            lineObj.setPoints(((xpos + x * cellw, ypos), (xpos + x * cellw, ypos + h)))
            graphicsContext.drawGraphicObject(lineObj)

        for y in range(0,widget.vHeight):
            lineObj.setPoints(((xpos, ypos + y * cellh), (xpos + w, ypos + y * cellh)))
            graphicsContext.drawGraphicObject(lineObj)



    #########################################################################################################
    ##
    #########################################################################################################
    def drawGroup(self, widget, graphicsContext, widgetProperties, parentRect=None):
        rect = self.calcWidgetRect(widget, parentRect)
        borderPen = self.determineProp(widgetProperties, "border", Pen(1, (92, 92, 92, 255), Pen.STYLE_SOLID))
        graphicsContext.drawRect(rect, borderPen)

    #########################################################################################################
    ##
    #########################################################################################################
    def drawFrame(self, widget, graphicsContext, widgetProperties, parentRect=None):
        rect = (0, 0, widget.width, widget.height)

        backgroundBrush = self.determineProp(widgetProperties, "background", Brush((255, 255, 255, 255), Brush.STYLE_SOLID))

        graphicsContext.drawFilledRect(rect, backgroundBrush)

        if not widget.borderless:
            borderProperties = widgetProperties.getProperty("BORDER")
            width = self.determineProp(borderProperties, "width", 0)
            color = self.determineProp(borderProperties, "color", (0, 0, 100, 255))

            borderRect = rect
            if width > 2:
                halfWidth = width / 2
                borderRect = (rect[0] + halfWidth - 1, rect[1] + halfWidth - 1, rect[2] - halfWidth, rect[3] - halfWidth)

            graphicsContext.drawRect(borderRect, pyui2.system.Pen(width, color, pyui2.system.Pen.STYLE_SOLID))

        if widget.frameResizing:
            pass # Draw the resizing widgets

    #########################################################################################################
    ##
    #########################################################################################################
    def drawCloseButton(self, widget, graphicsContext, widgetProperties, drawingArea):
        rect = self.calcWidgetRect(widget, None)
        backgroundBrush = self.determineProp(widgetProperties, "background", Brush((255, 255, 255, 255), Brush.STYLE_SOLID))
        buttonPen = self.determineProp(widgetProperties, "button", Pen(1, (0, 0, 0, 255), pyui2.system.Pen.STYLE_SOLID))

        drawList = widgetProperties.getProperty("drawlist")
        if drawList == None:
            graphicsContext.drawFilledRect(rect, backgroundBrush)
            graphicsContext.drawRect(rect, buttonPen)

            graphicsContext.drawLine(((rect[0] + 2, rect[1] + 2), (rect[0] + rect[2] - 2, rect[1] + rect[3] - 2)), buttonPen)
            graphicsContext.drawLine(((rect[0] + rect[2] - 2, rect[1] + 2), (rect[0] + 2, rect[1] + rect[3] - 2)), buttonPen)
        else:
            for item in drawList:
                # Make a copy of the drawing object since we are about to change its position to be relative
                # to the parent.
                grob = copy.copy(item)
                grob.setRectangle(rect)
                graphicsContext.drawGraphicObject(grob)

    #########################################################################################################
    ##
    #########################################################################################################
    def drawMinimizeButton(self, widget, graphicsContext, widgetProperties, drawingArea):
        rect = self.calcWidgetRect(widget, None)

    def drawMaximizeButton(self, widget, graphicsContext, widgetProperties, drawingArea):
        rect = self.calcWidgetRect(widget, None)

    #########################################################################################################
    ##
    #########################################################################################################
    def drawCaptionBar(self, widget, graphicsContext, widgetProperties, parentRect=None):
        rect = self.calcWidgetRect(widget, None)
        textRect = (widget.textRect[0] + widget.posX, widget.textRect[1] + widget.posY, widget.textRect[2], widget.textRect[3])

        backgroundBrush = self.determineProp(widgetProperties, "background", Brush((192, 192, 192, 255), Brush.STYLE_SOLID))
        font = self.determineProp(widgetProperties, "font", self.getProperty("DEFAULT FONT"))
        fontColor = self.determineProp(widgetProperties, "fontcolor", (255, 255, 255, 255))
        justification = self.determineProp(widgetProperties, "justified", "left")

        graphicsContext.drawFilledRect(rect, backgroundBrush)

        textObj = pyui2.system.Text(widget.text, textRect, font)
        graphicsContext.drawGraphicObject(textObj)

    #########################################################################################################
    ##
    #########################################################################################################
    def drawTabbedPanel(self, widget, graphicsContext, widgetProperties, parentRect=None):
        rect = self.calcWidgetRect(widget, parentRect)
        backgroundBrush = self.determineProp(widgetProperties, "background", Brush((200, 200, 200, 255), Brush.STYLE_SOLID))
        graphicsContext.drawFilledRect(rect, backgroundBrush)

    #########################################################################################################
    ##
    #########################################################################################################
    def drawTabBar(self, widget, graphicsContext, widgetProperties, parentRect=None):
        rect = self.calcWidgetRect(widget, parentRect)
        backgroundBrush = self.determineProp(widgetProperties, "background", Brush((222, 222, 222, 255), Brush.STYLE_SOLID))
        graphicsContext.drawFilledRect(rect, backgroundBrush)

    #########################################################################################################
    ##
    #########################################################################################################
    def drawTabButton(self, widget, graphicsContext, widgetProperties, parentRect=None):
        rect = self.calcWidgetRect(widget, parentRect)

        if widget.show:
            backgroundBrush = self.determineProp(widgetProperties, "background", Brush((192, 192, 192, 255), Brush.STYLE_SOLID))
            font = self.determineProp(widgetProperties, "font", self.getProperty("DEFAULT FONT"))
            fontColor = self.determineProp(widgetProperties, "fontcolor", (0, 0, 0, 255))

            graphicsContext.drawFilledRect(rect, backgroundBrush)

            if widget.text != "":
                textObj = pyui2.system.Text(widget.text, rect, font, fontColor, GCX.TEXT_CENTER)

                if widget.selected == True:
                    offsetRect = (rect[0] + 1, rect[1] + 1, rect[2], rect[3])
                    textObj.setRectangle(offsetRect)
                    graphicsContext.drawGraphicObject(textObj)

                textObj.setRectangle(rect)
                graphicsContext.drawGraphicObject(textObj)

    #########################################################################################################
    ##
    #########################################################################################################
    def drawTabScrollButton(self, widget, graphicsContext, widgetProperties, parentRect=None):
        if widget.show:
            rect = self.calcWidgetRect(widget, parentRect)
            backgroundBrush = self.determineProp(widgetProperties, "background", Brush((192, 192, 192, 255), Brush.STYLE_SOLID))
            borderPen = self.determineProp(widgetProperties, "border", Pen(1, (0, 0, 0, 255), Pen.STYLE_SOLID))

            rectObj = pyui2.system.Rectangle(rect, borderPen, backgroundBrush)
            graphicsContext.drawGraphicObject(rectObj)

            drawList = widgetProperties.getProperty("drawlist")
            if drawList == None:
                (x, y, w, h) = rect
                triBrush = Brush((0, 0, 0, 255), Brush.STYLE_SOLID)

                if widget.direction == 0:       #DIRECT_LEFT
                    points = ((x+w-3, y+3), (x+w-3, y+h-3), (x+3, y+(h/2)))
                elif widget.direction == 1:     #DIRECT_RIGHT
                    points = ((x+3, y+3), (x+w-3, y+(h/2)), (x+3, y+h-3))
                else:
                    return

                triObj = pyui2.system.Polygon(points, None, triBrush)
                graphicsContext.drawGraphicObject(triObj)
            else:
                for item in drawList:
                    # Make a copy of the drawing object since we are about to change its position to be relative
                    # to the parent.
                    grob = copy.copy(item)
                    grob.setRectangle(rect)
                    graphicsContext.drawGraphicObject(grob)


    #########################################################################################################
    ##
    #########################################################################################################
    def drawLabel(self, widget, graphicsContext, widgetProperties, parentRect=None):
        rect = self.calcWidgetRect(widget, parentRect)
        font = self.determineProp(widgetProperties, "font", self.getProperty("DEFAULT FONT"))
        fontColor = self.determineProp(widgetProperties, "fontcolor", (0, 0, 0, 255))

        if widget.border:
            borderPen = self.determineProp(widgetProperties, "border", pyui2.system.Pen(1, (0, 0, 0, 255), pyui2.system.Pen.STYLE_SOLID))
            borderObj = pyui2.system.Rectangle(rect, borderPen, None)
            graphicsContext.drawGraphicObject(borderObj)

        textObj = pyui2.system.Text(widget.text, rect, font, fontColor)
        textObj.setJustification(widget.align)

        if widget.shadow:
            shadowOffset = self.determineProp(widgetProperties, "shadowoffset", 1)
            shadowColor = self.determineProp(widgetProperties, "shadowcolor", (50, 50, 50, 255))

            offsetRect = (rect[0] + shadowOffset, rect[1] + shadowOffset, rect[2], rect[3])
            textObj.setRectangle(offsetRect)
            textObj.setColor(shadowColor)
            graphicsContext.drawGraphicObject(textObj)

        textObj.setRectangle(rect)
        textObj.setColor(fontColor)
        graphicsContext.drawGraphicObject(textObj)

    #########################################################################################################
    ##
    #########################################################################################################
    def drawButton(self, widget, graphicsContext, widgetProperties, parentRect=None):
        rect = self.calcWidgetRect(widget, parentRect)

        font = self.determineProp(widgetProperties, "font", self.getProperty("DEFAULT FONT"))
        fontColor = self.determineProp(widgetProperties, "fontcolor", (0, 0, 0, 255))
        color = self.determineProp(widgetProperties, "color", (0, 0, 0, 255))
        backgroundBrush = self.determineProp(widgetProperties, "background", Brush((192, 192, 192, 255), Brush.STYLE_SOLID))

        if widget.status == 2:
            rev = 1
        else:
            rev = 0

        rectObj = pyui2.system.Rectangle(rect, None, backgroundBrush)
        graphicsContext.drawGraphicObject(rectObj)
        self.draw3DRect(graphicsContext, rect, color, rev)
        if widget.text != "":
            graphicsContext.drawText(widget.text, rect, font, fontColor, GCX.TEXT_CENTER)

    #########################################################################################################
    ##
    #########################################################################################################
    def drawImageButton(self, widget, graphicsContext, widgetProperties, parentRect=None):
        rect = self.calcWidgetRect(widget, parentRect)

        if widget.status == 0:      # Normal
            img = self.presenter.getImage(widget.filename)
        elif widget.status == 1:    # Mouseover
            img = self.presenter.getImage(widget.mouseOverFilename)
        else:                       # Selected
            img = self.presenter.getImage(widget.selectFilename)

        graphicsContext.drawImage(img, rect)

        if widget.border:
            thick = 2
            if widget.hasFocus:
                thick = 3

            borderPen = self.determineProp(widgetProperties, "border", Pen(thick, (0, 0, 0, 255), Pen.STYLE_SOLID))
            borderRect = pyui2.system.Rectangle(rect, borderPen)
            graphicsContext.drawGraphicObject(borderRect)

    #########################################################################################################
    ##
    #########################################################################################################
    def drawCheckBox(self, widget, graphicsContext, widgetProperties, parentRect=None):
        rect = self.calcWidgetRect(widget, parentRect)

        font = self.determineProp(widgetProperties, "font", self.getProperty("DEFAULT FONT"))
        fontColor = self.determineProp(widgetProperties, "fontcolor", (0, 0, 0, 255))
        color = self.determineProp(widgetProperties, "color", (0, 0, 0, 255))

        boxRect = (rect[0], rect[1], 16, 16)
        boxPen = pyui2.system.Pen(1, color, pyui2.system.Pen.STYLE_SOLID)
        box = pyui2.system.Rectangle(boxRect, boxPen)
        graphicsContext.drawGraphicObject(box)

        if widget.checkState:
            pts1 = ((boxRect[0] + 1, boxRect[1] + 1), (boxRect[0] + boxRect[2] - 1, boxRect[1] + boxRect[3] - 1))
            pts2 = ((boxRect[0] + boxRect[2] - 1, boxRect[1] + 1), (boxRect[0] + 1, boxRect[1] + boxRect[3] - 1))
            chkLine1 = pyui2.system.Line(pts1, boxPen)
            chkLine2 = pyui2.system.Line(pts2, boxPen)
            graphicsContext.drawGraphicObject(chkLine1)
            graphicsContext.drawGraphicObject(chkLine2)

        textRect = (rect[0] + 20, rect[1], rect[2] - 20, rect[3])
        textObj = pyui2.system.Text(widget.text, textRect, font, fontColor)
        graphicsContext.drawGraphicObject(textObj)

    #########################################################################################################
    ##
    #########################################################################################################
    def drawRadioButton(self, widget, graphicsContext, widgetProperties, parentRect=None):
        rect = self.calcWidgetRect(widget, parentRect)

        font = self.determineProp(widgetProperties, "font", self.getProperty("DEFAULT FONT"))
        fontColor = self.determineProp(widgetProperties, "fontcolor", (0, 0, 0, 255))
        color = self.determineProp(widgetProperties, "color", (0, 0, 0, 255))

        circleRect = (rect[0], rect[1], 16, 16)
        circlePen = pyui2.system.Pen(1, color, pyui2.system.Pen.STYLE_SOLID)
        circle = pyui2.system.Circle(None, None, circlePen)
        circle.setRectangle(circleRect)
        graphicsContext.drawGraphicObject(circle)

        if widget.checkState:
            innerRect = (circleRect[0] + 3, circleRect[1] + 3, 10, 10)
            circleBrush = pyui2.system.Brush(color, pyui2.system.Brush.STYLE_SOLID)
            circle = pyui2.system.Circle(None, None, None, circleBrush)
            circle.setRectangle(innerRect)
            graphicsContext.drawGraphicObject(circle)

        textRect = (rect[0] + 20, rect[1], rect[2] - 20, rect[3])
        textObj = pyui2.system.Text(widget.text, textRect, font, fontColor)
        graphicsContext.drawGraphicObject(textObj)

    #########################################################################################################
    ##
    #########################################################################################################
    def drawSliderBar(self, widget, graphicsContext, widgetProperties, parentRect=None):
        rect = self.calcWidgetRect(widget, parentRect)

        bgBrush = self.determineProp(widgetProperties, "background", Brush((192, 192, 192, 255), Brush.STYLE_SOLID))
        color = self.determineProp(widgetProperties, "color", (192, 192, 192, 255))

        bgRect = pyui2.system.Rectangle(rect, None, bgBrush)
        graphicsContext.drawGraphicObject(bgRect)

        barWidth = widget.BARWIDTH
        if barWidth == None:
            barWidth = 8

        barHeight = rect[3] - 4
        if barHeight > 20:
            barHeight = 20

        interval = int(rect[2] / float(widget.range))
        half = int(rect[1] + rect[3]/2)

        self.draw3DRect(graphicsContext, (rect[0] + 1, half, rect[2] - 2, 3), color, 1, 1, True)

        diff = rect[2] - barWidth
        xpos = float(diff) / widget.range * widget.position

        self.draw3DRect(graphicsContext, (rect[0] + xpos, int(rect[1] + (rect[3]/2) - (barHeight/2)), int(barWidth), int(barHeight)), color, 0, 1, True)

    #########################################################################################################
    ##
    #########################################################################################################
    def drawEdit(self, widget, graphicsContext, widgetProperties, parentRect=None):
        rect = self.calcWidgetRect(widget, parentRect)
        (x,y,w,h) = rect

        frameColor = self.determineProp(widgetProperties, "framecolor", (192, 192, 192, 255))
        bgBrush = self.determineProp(widgetProperties, "background", Brush((255, 255, 255, 255), Brush.STYLE_SOLID))
        font = self.determineProp(widgetProperties, "font", self.getProperty("DEFAULT FONT"))
        fontColor = self.determineProp(widgetProperties, "fontcolor", (0, 0, 0, 255))
        buttonColor = self.determineProp(widgetProperties, "buttoncolor", (192, 192, 192, 255))
        selectColor = self.determineProp(widgetProperties, "selectcolor", (bgBrush.color[0]^255, bgBrush.color[1]^255, bgBrush.color[2]^255, 255))
        fontSelectColor = self.determineProp(widgetProperties, "fontselectcolor", (selectColor[0]^255, selectColor[1]^255, selectColor[2]^255, 255))

        rectObj = pyui2.system.Rectangle(rect, None, bgBrush)
        textObj = pyui2.system.Text(widget.text, rect, font, fontColor)
        graphicsContext.drawGraphicObject(rectObj)
        self.draw3DRect(graphicsContext, rect, frameColor, 1)
        graphicsContext.drawGraphicObject(textObj)

        if widget.hasFocus:
            caretX, textHeight = font.getTextSize(widget.text[0:widget.caretPos])
            if widget.readOnly == 0 and widget.selectPos != None:
                # draw selection highlight
                textSelectStart = min(widget.caretPos, widget.selectPos)
                textSelectEnd = max(widget.caretPos, widget.selectPos)
                selectX = font.getTextSize(widget.text[0:widget.selectPos])[0]
                selectX0 = min(caretX, selectX)
                selectX1 = max(caretX, selectX)
                if selectX0 < selectX1:
                    if selectX1 > rect[2]:
                        selectX1 = rect[2]

                    selectRect =(x+1+selectX0, y+1, selectX1-selectX0, textHeight)
                    selBrush = pyui2.system.Brush(selectColor, pyui2.system.Brush.STYLE_SOLID)
                    selectRectObj = pyui2.system.Rectangle(selectRect, None, selBrush)
                    selText = widget.text[textSelectStart:textSelectEnd]
                    graphicsContext.drawGraphicObject(selectRectObj)
                    if selText != None:
                        selectRect =(x+selectX0, y, selectX1-selectX0, textHeight)
                        selectTextObj = pyui2.system.Text(selText, selectRect, font, fontSelectColor)
                        graphicsContext.drawGraphicObject(selectTextObj)

            if widget.readOnly == 0:
                # Draw the caret
                if (x + caretX) < (widget.posX + rect[2]):
                    caretPen = pyui2.system.Pen(1, fontColor, pyui2.system.Pen.STYLE_SOLID)
                    caretPoints = ((x+caretX, y+1), (x+caretX, y+textHeight-2))
                    graphicsContext.drawLine(caretPoints, caretPen)

    #########################################################################################################
    ##
    #########################################################################################################
    def drawMenuBar(self, widget, graphicsContext, widgetProperties, parentRect=None):
        #rect = self.calcWidgetRect(widget, parentRect)
        rect = (0, 0, int(widget.rect[2]), int(widget.rect[3]))

        if widget.show:
            frameColor = self.determineProp(widgetProperties, "framecolor", (192, 192, 192, 255))
            menuColor = self.determineProp(widgetProperties, "menucolor", (192, 192, 192, 255))
            font = self.determineProp(widgetProperties, "font", self.getProperty("DEFAULT FONT"))
            fontColor = self.determineProp(widgetProperties, "fontcolor", (0, 0, 0, 255))
            buttonColor = self.determineProp(widgetProperties, "buttoncolor", (192, 192, 192, 255))
            selectColor = self.determineProp(widgetProperties, "selectcolor", (menuColor[0]^255, menuColor[1]^255, menuColor[2]^255, 255))
            fontSelectColor = self.determineProp(widgetProperties, "fontselectcolor", (selectColor[0]^255, selectColor[1]^255, selectColor[2]^255, 255))

            self.draw3DRect(graphicsContext, rect, frameColor, 1, 1, True)

            selBrush = pyui2.system.Brush(selectColor, pyui2.system.Brush.STYLE_SOLID)

            h = widget.height - 2 * widget.border
            x = widget.border
            for menu in widget.menus:
                (w,h) = font.getTextSize(menu.menuTitle)
                w = int(w * 1.33)

                menuRect = (x, rect[1], w, h)
                if menu == widget.highlight:
                    rectObj = pyui2.system.Rectangle(menuRect, None, selBrush)
                    graphicsContext.drawGraphicObject(rectObj);
                    textColor = fontSelectColor
                else:
                    textColor = fontColor

                textObj = pyui2.system.Text(menu.menuTitle, menuRect, font, textColor)
                textObj.setJustification(GCX.TEXT_CENTER)
                graphicsContext.drawGraphicObject(textObj);

                x += w

    #########################################################################################################
    ##
    #########################################################################################################
    def drawMenu(self, widget, graphicsContext, widgetProperties, parentRect=None):
        rect = (0, 0, int(widget.rect[2]), int(widget.rect[3]))
        if widget.show:
            frameColor = self.determineProp(widgetProperties, "framecolor", (192, 192, 192, 255))
            menuColor = self.determineProp(widgetProperties, "menucolor", (192, 192, 192, 255))
            font = self.determineProp(widgetProperties, "font", self.getProperty("DEFAULT FONT"))
            fontColor = self.determineProp(widgetProperties, "fontcolor", (0, 0, 0, 255))
            buttonColor = self.determineProp(widgetProperties, "buttoncolor", (192, 192, 192, 255))
            selectColor = self.determineProp(widgetProperties, "selectcolor", (menuColor[0]^255, menuColor[1]^255, menuColor[2]^255, 255))
            fontSelectColor = self.determineProp(widgetProperties, "fontselectcolor", (selectColor[0]^255, selectColor[1]^255, selectColor[2]^255, 255))

            selBrush = pyui2.system.Brush(selectColor, pyui2.system.Brush.STYLE_SOLID)

            self.draw3DRect(graphicsContext, rect, frameColor, 1, 1, True)

            y = widget.border
            for item in widget.items:
                textHeight = font.getTextSize(item.text)[1] + widget.border
                itemRect = item.rect#(widget.posX+widget.border, widget.posY+y, rect[2], textHeight)
                if item == widget.active:
                    rectObj = pyui2.system.Rectangle(itemRect, None, selBrush)
                    graphicsContext.drawGraphicObject(rectObj);
                    textColor = fontSelectColor
                else:
                    textColor = fontColor

                textObj = pyui2.system.Text(item.text, itemRect, font, textColor)
                graphicsContext.drawGraphicObject(textObj);

                y += textHeight

    #########################################################################################################
    ##
    #########################################################################################################
    def drawScrollBar(self, widget, graphicsContext, widgetProperties, parentRect=None):
        rect = self.calcWidgetRect(widget, parentRect)

        if widget.show:
            buttonColor = self.determineProp(widgetProperties, "buttoncolor", (192, 192, 192, 255))
            backBrush = self.determineProp(widgetProperties, "background", Brush((222, 222, 222, 255), Brush.STYLE_SOLID))

            (x,y,w,h)=(rect[0], rect[1]+1, rect[2]-1, rect[3]-2)
            backRect = pyui2.system.Rectangle((x,y,w,h), None, backBrush)
            graphicsContext.drawGraphicObject(backRect)

            scrollerSize = widgetProperties.getProperty("scrollersize")
            if scrollerSize == None:
                scrollerSize = 14

            if widget.alignment == 'v':
                upButtonRect = (x, y, w, scrollerSize)
                dnButtonRect = (x, y + h - scrollerSize, w, scrollerSize)
                scrollButtonRect = (x, y + widget.pos, w, widget.barSize)
            else:
                upButtonRect = (x, y, scrollerSize, h)
                dnButtonRect = (x + w - scrollerSize, y, scrollerSize, h)
                scrollButtonRect = (x + widget.pos, y, widget.barSize, h)

            self.draw3DRect(graphicsContext, upButtonRect, buttonColor, 0, 1, True)
            self.draw3DRect(graphicsContext, dnButtonRect, buttonColor, 0, 1, True)
            self.draw3DRect(graphicsContext, scrollButtonRect, buttonColor, 0, 1, True)


    #########################################################################################################
    ##
    #########################################################################################################
    def drawDropDown(self, widget, graphicsContext, widgetProperties, parentRect=None):
        rect = self.calcWidgetRect(widget, parentRect)
        if widget.show:
            borderPen = self.determineProp(widgetProperties, "border", Pen(1, (0, 0, 0, 255), Pen.STYLE_SOLID))
            backBrush = self.determineProp(widgetProperties, "background", Brush((255, 255, 255, 255), Brush.STYLE_SOLID))
            font = self.determineProp(widgetProperties, "font", self.getProperty("DEFAULT FONT"))
            fontColor = self.determineProp(widgetProperties, "fontcolor", (0, 0, 0, 255))
            buttonColor = self.determineProp(widgetProperties, "buttoncolor", (192, 192, 192, 255))

            frameRectObj = pyui2.system.Rectangle(rect, borderPen, backBrush)
            graphicsContext.drawGraphicObject(frameRectObj)

            text = ""
            if widget.selectionList.selected != -1:
                item = widget.selectionList.getSelectedItem()
                if item:
                    text = item.name

            buttonSize = rect[3] - 2
            buttonRect = (rect[0]+rect[2] - buttonSize, rect[1]+1, buttonSize, buttonSize)
            self.draw3DRect(graphicsContext, buttonRect, buttonColor, 0, 1, True)

            textObj = pyui2.system.Text(text, rect, font, fontColor)
            graphicsContext.drawGraphicObject(textObj);

    #########################################################################################################
    ##
    #########################################################################################################
    def drawSplitter(self, widget, graphicsContext, widgetProperties, parentRect=None):
        rect = self.calcWidgetRect(widget, parentRect)
        frameBorderWidth = self.getAggProperty(("FRAME", "BORDER", "width"))
        frameBorderColor = self.getAggProperty(("FRAME", "BORDER", "color"))
        self.draw3DRect(rect, frameBorderColor)

    #########################################################################################################
    ##
    #########################################################################################################
    def drawToolTip(self, widget, graphicsContext, widgetProperties, parentRect=None):
        rect = self.calcWidgetRect(widget, parentRect)
#        (text) = params
#        self.renderer.drawRect(pyui2.colors.black, rect)
#        self.renderer.drawRect(pyui2.colors.yellow, (rect[0] + 1, rect[1] + 1, rect[2] - 2, rect[3] - 2))
#        self.renderer.drawText(text, (rect[0] + 2, rect[1] + 2), pyui2.colors.black)
#
    #########################################################################################################
    ##
    #########################################################################################################
    def drawPicture(self, widget, graphicsContext, widgetProperties, parentRect=None):
        rect = self.calcWidgetRect(widget, parentRect)
        img = self.presenter.getImage(widget.filename)
        graphicsContext.drawImage(img, rect)

    #########################################################################################################
    ##
    #########################################################################################################
    def drawListBox(self, widget, graphicsContext, widgetProperties, parentRect=None):
        rect = self.calcWidgetRect(widget, parentRect)
        if widget.show:
            borderPen = self.determineProp(widgetProperties, "border", Pen(1, (0, 0, 0, 255), Pen.STYLE_SOLID))
            backBrush = self.determineProp(widgetProperties, "background", Brush((255, 255, 255, 255), Brush.STYLE_SOLID))
            selectColor = self.determineProp(widgetProperties, "selectcolor", (backBrush.color[0]^255, backBrush.color[1]^255, backBrush.color[2]^255, 255))
            font = self.determineProp(widgetProperties, "font", self.getProperty("DEFAULT FONT"))
            fontColor = self.determineProp(widgetProperties, "fontcolor", (0, 0, 0, 255))
            fontSelectColor = self.determineProp(widgetProperties, "fontselectcolor", (selectColor[0]^255, selectColor[1]^255, selectColor[2]^255, 255))

            scrollerSize = self.getAggProperty(("SCROLLBAR", "scrollersize"))
            if scrollerSize == None:
                scrollerSize = 14

            frameRectObj = pyui2.system.Rectangle(rect, borderPen, backBrush)
            graphicsContext.drawGraphicObject(frameRectObj)

            i = 0
            (textWidth, textHeight) = font.getTextSize("x")
            selBrush = pyui2.system.Brush(selectColor, pyui2.system.Brush.STYLE_SOLID)

            for item in widget.items:
                if i >= widget.topItem and i < widget.topItem + widget.numVisible:
                    itemRect = (rect[0] + 1, rect[1] + 2 + (i - widget.topItem) * textHeight, widget.width - scrollerSize, textHeight - 2)
                    itemText = item.name
                    if i == widget.selected:
                        rectObj = pyui2.system.Rectangle(itemRect, None, selBrush)
                        graphicsContext.drawGraphicObject(rectObj);
                        textColor = fontSelectColor
                    else:
                        textColor = fontColor

                    textObj = pyui2.system.Text(itemText, itemRect, font, textColor)
                    graphicsContext.drawGraphicObject(textObj);

                i = i + 1

    #########################################################################################################
    ##
    #########################################################################################################
    def drawNode(self, node, graphicsContext, pos, props, counter):
        (linePen, font, fontColor, backgroundBrush, selColor, fontSelColor) = props
        (x, y) = pos
        (itemCount, numItems, top) = counter

        nodePen = pyui2.system.Pen(1, (0, 0, 0, 255), Pen.STYLE_SOLID)

        iconX = x + 16
        textX = iconX + 16
        lineStartY = -1
        lineEndY = 0

        for subnode in node.nodes:
            if itemCount >= numItems + top:
                break

            if itemCount >= top:
                textSize = font.getTextSize(subnode.title)
                itemRect = (textX, y, textSize[0], textSize[1])

                textColor = fontColor
                if subnode.selected:
                    textColor = fontSelColor
                    selBrush = Brush(selColor, Brush.STYLE_SOLID)
                    selRect = pyui2.system.Rectangle(itemRect, None, selBrush)
                    graphicsContext.drawGraphicObject(selRect);

                textObj = pyui2.system.Text(subnode.title, itemRect, font, textColor)
                graphicsContext.drawGraphicObject(textObj);

                lineY = y + (textSize[1] / 2)
                graphicsContext.drawLine(((x, lineY), (iconX, lineY)), linePen)

                if lineStartY == -1:
                    lineStartY = lineY

                lineEndY = lineY

                y += textSize[1]

            itemCount += 1

            if len(subnode.nodes) > 0:
                if subnode.status == pyui2.widgets.Tree.OPEN:
                    (y, itemCount) = self.drawNode(subnode, graphicsContext, (iconX + 8, y), props, (itemCount, numItems, top))

        graphicsContext.drawLine(((x, lineStartY), (x, lineEndY)), linePen)

        return (y, itemCount)

    #########################################################################################################
    ##
    #########################################################################################################
    def drawNodeButtons(self, node, graphicsContext, pos, props, counter):
        (font, buttonPen, backgroundBrush) = props
        (x, y) = pos
        (itemCount, numItems, top) = counter

        iconX = x + 16
        textX = iconX + 16
        lineStartY = -1

        for node in node.nodes:
            if itemCount >= numItems + top:
                break

            if itemCount >= top:
                #print y
                textSize = font.getTextSize(node.title)
                itemRect = (textX, y, textSize[0], textSize[1])

                #print y, textSize
                lineY = y + (textSize[1] / 2)
                y += textSize[1]

                if len(node.nodes) > 0:
                    nodeRect = (x - 4, lineY - 4, 9, 9)
                    graphicsContext.drawFilledRect(nodeRect, backgroundBrush)
                    graphicsContext.drawRect(nodeRect, buttonPen)

                    if node.status == pyui2.widgets.Tree.CLOSED:
                        graphicsContext.drawLine(((x - 2, lineY), (x + 2, lineY)), buttonPen,)
                        graphicsContext.drawLine(((x, lineY - 2), (x, lineY + 2)), buttonPen,)
                    elif node.status == pyui2.widgets.Tree.OPEN:
                        graphicsContext.drawLine(((x - 2, lineY), (x + 2, lineY)), buttonPen,)


            itemCount += 1

            if len(node.nodes) > 0 and node.status == pyui2.widgets.Tree.OPEN:
                    (y, itemCount) = self.drawNodeButtons(node, graphicsContext, (iconX + 8, y), props, (itemCount, numItems, top))

        return (y, itemCount)

    #########################################################################################################
    ##
    #########################################################################################################
    def drawTree(self, tree, graphicsContext, widgetProperties, parentRect=None):
        rect = self.calcWidgetRect(tree, parentRect)

        backgroundBrush = self.determineProp(widgetProperties, "background", Brush((255, 255, 255, 255), Brush.STYLE_SOLID))
        borderPen = self.determineProp(widgetProperties, "border", Pen(1, (0, 0, 0, 255), pyui2.system.Pen.STYLE_SOLID))
        buttonPen = self.determineProp(widgetProperties, "button", Pen(1, (0, 0, 0, 255), pyui2.system.Pen.STYLE_SOLID))
        linePen = self.determineProp(widgetProperties, "border", Pen(1, (162, 162, 162, 255), pyui2.system.Pen.STYLE_SOLID))
        font = self.determineProp(widgetProperties, "font", self.getProperty("DEFAULT FONT"))
        fontColor = self.determineProp(widgetProperties, "fontcolor", (0, 0, 0, 255))
        selectColor = self.determineProp(widgetProperties, "selectcolor", (0, 0, 0, 255))
        fontSelectColor = self.determineProp(widgetProperties, "fontselectcolor", (selectColor[0]^255, selectColor[1]^255, selectColor[2]^255, 255))

        numItems = rect[3] / font.getTextSize("Wq")[1]
        itemCount = 0

        treeRect = pyui2.system.Rectangle(rect, borderPen, backgroundBrush)
        graphicsContext.drawGraphicObject(treeRect);

        x = rect[0] + 6
        y = rect[1] + 2

        self.drawNode(tree.topNode, graphicsContext, (x, y), (linePen, font, fontColor, backgroundBrush, selectColor, fontSelectColor), (itemCount, numItems, tree.top))
        self.drawNodeButtons(tree.topNode, graphicsContext, (x, y), (font, buttonPen, backgroundBrush), (itemCount, numItems, tree.top))

    #########################################################################################################
    ##
    #########################################################################################################
    def drawSheetButton(self, graphicsContext, rect, brush, pen=None, text=None, font=None, fontcolor=None):
        buttonObj = pyui2.system.Rectangle(rect, pen, brush)
        graphicsContext.drawGraphicObject(buttonObj)

        if text != None:
            textObj = pyui2.system.Text(text, rect, font, fontcolor)
            textObj.setJustification(GCX.TEXT_CENTER)
            graphicsContext.drawGraphicObject(textObj)


    #########################################################################################################
    ##
    #########################################################################################################
    def drawSheet(self, sheet, graphicsContext, widgetProperties, parentRect=None):
        rect = self.calcWidgetRect(sheet, parentRect)

        backgroundBrush = self.determineProp(widgetProperties, "background", Brush((255, 255, 255, 255), Brush.STYLE_SOLID))
        gridPen = self.determineProp(widgetProperties, "border", Pen(1, (0, 0, 0, 255), pyui2.system.Pen.STYLE_SOLID))
        buttonBrush = self.determineProp(widgetProperties, "background", Brush((192, 192, 192, 255), Brush.STYLE_SOLID))
        font = self.determineProp(widgetProperties, "font", self.getProperty("DEFAULT FONT"))
        fontColor = self.determineProp(widgetProperties, "fontcolor", (0, 0, 0, 255))

        rectObj = pyui2.system.Rectangle(rect, gridPen, backgroundBrush)
        graphicsContext.drawGraphicObject(rectObj)

        (w,h) = sheet.getWidthAndHeightFor(0,0)
        headerRect = (sheet.posX, sheet.posY, w, h)
        self.drawSheetButton(graphicsContext, headerRect, buttonBrush)

        # draw column titles and lines
        posX = sheet.posX + sheet.getColumnWidth(0)
        posY = sheet.posY
        for x in range(1, sheet.visibleColumns):
            (w,h) = sheet.getWidthAndHeightFor(x+sheet.hscroll.currentItem,0)
            headerRect = (posX, posY, w, h)
            self.drawSheetButton(graphicsContext, headerRect, buttonBrush, None, sheet.getColumnTitle(x+sheet.hscroll.currentItem), font, fontColor)
            graphicsContext.drawLine(((posX - 1, posY), (posX - 1, posY + rect[3]-12)), gridPen)
            posX = posX + w
        graphicsContext.drawLine(((posX - 1, posY), (posX - 1, posY + rect[3]-12)), gridPen)

#        # draw row titles and lines
        posX = sheet.posX
        posY = sheet.posY + sheet.getRowHeight(sheet.vscroll.currentItem)
        for y in range(1, sheet.visibleRows):
            (w,h) = sheet.getWidthAndHeightFor(0,y+sheet.vscroll.currentItem)
            headerRect = (posX, posY, w, h)
            self.drawSheetButton(graphicsContext, headerRect, buttonBrush, None, sheet.getRowTitle(y+sheet.vscroll.currentItem), font, fontColor)
            graphicsContext.drawLine(((posX, posY), (posX + rect[2] - 12, posY)), gridPen)
            posY = posY + h
        graphicsContext.drawLine(((posX, posY), (posX + rect[2] - 12, posY)), gridPen)

        # draw cell contents
        posY = sheet.posY + sheet.getRowHeight(sheet.vscroll.currentItem)
        textObj = pyui2.system.Text(None, None, font, fontColor)
        for y in range(1, sheet.visibleRows):
            posX = sheet.posX + sheet.getColumnWidth(0)
            for x in range(1, sheet.visibleColumns):
                value = sheet.cells.get((x+sheet.hscroll.currentItem, y+sheet.vscroll.currentItem))
                (w,h) = sheet.getWidthAndHeightFor(x+sheet.hscroll.currentItem, y+sheet.vscroll.currentItem)
                valRect = (posX+2, posY, w, h)
                if value:
                    #print "Value =", value
                    textObj.setText("%s"%value)
                    textObj.setRectangle(valRect)
                    graphicsContext.drawGraphicObject(textObj)

                posX += sheet.getColumnWidth(x+sheet.hscroll.currentItem)

            posY += sheet.getRowHeight(y+sheet.vscroll.currentItem)




