import pyui2
import string
import traceback

class PrimitiveLine:
    """A list of lines that contain primitives of wrapped text and other elements.
    """
    def __init__(self):
        self.primitives = []
        self.height = 12
        self.posX = 0 # used during construction

    def addPrimitive(self, primitive):
        if primitive.height > self.height:
            self.height = primitive.height
        self.primitives.append(primitive)
        self.posX += primitive.width

    def draw(self, renderer, posX, posY, area):
        for primitive in self.primitives:
            print "line prim:", primitive
            primitive.draw(renderer, posX, posY, area)
            posX += primitive.width

class Primitive:
    """A single renderable element that does not wrap over multiple lines.
    """
    def __init__(self, attrs, width, height, align=0):
        self.width = width
        self.height = height
        self.align = align
        self.attrs = attrs

    def draw(self, renderer, posX, posY, area):
        pass

    def findAttr(self, name):
        for aname, value in self.attrs:
            if name == aname:
                return value
        return None

    def setAttr(self, name, default):
        value = self.findAttr(name)
        if value:
            setattr(self, name, value)
        else:
            setattr(self, name, default)
            
class PrimitiveArea(Primitive):
    """A rectangular area that HTML can be renderered in that will wrap.
    The main page is an area, and it may have sub-areas for tables or
    other special tags. Areas contain a set of lines.
    """
    def __init__(self, attrs, width, height, fgColor):
        Primitive.__init__(self, attrs, width, height)
        self.lines = []
        self.currentLine = PrimitiveLine()
        self.fgColor = fgColor

    def addPrimitive(self, primitive):
        if self.currentLine.posX + primitive.width >= self.width:
            self.lines.append(self.currentLine)
            self.height += self.currentLine.height
            self.currentLine = PrimitiveLine()
        self.currentLine.addPrimitive(primitive)
        if self.height <= primitive.height:
            self.height = primitive.height


    def newLine(self):
        self.lines.append(self.currentLine)
        self.height += self.currentLine.height        
        self.currentLine = PrimitiveLine()

    def draw(self, renderer, posX, posY, top, height):
        """Draw each of the lines in the area.
        """
        absolutePosY = 0 # sum of all lines up to this point
        screenPosY = 0   # sum of lines that have ben drawn up to this point
        
        for line in self.lines:

            print "posX, posY: (%s,%s)" % (posX,posY), "height:", height, line.height, line       
            if absolutePosY-top + line.height > height:
                absolutePosY += line.height                
                print "not drawing:", line
                continue
            
            if absolutePosY >= top:
                line.draw(renderer, 3, absolutePosY - top+posY, self)
                
            absolutePosY += line.height

class PrimitiveTable(PrimitiveArea):
    """A HTML table. contains rows and columns...
    """
    def __init__(self, attrs, width, height=0, fgColor="#440022"):
        PrimitiveArea.__init__(self, attrs, width, height, parseColor(fgColor))

        self.setAttr("border", 1)
        self.setAttr("bgcolor", "#FFFFFF")
        self.setAttr("cellspacing", 1)
        self.setAttr("cellpadding", 1)
        self.setAttr("background", "")

        w = self.findAttr("width")
        if w:
            if w[-1] == "%":
                percent = int(w[:-1]) * 0.01
                self.width = width * percent
            else:
                self.width = int(w)
        print "Table width is ", self.width
        self.text = "table"
        
    def draw(self, renderer, posX, posY, area):
        print "\nBEGIN TABLE DRAWING!!!!", posX, posY, self.height
        #for l in self.lines:
        #    print "   line:", l
        #    for p in l.primitives:
        #        print "     prim:", p.text
        PrimitiveArea.draw(self, renderer, posX, posY, 0, self.height)
        print "END TABLE DRAWING!!!!\n\n"
        
class PrimitiveTableRow(PrimitiveLine):
    """A row within a table.
    """

    
#############  Text Primitives ################
    
class TextPrimitive(Primitive):
    """A piece of formatted text that does not wrap.
    """
    def __init__(self, formatState, text, width, height, align=0):
        self.formatState = formatState
        self.text = text
        Primitive.__init__(self, [], width, height, align)
        
    def draw(self, renderer, posX, posY, area):
        print "DRAW TEXT:", self.text
        textColor = self.formatState.color
        if textColor:
            color = parseColor(textColor)
        else:
            color = area.fgColor
        (font,width) = getFont(self.formatState)
        #renderer.drawText( self.text, (posX, posY), color, font=font)

class ListItemPrimitive(TextPrimitive):
    
    def draw(self, renderer, posX, posY, area):
        textColor = self.formatState.color
        if textColor:
            color = parseColor(textColor)
        else:
            color = area.fgColor
        (font,width) = getFont(self.formatState)        
        #renderer.drawRect( color, (posX + 12, posY + self.height/2 - 4, 8, 8) )
        #renderer.drawText( self.text, (posX+ 28, posY), color, font=font)


#############  Visible Primitives ################
    
