from qgis.core import *
import os
import sys
import inspect
from processing.core.Processing import Processing
from animoveAlgorithmProvider import animoveAlgorithmProvider


cmd_folder = os.path.split(inspect.getfile(inspect.currentframe()))[0]
if cmd_folder not in sys.path:
    sys.path.insert(0, cmd_folder)


class animoveProviderPlugin:
    def __init__(self):
        self.provider = animoveAlgorithmProvider()

    def initGui(self):
        Processing.addProvider(self.provider)

    def unload(self):
        Processing.removeProvider(self.provider)
