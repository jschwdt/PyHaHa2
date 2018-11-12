# -*- coding: utf-8 -*-
##############################################################################
# File:                cold_chuck_plots.py
# Created:             2018-08-27
# Last modification:   2018-11-12
# Author:              Michael Hufschmidt <michael.hufschmidt@desy.de>
#                                         <michael@hufschmidt-web.de>
# Copyright:           (C) Michael Hufschmidt 2018
# License (CC BY 4.0): https://creativecommons.org/licenses/by/4.0/deed.de
###############################################################################

u"""
Module: cold_chuck_plots
************************
The module data_plots.py contains classes to create standard data plots,
mainly from from CV- and IV-measurements of silicon
particle detectors created by the cold chuck setup.
For usage, simply add the following code to your Python program::

    from cold_chuck_plots import *

The module contains the classes:

* class ColdChuckPlots (PyHaHaPlot2)
* class IVPlot (ColdChuckPlots)
* class VoltagePlot (ColdChuckPlots)
* class CVPlot (ColdChuckPlots)
* class CfPlot (ColdChuckPlots)
* class YZfPlot (ColdChuckPlots)

"""
from cold_chuck_tools import *
from pyhaha import *

class ColdChuckPlots (PyHaHaPlot2):
    """
    This class sets the plotting parameters and defines some
    defaults for other plot classes. The plotting parameters are
    read from a file (default filename is ``pyhaha_plot_defaults``)
    which should be in the current directory. They can be adjusted
    with a dictionary provided as parameter *params* the constructor.
    If the parameter file is not found,
    Python will exit with an error message,

    *ccds* : object or list of objects
        One or several instances of class ColdChuckData, all should
        be based on either .cv or .iv - files,
        otherwise Python will exit with an error message.

    *plotparams* : dictionary, optional
        This parameter is passed to the constructor of the class
        ``PyHaHaPlot2``. See documentation of that class.

    *plotparams_file* : string, optional
        This parameter is passed to the constructor of the class
        ``PyHaHaPlot2``. See documentation of that class.
    """

    def __init__(self, ccds,  plotparams=None, \
                plotparams_file="pyhaha_plot_defaults"):
        if isinstance(ccds, list):
            self._ccds = ccds
        else:
            self._ccds = [ccds]
        pass
        PyHaHaPlot2.__init__(self, plotparams, plotparams_file)


    def make_title(self):
        """
        *return* : string
            The default plot title, based on the filename of the ccd object.
            If a list of filenames is provided to the constructor,
            the title is based on the device name of the first file.
        """
        if (len(self._ccds) > 1):
            header = self._ccds[0].get_header() + 's on ' +\
            self._ccds[0].get_meta_data()['device'] + '\n'
        else:
            header = self._ccds[0].get_header() + ', File: ' +\
            self._ccds[0].get_file_name() + '\n'
            print(header)
        return header

    def save_plot(self, filename=''):
        """
        Save the current plot in a file (mostly a .pdf-file).

        *filename* : string, optional
            If empty, the filename is calcuated with ccd.get_file_name() or -
            if a list of filenames is provided to the constructor - with the
            device name of the first file.
        """
        if (filename == ''):
            if (len(self._ccds) > 1):
                savefile = self._ccds[0].get_meta_data()['device'] + '.' + \
                           self. _plotparams_['savefig.format']
            else:
                savefile = self._ccds[0].get_file_name() + '.' + \
                           self. _plotparams_['savefig.format']
        else:
            savefile = filename
        plt.savefig(savefile)
        msg = "Plot saved as " + savefile
        print(msg)

