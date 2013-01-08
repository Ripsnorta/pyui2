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

import copy

"""The pyui2 Desktop. This manages the parts of pyui2 that are above the scope of individual windows.
"""
import pyui2




######## Exported method to grab the renderer, desktop and theme #########

def getDesktop():
    return Desktop.theDesktop

def getTheme():
    return Desktop.theDesktop.theme

def readTimer():
    return Desktop.theDesktop.readTimer()

######## New theme management #########
from pyui2.themes.presenter import Presenter

def setTheme(theme):
    Desktop.theDesktop.theme = theme
    Desktop.theDesktop.presenter.setTheme(theme)

def getPresenter():
    return Desktop.theDesktop.presenter

def setBackgroundDrawingFunction(backFunction):
    Desktop.theDesktop.presenter.setBackgroundDrawing(backFunction)

################# utility classes #######################

class guiEvent:
    """an event that can be processed by the system.
    """
    def __init__(self, type, id = 0, x = 0, y = 0, key = 0, mods = 0):
        self.type = type
        self.id = id      # this is the ID of the widgets that caused the event.
        self.pos = (x,y)
        self.key = key
        self.mods = mods

class guiCallback:
    """a timed callback object. If the callback method returns a logical true, then the callback will
    automatically be removed. This makes it easy to provide 1-shot timed callbacks. A callback with an interval
    of 0 will be called on every frame.
    """
    def __init__(self, method, interval, lastTrigger):
        self.method = method
        self.interval = interval
        self.lastTrigger = lastTrigger

    def process(self, time):
        if time >= self.lastTrigger + self.interval:
            result = self.method(time - self.lastTrigger)
            self.lastTrigger = time
            return result
        else:
            return 0

################### the desktop class ####################

