# -*- coding: utf-8 -*-

import os
import subprocess

from PyQt4 import QtGui

from processing.core.AlgorithmProvider import AlgorithmProvider
from processing.core.ProcessingLog import ProcessingLog

from sextante_animove.mcp import mcp
from sextante_animove.kernelDensity import kernelDensity


class animoveAlgorithmProvider(AlgorithmProvider):

    def __init__(self):
        AlgorithmProvider.__init__(self)
        self.activate = False

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

        ProcessingLog.addToLog(ProcessingLog.LOG_INFO,
                    "Scipy found: " + str(has_scipy))
        ProcessingLog.addToLog(ProcessingLog.LOG_INFO,
                    "Statsmodels found: " + str(has_statsmodels))
        ProcessingLog.addToLog(ProcessingLog.LOG_INFO,
                    "gdal_contour found: " + str(has_gdal_contour))

        if has_gdal_contour and (has_scipy or has_statsmodels):
            self.alglist.append(kernelDensity())

        for alg in self.alglist:
            alg.provider = self

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