class IVPlot(ColdChuckPlots):
    """
    This class creates simple IV-Plot(s) from measured data.
    The parameter provided to the constructor has the following meaning:

    *ccds* : object or list of objects
        One or several instances of class ColdChuckData, all should
        be based on .iv - files,
        otherwise Python will exit with an error message.
        A plot is created for each of of the ColdChuckData objects.

    *plotparams* : dictionary, optional
        This parameter is passed to the constructor of the class
        ``PyHaHaPlot2``. See documentation of that class.

    *plotparams_file* : string, optional
        This parameter is passed to the constructor of the class
        ``PyHaHaPlot2``. See documentation of that class.
    """
    def __init__(self, ccds, plotparams=None, \
                plotparams_file="pyhaha_plot_defaults"):
        ColdChuckPlots.__init__(self, ccds, plotparams, plotparams_file)
        for ccd in self._ccds:
            if  (ccd.get_volts() is None) or\
                (ccd.get_i_gr() is None) or\
                (ccd.get_i_gr is None):
                msg = 'ERROR! Class IVPlot could not be instanciated:\n' +\
                       'Object "{}" is not a valid IV-File'.\
                       format(ccd.get_filepath())
                print(msg)
                sys.exit()
            pass
        pass

    def make_plot(self, labels=None, y_factor=1.0e9, y_unit='nA', with_GR=True):
        """
        Create a standard IV-plot.
        Note: After a previous call of set_voltage_index_range
        or set_voltage_range the x-axis is restricted to that range.

        *labels* : string or list of strings, optional
            If the class is instanciated with several ColdChuckData objects,
            each of the plots is labeled with a matching label form that list.

        *y_factor* : float, optional
            Multiplies the currents with *y_factor* before
            creating the plot, defaults to 1.0e9.

        *y_unit* : string, optional
            Sets the unit for the y-axis, should be based on the inverse of
            *y_factor*, defaults to 'nA'. The string can contain
            Latex Code, a call to this method could be for instance
            ``make_plot(1.0e6, r"$\mu$A")``

        *with_GR* : bool, optional
            If True, include IV for the guard ring. Default is True
        """
        plt.title(self.make_title())
        if isinstance(labels, list):
            my_labels = labels
        else:
            my_labels = [labels]
        for i in range(len(self._ccds)):
            ccd = self._ccds[i]
            volts = ccd.get_volts()
            i_pad = np.abs(ccd.get_i_pad())  # in A
            i_gr = np.abs(ccd.get_i_gr())    # in A
            if labels is None:
                plt.plot(volts, y_factor*i_pad, label='Pad')
                if with_GR:
                    plt.plot(volts, y_factor*i_gr, label='GR')
            else:
                plt.plot(volts, y_factor*i_pad, label=my_labels[i] + ', Pad')
                if with_GR:
                    plt.plot(volts, y_factor*i_gr, label=my_labels[i] + ', GR')
        plt.xlabel("Bias Voltage [V]")
        plt.ylabel("Current [" + y_unit + "]")
        plt.legend(loc='best')

class VoltagePlot(ColdChuckPlots):
    """
    This class creates simple Voltage-Plot(s) from measured data.
    The parameter provided to the constructor has the following meaning:

    *ccds* : object or list of objects
        One or several instances of class ColdChuckData.
        A plot is created for each of of the ColdChuckData objects.

    *plotparams* : dictionary, optional
        This parameter is passed to the constructor of the class
        ``PyHaHaPlot2``. See documentation of that class.

    *plotparams_file* : string, optional
        This parameter is passed to the constructor of the class
        ``PyHaHaPlot2``. See documentation of that class.
    """
    def __init__(self, ccds, plotparams=None, \
                plotparams_file="pyhaha_plot_defaults"):
        ColdChuckPlots.__init__(self, ccds, plotparams, plotparams_file)
        for ccd in self._ccds:
            if  (ccd.get_volts() is None):
                msg = 'ERROR! Class VoltagePlot could not be instanciated:\n' +\
                       'Object "{}" is not a valid .iv / .cv file'.\
                       format(ccd.get_filepath())
                print(msg)
                sys.exit()
            pass
        pass

    def make_plot(self, y_unit='[V]'):
        """
        Create a standard plot voltage versus index.
        Note: After a previous call of set_voltage_index_range
        or set_voltage_range the x-axis is restricted to that range.

        *y_unit* : string, optional
            Sets the unit for the y-axis, defaults to '[V]'.
        """
        plt.title(self.make_title())
        for i in range(len(self._ccds)):
            ccd = self._ccds[i]
            volts = ccd.get_volts()
            plt.plot(range(len(volts)), volts)
        plt.xlabel("Index")
        plt.ylabel("Voltage " + y_unit)
#        plt.legend(loc='best')


