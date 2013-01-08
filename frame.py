import layouts
import pyui2
from pyui2.base import Base
from pyui2.panel import Panel
from pyui2.window import Window

from pyui2.desktop import getDesktop, getTheme, getPresenter
from pyui2.widgets.captionbar import CaptionBar

class Frame(Window):
    """A frame is a window that has a titlebar and borders. it is resizable and movable by dragging the titlebar.
    """

    NO_CAPTION = 1
    NO_RESIZE = 2
    BORDERLESS = 3
    TOPMOST = 4


    def __init__(self, x, y, w, h, title, flags = None):

        self.hitList = []

        self.theme = getTheme()
        self._menuBar = None
        self._captionBar = None
        self.innerRect = (0,0,w,h)

        self.captionBar = True
        self.frameResizing = True
        self.topmost = 0
        self.borderless = False
        self.moveable = True

        self.parseFlags(flags)
        self.title = ""

        Window.__init__(self, x, y, w, h, self.topmost)

        self.setTitle(title)
        if self.captionBar == True:
            #print "Setting caption bar:", title
            self.setCaptionBar(CaptionBar(title))

        self.resize(w, h)

        self.registerEvent(pyui2.locals.LMOUSEBUTTONDOWN, self._pyui2MouseDown)
        self.registerEvent(pyui2.locals.LMOUSEBUTTONUP, self._pyui2MouseUp)
        self.registerEvent(pyui2.locals.MOUSEMOVE, self._pyui2MouseMotion)
        self.moving = 0
        self.resizing = 0
        self.startX = 0
        self.startY = 0
        self.resizingCursor=0
        self.movingCursor=0
        self.backImage=None
        self.calcInnerRect()
        self.placeInnerObjects()


    def parseFlags(self, flags):
        if flags != None:
            for flag in flags:
                if flag == Frame.NO_CAPTION:
                    self.captionBar = False
                elif flag == Frame.NO_RESIZE:
                    self.frameResizing = False
                elif flag == Frame.BORDERLESS:
                    self.borderless = True
                elif flag == TOPMOST:
                    self.topmost = 1


    def placeInnerObjects(self):
        #print self.title, self.innerRect
        self._panel.moveto(self.innerRect[0], self.innerRect[1])
        self._panel.resize(self.innerRect[2], self.innerRect[3])
