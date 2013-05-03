import os.path
from PyQt4 import QtGui
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from sextante.parameters.ParameterVector import ParameterVector
from sextante.core.QGisLayers import QGisLayers
from sextante.outputs.OutputVector import OutputVector
from animoveAlgorithm import AnimoveAlgorithm
try:  # qgis 1.8 sextante 1.08
    from sextante.ftools import ftools_utils
except:
    from sextante.algs.ftools import ftools_utils
from sextante.core.SextanteLog import SextanteLog
from sextante.parameters.ParameterTableField import ParameterTableField
from sextante.parameters.ParameterNumber import ParameterNumber


class mcp(AnimoveAlgorithm):

    INPUT = "INPUT"
    OUTPUT = "OUTPUT"
    FIELD = "FIELD"
    PERCENT = "PERCENT"

    def getIcon(self):
        return QtGui.QIcon(os.path.dirname(__file__) + "/icons/mcp.png")

    def processAlgorithm(self, progress):
        perc = self.getParameterValue(mcp.PERCENT)
        field = self.getParameterValue(mcp.FIELD)
        inputLayer = QGisLayers.getObjectFromUri(
                        self.getParameterValue(mcp.INPUT))

        inputProvider = inputLayer.dataProvider()
        inputProvider.select(inputProvider.attributeIndexes())

        fields = [QgsField("ID", QVariant.String),
                  QgsField("Area", QVariant.Double),
                  QgsField("Perim", QVariant.Double)
                 ]
        writer = self.getWriter(mcp.OUTPUT, fields,
                        QGis.WKBPolygon, inputProvider.crs())

        index = inputProvider.fieldNameIndex(field)
        uniqueValues = ftools_utils.getUniqueValues(inputProvider, index)

        GEOS_EXCEPT = True
        FEATURE_EXCEPT = True

        progress_perc = 100 / len(uniqueValues)
        n = 0
        for value in uniqueValues:
            nElement = 0
            hull = []
            cx = 0.00  # x of mean coodinate
            cy = 0.00  # y of mean coordinate
            nf = 0
            try:
                inputProvider.select(inputProvider.attributeIndexes())
            except:
                pass

            for feature in QGisLayers.features(inputLayer):
                fieldValue = self.getFeatureAttributes(feature)[index]
                if (fieldValue.toString().trimmed() ==
                        value.toString().trimmed()):
                    points = ftools_utils.extractPoints(feature.geometry())
                    cx += points[0].x()
                    cy += points[0].y()
                    nf += 1

            cx = (cx / nf)
            cy = (cy / nf)
            meanPoint = QgsPoint(cx, cy)
            distArea = QgsDistanceArea()
            distanceGeometryMap = {}
            features = QGisLayers.features(inputLayer)
            for feature in features:
                fieldValue = self.getFeatureAttributes(feature)[index]
                if (fieldValue.toString().trimmed() ==
                        value.toString().trimmed()):
                    nElement += 1
                    geometry = QgsGeometry(feature.geometry())
                    distance = distArea.measureLine(meanPoint,
                                                    geometry.asPoint())
                    distanceGeometryMap[distance] = geometry
                    if perc == 100:
                        points = ftools_utils.extractPoints(geometry)
                        hull.extend(points)

            if perc != 100:
                if perc > 100:
                    perc = 100
                    SextanteLog.addToLog(SextanteLog.LOG_WARNING,
                        "Please insert a valid percentage (0-100%)")

                hull = self.percpoints(perc, distanceGeometryMap, nElement)

            if len(hull) >= 3:
                try:
                    outFeat = QgsFeature()
                    outFeat.setGeometry(QgsGeometry.fromMultiPoint(hull).
                                        convexHull())
                    measure = QgsDistanceArea()
                    self.setFeatureAttributes(outFeat, [value.toString(),
                                        measure.measure(geometry),
                                        measure.measurePerimeter(geometry)])
                    writer.addFeature(outFeat)
                except:
                    GEOS_EXCEPT = False
                    continue
            n += 1
            progress.setPercentage(progress_perc * n)

        del writer

        if not GEOS_EXCEPT:
            SextanteLog.addToLog(SextanteLog.LOG_WARNING,
                "Geometry exception while computing convex hull")
        if not FEATURE_EXCEPT:
            SextanteLog.addToLog(SextanteLog.LOG_WARNING,
                "Feature exception while computing convex hull")

    def defineCharacteristics(self):
        self.name = "Minimun Convex Polygon"
        self.group = "Tools"
        self.addParameter(ParameterVector(mcp.INPUT, "Input layer",
                            ParameterVector.VECTOR_TYPE_POINT))
        self.addParameter(ParameterTableField(mcp.FIELD, "Field", mcp.INPUT))
        self.addParameter(ParameterNumber(mcp.PERCENT, "Percent of fixes",
                            5, 100, 95))
        self.addOutput(OutputVector(mcp.OUTPUT, "Minimun Convex Polygon"))

    def percpoints(self, percent, list_distances, l):
        l = (l * percent) / 100
        hull = []
        n = 1
        for k in sorted(list_distances.keys()):
            if n < l:
                points = ftools_utils.extractPoints(list_distances[k])
                hull.extend(points)
                n += 1
            else:
                return hull

        return hull