class CVPlot(ColdChuckPlots):
    """
    This class creates a simple CV-Plot from measured data.
    The parameter provided to the constructor has the following meaning:

    *ccds* : object or list of objects
        One or several instances of class ColdChuckData, all should
        be based on .cv - files,
        otherwise Python will exit with an error message.
        A plot is created for each of of the ColdChuckData objects.

    *plotparams* : dictionary, optional
        This parameter is passed to the constructor of the class
        ``PyHaHaPlot2``. See documentation of that class.

    *plotparams_file* : string, optional
        This parameter is passed to the constructor of the class
        ``PyHaHaPlot2``. See documentation of that class.
    """
    def __init__(self, ccds, plotparams=None, \
                plotparams_file="pyhaha_plot_defaults"):
        ColdChuckPlots.__init__(self, ccds, plotparams, plotparams_file)
        for ccd in self._ccds:
            if  (ccd.get_volts() is None) or\
                (ccd.get_cp() is None) or\
                (ccd.get_frequency_labels() is None):
                msg = 'ERROR! Class CVPlot could not be instanciated:\n' +\
                      'Object "{}" is not a valid CV-File'.\
                      format(ccd.get_filepath())
                print(msg)
                sys.exit()
            pass
        pass

    def make_plot(self, labels=None, y_factor=1.0e-24, y_unit=r"$pF^{-2}$"):
        """
        Create a standard CV-plot by plotting :math:`\\frac{1}{C^2}`
        versus :math:`V_{Bias}` .
        Note: After a previous call of set_voltage_index_range
        or set_voltage_range the x-axis is restricted to that range.

        *labels* : string or list of strings, optional
            If the class is instanciated with several ColdChuckData objects,
            each of the plots is labeled with a matching label form that list.

        *y_factor* : float, optional
            Multiplies the  :math:`\\frac{1}{C^2}` values
            with *y_factor* before creating the plot, defaults to 1.0e-24.

        *y_unit* : string, optional
            Sets the unit for the y-axis, should be based on the inverse of
            *y_factor*, defaults to :math:`pF^{-2}` .
            The string can contain Latex Code, a call to this method
            could be for instance ``make_plot(1.0, r"$F^{-2}$")``
        """
        plt.title(self.make_title())
        if isinstance(labels, list):
            my_labels = labels
        else:
            my_labels = [labels]
        for i in range(len(self._ccds)):
            ccd = self._ccds[i]
            volts = ccd.get_volts()
            cp = ccd.get_cp()
            freq_labels = ccd.get_frequency_labels()
            if labels is None:
                for fi in range(len(freq_labels)):   # frequency index
                    plt.plot(volts, y_factor * cp[:, fi] **(-2), \
                    label=freq_labels[fi])
            else:
                for fi in range(len(freq_labels)):   # frequency index
                    plt.plot(volts, y_factor * cp[:, fi] **(-2), \
                    label=my_labels[i] + ', ' + freq_labels[fi])

        plt.xlabel("Bias Voltage [V]")
        plt.ylabel(r"$C_p^{-2}$ [" + y_unit + "]")
        plt.legend(loc='lower right', ncol=2)

class CfPlot(ColdChuckPlots):
    """
    This class creates a simple Cf-Plot from measured data.
    The parameter provided to the constructor has the following meaning:

    *ccds* : object or list of objects
        One or several instances of class ColdChuckData, all should
        be based on .cv - files,
        otherwise Python will exit with an error message.
        A plot is created for each of of the ColdChuckData objects.

    *plotparams* : dictionary, optional
        This parameter is passed to the constructor of the class
        ``PyHaHaPlot2``. See documentation of that class.

    *plotparams_file* : string, optional
        This parameter is passed to the constructor of the class
        ``PyHaHaPlot2``. See documentation of that class.
    """
    def __init__(self, ccds, plotparams=None, \
                plotparams_file="pyhaha_plot_defaults"):
        ColdChuckPlots.__init__(self, ccds, plotparams, plotparams_file)
        for ccd in self._ccds:
            if  (ccd.get_volts() is None) or\
                (ccd.get_cp() is None) or\
                (ccd.get_frequencies() is None) or\
                (ccd.get_frequency_labels() is None):
                msg = 'ERROR! Class CfPlot could not be instanciated:\n' +\
                      'Object "{}" is not a valid CV-File'.\
                      format(ccd.get_filepath())
                print(msg)
                sys.exit()
            pass
        pass

    def make_plot(self, volts, labels=None, y_factor=1.0e12, y_unit="pF"):
        """
        Create a standard Cf-plot by plotting :math:`C_p` versus
        frequency for a given voltage or list of voltages.
        Note: After a previous call of set_voltage_index_range
        or set_voltage_range the voltages are restricted to that range.

        *volts* : float or list of floats
            Bias voltage(s) to create the plot for. A call could be for
            instance ``make_plot(5.0)`` or
            ``make_plot([5.0, 50.0, 200.0])``

        *labels* : string or list of strings, optional
            If the class is instanciated with several ColdChuckData objects,
            each of the plots is labeled with a matching label form that list.

        *y_factor* : float, optional
            Multiplies the :math:`C_p` values with *y_factor*
            before creating the plot, defaults to 1.0e12.

        *y_unit* : string, optional
            Sets the unit for the y-axis, should be based on the inverse of
            *y_factor*, defaults to ``pF`` .
        """
        plt.title(self.make_title() + 'Capacitance versus frequency')
        if isinstance(volts, list):
            v_list = volts
        else:
            v_list = [volts]
        if isinstance(labels, list):
            my_labels = labels
        else:
            my_labels = [labels]
        for i in range(len(self._ccds)):
            ccd = self._ccds[i]
            freqs = ccd.get_frequencies()
            volts = ccd.get_volts()
            cp = ccd.get_cp()
            for v in v_list:
                vi = ccd.v_index(v)
                v_label = "{} V".format(volts[vi])
                if labels is None:
                    plt.plot(freqs, y_factor * cp[vi, :], label=v_label)
                else:
                    plt.plot(freqs, y_factor * cp[vi, :], \
                    label=my_labels[i] + ', ' + v_label)
                pass
        plt.xlabel("Frequency [Hz]")
        plt.semilogx()
        plt.ylabel(r"$C_p$ [" + y_unit + "]")
        plt.legend(loc='best')

