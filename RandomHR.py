# -*- coding: utf-8 -*-

"""
***************************************************************************
    RandomHR.py
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
from processing.core.ProcessingConfig import ProcessingConfig
from processing.core.GeoAlgorithm import GeoAlgorithm
from processing.core.GeoAlgorithmExecutionException import \
    GeoAlgorithmExecutionException
from processing.parameters.ParameterVector import ParameterVector
from processing.parameters.ParameterNumber import ParameterNumber
from processing.outputs.OutputVector import OutputVector
from processing.outputs.OutputHTML import OutputHTML
from processing.outputs.OutputFile import OutputFile

from processing.tools import dataobjects, vector


class RandomHR(GeoAlgorithm):
    HR_LAYER = 'HR_LAYER'
    STUDY_LAYER = 'STUDY_LAYER'
    ITERATIONS = 'ITERATIONS'
    RANDOM_HR = 'RANDOM_HR'
    HTML = 'HTML'
    RAW_DATA = 'RAW_DATA'
    SUMMARY_DATA = 'SUMMARY_DATA'

    def defineCharacteristics(self):
        self.name = 'Random HR'
        self.group = 'Random HR/Path'

        self.addParameter(ParameterVector(self.HR_LAYER,
            'Home ranges layer', [ParameterVector.VECTOR_TYPE_POLYGON]))
        self.addParameter(ParameterVector(self.STUDY_LAYER,
            'Study area layer', [ParameterVector.VECTOR_TYPE_POLYGON]))
        self.addParameter(ParameterNumber(self.ITERATIONS,
            'Number of iterations', 1, 999, 10))

        self.addOutput(OutputVector(self.RANDOM_HR, 'Random HR'))
        self.addOutput(OutputHTML(self.HTML, 'Random HR results'))
        self.addOutput(OutputFile(self.RAW_DATA, 'Raw output'))
        self.addOutput(OutputFile(self.SUMMARY_DATA, 'Output summary'))

    def processAlgorithm(self, progress):
        hrLayer = dataobjects.getObjectFromUri(
            self.getParameterValue(self.HR_LAYER))
        studyLayer = dataobjects.getObjectFromUri(
            self.getParameterValue(self.STUDY_LAYER))
        iterations = int(self.getParameterValue(self.ITERATIONS))

        toolLog = self.getOutputValue(self.HTML)
        rawFile = self.getOutputValue(self.RAW_DATA)
        sumFile = self.getOutputValue(self.SUMMARY_DATA)

        if studyLayer.featureCount() != 1:
            raise GeoAlgorithmExecutionException(
                'The study area layer should contain exactly one polygon or '
                'multipolygon.')

        # prepare frame polygon
        f = studyLayer.getFeatures(QgsFeatureRequest().setFilterFid(0)).next()
        rect = f.geometry().boundingBox()
        outside = QgsGeometry().fromRect(rect).difference(f.geometry())

        # generate output by copying features from home ranges layer
        crs = hrLayer.dataProvider().crs().authid()
        self.layer = QgsVectorLayer('MultiPolygon?crs=%s' % crs, 'tmp', 'memory')
        provider = self.layer.dataProvider()

        # also calculate areas
        areas = []
        da = QgsDistanceArea()

        features = vector.features(hrLayer)
        for f in features:
            provider.addFeatures([f])
            areas.append(da.measure(f.geometry()))

        # analyze source overlaps
        self.overlaps = []
        self.overlapsTotal = []

        self.overlaps += self._calculateOverlaps()
        self.overlapsTotal += [self._sum2d(self.overlaps[0])]

        html = '<table border="1">'
        html += '<tr><td colspan="3">'
        html += 'Number of homeranges: %d' % len(areas)
        html += '</td></tr>'
        html += '<tr><td colspan="3">'
        html += 'Total area of the homeranges: %.3f' % sum(areas)
        html += '</td></tr>'
        html += '<tr><td></td><td>total overlap area</td><td>SD</td></tr>'
        html += '<tr><td>observed</td><td>%.3f</td><td>n/a</td></tr>' % self.overlapsTotal[0]

        total = 100.0 / float(iterations)
        for i in xrange(iterations):
            for f in self.layer.getFeatures():
                sticksOut = True
                while sticksOut:
                    geom = self._rotate(f.geometry())
                    tries = 0
                    while sticksOut and tries < 50:
                        geom = self._move(geom, rect)
                        sticksOut = outside.intersects(geom)
                        tries += 1
                provider.changeGeometryValues({f.id(): geom})

            self.overlaps += self._calculateOverlaps()
            overlap = self._sum2d(self.overlaps[len(self.overlaps) - 1])
            self.overlapsTotal += [overlap]

            html += '<tr><td>iteration %d</td><td>%.3f</td><td>n/a</td></tr>' % (i + 1, overlap)

            progress.setPercentage(int((i + 1) * total))


        (mean, sd) = self._calculateStats()

        html += '<tr><td>mean</td><td>%.3f</td><td>%.3f</td></tr>' % (mean, sd)
        html += '</table>'
        html += '<h1>Result</h1>'

        dist = self.overlapsTotal[0] - mean
        if dist > 0:
            t = 'more'
        else:
            t = 'less'

        html += '<p>Distance between the observed and randomized value is: %0.3f (the observed one is %s).</p>' % (dist, t)
        html += '<p>The standard deviation is: %.3f.</p>' % sd
        html += '<p>The last iteration result has been saved.</p>'
        fl = open(toolLog, 'w')
        fl.write(html)
        fl.close()

        fields = QgsFields()
        fields.append(QgsField('id', QVariant.Int, '', 10, 0))
        writer = self.getOutputFromName(self.RANDOM_HR).getVectorWriter(
            fields, QGis.WKBMultiPolygon, hrLayer.dataProvider().crs())

        f = QgsFeature()
        f.initAttributes(1)
        f.setFields(fields)

        features = vector.features(self.layer)
        for feature in features:
            f.setGeometry(feature.geometry())
            f.setAttribute('id', feature.id())
            writer.addFeature(f)

        del writer

        self.writeRaw(rawFile, hrLayer, studyLayer, areas)
        self.writeSummary(sumFile, hrLayer, studyLayer)

    def _calculateOverlaps(self):
        # collect the geometries
        polygons = []
        for f in self.layer.getFeatures():
            geom = QgsGeometry(f.geometry())
            polygons.append(geom)

        # calculate
        result = []
        da = QgsDistanceArea()
        for i in range(len(polygons)):
            tmp = []
            for j in range(i + 1, len(polygons)):
                if polygons[i].intersects(polygons[j]):
                    overlap = da.measure(polygons[i].intersection(polygons[j]))
                else:
                    overlap = 0.0
                tmp.append(overlap)
            result += [tmp]
        return [result]

    def _sum2d(self, data):
        k = 0
        for i in data:
            for j in i:
                k += j
        return k

    def _rotate(self, geom):
        # randomize the angle
        angle = random.uniform(0, 2 * math.pi)
        sina = math.sin(angle)
        cosa = math.cos(angle)
        i = 0
        # create unique dict of verticles because of overlapping the
        # first and the last one
        unique = dict()
        vertex = geom.vertexAt(i)
        while vertex.x() != 0 and vertex.y() != 0:
            unique[i] = vertex
            vertex = geom.vertexAt( i )
            i += 1

        for key in unique.keys():
            vertex = unique[key]
            x = cosa * vertex.x() - sina * vertex.y()
            y = sina * vertex.x() + cosa * vertex.y()
            geom.moveVertex(x, y, key)

        return geom

    def _move(self, geom, rect):
        bbox = geom.boundingBox()
        # compute allowed movement range
        dxMin = rect.xMinimum() - bbox.xMinimum()
        dxMax = rect.xMaximum() - bbox.xMaximum()
        dyMin = rect.yMinimum() - bbox.yMinimum()
        dyMax = rect.yMaximum() - bbox.yMaximum()
        # randomize dx and dy
        dx = random.uniform(dxMin, dxMax)
        dy = random.uniform(dyMin, dyMax)
        # move
        geom.translate(dx, dy)
        return geom

    def _calculateStats(self):
        data = self.overlapsTotal[1:]
        mean = sum(data) / len(data)
        sd = 0
        for i in data:
            sd += (i - mean) * (i - mean)
        if len(data) > 1:
          sd = math.sqrt(sd / (len(data) - 1))
        else:
          sd = 0
        return (mean, sd)

    def writeSummary(self, fileName, hrLayer, studyLayer):
        sepField = ProcessingConfig.getSetting('FIELD_SEPARATOR')
        sepNumber = ProcessingConfig.getSetting('DECIMAL_SEPARATOR')

        with open(fileName, 'w') as f:
            f.write('Quantum GIS Random Home Range summary\n')
            f.write('Frame layer%s%s\n' % (sepField, studyLayer.name()))
            f.write('Home ranges layer%s%s\n' % (sepField, hrLayer.name()))
            f.write('Number of the home ranges%s%s\n' % (sepField, hrLayer.featureCount()))
            f.write('Number of iterations%s%s\n\n' % (sepField, len(self.overlaps) - 1))
            f.write(sepField + 'total overlap area' + sepField + 'SD\n')
            f.write('observed' + sepField + str(self.overlapsTotal[0]).replace('.', sepNumber) + sepField + '\n')
            for i in range(1, len(self.overlapsTotal)):
                f.write('iteration %s%s%s%s\n' % (i, sepField, str(self.overlapsTotal[i]).replace('.', sepNumber), sepField))

            (mean, sd) = self._calculateStats()
            f.write('mean' + sepField + str(mean).replace('.', sepNumber) + sepField + str(sd).replace('.',sepNumber) + '\n')
            f.write('observed-randomized' + sepField + str(self.overlapsTotal[0] - mean).replace('.', sepNumber) + sepField + '\n\n')

    def writeRaw(self, fileName, hrLayer, studyLayer, areas):
        sepField = ProcessingConfig.getSetting('FIELD_SEPARATOR')
        sepNumber = ProcessingConfig.getSetting('DECIMAL_SEPARATOR')

        with open(fileName, 'w') as f:
            f.write('Quantum GIS Random Home Range summary\n')
            f.write('Frame layer%s%s\n' % (sepField, studyLayer.name()))
            f.write('Home ranges layer%s%s\n' % (sepField, hrLayer.name()))
            f.write('Number of the home ranges%s%s\n' % (sepField, studyLayer.featureCount()))
            f.write('Number of iterations%s%s\n\n' % (sepField, len(self.overlaps) - 1))
            f.write('Note: The first column contains the home range area\n\n')
            for i in range(len(self.overlaps)):
                if i == 0:
                    f.write('Observed data:\n')
                else:
                    f.write('Iteration %s:\n' % i)

                for j in range(len(self.overlaps[i])):
                    text = str(areas[j]) + sepField
                    for k in range(len(self.overlaps[i]) - len(self.overlaps[i][j])):
                        text += sepField

                    for k in range(len(self.overlaps[i][j])):
                        val = self.overlaps[i][j][k]
                        text += str(val).replace('.', sepNumber) + sepField

                    text = text[:len(text) - 1] + '\n'
                    f.write(text)

                f.write('\n')
