This tutorial explains how to install the AniMove for SEXTANTE plugin in a Windows system.

Install Quantum GIS
-------------------

First you have to install Quantum GIS. We recommend to install it using the OSGeo4W installer:

  http://hub.qgis.org/projects/quantum-gis/wiki/Download#12-OSGeo4W-Installer
  
The AniMove plugin depends on *scipy* (>=0.11) and the standalone installer does not provide it.
If you install Quantum GIS using the standalone installer, some options will not be available.

Then, install SEXTANTE using the *Plugins -> Fetch Python plugins* menu.


Download the plugin
-------------------

Download the plugin:

    http://plugins.qgis.org/plugins/sextante_animove 

Unpack the downloaded zip file and place the *sextante_animove* folder into *<osgeo4w_dir>/apps/qgis/python/plugins*.
Now the plugin is installed.

Install dependencies
--------------------

Aside from *scipy*, the AniMove plugin depends on *statsmodels* (>=0.5), which is not provided by the OSGeo4W 
installer. To install it, firts we need to install the Python package manager (*pip*). To do so, you can follow
the instructions here:

  http://nathanw.net/2012/12/19/installing-python-setuptools-into-osgeo4w-python
  
Basically, it says that we have to download `ez_setup.py <http://peak.telecommunity.com/dist/ez_setup.py>`_ and
put it into *<osgeo4w_dir>*. Then open *<osgeo4w_dir>/OSGeo4W.bat* and execute::

  $ python ez_setup.py
  $ easy_install pip
  
Then, install *pandas* (required by *statsmodels*) and *statsmodels*::

  $ pip install --upgrade pandas
  $ pip install --upgrade statsmodels
  
**NOTE**: At the time of writing, the *statsmodels* required version (0.5) was still not released. If after 
upgrading *statsmodels*, the package version is still lower than 0.5, all you can do is wait for them to make 
the final release.

Check the installation
----------------------

In order to check the installation, you can open the Python console from Quantum GIS and check::

  > import scipy
  > scipy.version.version
  (check version >= 0.11)

  > import statsmodels
  > statsmodels.version.version
  (check version >= 0.5)

Then, open the *SEXTANTE Toolbox* and use the AniMove algorithms. If they don't appear, open the 
*SEXTANTE options and configuration} and Activate AniMove.
