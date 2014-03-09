This tutorial explains how to install the AniMove for QGIS plugin in a Windows system. 

These instructions show how to install the plugin using the OSGeo4W installer. Due to some plugin 
dependencies, it is necessary to install the 32bit version, since the 64bit version doesn't provide all 
the required packages.

If you install Quantum GIS using the standalone installer or the 64bit version of the OSGeo4W installer, 
some options will not be available.

Install Quantum GIS
-------------------

First you have to install Quantum GIS:

  http://hub.qgis.org/projects/quantum-gis/wiki/Download#12-OSGeo4W-Installer
  
Please, make sure that you install *python-scipy*. As explained above, this package is only available in the 
32 bit version of the OSGeo4W installer.

Download the plugin
-------------------

Download the plugin:

    http://plugins.qgis.org/plugins/sextante_animove 

Unpack the downloaded zip file and place the *sextante_animove* folder into *<osgeo4w_dir>/apps/qgis/python/plugins*.
Now the plugin is installed.

Install statsmodels
-------------------

Aside from *scipy*, the AniMove plugin depends on the optional package *statsmodels* (>=0.5), which is not provided 
by the OSGeo4W installer. 

To install it, first you need to add the OSGeo4W Python version to the Windows registry. 

**IMPORTANT**: This process may cause unexpected behavior if you have another Python version already installed in
the Windows registry. 

To add Python to a Windows (64 bit) registry, create a pyhton27.reg file with this content::
  
  Windows Registry Editor Version 5.00
  
  [HKEY_LOCAL_MACHINE\SOFTWARE\Wow6432Node\Python]
  
  [HKEY_LOCAL_MACHINE\SOFTWARE\Wow6432Node\Python\PythonCore]
  
  [HKEY_LOCAL_MACHINE\SOFTWARE\Wow6432Node\Python\PythonCore\2.7]
  
  [HKEY_LOCAL_MACHINE\SOFTWARE\Wow6432Node\Python\PythonCore\2.7\Help]
  
  [HKEY_LOCAL_MACHINE\SOFTWARE\Wow6432Node\Python\PythonCore\2.7\Help\Main Python Documentation]
  @="C:\\OSGeo4W\\apps\\Python27\\Doc\\python274.chm"
  
  [HKEY_LOCAL_MACHINE\SOFTWARE\Wow6432Node\Python\PythonCore\2.7\InstallPath]
  @="C:\\OSGeo4W\\apps\\Python27\\"
  
  [HKEY_LOCAL_MACHINE\SOFTWARE\Wow6432Node\Python\PythonCore\2.7\InstallPath\InstallGroup]
  @="Python 2.7"
  
  [HKEY_LOCAL_MACHINE\SOFTWARE\Wow6432Node\Python\PythonCore\2.7\Modules]
  
  [HKEY_LOCAL_MACHINE\SOFTWARE\Wow6432Node\Python\PythonCore\2.7\PythonPath]
  @="C:\\OSGeo4W\\apps\\Python27\\Lib;C:\\OSGeo4W\\apps\\Python27\\DLLs;C:\\OSGeo4W\\apps\\Python27\\Lib\\lib-tk"

Or, for 32 bit machines::

  Windows Registry Editor Version 5.00
  
  [HKEY_LOCAL_MACHINE\SOFTWARE\Python]
  
  [HKEY_LOCAL_MACHINE\SOFTWARE\Python\PythonCore]
  
  [HKEY_LOCAL_MACHINE\SOFTWARE\Python\PythonCore\2.7]
  
  [HKEY_LOCAL_MACHINE\SOFTWARE\Python\PythonCore\2.7\Help]
  
  [HKEY_LOCAL_MACHINE\SOFTWARE\Python\PythonCore\2.7\Help\Main Python Documentation]
  @="C:\\OSGeo4W\\apps\\Doc\\python272.chm"
  
  [HKEY_LOCAL_MACHINE\SOFTWARE\Python\PythonCore\2.7\InstallPath]
  @="C:\\OSGeo4W\\apps\\Python27\\"
  
  [HKEY_LOCAL_MACHINE\SOFTWARE\Python\PythonCore\2.7\InstallPath\InstallGroup]
  @="Python 2.7"
  
  [HKEY_LOCAL_MACHINE\SOFTWARE\Python\PythonCore\2.7\Modules]
  
  [HKEY_LOCAL_MACHINE\SOFTWARE\Python\PythonCore\2.7\PythonPath]
  @="C:\\OSGeo4W\\apps\\Python27\\Lib;C:\\OSGeo4W\\apps\\Python27\\DLLs;C:\\OSGeo4W\\apps\\Python27\\Lib\\lib-tk"
  
Please, note that you may need to change all references to *C:\\\\OSGeo4W\\\\apps\\\\Python27\\\\* to your actual
installation path.

Then, you only need to download the *statsmodels-0.5.0.win32-py2.7.exe* package from PyPI::

  https://pypi.python.org/pypi/statsmodels
  
and install it. 

Check the installation
----------------------

In order to check the installation, you can open the Python console from Quantum GIS and check::

  > import scipy
  > scipy.version.version
  (check version >= 0.11)

  > import statsmodels
  > statsmodels.version.version
  (check version >= 0.5)

Then, open the *Processing Toolbox* and use the AniMove algorithms. If they don't appear, open the 
*Processing options and configuration} and Activate AniMove. If it's already active, try deactivating 
and activating again.
