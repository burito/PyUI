import testopt
import time
import pyui

def onbutton(self):
    print "got a button " 
    
def run():
    opts = testopt.parseCommandLine(800, 600)
    done = 1
    frame = 0
    t = time.time()
    pyui.init(*opts)
    w = pyui.widgets.Frame(50, 100, 400, 400, "Test Window")
    m = pyui.widgets.FrameMenuBar()
    
    mm = pyui.widgets.FrameMenu("TestMe")
    mm.addItem("one", onbutton)
    mm.addItem("foobarme", onbutton)
    m.addMenu(mm)

    m2 = pyui.frame.FrameMenu("Second One")
    m2.addItem("Long test one", onbutton)
    m2.addItem("hello", onbutton)
    m2.addItem("Long test one", onbutton )
    m2.addItem("menu item", onbutton)
    m2.addItem("go go go ", onbutton)
    m2.addItem("Long test two", onbutton)

    m.addMenu(m2)
    w.setMenuBar(m)
    

    b = pyui.widgets.Button( "A button is here", onbutton)
    w.addChild(b)
    w.pack()

    w.setBackImage("max.bmp")
    pyui.run()

    print "done"
    pyui.quit()


if __name__ == '__main__':
    run()
