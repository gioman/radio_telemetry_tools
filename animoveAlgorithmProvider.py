import os
import subprocess

from PyQt4 import QtGui

from sextante.core.AlgorithmProvider import AlgorithmProvider
from sextante.core.SextanteLog import SextanteLog

from mcp import mcp
from kernelDensity import kernelDensity


class animoveAlgorithmProvider(AlgorithmProvider):

    def __init__(self):
        AlgorithmProvider.__init__(self)
        self.alglist = [mcp()]

        # Check scipy
        try:
            from scipy.stats.kde import gaussian_kde
            has_scipy = True
        except:
            has_scipy = False
        # Check statsmodels
        try:
            from statsmodels.nonparametric import kernel_density
            has_statsmodels = True
        except:
            has_statsmodels = False
        # Check gdal_contour
        try:
            subprocess.call('gdal_contour')
            has_gdal_contour = True
        except:
            has_gdal_contour = False

        SextanteLog.addToLog(SextanteLog.LOG_INFO,
                    "Scipy found: " + str(has_scipy))
        SextanteLog.addToLog(SextanteLog.LOG_INFO,
                    "Statsmodels found: " + str(has_statsmodels))
        SextanteLog.addToLog(SextanteLog.LOG_INFO,
                    "gdal_contour found: " + str(has_gdal_contour))

        if has_gdal_contour and (has_scipy or has_statsmodels):
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
