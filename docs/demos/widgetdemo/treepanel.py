###################################################################################
# Copyright (c) 2005 John Judd
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
# OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
###################################################################################

import pyui2
from widgetdemopanel import WidgetDemoPanel


READWRITE = 0
READONLY = 1

#############################################################################################################
##
#############################################################################################################
class TreePanel(WidgetDemoPanel):

    #########################################################################################################
    ##
    #########################################################################################################
    def __init__(self, owner):
        WidgetDemoPanel.__init__(self, owner)
        tree = pyui2.widgets.Tree()
        node1 = pyui2.widgets.TreeNode("Node 1")
        node1A = pyui2.widgets.TreeNode("Node 1A")
        node1B = pyui2.widgets.TreeNode("Node 1B")
        node1C = pyui2.widgets.TreeNode("Node 1C")
        node1Ca = pyui2.widgets.TreeNode("Node 1Ca")
        node1Cb = pyui2.widgets.TreeNode("Node 1Cb")
        node1Cc = pyui2.widgets.TreeNode("Node 1Cc")
        node1C.addNode(node1Ca)
        node1C.addNode(node1Cb)
        node1C.addNode(node1Cc)
        node1D = pyui2.widgets.TreeNode("Node 1D")
        node1E = pyui2.widgets.TreeNode("Node 1E")
        node1.addNode(node1A)
        node1.addNode(node1B)
        node1.addNode(node1C)
        node1.addNode(node1D)
        node1.addNode(node1E)
        node2 = pyui2.widgets.TreeNode("Node 2")
        node3 = pyui2.widgets.TreeNode("Node 3")
        node3A = pyui2.widgets.TreeNode("Node 3A")
        node3B = pyui2.widgets.TreeNode("Node 3B")
        node3C = pyui2.widgets.TreeNode("Node 3C")
        node3D = pyui2.widgets.TreeNode("Node 3D")
        node3E = pyui2.widgets.TreeNode("Node 3E")
        node3.addNode(node3A)
        node3.addNode(node3B)
        node3.addNode(node3C)
        node3.addNode(node3D)
        node3.addNode(node3E)
        node4 = pyui2.widgets.TreeNode("Node 4")
        node5 = pyui2.widgets.TreeNode("Node 5")

        tree.addNode(node1)
        tree.addNode(node2)
        tree.addNode(node3)
        tree.addNode(node4)
        tree.addNode(node5)

        self.widgetGroup.addChild(tree, (7, 0, 7, 9))

        self.completeInit()