class ImagePrimitive(Primitive):
    def __init__(self, attrs, width):
        Primitive.__init__(self, attrs, 0,0,1)

        img = self.findAttr("src")
        if img:
            self.img = img
        self.text=img
        (width,height) = getPresenter().getImageSize(img)
        
        w = self.findAttr("width")
        if w:
            self.width = int(w)
        else:
            self.width = width
            
        h = self.findAttr("height")
        if h:
            self.height = int(h)
        else:
            self.height = height
            
    def draw(self, renderer, posX, posY, area):
        #renderer.drawImage( (posX, posY, self.width, self.height), self.img)
        pass


class HRPrimitive(Primitive):
    def __init__(self, attrs, w):
        Primitive.__init__(self, attrs, w,0,1)
        self.text="HR"

    def draw(self, renderer, posX, posY, area):
        #renderer.drawRect( pyui2.colors.grey, (posX, posY, self.width, 2) )
        pass
                
def constructWrapped(panel, token, formatState):
    """This constructs multiple text primitives from a piece of text.
    """
    text = token.data
    text = text.replace("\n"," ")

    (font,characterWidth) = getFont( formatState )
    availablePixels = panel.windowRect[2] - panel.areas[-1].currentLine.posX
    availableChars = availablePixels / characterWidth

    if self.font:
        font = self.font
    else:
        font = getTheme().defaultFont

    (w,h) = font.getTextSize(text)

    if availablePixels > w:
        # all the text fits on one line
        #print "CON: full line:", text
        newPrim = TextPrimitive(formatState, text, w, h)
        panel.areas[-1].addPrimitive(newPrim)
        return

    while len(text) > 0:            
            
        # add characters until it wraps
        lineText = ""
        count = 0
        for c in text:
            lineText += c
            (w,h) = font.getTextSize(lineText)

            if w >= availablePixels-10:
                newPrim = TextPrimitive(formatState, lineText, w, h)
                panel.areas[-1].addPrimitive(newPrim)                
                text = text[count:]
                availablePixels = panel.windowRect[2]                
                #print "Breaking... count=", count
                break

            #print "CON: portion: <%s>" % w, availablePixels, count, lineText, len(text)            
            count += 1
        if count == len(text):
            newPrim = TextPrimitive(formatState, lineText, w, h)
            panel.areas[-1].addPrimitive(newPrim)
            break

def constructPreformatted(panel, token, formatState):
    """construct primitives for preformatted text
    """
    text = token.data
    textLines = text.split("\n")

    (font,characterWidth) = getFont( formatState )
    if font:
        font = self.font
    else:
        font = getTheme().defaultFont

    count = 0
    out = []
    for t in textLines:
        if count > 0:
            out.append(None)
        out.append(t)
        count += 1
    for text in out:
        if text == None:
            panel.areas[-1].newLine()
            continue

        availablePixels = panel.windowRect[2] - panel.areas[-1].currentLine.posX
        availableChars = availablePixels / characterWidth

        (w,h) = font.getTextSize(text)    
        newPrim = TextPrimitive(formatState, text[:availableChars], w, h)
        panel.areas[-1].addPrimitive(newPrim)
        
def constructSingleLine(panel, token, formatState):
    """construct primitives for a single non-wrapped line..
    NOTE: should an indented wrapped line.
    """
    text = token.data
    text = text.replace("\n"," ")
    (font,characterWidth) = getFont( formatState )
    availablePixels = panel.windowRect[2] - panel.areas[-1].currentLine.posX
    availableChars = availablePixels / characterWidth

    if self.font:
        font = self.font
    else:
        font = getTheme().defaultFont

    (w,h) = font.getTextSize(text)    
    newPrim = ListItemPrimitive(formatState, text[:availableChars], w, h)
    panel.areas[-1].addPrimitive(newPrim)
        

fontCache = {}

def getFont(formatState):

    flags = 0
    if formatState.bold:
        flags = flags | pyui2.locals.BOLD
    if formatState.italic:
        flags = flags | pyui2.locals.ITALIC
    if formatState.underline:
        flags = flags | pyui2.locals.UNDERLINE

    # only use position face sizes
    if int(formatState.size) < 0:
        size = 10
    else:
        size = int(formatState.size)

    # only one face..
    face = formatState.face.split(",")[0]
    key = (face, int(size), flags)

    if fontCache.has_key(key):
        return fontCache[key]

    font = pyui2.system.GetDeviceContext().createFont, key)
    (width,h) = font.getTextSize('o')
    fontCache[key] = (font,width)
    formatState.font = font
    return (font, width)
    

def parseColor( htmlColor):

    #print "HTML COLOR:", htmlColor
    r = htmlColor[1:3]
    g = htmlColor[3:5]
    b = htmlColor[5:7]
    
    # horrible hack to convert hex to decimal.
    # how is this one in python?!?
    hexes = "0123456789abcdef"
    r1 = hexes.index(string.lower(r[0]))*16
    r2 = hexes.index(string.lower(r[1]))
    r = r1 + r2
    g1 = hexes.index(string.lower(g[0]))*16
    g2 = hexes.index(string.lower(g[1]))
    g = g1 + g2
    b1 = hexes.index(string.lower(b[0]))*16
    b2 = hexes.index(string.lower(b[1]))        
    b = b1 + b2
    return (r, g, b, 255)    
