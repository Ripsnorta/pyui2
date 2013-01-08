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
import re
import os, stat
import string

import pyui2
from pyui2 import locals
from pyui2.desktop import getDesktop, getTheme
from dialog import Dialog


EVENT_OUTPUT = pyui2.desktop.getUserEvent()


class FileDialog(Dialog):
    """A dialog to allow the user to select a file. Allows regex wildcard filters
    and calls the "callback" method when done.

    Always use the forward slash '/' to separate paths, not the other slash '\'.

    The filter matches using python regular expressions. Note that the wildcard for
    matching anything is ".*" not just "*" as the asterisk is a "repeating character"
    modifier in the regular expression language...
    """
    def __init__(self, startDir, callback, filter = ".*"):
        currentDir = startDir.replace('\\','/')
        self.callback = callback
        self.filter = filter
        Dialog.__init__(self, -1, -1, 400,240, "File Dialog")
        self.setLayout(pyui2.layouts.TableLayoutManager(6,8))
        
        self.dirLabel = pyui2.widgets.Label("Directory:")
        self.fileLabel = pyui2.widgets.Label("Filename:")
        self.filterLabel = pyui2.widgets.Label("Filter:")

        self.dirBox = pyui2.widgets.Label(currentDir)
        self.filesBox = pyui2.widgets.ListBox(self._pyui2Selected, self._pyui2DoubleClicked)
        self.nameBox = pyui2.widgets.Label("")
        self.filterBox = pyui2.widgets.Edit(self.filter,10,self._pyui2Filter)

        self.dirButton = pyui2.widgets.Button("Up", self._pyui2Up)
        self.openButton = pyui2.widgets.Button("Open", self._pyui2Open)
        self.closeButton = pyui2.widgets.Button("Close", self._pyui2Close)

        self.addChild( self.dirLabel,    (0,0,2,1) )
        self.addChild( self.fileLabel,   (0,6,2,1) )
        self.addChild( self.filterLabel, (0,7,2,1) )
        self.addChild( self.dirBox,      (2,0,3,1) )
        self.addChild( self.filesBox,    (0,1,6,5) )
        self.addChild( self.nameBox,     (2,6,3,1) )
        self.addChild( self.filterBox,   (2,7,3,1) )
        self.addChild( self.dirButton,   (5,0,1,1) )
        self.addChild( self.openButton,  (5,6,1,1) )
        self.addChild( self.closeButton, (5,7,1,1) )        

        self.pack()
        self.setCurrentDir(currentDir)

    def setCurrentDir(self, newDir):
        """This will fail if newDir is not a valid directory.
        """
        try:
            info = os.stat(newDir)
            isdir = stat.S_ISDIR(info[stat.ST_MODE])
        except OSError, e:
            print "Invalid Dir:", newDir
            return None
        if isdir:
            self.currentDir = newDir
            return self.populateDir()
        return None
            
    def populateDir(self):
        """Load the current directory. Load directories first, then all
        the files.
        """
        self.filesBox.clear()
        self.dirBox.setText(self.currentDir)
        self.nameBox.setText("")
        all = os.listdir(self.currentDir+"/")
        files = []
        for filename in all:
            info = os.stat(self.currentDir+"/"+filename)
            isdir = stat.S_ISDIR(info[stat.ST_MODE])
            if isdir:
                self.filesBox.addItem(filename, 1, pyui2.colors.blue)
            else:
                files.append(filename)
        for filename in files:
            if re.search(self.filter, filename):
                self.filesBox.addItem(filename, 0, pyui2.colors.black)

    def _pyui2Filter(self, filter):
        self.filter = filter.text
        self.populateDir()
        self.filterBox.setText(self.filter)
        return 1
    
    def _pyui2Up(self, button):
        path = self.currentDir.split("/")[:-1]
        self.setCurrentDir( string.join(path, "/") )

    def _pyui2Selected(self, item):
        if not item:
            self.nameBox.setText("")
        else:
            self.nameBox.setText(item.name)
        return 1

    def _pyui2DoubleClicked(self, item):
        if not item:
            self.nameBox.setText("")
        else:
            self.nameBox.setText(item.name)
            self._pyui2Open(None)
        return 1
        
    def _pyui2Open(self, button):
        """Open a file or a directory
        """
        if len(self.nameBox.text) == 0:
            return 0
        fullpath = self.currentDir+"/"+self.nameBox.text
        info = os.stat(fullpath)
        isdir = stat.S_ISDIR(info[stat.ST_MODE])
        if isdir:
            self.setCurrentDir( fullpath )
        else:
            self.close(1)
            self.callback(fullpath)
        return 1

    def _pyui2Close(self, button):
        self.close(0)

