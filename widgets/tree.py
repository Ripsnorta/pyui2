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

import pyui2

from pyui2.desktop import getDesktop, getTheme
from pyui2.base import Base
from pyui2.panel import Panel
from pyui2.window import Window


itemHeight = 18


class Tree(Base):
    """A tree widget. Has a built-in tree node, plus user added nodes. The built-in top
    node is not drawn, only children of it are drawn. Nodes can be added at any time to
    the tree.
    """

    OPEN = 1
    CLOSED = 2
    openButton   = "open.png"
    closedButton = "closed.png"
    emptyButton  = "empty.png"
    default      = "folder.png"


    widgetLabel = "TREE"

    def __init__(self):
        Base.__init__(self)

        self.selectedNode = None
        self.registerEvent(pyui2.locals.LMOUSEBUTTONDOWN, self.onMouseDown)
        self.registerEvent(pyui2.locals.SCROLLPOS, self.onScrollPos)
        self.registerEvent(pyui2.locals.TREENODE_SELECTED, self.onSelection)
        self.vscroll = pyui2.widgets.VScroll()
        self.addChild(self.vscroll)
        self.top = 0
        self.numNodes = 0  #number of visible nodes
        self.topNode = TreeNode(None, None)
        self.topNode.tree = self
        self.topNode.parent = None
        self.topNode.status = Tree.OPEN
        self.drawRootNode = False

    def setDrawRootNode(self, drawRootNode=True):
        self.drawRootNode = drawRootNode

    def resize(self, w, h):
        Base.resize(self, w, h)
        self.vscroll.moveto(self.posX + self.width - 10, self.posY)
        self.vscroll.resize(10, self.height)
        self.vscroll.setNumItems(self.numNodes, self.height / itemHeight)

    def addNode(self, node):
        self.topNode.addNode(node)
        self.countOpenNodes()

    def getSelectedNode(self):
        return self.findSelected(self.topNode)

    def findSelected(self, node):
        """help method to recursively find the selected node.
        """
        if node.selected:
            return node
        else:
            for child in node.nodes:
                ret = self.findSelected(child)
                if ret:
                    return ret
        return

    def present(self, presenter, graphicsContext, parentRect=None):
        presenter.drawWidget(self.widgetLabel, self, graphicsContext, parentRect)

        offsetX = 0
        offsetY = 0
        if parentRect != None:
            offsetX = parentRect[0]
            offsetY = parentRect[1]

        for child in self.children:
            child.present(presenter, graphicsContext, (self.posX+offsetX, self.posY+offsetY, self.windowRect[2], self.windowRect[3]))

    def onScrollPos(self, event):
        if event.id == self.vscroll.id:
            self.top = event.pos
            #print self.top
            self.setDirty(1)
            #print "%d Nodes %d visible %d top" % (self.numNodes, self.height/26, self.top)

    def onMouseDown(self, event):
        if not self.hit(event.pos):
            return 0

        # Adjust for window coordinates and get the x y point relative to the top left of the
        # tree widget.
        adjEvtPos = self.convertToWindowCoords(event.pos)
        (hitX, hitY) = (adjEvtPos[0] - self.posX, adjEvtPos[1] - self.posY)
        #print (hitX, hitY)

        font = getTheme().getProperty("font")
        if font == None:
            font = getTheme().getProperty("DEFAULT FONT")

        itemCount = 0
        if self.CheckNodes(self.topNode, 0, hitX, hitY, font, itemCount, self.top):
            self.setDirty(1)

        self.countOpenNodes()
        return 1

    def CheckNodes(self, node, y, hitX, hitY, font, itemCount, top):
        for subnode in node.nodes:
            if y == -1:
                break

            if itemCount >= top:
                textSize = font.getTextSize(subnode.title)
                subnode.setRectangle((0, y, self.width, textSize[1]))

                y += textSize[1]

                if subnode.onMouseDown((hitX, hitY), font, self):
                    y = -1
                    break

            itemCount += 1
            if len(subnode.nodes) > 0 and subnode.status == pyui2.widgets.Tree.OPEN:
                (y, itemCount) = self.CheckNodes(subnode, y, hitX, hitY, font, itemCount, top)

        return (y, itemCount)

    def clearSelections(self, node, selNode=None):
        for subnode in node.nodes:
            if selNode == None:
                subnode.selected = 0
            elif subnode != selNode:
                subnode.selected = 0

            if len(subnode.nodes) > 0:
                self.clearSelections(subnode, selNode)

    def onSelection(self, data):
        #print "Selection Made:", data.node
        self.clearSelections(self.topNode, data.node)


    def countOpenNodes(self):
        """Count the number of visible nodes. used for the scroll bar.
        """
        self.numNodes = self.topNode.countOpenNodes()
        self.vscroll.setNumItems(self.numNodes, self.height / itemHeight)
        return self.numNodes

    def destroy(self):
        self.topNode.destroy()
        self.topNode = None
        self.vscroll = None
        return pyui2.widgets.Base.destroy(self)


