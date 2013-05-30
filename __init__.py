def name():
    return "AniMove for SEXTANTE"


def description():
    return "MCP and Kernel functions for UD"


def version():
    return "Version 1.3.3"


def icon():
    return "icons/animalmove.png"


def qgisMinimumVersion():
    return "1.0"


def qgisMaximumVersion():
    return "1.8"


def author():
    return "Francesco Boccacci"


def email():
    return "francescoboccacci@libero.it"


def repository():
    return "https://github.com/geomatico/sextante_animove"


def classFactory(iface):
    from animoveProviderPlugin import animoveProviderPlugin
    return animoveProviderPlugin()
