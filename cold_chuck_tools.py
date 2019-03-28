# -*- coding: utf-8 -*-
##############################################################################
# File:                cold_chuck_tools.py
# Created:             2018-08-27
# Last modification:   2019-03-28
# Author:              Michael Hufschmidt <michael.hufschmidt@desy.de>
#                                         <michael@hufschmidt-web.de>
# Copyright:           (C) Michael Hufschmidt 2018
# License (CC BY 4.0): https://creativecommons.org/licenses/by/4.0/deed.de
###############################################################################

u"""
Module: cold_chuck_tools
************************
The module cold_chuck_tools.py contains classes to read
and analyse data-files from CV- and IV-measurements of silicon
particle detectors created by the cold chuck setup.
For usage, simply add the following code to your Python program::

    from cold_chuck_tools import *

The module defines the global constants:

* MYHOME (my home directory)
* M_DATA_DIR (= '~/m_data/' which shold be s symlink to a gvfs share)
* RD_DATA_DIR (= '/scratch_nmsamba/' which shold be s symlink to a gvfs share)
* DATE_REGEX (regular expression for dates in ISO format)

The module contains the classes:

* class ColdChuckData

"""

from file_utils import *
from pyhaha import *

MYHOME = os.getenv('HOME')
M_DATA_DIR  = MYHOME + '/m_data/'            # should be a symlink
RD_DATA_DIR = MYHOME + '/scratch_nmsamba/'   # should be a symlink
DATE_REGEX = '_[12][09][0-9][0-9]-[01][0-9]-[0-3][0-9]'


class ColdChuckData():
    """
    This class reads the data-files ``xxx.cv`` or ``xxx.iv`` created by the
    cold chuck lab setup. When using Python 3.x, the character-set will
    automatically be converted from iso-8859-1 (used by Windows XP) to
    utf-8 (used by Python). Suitable methods to obtain data are provided.

    To create an instance of ColdChuckData you can use as an exmaple::

        ccd = ColdChuckData('FTH200N_04_DiodeS_14_2015-11-05_4.cv', 'myDataDir')

    The parameter(s) provided to the constructor have the following meaning:

    *filename* : string
        Filename to read, e.g.
        ``FTH200N_04_DiodeS_14_2015-11-05_4.cv``
    *directory* : string, optional
        The directory which contains the data-file (if not it is not in the
        current directory).
    *fullpath* : string, optional
        If *filename* is an empty string, searching of the file
        in different directories as described below is skipped,
        and *fullpath* ist assumed to contain the absolute directory and
        filename, instanciation would then be::

            ccd = ColdChuckData(fullpath=<complete path + filename>)

    *logfile* : Instance of an open text-file or None
        If logfile points ot an open writeable text- file, error messages will
        be sent to the file, otherwise they will be printed to stdout.

    The file  ``FTH200N_04_DiodeS_14_2015-11-05_4.cv`` is looked for
    in directories according to the following order:

    1.) In Python's current directory ``./``

    2.) In the directory provided by the parameter *directory*

    3.) In ``<md>/macroscopic/FTH200N_04_DiodeS_14/``

    4.) In ``<md>/macroscopic/FTH200N/FTH200N_04_DiodeS_14/``

    ``<md>`` is the ``m_data``-directory within ``afs``. Under Linux it
    can be accessed from Python with
    ``/run/user/<uuu>/gvfs/smb-share:server=uh2usnmserver,share=m_data``.
    ``<uuu>`` is the numerical user-id (e.g. 26356) of the current user.
    This requires the smb-shares to be mounted, for instance by using a call
    to the function ``mount_gvfs() `` when starting the program.

    If the file is not found in either of these directories, Python will
    exit with an error message.
    """

    def __init__(self, filename='', directory='', fullpath='', logfile=None):
