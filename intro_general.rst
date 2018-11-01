General Introduction
********************

**PyHaHa2** is a software project within the Particle Physics and Detector
Development Group of the Universität Hamburg, Institut für
Experimentalpyhsik, http://wwwiexp.desy.de/groups/pd/ .
It is the upwards compatible successor of the PyHaHa project.

The objective is to provide universal Python classes to analyze
the data files created by several Labview programs, usually these are located
somewhere under m_data on the uh2usnmserver.
These classes can easily be adapted to specific needs and
analyses. Future expansions will be possible.


Recommended Software Stack
--------------------------
* Linux Ubuntu 16.04 (also tested on Ubuntu 14.04)
* Python 3.5.x (also tested with Python 2.7.6) with numpy, scipy, matplotlib.pyplot and others

**Warning:** Some classes require numpy version :math:`\ge` 1.11.

* Git (version control system for distributed software development)
* `Sphinx <http://www.sphinx-doc.org/en/stable/>`_ (tool to create intelligent and beautiful documentation like this one)

Helpful, but not absolutely neccessary:

* `Spyder3 <https://pythonhosted.org/spyder/>`_ (IDE for Python 3.5.x, alternatively Spyder for Python 2.7.x or any other editor.)
* `Pylint <https://www.pylint.org/>`_ for checking your source with respect to the `PEP 8 <https://pep8.org/>`_ style guide for Python code

Source code analysis with Pylint can be done within Spyder
(menu "Source" / "Run static code analysis"). You should target for
an overall rating > 7.0 of your programs.

Installlation and Update
------------------------
With ``git`` it is very easy to obtain the package and the complete history
of all sources including documentation. The complete reference to ``git``
is published at https://git-scm.com/doc, a simple introduction can
be found here: http://rogerdudler.github.io/git-guide/index.de.html .

First time users go to a directory where they collect their own
Python libraries (for instance ``~/my_Phyton_libs/`` and create
a sub-directory ``~/my_Python_libs/PyHaHa2``
under that directory with the command::

    git clone https://github.com/MiHuf/PyHaHa2.git

After that, you will find this document under ``PyHaHa2/doc/latex/PyHaHa2.pdf``

After some time it may be neccessary to update your local ``PyHaHa2``
directory with the latest project version. Therefore you should move
into your local ``PyHaHa2`` directory and use the command::

    git pull

To and create / update this documentation, move to the local ``PyHaHa2``
directory and use the command::

    make latexpdf

If that does not work "Extension error: Could not import extension
sphinx.ext.imgmath (exception: No module named imgmath)",
you will need to install python-pip or python3-pip from the software
center and then::

    pip3 install --user pip --upgrade
    pip3 install --user sphinx
    pip3 install --user sphinx --upgrade
    pip3 install --user pymysql
    pip3 install --user pymysql --upgrade

The last two lines are only needed for directly accessing data from
the database ``uh2detlab`` at ``uh2usnmfile01.desy.de``.

For active participation on the project you will need an own git account
with collaborator access to this project. Before doing any changes, be sure
to first update your local ``PyHaHa2`` directory with a ``git pull``.
You can then modify the source code or add new files in your local directory.
At the end of the day, after finishing your modifications, you should
publish your work with::

    git commit -a -m "Short description of my modifications"
    git push

Very useful are these git commands::

    git --help
    git status

Usage
-----

For using PyHaHa2 all the modules ``xxx.py`` defined in the directory PyHaHa2/
need to be accessable by your programs. Currently these are:

* ``pyhaha.py`` (Main module, imports all othe modules)
* ``cold_chuck_tools.py``
* ``transient_tools.py``
* ``pyhaha_plots.py``
* ``cold_chuck_plots.py``
* ``transient_plots.py``
* ``file_utils.py``
* ``conf.py`` (needed for Sphinx)

Rather than copying these files to your local development directory,
you should ensure, that you can use the modules from anywhere. You can achieve
this by modifying your local file ``~/.bashrc`` or ``~/.profile``
and add the line::

    export PYTHONPATH=$PYTHONPATH:'~/my_Python_libs/PyHaHa2/'

to the end of ``~/.bashrc`` or ``~/.profile``. When using the PyHaHa2
tools, you then only need to add the code line::

    from pyhaha import *

to the beginning of your Python program.

* Your datafile(s) ``xxx.iv`` or ``xxx.cv``

The datafiles can be located in your working directory
or in a separate directory (``data_dir``) provided as a parameter
to the constructor of the class ``ColdChuckData`` or ``ScopeData``.
or elsewhere.

* A copy the file ``pyhaha_plot_defaults`` in your woking directory

This file is requiued in your woking directory for all plot programs.
You can edit this file for using personal plot defaults.

In order to enable instances of ``ColdChuckData`` or ``ScopeData``
to load the files directly from the
GVFs shares ``m_data/macroscopic/`` or ``scratch_nmsamba/rd_data/`` on
uh2usnmserver, it is recommended to create symlinks  ``~/m_data/`` and
``~/scratch_nmsamba/`` in your home directory pointing to the
shares "smb://uh2usnmserver/xxx".

This can be done by mounting the shares m_data and
scratch_nmsamba with the file server (Nautilus) before: Connect to
"smb://uh2usnmserver/xxx" as registered user. Make sure to chose to save the
password forever. After that you can create the symlinks.

See also the function mount_gvfs() in the module file_utils.
