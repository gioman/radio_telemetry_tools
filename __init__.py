def name():
    return "AniMove for SEXTANTE"


def description():
    return "MCP and Kernel functions for UD"


def version():
    return "Version 1.3.4"


def icon():
    return "icons/animalmove.png"


def qgisMinimumVersion():
    return "2.0"


def qgisMaximumVersion():
    return "2.99"


def author():
    return "Francesco Boccacci"


def email():
    return "francescoboccacci@libero.it"


def repository():
    return "https://github.com/geomatico/sextante_animove"


def classFactory(iface):
    from animoveProviderPlugin import animoveProviderPlugin
    return animoveProviderPlugin()
