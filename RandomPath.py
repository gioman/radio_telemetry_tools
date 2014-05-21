# -*- coding: utf-8 -*-

"""
***************************************************************************
    RandomPath.py
    ---------------------
    Date                 : May 2014
    Copyright            : (C) 2014 by Alexander Bruy
    Email                : alexander dot bruy at gmail dot com
***************************************************************************
*                                                                         *
*   This program is free software; you can redistribute it and/or modify  *
*   it under the terms of the GNU General Public License as published by  *
*   the Free Software Foundation; either version 2 of the License, or     *
*   (at your option) any later version.                                   *
*                                                                         *
***************************************************************************
"""

__author__ = 'Alexander Bruy'
__date__ = 'May 2014'
__copyright__ = '(C) 2014, Alexander Bruy'

# This will get replaced with a git SHA1 when you do a git archive

__revision__ = '$Format:%H$'

import math
import random

from PyQt4.QtCore import *
from PyQt4.QtGui import *

from qgis.core import *

from processing.core.Processing import Processing
from processing.core.GeoAlgorithm import GeoAlgorithm
from processing.core.ProcessingLog import ProcessingLog
from processing.core.GeoAlgorithmExecutionException import \
    GeoAlgorithmExecutionException
from processing.parameters.ParameterVector import ParameterVector
from processing.parameters.ParameterNumber import ParameterNumber
from processing.parameters.ParameterRange import ParameterRange
from processing.outputs.OutputVector import OutputVector


from processing.tools import dataobjects, vector


class RandomPath(GeoAlgorithm):
    PATHS_LAYER = 'PATHS_LAYER'
    BOUND_LAYER = 'BOUND_LAYER'
    ANGLE_RANGE = 'ANGLE_RANGE'
    ITERATIONS = 'ITERATIONS'
    OVERLAY_LAYER = 'OVERLAY_LAYER'
    RANDOM_PATHS = 'RANDOM_PATHS'

    def defineCharacteristics(self):
        self.name = 'Random path'
        self.group = 'Random HR/Path'

        self.addParameter(ParameterVector(self.PATHS_LAYER,
            'Input paths layer', [ParameterVector.VECTOR_TYPE_LINE]))
        self.addParameter(ParameterVector(self.BOUND_LAYER,
            'Study area layer', [ParameterVector.VECTOR_TYPE_POLYGON]))
        self.addParameter(ParameterRange(self.ANGLE_RANGE,
            'Range for the random angles', '0,360'))
        self.addParameter(ParameterNumber(self.ITERATIONS,
            'Number of iterations', 1, 999, 10))
        self.addParameter(ParameterVector(self.OVERLAY_LAYER,
            'Overlay layer',[ParameterVector.VECTOR_TYPE_LINE,
            ParameterVector.VECTOR_TYPE_POLYGON], optional=True))

        self.addOutput(OutputVector(self.RANDOM_PATHS, 'Random paths'))

    def processAlgorithm(self, progress):
        pathsLayer = dataobjects.getObjectFromUri(
            self.getParameterValue(self.PATHS_LAYER))
        boundLayer = dataobjects.getObjectFromUri(
            self.getParameterValue(self.BOUND_LAYER))
        overlayLayer = dataobjects.getObjectFromUri(
            self.getParameterValue(self.OVERLAY_LAYER))
        angles = self.getParameterValue(self.ANGLE_RANGE)
        iterations = int(self.getParameterValue(self.ITERATIONS))

        tmp = angles.split(',')
        minAngle = float(tmp[0])
        maxAngle = float(tmp[1])

        fields = QgsFields()
        fields.append(QgsField('id', QVariant.Int, '', 10, 0))
        fields.append(QgsField('intersect', QVariant.Int, '', 10, 0))
        writer = self.getOutputFromName(self.RANDOM_PATHS).getVectorWriter(
            fields, QGis.WKBMultiLineString, pathsLayer.dataProvider().crs())

        f = QgsFeature()
        f.initAttributes(2)
        f.setFields(fields)

        progress.setInfo('Analyze input data...')
        if boundLayer.featureCount() != 1:
            raise GeoAlgorithmExecutionException(
                'The study area layer should contain exactly one polygon or '
                'multipolygon.')

        if overlayLayer is not None:
            index = vector.spatialindex(overlayLayer)

        bbox = boundLayer.extent()
        extent = QgsGeometry().fromRect(bbox)

        request = QgsFeatureRequest()


        total = 100.0 / iterations

        output = []
        for i in xrange(iterations):
            features = vector.features(pathsLayer)
            for feature in features:
                geom = feature.geometry()
                if geom.isMultipart():
                    lines = geom.asMultiPolyline()
                    for points in lines:
                        output.append(self._randomPath(points, bbox, extent, minAngle, maxAngle))
                    geom = QgsGeometry.fromMultiPolyline(output)
                else:
                    points = geom.asPolyline()
                    output = self._randomPath(points, bbox, extent, minAngle, maxAngle)
                    geom = QgsGeometry.fromPolyline(output)

                intersects = 0
                if overlayLayer is not None:
                    rect = geom.boundingBox()
                    ids = index.intersects(rect)
                    for i in ids:
                        ft = overlayLayer.getFeatures(request.setFilterFid(i)).next()
                        tmpGeom = ft.geometry()
                        if geom.intersects(tmpGeom):
                            intersects = 1

                f.setGeometry(geom)
                f.setAttribute('id', feature.id())
                f.setAttribute('intersect', intersects)
                writer.addFeature(f)
                output[:] = []
            progress.setPercentage(int((i + 1) * total))

        del writer

    def _randomPath(self, points, bbox, extent, minAngle, maxAngle):
        random.seed()
        output = []
        rx = bbox.xMinimum() + bbox.width() * random.random()
        ry = bbox.yMinimum() + bbox.height() * random.random()
        pnt = QgsPoint(rx, ry)

        output.append(pnt)

        nIterations = 0
        nPoints = len(points)
        maxIterations = nPoints * 200

        da = QgsDistanceArea()
        #~ while nIterations < maxIterations and len(output) < nPoints:
            #~ for i in xrange(len(points) - 1):
                #~ p0 = output[-1]
                #~ p1 = points[i]
                #~ p2 = points[i + 1]
                #~ distance = da.measureLine(p1, p2)