class Desktop:
    """The Desktop. I am the container for all global pyui2 data.
    """

    lastEvent = 999    # used to generate user event numbers
    theDesktop = None

    def __init__(self, width, height, fullscreen, ThemeClass, deviceName):
        # setup singleton desktop
        Desktop.theDesktop = self

        self.presenter = Presenter(width, height, fullscreen)
        self.presenter.determineDeviceContext(deviceName)

        newTheme = ThemeClass()
        setTheme(newTheme)

        self.width = width
        self.height = height

        self.lastID= 1000
        self.windows = []               # list of top level windows
        self.allWidgets = {}            # list of ALL the widgets
        self.running = 1                # set this to zero to exit
        self.userEvents = []            # list of user events to be processed
        self.focusWidget = None         # widget with the focus
        self.userHandlers = {}          # map of user event handlers
        self.callbacks = {}             # list of timed callback methods (dict for fast removal)
        self.modal = None               # current modal dialog
        self.waiting = 0                # flag for waiting mode
        self.tooltipCallback = None     # callback to enable tooltip
        self.toooltipFocus = None       # widget with tooltip focus
        self.tooltipPosition = None     # position of mouse when tooltip is activated
        self.tooltipWindow = None       #pyui2.widgets.TooltipWindow(5,50,100,100)

        #self.theme.setArrowCursor()


    def setDeviceContext(self, deviceName):
        self.presenter.determineDeviceContext(deviceName)


    def quit(self):
        """Called to destroy all the windows on shutdown.
        """
        #use a copy of list as we delete from it.
        ww = copy.copy(self.windows)
        for w in ww:
            w.destroy()
        self.running = 0
        self.windows = []
        self.allWidgets = {}
        del Desktop.theDesktop
        Desktop.theDesktop = None
        self.presenter.getDeviceContext().quit()


    def update(self):
        """Called constantly by the application to process pyui2 events and scheduled callbacks.
        """
        self.presenter.getDeviceContext().update()
        # process user events
        while self.running and self.userEvents:
            e = self.userEvents.pop(0)

            self.handleEvent(e)
            if not self.running:
                return self.running
        # process timer callbacks
        timer = self.presenter.getDeviceContext().readTimer()
        for callback in self.callbacks.keys():
            if callback.process(timer):
                del self.callbacks[callback]
        return self.running

    def draw(self):
        """Called to draw the widgets!
        """
        self.presenter.present(self.windows)

    def findWidget(self, id):
        """Lookup a widget by its ID.
        (public)
        """
        return self.allWidgets.get(id, None)

    def registerWidget(self, widget):
        """Register a top level window instance with the system.
        (internal)
        """
        widget.id = self.nextID()
        self.allWidgets[widget.id] = widget

    def removeWidget(self, widget):
        """Remove a widget previously registered from the top-level widget list
        """
        self.windows.remove(widget)

    def destroyWidget(self, widget):
        """cleanup all global references to widget. This is called by destroy() so don't call it twice.
        (internal)
        """
        if self.allWidgets.has_key(widget.id):
            del self.allWidgets[widget.id]
        for w in self.windows:
            if w.id == widget.id:
                self.windows.remove(w)
                break

        if self.focusWidget == widget:
            self.focusWidget = None

    def activateWindow(self, window):
        """This adds a window to the set of windows and puts it on top, except
        for any topMost widgets on the screen.
        """
        if window == None:
            return

        i = 0
        try:
            self.windows.remove(window)
        except ValueError:
            pass

        if not window.topMost:
            for w in self.windows:
                if not w.topMost:
                    break
                i += 1

        self.windows.insert(i, window)

    def addWindow(self, window):
        """This adds a window to the set of windows and puts it on top, except
        for any topMost widgets on the screen.
        """
        self.activateWindow(window)
        self.focusWidget = None

    def registerHandler(self, eventType, handler):
        """Register a user defined handler for an event.
        (public)
        """
        self.userHandlers[eventType] = handler

    def unregisterHandler(self, eventType):
        """Un-Register a user defined handler for an event.
        (public)
        """
        del self.userHandlers[eventType]

    def readTimer(self):
        return self.presenter.getDeviceContext().readTimer()

    def handleEvent(self, event):
        """Process all outstanding events.
        (private)
        """
        if event.type != 0:
            if event.type == pyui2.locals.QUIT:
                self.quit()
                print "DONE!"
                return

            # pre-handle mouse move events here for tool tips
            if event.type == pyui2.locals.MOUSEMOVE:
                self.updateToolTips(event)

            # events go to the focus branch first
            w = self.focusWidget
            while w != None:
                if w.handleEvent(event):
                    return
                if w == self.modal:
                    break
                w = w.parent

            if self.modal and ((event.type & pyui2.locals.EVENT_MASK) == pyui2.locals.EVENT_MOUSE or
                           (event.type & pyui2.locals.EVENT_MASK) == pyui2.locals.EVENT_KEYBOARD):
                return self.updateModal(event)

            # pass events to all widgets
            for w in self.windows:
                if w.handleEvent(event):
                    return

            # check for application handlers
            if self.userHandlers.has_key(event.type):
                if self.userHandlers[event.type](event) == 1:
                    return


    def updateToolTips(self, event):
        ##NOTE: turned off for now...
        return
        # find the widget under the mouse
        found = None
        for w in self.windows:
            if w == self.tooltipWindow:
                continue
            found = w.checkHit(event.pos)
            if found:
                break
        #print "Mouse Move. found = ", found
        # cancel current tooltip callback
        if self.tooltipCallback:
            self.removeCallback(self.tooltipCallback)
            self.tooltipCallback = None
        # disable current tooltip window
        if self.tooltipWindow:
            self.tooltipWindow.setShow(0)
        if found:
            # setup a callback to enable the tooltip after a delay
            self.tooltipCallback = addCallback(self.enableTooltip, 0.333)
            self.tooltipFocus = found
            self.tooltipPosition = event.pos
        else:
            self.tooltipFocus = None

    def updateModal(self, event):
        """in modal mode, only the modal dialog gets mouse events
        """
        if self.modal.handleEvent(event):
            return
        if event.type == pyui2.locals.KEYDOWN and event.key == pyui2.locals.K_ESCAPE:
            self.modal.setShow(0)
            self.modal = None
        return

    def setModal(self, window):
        """Sets the modal window.
        (internal)
        """
        self.modal = window
        if window:
            window.getFocus()

    def getModal(self):
        return self.modal

    def setWaiting(self, value):
        self.waiting = value
        if value:
            self.theme.setWaitCursor()
        else:
            self.theme.setArrowCursor()

    def setFocus(self, widget):
        """Set the focus to this widget.
        """
        if not widget:
            self.focusWidgets = None
            return
        if self.focusWidget and self.focusWidget != widget:
            self.focusWidget.loseFocus()
        self.focusWidget = widget

    def getFocus(self):
        """return the current focused widget.
        """
        return self.focusWidget

    def getTheme(self):
        """return the global theme object"""
        return self.theme

    def setTheme(self, theme):
        """sets the global theme object
        """
        self.theme = theme

    def postUserEvent(self, type, x = 0, y = 0, key = 0, mods = 0):
        """Post a user event into the system. This comes from a non-widget object
        (public)
        """
        newEvent = guiEvent(type, 0, x, y, key, mods)
        self.userEvents.append(newEvent)
        return newEvent

    def postEvent(self, type, id = 0):
        """Post an event object into the system. Comes from a widget object.
        (internal)
        """
        newEvent = guiEvent(type, id, 0, 0)
        self.userEvents.append(newEvent)
        return newEvent

    def addCallback(self, method, interval = 0):
        callback = guiCallback(method, interval, self.presenter.readTimer() )
        self.callbacks[callback] = None
        return callback

    def removeCallback(self, callback):
        if self.callbacks.has_key(callback):
            del self.callbacks[callback]

    def findWindowByHandle(self, handle):
        for w in self.windows:
            if w.handle == handle:
                return w
        return None

    def enableTooltip(self, interval):
        result = self.ooltipFocus.getToolTipInfo(self.tooltipPosition)
        self.removeCallback(self.tooltipCallback)
        self.tooltipCallback = None
        #print "Enabling tool tip", result, gTooltipWindow
        if result:
            (text, rect) = result
            self.tooltipWindow.activate(text, rect)
            self.activateWindow(self.tooltipWindow)

    def setMustFill(self):
        """tell the UI the screen must be cleared. if this is not set, only dirt rects get updated.
        Setting this means that all the windows will redraw.
        """
        self.presenter.setMustFill()

    def getMustFill(self):
        return self.presenter.mustFill

    def dirtyCollidingWindows(self, inRect):
        """If a dirty rect collides with any other rects, they should be dirty also. This recurses
        so that all colliding rects get dirtied. the second parameter to setDirty() prevents infinite
        recursion.
        """
        self.presenter.dirtyCollidingWindows(inRect)

    def nextID(self):
        self.lastID = self.lastID + 1
        return self.lastID

    def getSize(self):
        return (self.width, self.height)


def getUserEvent():
    """Request an event ID in the user event space.
    NOTE: this is not part of the desktop as it can be called before the desktop object
    is created.
    (public)
    """
    e = pyui2.locals.USEREVENT + Desktop.lastEvent
    Desktop.lastEvent = Desktop.lastEvent + 1
    return e