class YZfPlot(ColdChuckPlots):
    """
    This class creates a simple Yf-Plot or Zf-Plot (absolute value
    of the admittance or impedance) versus frequency from measured data.
    The parameter provided to the constructor has the following meaning:

    *ccds* : object or list of objects
        One or several instances of class ColdChuckData, all should
        be based on .cv - files,
        otherwise Python will exit with an error message.
        A plot is created for each of of the ColdChuckData objects.

    *plotparams* : dictionary, optional
        This parameter is passed to the constructor of the class
        ``PyHaHaPlot2``. See documentation of that class.

    *plotparams_file* : string, optional
        This parameter is passed to the constructor of the class
        ``PyHaHaPlot2``. See documentation of that class.
    """
    def __init__(self, ccds, plotparams=None, \
                plotparams_file="pyhaha_plot_defaults"):
        ColdChuckPlots.__init__(self, ccds, plotparams, plotparams_file)
        for ccd in self._ccds:
            if  (ccd.get_volts() is None) or\
                (ccd.get_Yabs_Phi() is None) or\
                (ccd.get_frequencies() is None) or\
                (ccd.get_frequency_labels() is None):
                msg = 'ERROR! Class YZfPlot could not be instanciated:\n' +\
                      'Object "{}" is not a valid CV-File'.\
                      format(ccd.get_filepath())
                print(msg)
                sys.exit()
            pass
        pass

    def make_plot(self, volts, labels=None, plot_type='Y'):
        """
        Create a standard Yf-plot or Zf-plot by plotting the
        admittance :math:`|Y|` or impedance :math:`|Z|`
        versus frequency for a given voltage or list of voltages.
        Note: After a previous call of set_voltage_index_range
        or set_voltage_range the voltages are restricted to that range.

        *volts* : float or list of floats
            Bias voltage(s) to create the plot for. A call could be for
            instance ``make_plot(5.0)`` or
            ``make_plot([5.0, 50.0, 200.0])``

        *labels* : string or list of strings, optional
            If the class is instanciated with several ColdChuckData objects,
            each of the plots is labeled with a matching label form that list.

        *plot_type* : string, optional
            Either 'Y', 'Z' or 'B'. Determines whether the admittance
            :math:`|Y|` (*plot_type* = 'Y'), or the impedance :math:`|Z|`
            (*plot_type* = 'Z') or both are plotted (*plot_type* = 'B').
            Note the different y-scales of both are plotted.
            Default is 'Y'.
        """
        if isinstance(volts, list):
            v_list = volts
        else:
            v_list = [volts]
        if isinstance(labels, list):
            my_labels = labels
        else:
            my_labels = [labels]
        if (plot_type == 'Y'):
            plt.title(self.make_title() + r'Admittance $|Y|$ versus  frequency')
            plt.ylabel(r"$|Y|$ [$\Omega^{-1}$]")
        elif  (plot_type == 'Z'):
            plt.title(self.make_title() + r'Impedance $|Z|$ versus frequency')
            plt.ylabel(r"$|Z|$ [$\Omega$]")
        elif  (plot_type == 'B'):
            plt.title(self.make_title() + \
                r'Admittance $|Y|$ and Impedance $|Z|$ versus frequency')
            plt.ylabel(r"$|Z|, |Y|$ [$\Omega, \Omega^{-1}$]")
        for i in range(len(self._ccds)):
            ccd = self._ccds[i]
            freqs = ccd.get_frequencies()
            volts = ccd.get_volts()
            Yabs, _Phi = ccd.get_Yabs_Phi()
            for v in v_list:
                vi = ccd.v_index(v)
                if labels is None:
                    my_label = "{} V".format(volts[vi])
                else:
                    my_label = my_labels[i] + ', ' +  '{} V'.format(volts[vi])
                if (plot_type == 'Y'):
                    plt.plot(freqs, Yabs[vi, :], label=my_label)
                elif  (plot_type == 'Z'):
                    plt.plot(freqs, 1.0 / Yabs[vi, :], label=my_label)
                elif  (plot_type == 'B'):
                    plt.plot(freqs, Yabs[vi, :], label=my_label)
                    plt.plot(freqs, 1.0 / Yabs[vi, :])
                    pass
        plt.xlabel("Frequency [Hz]")
        plt.loglog()
        plt.legend(loc='best')