#~
                #~ angle = minAngle + maxAngle * random.random()
#~
                #~ # correction for angles outside of 0 - 360
                #~ while (angle > 360.0):
                    #~ angle = angle - 360.0
                #~ while (angle < 0.0):
                    #~ angle = angle + 360.0
#~
                #~ angle = math.radians(angle)
                #~ zen = math.radians(90)
                #~ d = distance * math.sin(zen)
                #~ x = p0.x() + d * math.sin(angle)
                #~ y = p0.y() + d * math.cos(angle)
#~
                #~ pnt = QgsPoint(x, y)
                #~ geom = QgsGeometry.fromPoint(pnt)
                #~ if geom.within(extent):
                    #~ output.append(pnt)
#~
                #~ nIterations += 1

        for i in xrange(len(points) - 1):
            p0 = output[-1]
            p1 = points[i]
            p2 = points[i + 1]
            distance = da.measureLine(p1, p2)

            while True:
                angle = minAngle + maxAngle * random.random()

                # correction for angles outside of 0 - 360
                while (angle > 360.0):
                    angle = angle - 360.0
                while (angle < 0.0):
                    angle = angle + 360.0

                angle = math.radians(angle)
                zen = math.radians(90)
                d = distance * math.sin(zen)
                x = p0.x() + d * math.sin(angle)
                y = p0.y() + d * math.cos(angle)

                pnt = QgsPoint(x, y)
                geom = QgsGeometry.fromPoint(pnt)
                if geom.within(extent):
                    output.append(pnt)
                    break

        if len(output) < nPoints:
             ProcessingLog.addToLog(
                 ProcessingLog.LOG_INFO,
                 'Can not generate random path. Maximum number of attempts '
                 'exceeded.')

        return output
