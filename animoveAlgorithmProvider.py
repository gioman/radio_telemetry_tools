import os
import subprocess

from PyQt4 import QtGui

from sextante.core.AlgorithmProvider import AlgorithmProvider

from mcp import mcp
from kernelDensity import kernelDensity


class animoveAlgorithmProvider(AlgorithmProvider):

    def __init__(self):
        AlgorithmProvider.__init__(self)
        self.alglist = [mcp()]
        
        can_execute_kernel = True
        try:
            from scipy.stats.kde import gaussian_kde
        except:
            try:
                from statsmodels.nonparametric import kernel_density
            except:
                # No gaussian_kde (scipy) or kernel_density (statsmodels)
                # We cannot execute the kernelDensity algorithm
                can_execute_kernel = False
        try:
            subprocess.call('gdal_contour')
        except:
            # Cannot execute gdal_contour
            can_execute_kernel = False
        
        if can_execute_kernel:
            self.alglist.append(kernelDensity())        

    def getDescription(self):
        return "AniMove (MCP and Kernel analysis UD)"

    def getName(self):
        return "AniMove"

    def getIcon(self):
        return  QtGui.QIcon(os.path.dirname(__file__)
                        + "/icons/animalmove.png")

    def _loadAlgorithms(self):
        self.algs = self.alglist

    def getSupportedOutputTableExtensions(self):
        return ["csv"]

    def supportsNonFileBasedOutput(self):
        return True
