This tutorial explains how to install the AniMove for QGIS plugin in a deb-based system (Ubuntu, Linux Mint,...).
We assume that you have installed QGIS (<= 2.0) from the official deb repo (via Package Manager or apt-get).

Download the plugin
-------------------

First, you have to download the plugin:

  http://plugins.qgis.org/plugins/sextante_animove
  
Unpack the downloaded zip file and place the *sextante_animove* folder into *<user_home>/.qgis2/python/plugins*. Now
the plugin is installed.

Install dependencies
--------------------

There are some dependencies that have to be installed in order to have all the algorithms and options available. 

To do so, we install *numpy*, *scipy* and *statsmodels*. Open a Terminal and execute::

  $ sudo apt-get install python-numpy python-scipy
  
You can also install these packages using the Package Manager of your distribution.

Update dependencies
-------------------
  
Some dependency versions are required by the plugin in order to have all algorithms and options available 
(scipy >= 0.11, statsmodels >= 0.5). Since some deb distributions provided lower versions at the time of 
the writing, we need to update the Python packages. If your deb distribution provides package versions 
that match the plugin requirements, you can skip this section.

First, install the Python package manager (*pip*) and some required developer packages::

  $ sudo apt-get install python-dev python-pip libblas-dev liblapack-dev gfortran
  
Then, upgrade the *numpy* and *scipy* Python packages::

  $ sudo pip install --upgrade numpy scipy
  
Finally, install `statsmodels <http://statsmodels.sourceforge.net/devel/install.html>`_. Probably the
easiest way to install it is from source code. First, install the *patsy* and *pandas* dependencies::

  $ sudo pip install --upgrade patsy pandas

And then unpack the *.tar.gz* package and install::

  $ sudo python setup.py install

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
  
Then, you can execute QGIS, open the *Processing Toolbox* and use the AniMove algorithms. If they don't appear, open
the *Processing options and configuration* and *Activate* AniMove.

