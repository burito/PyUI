# PyUI
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

"""PyGame openGL renderer
"""

import sys
import time

import pyui
import pygame
from pyui.renderers import openglBase
from pygame import locals

from pyui.desktop import getDesktop, getTheme, getRenderer

from OpenGL.GL import *

class OpenGLPygame(openglBase.OpenGLBase):
    """ PyGame 3D wrapper for the GL renderer
    """

    name = "P3D"
    
    def __init__(self, w, h, fullscreen, title):
        openglBase.OpenGLBase.__init__(self, w, h, fullscreen, title)
        pygame.init()
        pygame.display.set_caption(title)
        if fullscreen:
            self.screen = pygame.display.set_mode((w, h), locals.OPENGL | locals.DOUBLEBUF | locals.FULLSCREEN)
        else:
            self.screen = pygame.display.set_mode((w, h), locals.OPENGL | locals.DOUBLEBUF)

        pygame.key.set_mods(locals.KMOD_NONE)
        pygame.mouse.set_visible(0)
        #self.defaultFont = GLFont("times new roman", 12, 0)

    def draw(self, windows):
        apply(self.drawBackMethod, self.drawBackArgs)        
        self.setup2D()                        
        for i in xrange(len(windows)-1, -1, -1):
            w = windows[i]
            self.setWindowOrigin(w.posX, w.posY)
            if w.dirty:
                ## use display lists for deferred rendering...
                if not hasattr(w, "displayList"):
                    w.displayList = 0
                if w.displayList:
                    glDeleteLists(w.displayList,1)
                w.displayList = glGenLists(1)
                glNewList(w.displayList, GL_COMPILE_AND_EXECUTE)
                w.drawWindow(self)                
                glEndList()
            else:
                glCallList(w.displayList)

        self.setWindowOrigin(0,0)
        self.drawMouseCursor()
        self.teardown2D()
    
        pygame.display.flip()

        self.mustFill = 0
        self.dirtyRects = []
        

    def update(self):
        """PyGame event handling.
        """
        desktop = getDesktop()
        ## process all pending system events.
        event = pygame.event.poll()
        while event.type != locals.NOEVENT:
            
            # special case to handle multiple mouse buttons!
            if event.type == locals.MOUSEBUTTONDOWN:
                if event.dict['button'] == 1:
                    desktop.postUserEvent(pyui.locals.LMOUSEBUTTONDOWN, event.pos[0], event.pos[1])
                elif event.dict['button'] == 3:
                    desktop.postUserEvent(pyui.locals.RMOUSEBUTTONDOWN, event.pos[0], event.pos[1])
                    
            elif event.type == locals.MOUSEBUTTONUP:
                if event.dict['button'] == 1:
                    desktop.postUserEvent(pyui.locals.LMOUSEBUTTONUP, event.pos[0], event.pos[1])
                elif event.dict['button'] == 3:
                    desktop.postUserEvent(pyui.locals.RMOUSEBUTTONUP, event.pos[0], event.pos[1])
                    
            elif event.type == locals.MOUSEMOTION:
                self.mousePosition = event.pos
                desktop.postUserEvent(pyui.locals.MOUSEMOVE, event.pos[0], event.pos[1])

            elif event.type == locals.KEYDOWN:
                character = event.unicode
                code = 0
                if len(character) > 0:
                    code = ord(character)
                else:
                    code = event.key
                    #code = event.key, code                    
                desktop.postUserEvent(pyui.locals.KEYDOWN, 0, 0, code, pygame.key.get_mods())
                #if code >= 32 and code < 128:
                #    desktop.postUserEvent(pyui.locals.CHAR, 0, 0, character, pygame.key.get_mods())
            elif event.type == locals.KEYUP:
                code = event.key
                desktop.postUserEvent(pyui.locals.KEYUP, 0, 0, code, pygame.key.get_mods())
                
            else:
                try:
                    desktop.postUserEvent(event.type)
                except:
                    print "Error handling event %s" % repr(event)
            event = pygame.event.poll()

            self.mousePosition = pygame.mouse.get_pos()
            
    def quit(self):
        pygame.quit()          
        
    def loadTexture(self, filename, label = None):
        """This loads images without using P.I.L! Yay.
        """
        if label:
            if self.textures.has_key(label):
                return
        else:
            if self.textures.has_key(filename):
                return

        try:
            surface = pygame.image.load(filename)
        except:
            surface = pygame.image.load(  pyui.__path__[0] + "/images/" + filename )
        data = pygame.image.tostring(surface, "RGBA", 1)
        ix = surface.get_width()
        iy = surface.get_height()
        
        # Create Texture
        texture = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, texture)   # 2d texture (x and y size)
        glPixelStorei(GL_UNPACK_ALIGNMENT,1)
        glTexImage2D(GL_TEXTURE_2D, 0, 4, ix, iy, 0, GL_RGBA, GL_UNSIGNED_BYTE, data)

        if label:
            self.textures[label] = texture
        else:
            self.textures[filename] = texture

        glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_MODULATE)    
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)



    def drawText(self, text, pos, color, font=None):
        t = self.ft.render(text)
        ddata = t.img.tostring()
        ix = t.width
        iy = t.height
        # Create Texture
        texture = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, texture)   # 2d texture (x and y size)
        glPixelStorei(GL_UNPACK_ALIGNMENT,1)
        glTexImage2D(GL_TEXTURE_2D, 0, 4, 64, 32, 0, GL_RGBA, GL_UNSIGNED_BYTE, ddata)

        glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_MODULATE)    
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)


        glColor4ub( 255, 255, 255, 255 )
        glEnable(GL_TEXTURE_2D)
        glBindTexture( GL_TEXTURE_2D, texture)

        textureCoords = [[0.0,1.0],[1.0,1.0],[1.0,0.0],[0.0,0.0]]
        
        glBegin(GL_QUADS)
        glTexCoord2f(textureCoords[0][0], textureCoords[0][1])
        glVertex2i( pos[0], pos[1] )
        glTexCoord2f(textureCoords[1][0], textureCoords[1][1])
        glVertex2i( pos[0] + ix, pos[1])
        glTexCoord2f(textureCoords[2][0], textureCoords[2][1])
        glVertex2i( pos[0] + ix, pos[1] + iy)
        glTexCoord2f(textureCoords[3][0], textureCoords[3][1])
        glVertex2i( pos[0], pos[1] + iy)
        glEnd()

    def createFont(self, face, size, flags):
        newFont = GLFont(face, size, flags)
        return newFont

    def drawText(self, text, pos, color, font = None):
        if not font:
            font = getTheme().defaultFont
        font.drawText(text, pos, color)

    def getTextSize(self, text, font = None):
        if not font:
            font = getTheme().defaultFont
        return font.getTextSize(text)
    
