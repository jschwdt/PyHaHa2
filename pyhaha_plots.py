# -*- coding: utf-8 -*-
##############################################################################
# File:                pyhaha_plots.py
# Created:             2018-09-10
# Last modification:   2018-09-17
# Author:              Michael Hufschmidt <michael.hufschmidt@desy.de>
#                                         <michael@hufschmidt-web.de>
# Copyright:           (C) Michael Hufschmidt 2018
# License (CC BY 4.0): https://creativecommons.org/licenses/by/4.0/deed.de
###############################################################################

u"""
Module: pyhaha_plots
********************
The module pyhaha_plots.py only contains the class PyHaHaPlot2 which is
the superclass class for other plot classes.  The picture below illustrates
the class hierarchy:

.. figure:: class_hierarchy.png
    :width: 80 %

It is not intended to instanciate PyHaHaPlot2 directly.
"""
from pyhaha import *

class PyHaHaPlot2():
    """
    This class sets the plotting parameters and defines some
    defaults for inherited  plot classes. The plotting parameters are
    read from a file (default filename is ``pyhaha_plot_defaults``)
    which should be in the current directory. They can be adjusted
    with a dictionary provided as parameter *params* the constructor.
    It is not intended to use this module directly.
    If the parameter file is not found,
    Python will exit with an error message.

    *plotparams* : dictionary, optional
        Parameters to be provided to plt.rcParams.update(...), to overwrite
        some paramters loaded from ``pyhaha_plot_defaults`` for this specific
        plot. Check the file ``matplotlibrc.orig`` for the format
        and meaning of the entries.

    *plotparams_file* : string, optional
        If empty, the parameters dictionary is read from the file
        ``pyhaha_plot_defaults``, which has to be present in the current
        directory. Otherwise you can define your onw filename. In any case,
        this file has to exist in the current directory.
    """

    _plotparams_ = dict()               # class variable

    def __init__(self, plotparams=None, plotparams_file="pyhaha_plot_defaults"):
#        print('PyHaHaPlot2.__init__')
        self.load_plotparams(plotparams_file)
        if plotparams is not None:
            PyHaHaPlot2._plotparams_.update(plotparams)
            plt.rcParams.update(plotparams)
        pass

    def get_plotparams(self):
        """
        *return* : dictionary
            plot parameters as currently stored in this class
        """
        return PyHaHaPlot2._plotparams_

    def update_plotparams(self, plotparams):
        """
        *params* : dictionary
            parameters to update the plt.rcParams.update(...),
            and the parameters stored in this class. These parameters will
            be used for all subsequent plots.
            Check the file ``matplotlibrc.orig`` for the format
            and meaning of the entries.
        """
        PyHaHaPlot2._plotparams_.update(plotparams)
        plt.rcParams.update(plotparams)

    def load_plotparams(self, plotparams_file="pyhaha_plot_defaults"):
        """
        Sets the default parameters to be provided to plt.rcParams.update(...),
        and stores them in a class variable.
        Check the file ``matplotlibrc.orig`` for the format
        and meaning of the entries.

        *plotparams_file* : string, optional
            If empty, the dictionary is read from the
            file ``pyhaha_plot_defaults``, otherwise you can define your
            plot parameters in a file of your own.
        """
        try:
            fi = open(plotparams_file, 'r')
            PyHaHaPlot2._plotparams_ = eval(fi.read())
            fi.close()
        except(IOError):
            msg = 'ERROR! Class PyHaHaPlot2 could not be instanciated:\n' +\
                   'File "{}" could not be opened'.format(plotparams_file)
            sys.exit(msg)
        plt.rcParams.update(PyHaHaPlot2._plotparams_)
        return None

