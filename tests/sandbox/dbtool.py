import testopt
import time
import pyui

from twisted.internet import main
from twisted.enterprise import adbapi, row

from pyui.desktop import getDesktop, getTheme, getRenderer
from pyui.database import DBGridPanel


class TPRow(row.RowObject):
    rowColumns = [ "identity_name", "perspective_name", "service_name", "perspective_type" ]
    
class AvatarRow(row.RowObject):
    rowColumns = [ "id", "name", "description", "startingroomid", "startingtownid", "score", "bodyid" ]

class RoomRow(row.RowObject):
    rowColumns = [
        "id", "townid", "name", "objecttypename", "description", "ownerid", "posx", "posy", "width","height" ]

class TestApp:
    """Test application for the DBGrid tests.
    """
    last = 0
    frames = 0
    reflector = None

    def __init__(self):
        opts = testopt.parseCommandLine(800, 600)
        pyui.init(800,600,"p3d")

        ## DB init stuff
        self.dbpool = adbapi.ConnectionPool("pyPgSQL.PgSQL", "sean", host="localhost:5432")    
        self.application = main.Application("testApp")
        self.reflector = row.DBReflector(self.dbpool, [], self.makeGrids)

        main.addTimeout(self.tick, 0.001)        # make sure we can be shut down on windows.
        self.application.run()
        
    def tick(self):
        try:
            pyui.core.update()
            pyui.core.draw()
        except:
            #TODO: handle exceptions properly!
            print "Exception in pyui"
            raise
        
        main.addTimeout(self.tick, 0.001)
        
        if not getDesktop().running:
            main.shutDown()
            pyui.quit()

        now = time.time()
        if  now - self.last > 1:
            print "FPS:", self.frames
            self.frames = 0
            self.last = now
        self.frames = self.frames + 1
    
    def makeGrids(self, dummy):
        self.w1 = pyui.widgets.Frame(30, 10, 600, 260, "Avatars")    
        self.g1 = DBGridPanel(AvatarRow, "avatars", [("id","int4")], 8, self.reflector)
        self.w1.replacePanel(self.g1)

        self.w2 = pyui.widgets.Frame(30, 300, 600, 260, "Perspectives")
        self.g2 = DBGridPanel(TPRow, "twisted_perspectives", [("identity_name","varchar"),
                                                              ("perspective_name","varchar"),
                                                              ("service_name","varchar")], 12, self.reflector)
        self.w2.replacePanel(self.g2)

if __name__ == '__main__':
    TestApp()
