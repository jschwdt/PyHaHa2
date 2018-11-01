# -*- coding: utf-8 -*-
##############################################################################
# File:                transient_plots.py
# Created:             2018-09-06
# Last modification:   2018-09-24
# Author:              Michael Hufschmidt <michael.hufschmidt@desy.de>
#                                         <michael@hufschmidt-web.de>
# Copyright:           (C) Michael Hufschmidt 2018
# License (CC BY 4.0): https://creativecommons.org/licenses/by/4.0/deed.de
###############################################################################

u"""
Module: transient_plots
***********************
The module transient_plots.py contains classes to create
standard data plots from scope data.
**Warning:** Some of the classes in this module
require numpy version :math:`\ge` 1.11.

For usage, simply add the following code to your Python program::

    from transient_plots import *

The module contains the classes:

* class TransientPlots (PyHaHaPlot2)
* class WaveformPlot (TransientPlots)
* class SpectrumPlot (TransientPlots)

"""
from pyhaha import *

class TransientPlots(PyHaHaPlot2):
    """
    This class sets the plotting parameters and defines some
    defaults for other plot classes. The plotting parameters are
    read from a file (default filename is ``pyhaha_plot_defaults``)
    which should be in the current directory. They can be adjusted
    with a dictionary provided as parameter *params* the constructor.
    If the parameter file is not found,
    Python will exit with an error message,

    *sds* : object or list of objects
        All have to be instances of class ScopeData
        otherwise Python will exit with an error message.
        **Note**: The current version only supports one instance.

    *plotparams* : dictionary, optional
        This parameter is passed to the constructor of the class
        ``PyHaHaPlot2``. See documentation of that class.

    *plotparams_file* : string, optional
        This parameter is passed to the constructor of the class
        ``PyHaHaPlot2``. See documentation of that class.
    """

    def __init__(self, sds, plotparams=None, \
                plotparams_file="pyhaha_plot_defaults"):
#        print('TransientPlots.__init__')
        self._sds = []
        if isinstance(sds, list):
            self._sds = sds
        else:
            self._sds = [sds]
        pass
        PyHaHaPlot2.__init__(self, plotparams, plotparams_file)

    def make_title(self):
        """
        *return* : string
            The default plot title, based on the filename of the sds object.
            If a list of filenames is provided to the constructor,
            the title is based on the device name of the first file.
        """
        header = self._sds[0].get_basename()
        return header

    def save_plot(self, filename=''):
        """
        Save the current plot in a file (mostly a .pdf-file).

        *filename* : string, optional
            If empty, the filename is calcuated with ccd.get_file_name() or -
            if a list of filenames is provided to the constructor - with the
            device name of the first file.
        """
        if filename == '':
            filename = self._sds[0].get_basename() + '.' + \
                self._plotparams_['savefig.format']
        plt.savefig(filename)
        msg = "Plot saved as " + filename
        print(msg)

class WaveformPlot(TransientPlots):
    """
    This class creates a waverform plot from measured data.
    The parameter provided to the constructor has the following meaning:

    *sds* : object or list of objects
        One or several instances of class ScopeData
        **Note**: The current version only supports one instance.

    *plotparams* : dictionary, optional
        This parameter is passed to the constructor of the class
        ``PyHaHaPlot2``. See documentation of that class.

    *plotparams_file* : string, optional
        This parameter is passed to the constructor of the class
        ``PyHaHaPlot2``. See documentation of that class.
    """
    def __init__(self, sds,
                 plotparams=None, plotparams_file="pyhaha_plot_defaults"):
#        print("MultiwaveformPlot.__init__")
        TransientPlots.__init__(self, sds, plotparams, plotparams_file)
        try:
            self._props = self._sds[0].get_props()
        except:
            msg = 'ERROR! Class MultiwaveformPlot could not be ' +\
                   'instanciated:\n' +\
                   'File "{}" is not a valid basename'.\
                   format(self._sds[0].get_basename())
            sys.exit(msg)
            pass
        pass

    def make_plot(self, data_slot=None, data_max=100, \
                  x_factor=1.0e9, x_unit='ns', \
                  y_factor=1.0e3, y_unit='mV'):
        """
        Create a ROHDE & SCHWARZ Multiwafeform Plot.

        *data_max* : integer, optional
            Only plot data with data-indexes up to
            *data_max*, default is 100.

        *data_slot* : integer, optional
            If set: Only plot data[data_slot], default is None, full
            spectrum will be plotted.

        *x_factor* : float, optional
            Multiplies the times with *x_factor* before
            creating the plot, defaults to 1.0e9.

        *x_unit* : string, optional
            Sets the unit for the x-axis, should be based on the inverse of
            *x_factor*, defaults to 'ns'. The string can contain
            Latex Code, a call to this method could be for instance
            ``make_plot(x_factor=1.0e6, x_unit=r"$\mu$s")``.

        *y_factor* : float, optional
            Multiplies the voltages with *y_factor* before
            creating the plot, defaults to 1.0e3.

        *y_unit* : string, optional
            Sets the unit for the y-axis, should be based on the inverse of
            *y_factor*, defaults to 'mV'. The string can contain
            Latex Code, a call to this method could be for instance
            ``make_plot(x_factor=1.0e6, x_unit=r"$\mu$V")``.
        """
        XStart = self._props['XStart']
        XStop = self._props['XStop']
        RecordLength = self._props['RecordLength']
        data = self._sds[0].get_data()
        plt.title(self.make_title())
        plt.xlabel("Time [" + x_unit + "]")
        plt.ylabel("Voltage [" + y_unit + "]")
        plt.grid(True)
        if data_slot is None:             # Spectrum plot
            xaxisrepeat = np.tile(x_factor * \
                    np.linspace(XStart, XStop, RecordLength), \
                    data_max)
            plt.plot(xaxisrepeat, y_factor * data[0 : data_max].flatten(), \
                    linewidth=0.1)
        else:                         # Single plot
            xaxis = x_factor * np.linspace(XStart, XStop, RecordLength)
            plt.plot(xaxis, y_factor * data[data_slot].flatten(), linewidth=0.1)


