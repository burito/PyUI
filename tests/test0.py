import testopt
import time
import pyui
from pyui import widgets, frame, core

def onbutton(self):
    print "got a button " 
    
def run():
    opts = testopt.parseCommandLine(800, 600)
    done = 1
    t = time.time()
    core.init(*opts)
    w = widgets.Frame(50, 100, 400, 400, "Test Window")
    m = frame.FrameMenuBar()
    
    mm = frame.FrameMenu("TestMe")
    mm.addItem("one", onbutton)
    mm.addItem("foobarme", onbutton)
    m.addMenu(mm)

    m2 = frame.FrameMenu("Second One")
    m2.addItem("Long test one", onbutton)
    m2.addItem("hello", onbutton)
    m2.addItem("Long test one", onbutton )
    m2.addItem("menu item", onbutton)
    m2.addItem("go go go ", onbutton)
    m2.addItem("Long test two", onbutton)

    m.addMenu(m2)
    w.setMenuBar(m)
    

    b = widgets.Button( "A button is here", onbutton)
    w.addChild(b)
    w.pack()

    w.setBackImage("max.bmp")
    core.run()

    print "done"
    core.quit()


if __name__ == '__main__':
    run()
