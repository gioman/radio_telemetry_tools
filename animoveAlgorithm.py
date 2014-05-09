# -*- coding: utf-8 -*-

from processing.core.GeoAlgorithm import GeoAlgorithm


class AnimoveAlgorithm(GeoAlgorithm):

    def getFeatureAttributes(self, feature):
        try:
            return feature.attributeMap()
        except:
            return feature.attributes()

    def setFeatureAttributes(self, feature, attributes):
        try:
            atts = []
            for attribute in attributes:
                atts.append(attribute)
            feature.setAttributes(atts)
        except:
            i = 0
            for attribute in attributes:
                feature.addAttribute(i, attribute)
                i = i + 1

    def getWriter(self, name, fields, geomType, crs):
        try:
            return self.getOutputFromName(name).getVectorWriter(
                                fields, geomType, crs)
        except:
            i = 0
            fieldsMap = {}
            for field in fields:
                fieldsMap.update({i: field})
                i = i + 1
            return self.getOutputFromName(name).getVectorWriter(
                                fieldsMap, geomType, crs)