#        pyhaha.get_globals()
        # Try to open filename in local directory
        self._filepath = filename
        self._lines = []
        self._meta_lines = []
        self._meta_data = {}
        self._meta_data_lines = {}
        self._data_lines = []
        self._data = []
        self._data_rows = 0
        self._voltage_index_range = [0, 0]
        if (filename == ''):
            self._filepath = fullpath
            try:
                self._file_ext = fullpath[str.rindex(fullpath, '.'):]
            except:
                self._file_ext = ''
            self._file_name = fullpath[str.rindex(fullpath, '/') + 1:]
        else:
            self._file_name = filename
            try:
                self._file_ext = filename[str.rindex(filename, '.'):]
            except:
                self._file_ext = ''
            if not os.path.isfile(self._filepath):
                # Try 1.) filename in directory as provided with the parameter
                self._filepath = directory + '/' + filename
            if not os.path.isfile(self._filepath):
                # Try 3.)
                # .../macroscopic/tio2/tio2_2013-11-11_1.cv
                type_dir = filename[0:filename.find('_')] + '/'
                self._filepath = M_DATA_DIR + 'macroscopic/' + type_dir + filename
            if not os.path.isfile(self._filepath):
                # .../macroscopic/FTH200N/FTH200N_04_DiodeS_14/FTH200N_04_DiodeS_14_2015-11-05_4.cv
                type_dir = filename[0:filename.find('_')] + '/'
                match = re.search(DATE_REGEX, filename)
                if (match != None):
                    device = filename[0:filename.find(match.group())] # filename without date
                    self._filepath = M_DATA_DIR + 'macroscopic/' + \
                                     type_dir + device +"/" + filename
            if not os.path.isfile(self._filepath):
                # Try 4.)
                group_dir = filename[0:filename.find('_')] + '/'
                if (match != None):
                    match = re.search(DATE_REGEX, filename)
                    device = filename[0:filename.find(match.group())] # filename without date
                    self._filepath = M_DATA_DIR + 'macroscopic/' + \
                                     group_dir  +  \
                                     device +"/" + filename
            if not os.path.isfile(self._filepath):
                group_dir = filename[0:filename.find('_')].upper() + '/'
                match = re.search(DATE_REGEX, filename)
                if (match != None):
                    device = filename[0:filename.find(match.group())] # filename without date
                    self._filepath = M_DATA_DIR + 'macroscopic/' + \
                                     group_dir +  \
                                     device +"/" + filename
        try:
            if (sys.version_info.major == 3):
                fi = open(self._filepath, 'r', encoding='latin1')
            else:
                fi = open(self._filepath, 'r')
            for line in fi.readlines():
                self._lines.append(line.rstrip())
            pass
            fi.close()
        except(IOError):
            msg = '??? ColdChuckData ERROR: Class ColdChuckData ' +\
                  'could not be instanciated:\n' +\
                  'File "{}" could not be opened'.format(self._filepath)
            log_to_file(msg, logfile)
#            print(msg)
#            sys.exit()
            return None
        pass
        if len(self._lines) < 1:
            msg = '??? ColdChuckData ERROR: Class ColdChuckData ' +\
                  'could not be instanciated:\n' +\
                  'File "{}" is empty'.format(self._filepath)
            log_to_file(msg, logfile)
#            print(msg)
#            sys.exit()
            return None
        # populate _meta_lines and _data_lines from _lines
        is_meta_data = True            # seting for the first lines
        for nr in range(len(self._lines)):
            the_line = self._lines[nr].strip() # remove leading and trailing whitespaces
            if the_line[0 : 5] == 'BEGIN':
                is_meta_data = False
            if is_meta_data:           # collect meta data
                if (len(the_line)) == 0:  # skip empty lines
                    msg = '*** Line {} is empty!'.format(nr + 1)
                    log_to_file(msg, logfile)
