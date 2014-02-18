AniMove algorithms for QGIS
---------------------------

QGIS provides a processing environment that can be used to call native and third party algorithms,
making your spatial analysis tasks more productive and easy to accomplish.

AniMove plugin implements, as a processing submodule, kernel analyses with the following
algs:

* **href**: the *reference* bandwidth is used in the estimation.
* **LSCV (The Least Square Cross Validation)**: the *LSCV* bandwidth is used in the estimation.
* **Scott's Rule of Thumb**: the Scott's rule of thumb is used for bandwidth estimation.
* **Silverman's Rule of Thumb**: the Silverman's rule of thumb is used for bandwidth estimation.
* kernel with adjusted *h*

Utilization distribution and contour lines are produced, and area of the contour
polygons are calculated.

Additionally, restricted Minimum Convex Polygons (MCP) are implemented, as:

* MCP calculation of the smallest convex polygon enclosing all the relocations of the
animal, excluding an user-selected percentage of locations furthest from a centre.



Support
-------

Part of the [AniMove project](http://www.faunalia.it/animove) supported by Faunalia.

The plugin was developed by:

* Jorge Arévalo ([geomati.co](http://geomati.co))
* Francesco Boccacci 
* Víctor González ([geomati.co](http://geomati.co))

and financially supported by:

* Marco Zaccaroni - Department of Biology, University of Firenze
* António Mira
* Dimitris Poursanidis
* Giovanni Manghi
* Stefano Anile
* Wildlife Conservation Research Unit (WildCRU), University of Oxford
* Julia Hazel
