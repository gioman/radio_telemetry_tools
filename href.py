import os
import re
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

from sextante.parameters.ParameterTableField import ParameterTableField
from sextante.parameters.ParameterNumber import ParameterNumber
import numpy as np
from scipy import stats
from osgeo import gdal, osr
import datetime
from sextante.core.SextanteUtils import SextanteUtils


class href(AnimoveAlgorithm):

    INPUT = "INPUT"
    OUTPUT = "OUTPUT"
    FIELD = "FIELD"
    PERCENT = "PERCENT"

    def getIcon(self):
        return QtGui.QIcon(os.path.dirname(__file__) + "/icons/href.png")

    def processAlgorithm(self, progress):
        currentPath = os.path.dirname(os.path.abspath(__file__))

        # Get parameters
        perc = self.getParameterValue(href.PERCENT)
        field = self.getParameterValue(href.FIELD)
        inputLayer = QGisLayers.getObjectFromUri(
                            self.getParameterValue(href.INPUT))
        resolution = 50

        # Adjust parameters if necessary
        if perc > 100:
            perc = 100

        # Get layer info and create the writer for the output layer
        epsg = inputLayer.crs().srsid()
        name = inputLayer.name()
        inputProvider = inputLayer.dataProvider()
        try:
            inputProvider.select(inputProvider.attributeIndexes())
        except:
            pass

        fieldIndex = inputProvider.fieldNameIndex(field)
        uniqueValues = ftools_utils.getUniqueValues(inputProvider, fieldIndex)

        fields = [QgsField("ID", QVariant.String),
                  QgsField("Area", QVariant.Double),
                  QgsField("Perim", QVariant.Double)]
        writer = self.getWriter(href.OUTPUT, fields,
                    QGis.WKBMultiLineString, inputProvider.crs())

        # Prepare percentage progress and start
        progress_perc = 100 / len(uniqueValues)
        n = 0
        for value in uniqueValues:
            # Filter x,y points with desired field value (value)
            xPoints = []
            yPoints = []
            for feature in QGisLayers.features(inputLayer):
                fieldValue = self.getFeatureAttributes(feature)[fieldIndex]
                if (fieldValue.toString().trimmed() ==
                            value.toString().trimmed()):
                    points = ftools_utils.extractPoints(feature.geometry())
                    xPoints.append(points[0].x())
                    yPoints.append(points[0].y())

            if len(xPoints) == 0:  # number of selected features
                continue

            # Compute kernel (X, Y, Z) with scipy.stats.kde.gaussian_kde --
            # Representation of a kernel-density estimate using Gaussian
            # kernels.
            xmin = min(xPoints) - 0.5 * (max(xPoints) - min(xPoints))
            xmax = max(xPoints) + 0.5 * (max(xPoints) - min(xPoints))
            ymin = min(yPoints) - 0.5 * (max(yPoints) - min(yPoints))
            ymax = max(yPoints) + 0.5 * (max(yPoints) - min(yPoints))
            X, Y = np.mgrid[xmin:xmax:complex(resolution),
                            ymin:ymax:complex(resolution)]
            positions = np.vstack([X.ravel(), Y.ravel()])
            values = np.vstack([xPoints, yPoints])
            kernel = stats.kde.gaussian_kde(values)
            Z = np.reshape(kernel(positions).T, X.T.shape)

            # Write kernel to GeoTIFF
            raster_name = (str(name) + '_' + str(perc) + '_' +
                        str(value.toString()) + '_' +
                        str(datetime.date.today()))
            self.to_geotiff(currentPath + '/raster_output/' + raster_name,
                        xmin, xmax, ymin, ymax, X, Y, Z, epsg)

            # Create contour lines (temporary .shp) from GeoTIFF
            if SextanteUtils.isWindows():
                cmd = "gdal_contour.exe "
            else:
                cmd = "gdal_contour "
            basename = "c" + str(n)
            shpFile = os.path.join(currentPath, basename + ".shp")
            print (cmd + currentPath + "/raster_output/"
                          + raster_name + " -a values -i 10 "
                          + shpFile)
            os.system(cmd + currentPath + "/raster_output/"
                          + raster_name + " -a values -i 10 "
                          + shpFile)

            # Read contour lines from temporary .shp
            layer = QgsVectorLayer(shpFile, basename, "ogr")
            provider = layer.dataProvider()
            try:
                provider.select(provider.attributeIndexes())
            except:
                pass

            # Create an array containing all polylines in the temporary
            # .shp and compute the sum of all areas and perimeters
            outGeom = []
            area = 0
            perim = 0
            measure = QgsDistanceArea()
            features = QGisLayers.features(layer)
            for feat in features:
                polyline = feat.geometry().asPolyline()
                polygon = QgsGeometry.fromPolygon([polyline])
                perim += measure.measurePerimeter(polygon)
                area += measure.measure(polygon)
                outGeom.append(polyline)

            # Create feature and write
            outFeat = QgsFeature()
            outFeat.setGeometry(QgsGeometry.fromMultiPolyline(outGeom))
            self.setFeatureAttributes(feature, [value.toString(), area, perim])
            writer.addFeature(outFeat)

            # Remove temporary files and update progress
            for f in os.listdir(currentPath):
                if re.search(basename + ".*", f):
                    os.remove(os.path.join(currentPath, f))
            n += 1
            progress.setPercentage(progress_perc * n)

        del writer

    def defineCharacteristics(self):
        self.name = "Kernel Density Estimation"
        self.group = "Tools"
        self.addParameter(ParameterVector(href.INPUT, "Input layer",
                            ParameterVector.VECTOR_TYPE_POINT))
        self.addParameter(ParameterTableField(href.FIELD, "Group fixes by",
                            href.INPUT))
        self.addParameter(ParameterNumber(href.PERCENT,
                            "Percentage of Utilisation Distribution(UD)",
                            5, 100, 95))
        self.addOutput(OutputVector(href.OUTPUT, "Kernel Density Estimation"))

    def to_geotiff(self, fname, xmin, xmax, ymin, ymax, X, Y, Z, epsg):
        '''
        saves the kernel as a GEOTIFF image
        '''
        driver = gdal.GetDriverByName("GTiff")
        out = driver.Create(fname, len(X), len(Y), 1, gdal.GDT_Float64)
        # pixel sizes
        xps = (xmax - xmin) / float(len(X))
        yps = (ymax - ymin) / float(len(Y))
        out.SetGeoTransform((xmin, xps, 0, ymin, 0, yps))
        coord_system = osr.SpatialReference()
        coord_system.ImportFromEPSG(epsg)
        out.SetProjection(coord_system.ExportToWkt())

        Z = Z.clip(0) * 100.0 / Z.max()

        out.GetRasterBand(1).WriteArray(Z.T)