class TreeNode:
    """A Node in the Tree widgets. Can be open or closed. Uses a default icon of a folder.
    """
    def __init__(self, title, icon = None):
        self.title = title
        self.icon = icon
        self.status = Tree.CLOSED
        self.nodes = []    # list of sub nodes
        self.selected = 0
        self.posX = 0
        self.posY = 0

    def setRectangle(self, rect):
        self.rect = rect

    def addNode(self, node):
        node.tree = self
        node.parent = self
        self.nodes.append(node)

    def checkY(self, y):
        # check for direct hit
        #print "checking %s y: %d self.posY: %d" % ( repr(self), y, self.posY)
        if y > self.posY and y < self.posY + itemHeight:
            return self
        if self.status == Tree.OPEN:
            # check for open children
            for node in self.nodes:
                subNode = node.checkY(y)
                if subNode:
                    return subNode
        #print "checked %s" % ( repr(self) )
        return None

    def countOpenNodes(self):
        num = 0
        for node in self.nodes:
            num = num + 1
            if node.status == Tree.OPEN:
                num = num + node.countOpenNodes()
        return num

    def inRect(self, pos, rect):
        return (rect[0] <= pos[0] <= (rect[0] + rect[2])) and (rect[1] <= pos[1] <= (rect[1] + rect[3]))

    def onMouseDown(self, hitPos, font, tree):
        if self.inRect(hitPos, self.rect):
            if self.selected == 0:
                self.selected = 1
                evt = tree.postEvent(pyui2.locals.TREENODE_SELECTED)
                evt.node = self

            if self.status == Tree.CLOSED and len(self.nodes) > 0:
                self.status = Tree.OPEN
            else:
                self.status = Tree.CLOSED

            return True

        return False

    def findNode(self, y):
        if y > self.posY and y < self.posY + itemHeight:
            return self
        if self.status == Tree.OPEN and len(self.nodes) > 0:
            for node in self.nodes:
                result = node.findNode(y)
                if result:
                    return result
        return None


    def destroy(self):
        for node in self.nodes:
            node.destroy()
        self.nodes = None
        self.parent = None
        self.tree = None



def init():
    pyui2.core.loadpyui2Image(Tree.openButton)
    pyui2.core.loadpyui2Image(Tree.closedButton)
    pyui2.core.loadpyui2Image(Tree.emptyButton)
    pyui2.core.loadpyui2Image(Tree.default)
    pyui2.core.loadpyui2Image("none.png")
    pyui2.core.loadpyui2Image("numeric.png")
    pyui2.core.loadpyui2Image("instance.png")
    pyui2.core.loadpyui2Image("string.png")
    pyui2.core.loadpyui2Image("list.png")
    pyui2.core.loadpyui2Image("dictionary.png")
    pyui2.core.loadpyui2Image("function.png")
