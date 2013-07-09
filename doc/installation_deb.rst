This tutorial explains how to install the AniMove for SEXTANTE plugin in a deb-based system (Ubuntu, Linux Mint,...). 
We assume that you have installed QGIS (<= 1.9) from the official deb repo (via Package Manager or apt-get).

Download the plugin
-------------------

First, you have to download the plugin itself from `http://plugins.qgis.org/plugins/sextante_animove <http://plugins.qgis.org/plugins/sextante_animove>`_.

Unpack the downloaded zip file and place the *sextante_animove* folder into *<user_home>/.qgis/python/plugins*. Now
the plugin is installed.

Install dependencies
--------------------

There are some dependencies that have to be installed in order to have all the algorithms and options available. 

To do so, we install *numpy*, *scipy* and *statsmodels*. Open a Terminal and execute::

  $ sudo apt-get install python-numpy python-scipy python-statsmodels
  
You can also install these packages using the Package Manager of your distribution.

Update dependencies
-------------------
  
Some dependency versions are required by the plugin in order to have all algorithms and options available 
(scipy >= 0.11, statsmodels >= 0.5). Since some deb distributions provided lower versions at the time of 
the writing, we need to update the Python packages. If your deb distribution provides package versions 
that match the plugin requirements, you can skip this section.

First, install the Python package manager (*pip*) and some required developer packages::

  $ sudo apt-get install python-pip libblas-dev liblapack-dev gfortran
  
Then, upgrade the *numpy* and *scipy* Python packages::

  $ sudo pip install --upgrade numpy scipy
  
Finally, install/upgrade *pandas* (required by *statsmodels*) and *statsmodels*::

  $ sudo pip install -- upgrade pandas
  $ sudo pip install -- upgrade statsmodels

**NOTE**: At the time of writing, the *statsmodels* required version (0.5) was still not released. If after upgrading
*statsmodels*, the package version is still lower than 0.5, all you can do is wait for them to make the final release.


Check the installation
----------------------

In order to check the installation, you can execute *python* from a Terminal::

  $ python
  
  > import scipy
  > scipy.version.version
  (check version >= 0.11)
  
  > import statsmodels
  > statsmodels.version.version
  (check version >= 0.5)
  
Then, you can execute QGIS, open the *SEXTANTE Toolbox* and use the AniMove algorithms. If they don't appear, open
the *SEXTANTE options and configuration* and *Activate* the AniMove algorithms.

