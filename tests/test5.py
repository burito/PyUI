import time
import pyui
from pyui.locals import *

        
class game:
    def __init__(self):

        # create gui objects
        #self.console = pyui.dialogs.Console(20,20,300,200)
        self.win = pyui.viewer.Viewer(50, 50, pyui)
        self.win.pack()

    
def run():
    
    import testopt
    opts = testopt.parseCommandLine(800, 600)
    pyui.init(*opts)
    pyui.desktop.getRenderer().setMouseCursor("cursor.png", 11,7)
    g = game()
    pyui.run()


if __name__ == '__main__':
    run()