class GLFont:
    def __init__(self, faceFile, size, flags):
        self.faceFile = faceFile
        self.size = size
        self.flags = flags
        print "Creating font:", faceFile
        if fontRegistery.has_key(faceFile):
            faceFile = "c:/WINNT/Fonts/" + fontRegistery[faceFile]
        self.font = pygame.font.Font(faceFile, size*1.3)
            
        self.charInfo = []  # tuples of (width, height, texture coordinates) for each character
        self.textCache = {}
        self.createGlyphs()

    def createGlyphs(self):
        testSurface = self.font.render("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRTSUTWXYZ", 1, (255,255,255,255))
        charWidth = testSurface.get_width()
        charHeight = testSurface.get_height()
        charSurfaces = []

        # create the character surfaces
        totalWidth = 0
        for i in range(0,128):
            try:
                charSurface = self.font.render( chr(i), 1, (255,255,255,255))
            except:
                charSurfaces.append( None )
            else:
                charSurfaces.append(charSurface)
                totalWidth += charSurface.get_width()

        # TODO: calculate this properly
        if totalWidth > 1300:
            SZ = 512
        else:
            SZ = 256
        totalWidth = SZ
        totalHeight = SZ
        
        # pack the surfaces into a single texture
        x = pygame.surface.Surface((totalWidth, totalHeight),
                                   flags=pygame.HWSURFACE |pygame.SRCALPHA,
                                   depth=32,
                                   masks=(0,0,0,0))
        self.packedSurface = x.convert_alpha()
        self.packedSurface.fill((0,0,0,0))
        positionX = 0
        positionY = 0
        c = 0
        for charSurf in charSurfaces:
            if not charSurf:
                self.charInfo.append( (0,0, (0,0,0,0)) )
                continue

            if positionX + charSurf.get_width() > SZ:
                positionX = 0
                positionY += charSurf.get_height()
                
            self.packedSurface.blit(charSurf, (positionX, positionY) )
            
            # calculate texture coords
            left = positionX/(float)(totalWidth)
            top = 1- positionY/(float)(totalHeight)            
            right = (positionX+charSurf.get_width()) / (float)(totalWidth)
            bottom = 1 - ((positionY+charSurf.get_height()) / (float)(totalHeight))
            texCoords = (left, top, right, bottom)

            self.charInfo.append( (charSurf.get_width(), charSurf.get_height(), texCoords) )
            positionX += charSurf.get_width()
            c += 1

        # create GL texture from surface
        self.texture = glGenTextures(1)
        data = pygame.image.tostring(self.packedSurface, "RGBA", 1)        
        glBindTexture(GL_TEXTURE_2D, self.texture)
        glPixelStorei(GL_UNPACK_ALIGNMENT,1)
        #print "w: %s h: %d"  %( totalWidth, totalHeight)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, totalWidth, totalHeight, 0, GL_RGBA, GL_UNSIGNED_BYTE, data)
        
        glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_MODULATE)    
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)

        # create display lists for each of the characters
        self.displayLists = []
        for (width, height, coords) in self.charInfo:
            if not width and not height:
                self.displayLists.append(0)
                continue
            newList = glGenLists(1)
            glNewList(newList, GL_COMPILE)
            glBegin(GL_QUADS)
            glTexCoord2f(coords[0], coords[1])
            glVertex2i(0, 0)
            glTexCoord2f(coords[2], coords[1])
            glVertex2i(width, 0)
            glTexCoord2f(coords[2], coords[3])
            glVertex2i(width, height)
            glTexCoord2f(coords[0], coords[3])
            glVertex2i(0, height)
            glEnd()
            glEndList()
            self.displayLists.append(newList)

    def drawText(self, text, pos, color):
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, self.texture)
        glColorub(color)
        xPos = pos[0]
        yPos = pos[1]-5
        glPushMatrix()
        glTranslate(xPos,yPos,0)
        for c in text:
            width = self.charInfo[ord(c)][0]
            glCallList( self.displayLists[ord(c)])
            glTranslate(width,0,0)
        glPopMatrix()                            
        glDisable(GL_TEXTURE_2D)

    def cacheText(self, text):
        ##TODO
        #glPushMatrix()
        #glTranslate(xPos,yPos,0)
        if not self.textCache.has_key(text):
            foo = glGenLists(1)
            print "foo = ", foo
            glNewList(foo, GL_COMPILE)
            glPushMatrix()            

            for c in text:
                width = self.charInfo[ord(c)][0]
                glCallList( self.displayLists[ord(c)])
                glTranslate(width,0,0)
            glPopMatrix()                            
            glEndList()
            self.textCache[text] = newList

        
    def getTextSize(self, text):
        w = 0
        h = 0
        for c in text:
            (width, height, coords) = self.charInfo[ord(c)]
            w += width
            h = max(height,h)
        return (w,h/1.4)
        

fontRegistery = {
    "comic sans ms":"comic.ttf",
    "courier new":"cour.ttf",
    "courier":"cour.ttf",    
    "impact":"impact.ttf",
    "microsoft sans serif":"micross.ttf",
    "times new roman":"times.ttf",
    "times":"times.ttf"
    }
    