#                    print(msg)
                    pass
                else:
                    self._meta_lines.append(the_line)
            else:                      # collect data
                if the_line[0 : 5] != 'BEGIN' and the_line[0:3] != 'END':
                  #  if (len(the_line) > 0):   # skip empty lines
                    self._data_lines.append(the_line)
            pass
        # populate _data
        self._data_rows = len(self._data_lines)
        try:
            cols = len(str.split(self._data_lines[0], '\t')) # could be done better
            self._data = np.zeros((self._data_rows, cols))
            for nr in range(self._data_rows):
                c = 0
                for col in self._data_lines[nr].split('\t'):
                    try:
                        x = float(col)
                    except:
                        x = 0.0
                    self._data[nr, c] = x
                    c += 1
                pass
            self._voltage_index_range = [0, self._data_rows -1]
        except IndexError:
            msg = "??? ColdChuckData: Bad Format in file {}".format(self._filepath)
            log_to_file(msg, logfile)
#            print(msg)
#            sys.exit()
            cols = []
            self._data = []
            self._voltage_index_range = []
        pass
        return None
    # End of the constructor

    def get_file_name(self):
        """
        *return* : string
            The filename of the data-file as provided to the constructor.
        """
        return self._file_name

    def get_file_ext(self):
        """
        *return* : string
            The extension of the data-file (mostly .cv or .iv)
        """
        return self._file_ext

    def get_filepath(self):
        """
        *return* : string
            The path where the data-file was finally found
        """
        return self._filepath

    def get_lines(self):
        """
        *return* : list of string
            All lines in the data-file
        """
        return self._lines

    def get_meta_lines(self):
        """
        *return* : list of string
            All lines in the data-file containing meta-data
            (up to the first 'BEGIN')
        """
        return self._meta_lines

    def get_data_lines(self):
        """
        *return* : list of string
            All lines in the data-file between 'BEGIN' and 'END' (the data)
        """
        return self._data_lines

    def get_header(self):
        """
        *return* : string
            The first line of the data-file
        """
        try:
            head = self._lines[0]
        except:
            head = None
        return head

    def get_meta_data(self, with_line_number=False):
        """
        This method builds a dictionary for all meta_data. The index is taken
        from lines beginning or ending with ':' excluding the ':' itself
        (e.g.'tester' or 'Annealing time [min]').
        The content is given by subsequent line(s) (e.g. 'Michael')
        and is either a string or a list of strings.
        For instance
        ``print(ccd.get_meta_data()['tester'])`` may print ``Michael``.

        New in Version 0.9.9.3: Lines ending with a ':' are also recognized as
        an index. Empty lines are ignored.
        Parameters:

        *with_line_number* : bool, optional
            If True, the line number is added to the index (e.g. '07: tester').

            If *with_line_number* = True, the complete meta-data can then be
            printed by::

                for k in sorted(ccd.get_meta_data(True)):
                    print(k, ccd.get_meta_data(True)[k])

        *return* : dictionary
            containing all meta-data as key / value pairs of strings
        """
        def is_key(line):
            # checks whether a line is a key
            key = False
            if (len(line)) > 0:
                key = (line[0] == ':') or line.endswith(':')
            return key

        def add_to_meta_data(nr, key, values):
            # adds a key / value pair entry as string,
            # if value consits of several lines, a list of strings is added.
            if (len(values) == 1):
                value = values[0]
            else:
                value = values
            self._meta_data[key] = value
            self._meta_data_lines['{:02d}: {:s}'.format(nr, key)] = value
            return

        self._meta_data = {}
        self._meta_data_lines = {}
        key = ''
        values = []
        count = len(self._meta_lines)
        if (count is None) or (count == 0):
            return None
        dict_nr = 0
        nr = 0
        while True:                    # loop through meta lines
            the_line = self._meta_lines[nr]
            if (is_key(the_line)):     # line is a key
                if (len(key) > 0):     # add previous entry to dict
                    add_to_meta_data(dict_nr, key, values)
                key = the_line.strip(':')
                values = []
                dict_nr = nr + 1
            else:                      # line is data
                values.append(the_line)
            pass
            nr += 1
            if (nr >= count):
                add_to_meta_data(dict_nr, key, values)  # add last entry to dict
                break
        if with_line_number:
            return self._meta_data_lines
        else:
            return self._meta_data

    def get_data(self, i_range=None):
        """
        *return* : numpy array of float
            Data lines, interpreted as 2-dimesional array of floats.
            Note: After a previous call of set_voltage_index_range
            or set_voltage_range only the restricted part of the
            measured data is returned.
        """
        if i_range == None:
            return self._data[self._voltage_index_range[0] : self._voltage_index_range[1] + 1, :]
        else:
            return self._data[i_range[0] : i_range[1] + 1, :]

    def set_data(self, new_data):
        """
        Replaces the origial datalines within the class instance by the numpy
        array new_data which may contain
        manipulated data (for instance with an offset calcutaion). Subsequent
        calls to get_data() will then return the new numpy array. Parameters:

        *new_data* : numpy array
            New data lines, 2-dimesional array of float, to be
            stored in the class instance

        *return* :
            No return value
        """
        self._data = new_data
        return None


    def get_frequencies(self):
        """
        This method returns ``None`` if not a .cv file. Otherwise:

        *return* : list of float
            All frequencies as from the meta-data line 'List of frequencies'
            for further calculations. Example:
            ``[490.0, 1010.0, 1900.0, 5000.0]``
        """
        if (self._file_ext.lower() != '.cv'):
            return None
        freqs = self.get_meta_data()['List of frequencies'].split(',')
        freqs.remove('')              # remove empty item at the end
        numbers = []
        for value in freqs:
            number = value.rstrip(string.ascii_letters)         # remove unit
            number = float(number.strip())
            unit = value.lstrip('0123456789,.').strip().lower() # remove number
            if unit == 'mhz':
                number = 1.0e6 * number
            elif unit == 'khz':
                number = 1.0e3 * number
            else:
                pass
            numbers.append(number)
        return np.array(numbers)

    def get_frequency_labels(self, decimal=0):
        """
        This method returns ``None`` if not a .cv file. Otherwise:

        *decimal* : int, optional
            Number of digits after the decimal point, defaults to zero.

        *return* : list of string
            All frequencies as from the meta-data line 'List of frequencies',
            reformated with <*decimal*> digits after the decimal point,
            together with a suitable unit (e.g. 'Hz', 'kHz', 'MHz').
            The units are chosen so that the numbers will always be < 1000.
            Example: ``['490 Hz', '1 kHz', '2 kHz', '5 kHz']``.
            Useful for labeling data-lines in a plot.
        """
        if (self._file_ext.lower() != '.cv'):
            return None
        labels = []
        for fr in self.get_frequencies():
            if fr >= 1.0e6:
                labels.append('{0:.{1}f} MHz'.format(fr / 1.0e6, decimal))
            elif fr >= 1.0e3:
                labels.append('{0:.{1}f} kHz'.format(fr / 1.0e3, decimal))
            else:
                labels.append('{0:.{1}f} Hz'.format(fr, decimal))
            pass
        return labels

    def get_volts(self):
        """
        *return* : list of float
            The first column of the data array (the voltage)
            Note: After a previous call of set_voltage_index_range
            or set_voltage_range only the restricted part of the
            measured data is returned.
        """
        try:
            return self._data[self._voltage_index_range[0] \
                : self._voltage_index_range[1] + 1, 0]
        except TypeError:
            return None
        except IndexError:
            return None

    def v_index(self, volt_in):
        """
        For a given voltage or a given list of voltages provided as parameter
        *volt_in*, this method searches for an item in the numpy-list of
        voltages from that data-file which is closest to that voltage(s) and
        either returns the index or a list of indices.
        The voltages in the data-file **must** be ordered monotonic in
        ascending order. (Hence not suitable for hysteresis measurements!)

        *volt_in* : float or list of floats
            Voltage to search for in the data-file.

        *return* : int or list of int
            Index (indices) of the item(s) in the data-file.
            Note: After a previous call of set_voltage_index_range
            or set_voltage_range the return values are restricted
            to that range.
        """
        volts = self.get_volts()
        indices = []
        if isinstance(volt_in, list):
            v_list = volt_in
        else:
            v_list = [volt_in]
        for v in v_list:
            vi = 0                         # voltage index
            err = 1.0e3                    # start with a large value
            while (vi < len(volts)) and (np.abs(volts[vi] - float(v)) < err):
                err = np.abs(volts[vi] - v)
                vi = vi + 1
            indices.append(vi - 1)
        if isinstance(volt_in, list):
            return indices
        else:
            return indices[0]

    def set_voltage_index_range(self, i_range=None):
        """
        This method sets an index range for voltages in the data array so that
        the return values from **all subsequent calls**  to the get_xxx -
        methods will be restricted to the given voltage indices.

        Particularly all subsquent plots and fits will only use that
        index range. To reset the index range to full range use
        ``set_voltage_index_range()``

        *i_range* : list of exactly two integers
            Sets the first and the last voltage index for data output, for
            instance ``set_voltage_index_range([10, 40])``
        """
        if (i_range == None):
            self._voltage_index_range = [0, self._data_rows - 1]
        else:  # $$$ TODO: Check!!!
            self._voltage_index_range = [max(0, i_range[0]), \
                min(self._data_rows, i_range[1])]
            pass
        return None

    def set_voltage_range(self, v_min=None, v_max=None):
        """
        This method calls ``set_voltage_index_range(...)`` (see asbove) to
        set an index range for voltages in the data array so that
        the return values from **all subsequent calls**  to the get_xxx -
        methods will be restricted to the given voltage range.
        Particularly all subsquent plots and fits will only use that
        voltage range.

        The indices are calculated by calling the method ``v_index(...)``,
        hence it will work properly only if the voltages in the
        data-file are ordered monotonic an ascending order. (No hysteresis
        measurements!)

        A valid call could be ``set_voltage_range(5.0, 100.0)``

        To reset the voltage range to full range use ``set_voltage_range()``

        *v_min* : float, optional
            Sets the lower voltage limit, defaults to the minimal voltage
            in the data array.

        *v_max* : float, optional
            Sets the upper voltage limit, defaults to the maximal voltage
            in the data array.
        """
        self.set_voltage_index_range()
        if (v_min != None):
            i_min = self.v_index(v_min)
        else:
            i_min = 0
        if (v_max != None):
            i_max = self.v_index(v_max)
        else:
            i_max = self._data_rows
        self.set_voltage_index_range([i_min, i_max])
        return None

    def get_temps(self):
        """
        *return* : list of float
            The second column of the data array (the temperature).
            Note: After a previous call of set_voltage_index_range
            or set_voltage_range the return values are restricted
            to that range.
        """
        return self._data[self._voltage_index_range[0] \
            : self._voltage_index_range[1] + 1, 1]

    def get_cp(self, factor=1.0):
        """
        This method returns ``None`` if not a .cv file. Otherwise:

        Returns the :math:`C_p`-values (capacitance of an equivalent
        parallel circuit) from the data. These are directly provided by
        the Agilent LRC meter (assuming the default setting to
        :math:`C_p`-mode).

        .. image:: Cp_Cs.png
            :align: center
            :width: 90 %


        *factor* : float, optional
            multiplies the :math:`C_p`-values  with *factor* when
            returning the array. For instance a ``get_cp(1e12)`` will
            return capacitances in pF rather than F.

        *return* : 2-dimensional numpy array of float
            :math:`C_p`-values, multiplied by *factor*, one line
            for each voltage, one column for each frequency.
            Note: After a previous call of set_voltage_index_range
            or set_voltage_range the return values are restricted
            to that range.
        """
        if (self._file_ext.lower() != '.cv'):
            return None
        num_f = len(self.get_frequencies())
        return  factor * self._data[self._voltage_index_range[0] \
            : self._voltage_index_range[1] + 1, 2 : 2 + num_f]

    def get_gp(self, factor=1.0):
        """
        This method returns ``None`` if not a .cv file. Otherwise:

        Returns the  :math:`G_p`-values (admittance of an equivalent
        parallel circuit, :math:`G_p = \\frac{1}{R_p}`, see figure above)
        directly from the data, as they are provided by the Agilent LRC meter
        (assuming the default setting to :math:`C_p`-mode).
        Note: The :math:`G_p`-values can be negative!

        *factor* : float, optional
            multiplies the :math:`G_p`-values  with *factor* when
            returning the array.

        *return* : 2-dimensional numpy array of float
            :math:`G_p`-values, one line for each voltage,
            one column for each frequency.
            Note: After a previous call of set_voltage_index_range
            or set_voltage_range the return values are restricted
            to that range.
        """
        if (self._file_ext.lower() != '.cv'):
            return None
        num_f = len(self.get_frequencies())
        return  factor * self._data[self._voltage_index_range[0] \
            : self._voltage_index_range[1] + 1, 2 + num_f :]


    def get_Y(self, factor=1.0):
        """
        This method returns ``None`` if not a .cv file. Otherwise:

        Returns the complex admittance :math:`Y = G_p + i \; \omega \cdot C_p`
        directly from the values provided by the Agilent LRC meter (assuming
        the default setting to :math:`C_p`-mode). For the norm :math:`|Y|`
        and the phase :math:`\phi_Y`, the function ``get_Yabs_Phi`` should be
        used. The complex impedance ``Z`` can be calcluated from that using
        Python's complex arithmetic :math:`Z = 1 / Y`.

        *factor* : float, optional
            multiplies the :math:`Y`-values  with *factor* when
            returning the complex array.

        *return* : 2-dimensional numpy array of complex
            :math:`Y`-values, one line for each voltage,
            one column for each frequency.
            Note: After a previous call of set_voltage_index_range
            or set_voltage_range the return values are restricted
            to that range.
        """
        if (self._file_ext.lower() != '.cv'):
            return None
        cp = self.get_cp()
        gp = self.get_gp()
        freqs = self.get_frequencies()
        Y = np.zeros((cp.shape), dtype=complex)
        for fi in range(len(freqs)):        # frequency index
            w = 2.0 * np.pi * freqs[fi]     # omega
            for vi in range(len(cp)):      # voltage index
                Y[vi, fi] = factor * np.complex(gp[vi, fi], w * cp[vi, fi])
        return Y

    def get_Yabs_Phi(self, factor=1.0):
        """
        This method returns ``None`` if not a .cv file. Otherwise:

        Returns the norm :math:`|Y|` and the phase :math:`\phi_Y` of the
        complex admittance :math:`Y = G_p + i \; \omega \cdot C_p` directly
        from the values provided by the Agilent LRC meter (assuming the
        default setting to :math:`C_p`-mode). Corresponding values
        :math:`|Z|, \phi_Z` for the impedance can easily be calcluated with
        :math:`|Z| = 1.0 / |Y|` and :math:`\phi_Z = \pi +  \phi_Y`.

        *factor* : float, optional
            multiplies the :math:`|Y|`-values  with *factor* when
            returning the array, has no effect on the :math:`\phi_Y`-values.

        *return* : Two 2-dimensional numpy arrays of real
            :math:`|Y|`-values and :math:`\phi_Y`-values, each having
            one line for each voltage, one column for each frequency.
            Note: After a previous call of set_voltage_index_range
            or set_voltage_range the return values are restricted
            to that range.
        """
        if (self._file_ext.lower() != '.cv'):
            return None
        cp = self.get_cp()
        gp = self.get_gp()
        freqs = self.get_frequencies()
        r = np.zeros((cp.shape))
        phi = np.zeros((cp.shape))
        for fi in range(len(freqs)):        # frequency index
            w = 2.0 * np.pi * freqs[fi]     # omega
            for vi in range(len(cp)):      # voltage index
                [r[vi, fi], phi[vi, fi]] = \
                cmath.polar(np.complex(gp[vi, fi], w * cp[vi, fi]))
        return factor * r, phi


    def get_cs(self, factor=1.0):
        """
        This method returns ``None`` if not a .cv file. Otherwise:

        Returns the :math:`C_s`-values (capacitance of an equivalent
        serial circuit, see picture above). These are calculated using
        the :math:`C_p` and :math:`G_p` data together with the
        frequencies :math:`f` from the meta-data line 'List of frequencies'
        with the following formula:

        .. math::
            \\omega=2 \pi f \; ; \quad
            C_s= \\frac{G_p^2 + (\\omega C_p)^2}{\\omega^2C_p}

        *factor* : float, optional
            multiplies the :math:`C_s`-values  with *factor* when
            returning the array. For instance a ``get_cs(1e12)`` will
            return capacitances in pF rather than F.

        *return* : 2-dimensional numpy array of float
            :math:`C_s`-values, one line for each voltage,
            one column for each frequency.
            Note: After a previous call of set_voltage_index_range
            or set_voltage_range the return values are restricted
            to that range.
        """
        if (self._file_ext.lower() != '.cv'):
            return None
        cp = self.get_cp()
        gp = self.get_gp()
        freqs = self.get_frequencies()
        cs = np.zeros(cp.shape)
        for fi in range(len(freqs)):     # frequency index
            w = 2.0 * np.pi * freqs[fi]  # omega
            cs[:, fi] \
                = (gp[:, fi]**2 \
                + (w * cp[:, fi])**2) \
                / (w**2 * cp[:, fi])
        return factor * cs

    def get_rs(self, factor=1.0):
        """
        This method returns ``None`` if not a .cv file. Otherwise:

        Returns the  :math:`R_s`-values (resistance of an equivalent
        serial circuit, see picture above). These are calculated using
        the :math:`C_p` and :math:`G_p` data together with the frequencies
        :math:`f` from the meta-data line 'List of frequencies'
        with the following formula:

        .. math::
            \\omega=2 \pi f \; ; \quad
            R_s = \\frac{1}{G_s} = \\frac{G_p}{G_p^2 + (\\omega C_p)^2}

        Returns an array of floats with a
        column for each frequency and a line for each voltage.

        *factor* : float, optional
            multiplies the :math:`R_s`-values  with *factor* when
            returning the array.

        *return* : 2-dimensional numpy array of float
            :math:`R_s`-values, one line for each voltage,
            one column for each frequency.
            Note: After a previous call of set_voltage_index_range
            or set_voltage_range the return values are restricted
            to that range.
        """
        if (self._file_ext.lower() != '.cv'):
            return None
        cp = self.get_cp()
        gp = self.get_gp()
        freqs = self.get_frequencies()
        rs = np.zeros(gp.shape)
        for fi in range(len(freqs)):     # frequency index
            w = 2.0 * np.pi * freqs[fi]  # omega
            rs[:, fi] = gp[:, fi] / (gp[:, fi]**2 + (w * cp[:, fi])**2)
        return factor * rs

    def get_i_pad(self, factor=1.0):
        """
        This method returns ``None`` if not a .iv file. Otherwise:

        Returns the pad current , optionally multiplied by *factor*,
        hence ``get_i_pad(1e9)`` will return the current in nA.


        *factor* : float, optional
            multiplies current-values  with *factor* when
            returning the array.

        *return* : list of float
            The third column of the data array (the pad current).
            Note: After a previous call of set_voltage_index_range
            or set_voltage_range the return values are restricted
            to that range.
        """
        if (self._file_ext.lower() != '.iv'):
            return None
        return factor * self._data[self._voltage_index_range[0] \
            : self._voltage_index_range[1] + 1, 2]

    def get_i_gr(self, factor=1.0):
        """
        This method returns ``None`` if not a .iv file. Otherwise:

        Returns the guard ring current , optionally multiplied by *factor*,
        hence ``get_i_gr(1e9)`` will return the current in nA.

        *factor* : float, optional
            multiplies current-values  with *factor* when
            returning the array.

        *return* : list of float
            The fourth column of the data array (the guard ring current).
            Note: After a previous call of set_voltage_index_range
            or set_voltage_range the return values are restricted
            to that range.
        """
        if (self._file_ext.lower() != '.iv'):
            return None
        return factor * self._data[self._voltage_index_range[0] \
            : self._voltage_index_range[1] + 1, 3]
