# -*- coding: utf-8 -*-

def classFactory(iface):
    from sextante_animove.animoveProviderPlugin import animoveProviderPlugin
    return animoveProviderPlugin()
