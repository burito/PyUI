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
        

    def draw(self, windows):
        self.clear()
        self.setup2D()
                
        for i in xrange(len(windows)-1, -1, -1):
            w = windows[i]
            self.setWindowOrigin(w.posX, w.posY)
            if w.dirty:
                ## use display lists for deferred rendering...
                w.drawWindow(self)
                w.displayList = glGenLists(1)
                glNewList(w.displayList, GL_COMPILE_AND_EXECUTE)
                for command in w.drawCommands:
                    apply(command[0], command[1:])
                glEndList()
            else:
                glCallList(w.displayList)

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

    def quit(self):
        pygame.quit()          
        

