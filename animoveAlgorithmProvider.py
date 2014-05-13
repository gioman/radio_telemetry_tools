# -*- coding: utf-8 -*-

import os
import subprocess

from PyQt4.QtGui import *

from processing.core.AlgorithmProvider import AlgorithmProvider
from processing.core.ProcessingLog import ProcessingLog
from processing.core.ProcessingConfig import Setting, ProcessingConfig

from sextante_animove.mcp import mcp
from sextante_animove.kernelDensity import kernelDensity
from sextante_animove.RandomHR import RandomHR


class animoveAlgorithmProvider(AlgorithmProvider):

    FIELD_SEPARATOR = 'FIELD_SEPARATOR'
    DECIMAL_SEPARATOR = 'DECIMAL_SEPARATOR'

    def __init__(self):
        AlgorithmProvider.__init__(self)

        self.activate = False

        self.alglist = [mcp(), RandomHR()]

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

        if has_gdal_contour and (has_scipy or has_statsmodels):
            self.alglist.append(kernelDensity())

        for alg in self.alglist:
            alg.provider = self

    def initializeSettings(self):
        AlgorithmProvider.initializeSettings(self)

        ProcessingConfig.addSetting(Setting('AniMove',
            self.FIELD_SEPARATOR, 'CSV field separator', ','))
        ProcessingConfig.addSetting(Setting('AniMove',
            self.DECIMAL_SEPARATOR, 'CSV decimal separator', '.'))

    def unload(self):
        AlgorithmProvider.unload(self)

        ProcessingConfig.removeSetting(self.FIELD_SEPARATOR)
        ProcessingConfig.removeSetting(self.DECIMAL_SEPARATOR)

    def getDescription(self):
        return 'AniMove'

    def getName(self):
        return 'AniMove'

    def getIcon(self):
        return  QIcon(os.path.dirname(__file__) + '/icons/animalmove.png')

    def _loadAlgorithms(self):
        self.algs = self.alglist

    def supportsNonFileBasedOutput(self):
        return True