#        hitList.append((pyui2.locals.HIT_FRAME_RESIZE_RIGHT, (x,y,w,h)))
#        hitList.append((pyui2.locals.HIT_FRAME_RESIZE_BOTTOM, (x,y,w,h)))
#        hitList.append((pyui2.locals.HIT_FRAME_RESIZE_BOTTOM_RIGHT, (x,y,w,h)))
#        hitList.reverse()

        if self._captionBar != None:
            self._captionBar.resize(self.innerRect[2], self._captionBar.rect[3])

        if self._menuBar:
            self._menuBar.resize(self.innerRect[2], self._menuBar.rect[3])


    def calcInnerRect(self):
        """calculate the size of the inner rectangle of the frame. this excludes
        the frame borders and the menubar.
        """
        left = 0
        top = 0
        width = self.width
        height = self.height

        if self._captionBar != None:
            top += self._captionBar.getHeight()
            height -= self._captionBar.getHeight()

        if self._menuBar:
            top += self._menuBar.height
            height -= self._menuBar.height

        left += self.theme.getFrameBorderLeft()
        width -= (self.theme.getFrameBorderLeft() + self.theme.getFrameBorderRight())
        top += self.theme.getFrameBorderTop()
        height -= (self.theme.getFrameBorderBottom() + self.theme.getFrameBorderTop())

        self.innerRect = (left, top, width, height)


    def setMenuBar(self, menuBar):
        if self._menuBar:
            Base.removeChild(self, self._menuBar)

        self._menuBar = menuBar

        Base.addChild(self, self._menuBar)
        self._menuBar.setWindow(self)

        self._menuBar.moveto( self.theme.getFrameBorderLeft(), self.theme.getFrameBorderTop() )
        self._menuBar.resize( self.innerRect[2], self._menuBar.height)
        self.calcInnerRect()
        self.placeInnerObjects()


    def setCaptionBar(self, captionBar):
        if self._captionBar:
            Base.removeChild(self, self._captionBar)

        self._captionBar = captionBar

        Base.addChild(self, self._captionBar)
        self._captionBar.setWindow(self)

        self._captionBar.moveto(self.theme.getFrameBorderLeft(), self.theme.getFrameBorderTop())
        self._captionBar.resize(self.innerRect[2], self._captionBar.height)
        self.calcInnerRect()
        self.placeInnerObjects()


    def setTitle(self, title):
        self.title = title
        if self._captionBar:
            self._captionBar.setText(title)


    def setBackImage(self, filename):
        self.backImage = filename


    def present(self, presenter):
        """Performs the rendering of the window and it's children to the windows graphic context.
        """
        if self.show:
            #print "Presenting:", self.title
            if self.graphicsContext.getSize() != (self.width, self.height):
                # The size has changed since we last rendered, we need to resize the graphics context.
                # Note we only really need to do this when we redraw it, since creating and releasing
                # the context every time we get a window resize call may be very inefficient.
                self.graphicsContext.resize((self.width, self.height))

            # Draw the window first
            presenter.drawWidget("FRAME", self, self.graphicsContext)

            # Draw each of the children on to the graphics context using the theme supplied through
            # the presenter
            #print self.children
            for child in self.children:
                #print child
                child.present(presenter, self.graphicsContext)



    def replacePanel(self, panel):
        Window.replacePanel(self, panel)
        self.calcInnerRect()
        self.placeInnerObjects()


    def hitFrameRegion(self, pos):
        # put hit position in window relative coords
        x = pos[0] - self.rect[0]
        y = pos[1] - self.rect[1]

        # scan through hit regions
        for (regionId, rect) in self.hitList:
            #print regionId, rect, x, y
            if x >= rect[0] and y >= rect[1] and x < rect[0]+rect[2] and y < rect[1]+rect[3]:
                #print "Found region ID:", regionId
                return regionId
        else:
            return None


    def _pyui2MouseMotion(self, event):
        if self.resizing:
            mouseX = event.pos[0] - self.posX
            mouseY = event.pos[1] - self.posY
            if mouseX < 64:
                mouseX = 64
            if mouseY < 64:
                mouseY = 64
            self.frameResize( self.width + mouseX - self.startX, self.height + mouseY - self.startY)
            (self.startX, self.startY) = (mouseX, mouseY)
            return 1

        # set the proper cursor
        regionId = self.hitFrameRegion(event.pos)
        if regionId == pyui2.locals.HIT_FRAME_RESIZE_BOTTOM_RIGHT:
            self.resizingCursor=1
            self.theme.setResizeCursor()
        elif self.resizingCursor:
            self.resizingCursor=0
            self.theme.setArrowCursor()

        if not self.hit(event.pos):
            if self.resizingCursor and not self.resizing:
                self.resizingCursor=0
                self.theme.setArrowCursor()
            return 0
        else:
            return 1


    def _pyui2MouseDown(self, event):
        if not self.hit(event.pos):
            return 0

        self.getFocus()
        regionId = self.hitFrameRegion(event.pos)

        # check for closing
        if regionId == pyui2.locals.HIT_FRAME_CLOSE:
            return self.frameClose()


        # check for resizing
        if regionId == pyui2.locals.HIT_FRAME_RESIZE_BOTTOM_RIGHT:
            self.resizing = 1
            self.startX = event.pos[0] - self.posX
            self.startY = event.pos[1] - self.posY
            return 1

        return 1


    def _pyui2MouseUp(self, event):
        if self.resizing:
            self.resizing = 0
            return 1
        if self.resizingCursor:
            self.resizingCursor=0
            self.theme.setArrowCursor()
        if not self.hit(event.pos):
            return 0
        return 1


    def resize(self, w, h):
        if w < 64:
            w = 64
        if h < 64:
            h = 64
        Base.resize(self, w, h)
        self.calcInnerRect()
        self.placeInnerObjects()


    def _pyui2CloseButton(self):
        self.theme.setArrowCursor()
        self.destroy()
        return 1


    def handleEvent(self, event):
        """ do menu, then panel
        """
        if not self.show:
            return
        if self._captionBar:
            if self._captionBar.handleEvent(event):
                return 1
        if self._menuBar:
            if self._menuBar.handleEvent(event):
                return 1
        if self._panel:
            if self._panel.handleEvent(event):
                return 1
        if self.eventMap.has_key(event.type):
            if self.eventMap[event.type](event):
                return 1
        return 0


    def frameResize(self, w, h):
        """Called when the resize corner is dragged.
        Override this to customize resizing behavior.
        """
        self.resize(w,h)


    def frameMove(self, x, y):
        """Called when the frame is dragged around.
        Override this to customize dragging behavior.
        """
        self.move(x, y)


    def frameClose(self):
        """Called when the frame close button is clicked
        Override this to customize the close button behavior.
        """
        return self._pyui2CloseButton()


    def centerInDesktop(self):
        """Reposition the frame so that it is centered in the desktop.
        """
        sx, sy = getPresenter().getScreenSize()

        newPosX = (sx / 2) - (self.width / 2)
        newPosY = (sy / 2) - (self.height / 2)

        self.moveto(newPosX, newPosY)


    def addChild(self, child, option = None):

        Window.addChild(self, child, option)