class SpectrumPlot(TransientPlots):
    """
    This class creates a spectrum plot from measured data.
    The parameter provided to the constructor has the following meaning:

    *sds* : object or list of objects
        One or several instances of class ScopeData
        **Note**: The current version only supports one instance.

    *plotparams* : dictionary, optional
        This parameter is passed to the constructor of the class
        ``PyHaHaPlot2``. See documentation of that class.

    *plotparams_file* : string, optional
        This parameter is passed to the constructor of the class
        ``PyHaHaPlot2``. See documentation of that class.
    """
    def __init__(self, sds,
                 plotparams=None, plotparams_file="pyhaha_plot_defaults"):
#        print("SpectrumPlot.__init__")
        TransientPlots.__init__(self, sds, plotparams, plotparams_file)
        try:
            self._props = self._sds[0].get_props()
        except:
            msg = 'ERROR! Class SpectrumPlot could not be ' +\
                   'instanciated:\n' +\
                   'File "{}" is not a valid basename'.\
                   format(self._sds[0].get_basename())
            sys.exit(msg)
            pass
        pass

    def make_plot(self, idx_min=2200, idx_max=3500, \
                  x_factor=1.0e9, x_unit='ns', \
                  y_factor=1.0e3, y_unit='mV'):
        """
        Create a spectrum plot.

        *idx_min* : integer, optional
            Only plot data with an rawdata-index starting at
            *idx_min*, default is 2200.

        *idx_max* : integer, optional
            Only plot data with an rawdata-index ending  at
            *idx_max*, default is 3500.

        *x_factor* : float, optional
            Multiplies the times with *x_factor* before
            creating the plot, defaults to 1.0e9.

        *x_unit* : string, optional
            Sets the unit for the x-axis, should be based on the inverse of
            *x_factor*, defaults to 'ns'. The string can contain
            Latex Code, a call to this method could be for instance
            ``make_plot(x_factor=1.0e6, x_unit=r"$\mu$s")``.

        *y_factor* : float, optional
            Multiplies the voltages with *y_factor* before
            creating the plot, defaults to 1.0e3.

        *y_unit* : string, optional
            Sets the unit for the y-axis, should be based on the inverse of
            *y_factor*, defaults to 'mV'. The string can contain
            Latex Code, a call to this method could be for instance
            ``make_plot(x_factor=1.0e6, x_unit=r"$\mu$V")``.
        """
        XStart = self._props['XStart']
        XStop = self._props['XStop']
        RecordLength = self._props['RecordLength']
        rawdata = self._sds[0].get_rawdata()

        plt.title(self.make_title())
        plt.xlabel("Time [" + x_unit + "]")
        plt.ylabel("Voltage [" + y_unit + "]")

        xaxis = x_factor * np.linspace(self._props['XStart'], \
                        self._props['XStop'], self._props['RecordLength'])
        yaxis = y_factor * (np.linspace(-128, 127, 256) * \
            self._props['ConversionFactor'] + self._props['ConversionOffset'])
        screen = np.ones((RecordLength, 256), dtype=np.int16)
        for x in range(0, RecordLength - 1):
            unique, counts = np.unique(rawdata['sig'][:,x], return_counts=True)
            for i, val in enumerate(unique, 0):
                screen[x, val+128] = counts[i]
        zmax = screen.max()
        print("idx_min:\t\t%d\t%.2e" % (idx_min, xaxis[idx_min]))
        print("idx_max:\t\t%d\t%.2e" % (idx_max, xaxis[idx_max]))
        print("zmax:\t\t%d\n" % zmax)
        plt.imshow(screen[idx_min:idx_max,:].T, aspect='auto', \
                   interpolation='bilinear', cmap='hot', origin='lower', \
                   extent=[xaxis[idx_min], xaxis[idx_max], \
                   yaxis[0], yaxis[255]], \
                   norm=colors.LogNorm(vmin=1, vmax=zmax))
        plt.colorbar()
