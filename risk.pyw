import sys

from gui import riskgui
from gui import riskengine

try:
    import psyco #can't hurt - speeds up AI for autogames
    psyco.full()
except:
    pass #too bad

__version__ = "0.7.1"

if len(sys.argv) > 1 and sys.argv[1] == "-d":
    riskengine.debugging = 1

riskengine.setupdebugging()
riskengine.openworldfile("world.zip")
riskengine.loadterritories()
riskgui.setupdata()
riskgui.rungame()

