Radio Telemetry Tools for the QGIS Processing Toolbox
-----------------------------------------------------

## Introduction

This plugin is a fork of

https://github.com/alexbruy/sextante_animove

that was a fork of

https://github.com/geomatico/sextante_animove

that was a fork of

https://github.com/volterra79/sextante_animove

As the development of this toolbox seems stopped in all the above repositories, we at NaturalGIS (http://www.naturalgis.pt/) will try to restore it with our own resources, starting from fixing the known issues and eventually adding new features.

The plugin was originally developed (in order) by:

* Francesco Boccacci
* Jorge Arévalo ([geomati.co](http://geomati.co))
* Víctor González ([geomati.co](http://geomati.co))
* Alexander Bruy for Faunalia

and financially supported by:

* Marco Zaccaroni - Department of Biology, University of Firenze
* Dimitris Poursanidis
* Giovanni Manghi
* Stefano Anile
* Wildlife Conservation Research Unit (WildCRU), University of Oxford
* Julia Hazel
* Prof. António Mira (University of Évora, Portugal, Unidade de Biologia da Conservação)
* Dr. Rosana Peixoto PhD

## Analyses

The Radio Telemetry Tools plugin implements, as a QGIS Processing toolbox, kernel analyses with the following algs:

* **href**: the *reference* bandwidth is used in the estimation.
* **LSCV (The Least Square Cross Validation)**: the *LSCV* bandwidth is used in the estimation.
* **Scott's Rule of Thumb**: the Scott's rule of thumb is used for bandwidth estimation.
* **Silverman's Rule of Thumb**: the Silverman's rule of thumb is used for bandwidth estimation.
* **kernel** with adjusted h.

Utilization distribution and contour lines are produced, and area of the contour polygons are calculated. Additionally, restricted Minimum Convex Polygons (MCP) are implemented, as:

* calculation of the smallest convex polygon enclosing all the relocations of the animal, excluding an user-selected percentage of locations furthest from a centre.

Since version 1.4.0 the plugin adds new functionalities:

* A porting to the Processing toolbox of the "RandomHR" plugin (Randomization of home ranges within a study area, see http://plugins.qgis.org/plugins/randomHR/) that was previously available for QGIS 1.x but not for 2.x

* A new tool called "Random Path" that allows to randomize paths (lines) with many options: keep angles, randomize angles (range as user choice), randomize starting points, keep starting points, use a point layer for starting points, check if the random path crosses features of a specified line/polygon layer.

## Python dependencies

* Some of the bandwidth methods are only available with the Python libraries **scipy** >= 0.11 (custom bandwidth value) and **statsmodels** >= 0.5 (LSCV, maximum likelihood cross-validation).

* The Python library **scipy** >= 0.10 **and** the **gdal_contour** utility **must** be installed in order to have the kernel density algorithm available. The latter is not a real dependency as the GDAL library (http://www.gdal.org/) and its utilities (http://www.gdal.org/gdal_utilities.html) are part of any QGIS installation on any platform.

### Installing the python dependencies

#### On Ubuntu GNU/Linux:

* On Ubuntu 14.04 (and derived distributions) and above:

    `sudo apt-get install python-scipy python-numpy python-pandas python-statsmodels`

#### On MS Windows:

* Install QGIS with the OSGeo4W installer (https://trac.osgeo.org/osgeo4w/) follwing the "advanced install" method

* Among the available (optional) libraries install "python-scipy" and "pyton-numpy"

* After the installation of QGIS save the following script (and .py file, not .txt) inside the "C:\OSGeo4W\apps\Python27" folder

    `https://raw.github.com/pypa/pip/master/contrib/get-pip.py`
    
* Open the "OSGeo4W" shell

* Launch the command 

    `python c:\OSGeo4W\apps\Python27\get-pip.py`
    
* Launch the commands

    `pip install pandas`
    
    `pip install statsmodels`
    
    `pip install numpy --upgrade`
    
### Installing the plugin

* Use the "Manage and Install plugins" tools in QGIS