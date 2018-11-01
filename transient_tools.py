# -*- coding: utf-8 -*-
##############################################################################
# File:                transient_tools.py
# Created:             2018-08-30
# Last modification:   2018-09-24
# Author:              Stepan Martens <smartens@desy.de>
#                      Michael Hufschmidt <michael.hufschmidt@desy.de>
#                                         <michael@hufschmidt-web.de>
# Copyright:
# License (CC BY 4.0): https://creativecommons.org/licenses/by/4.0/deed.de
###############################################################################

u"""
Module: transient_tools
************************
The module transient_tools.py contains classes to read
and analyse data-files from scopes.
For usage, simply add the following code to your Python program::

    from transient_tools import *

The module defines the global constants:

* MYHOME (my home directory)
* M_DATA_DIR (= '~/m_data/' which shold be s symlink to a gvfs share)
* RD_DATA_DIR (= '/scratch_nmsamba/' which shold be s symlink to a gvfs share)
* DATE_REGEX (regular expression for dates in ISO format)

The module contains the classes:

* class ScopeData

"""

from pyhaha import *

MYHOME = os.getenv('HOME')
M_DATA_DIR  = MYHOME + '/m_data/'            # should be a symlink
RD_DATA_DIR = MYHOME + '/scratch_nmsamba/'   # should be a symlink
DATE_REGEX = '_[12][09][0-9][0-9]-[01][0-9]-[0-3][0-9]'

class ScopeData:
    """
    This class reads the header and data-files ``xxx.bin`` and
    ``xxx.Wfm.bin`` created by the setups with scopes.
    Suitable methods to obtain data are provided.

    To create an instance of ScopeData you can use as an exmaple::

        sd = ScopeData('03_20GSs_400ns_49807_raw', 'myDataDir')

    The parameter(s) provided to the constructor have the following meaning:

    *filename* : string
        Filename to read, e.g.
        ``'xxx_raw'``
        note that this parameter is only the basename, actually read will then
        be the files ``xxx_raw.bin`` and ``xxx_raw.Wfm.bin``
    *directory* : string, optional
        The directory which contains the data-file (if not it is not in the
        current directory).
        """

    def __init__(self, filename='', directory=''):
        self._basename = filename
        self._headerfilename = directory + '/' + filename + '.bin'
        self._datafilename = directory + '/' + filename + '.Wfm.bin'
        self._props = collections.OrderedDict()
        self._rawdata = None
        self._data = None
        self._datatype = None
        self._screen = None

        if not os.path.isfile(self._headerfilename):
            msg = '??? ScopeData ERROR: Class ScopeData ' +\
                  'could not be instanciated:\n' +\
                  'Header-File "{}" could not be opened'\
                  .format(self._headerfilename)
            print(msg)
#            sys.exit()
            return None
        if not os.path.isfile(self._datafilename):
            msg = '??? ScopeData ERROR: Class ScopeData ' +\
                  'could not be instanciated:\n' +\
                  'Data-File "{}" could not be opened'\
                  .format(self._datafilename)
            print(msg)
#            sys.exit()
            return None

        # Parse properties
        doc = et.parse(self._headerfilename)
        propsextract = doc.xpath('//Group/Prop')
        props = [i.attrib for i in propsextract]
        self._props['Resolution'] = float(self.getpropval(props,'Resolution'))
        rl = int(self.getpropval(props,'RecordLength'))
        self._props['RecordLength'] = rl
        self._props['XStart'] = float(self.getpropval(props,'XStart'))
        self._props['XStop'] = float(self.getpropval(props,'XStop'))
        self._props['HardwareXStart'] = float(self.getpropval(props,'HardwareXStart'))
        self._props['HardwareXStop'] = float(self.getpropval(props,'HardwareXStop'))
        shl = int(self.getpropval(props,'SignalHardwareRecordLength'))
        self._props['SignalHardwareRecordLength'] = shl
        lss = int(self.getpropval(props,'LeadingSettlingSamples'))
        self._props['LeadingSettlingSamples'] = lss
        vpos = float(self.getpropval(props,'VerticalPosition'))
        self._props['VerticalPosition'] = vpos
        vscal = float(self.getpropval(props,'VerticalScale'))
        self._props['VerticalScale'] = vscal
        voff = float(self.getpropval(props,'VerticalOffset'))
        self._props['VerticalOffset'] = voff
        noql = int(self.getpropval(props,'NofQuantisationLevels'))
        self._props['NofQuantisationLevels'] = noql
        vdc = int(self.getpropval(props,'VerticalDivisionCount'))
        self._props['VerticalDivisionCount'] = vdc
        tss = shl - rl - lss
        self._props['TrailingSettlingSaples'] = tss
        cof = vscal * vdc / noql
        self._props['ConversionFactor'] = cof
        coo = voff - vpos * vscal
        self._props['ConversionOffset'] = coo

        # Load data
        self._datatype = dtype=([('pre', np.int8, lss),
                     ('sig', np.int8, rl),
                     ('aff', np.int8, tss)])
        return None
        # End of the constructor

    def getpropval(self, proplist, propname):
        """
        Returns the property *propname* from a propertylist. Parameters:

        *proplist* list of element props
            Usually created with xml tools.

        *propname* string
            The property to search for.

        *return* : string
            Value of that prorperty. In case of numerical properties you
            need to typecast this value.
        """
        my_prop =  list(filter(lambda x: x['Name'] == propname, proplist))[0].get('Value')
        return my_prop

    def get_props(self):
        """
        Returns all properties as an odered dictrionary

        *return* : OrderedDict
            Important properties as evaluatec from the xml Header-File.
        """
        return self._props

    def get_basename(self):
        """
        *return* : string
            The basename used for calculating the headerfilename and
            datafilename.
        """
        return self._basename

    def print_filenames(self):
        """
        Prints the filenames

        *return* : None
        """
        print('Base-Name   = {}'.format(self._basename))
        print('Header-File = {}'.format(self._headerfilename))
        print('Data-File   = {}'.format(self._datafilename))
        return None


    def print_props(self):
        """
        Prints all properties and values as an odered dictrionary

        *return* : None
        """
        for key in self._props:
           print('{:<27} = {}'.format(key, self._props[key]))
        return None

    def get_rawdata(self):
        """
        Parse the data-file and return raw data. The data-file will only be
        parsed once, if self._rawdata already contains data, these will be
        returned.

        *return* : array of numpy-arrays
            raw data for advanced calucations
        """
        if self._rawdata is None:
            self._rawdata = np.fromfile(\
                self._datafilename, count=-1, dtype=self._datatype)
        return self._rawdata

    def get_data(self):
        """
        Parse the data-file and return data. The data-file will only be
        parsed once, if self._data already contains data, these will be
        returned.

        *return* : array of numpy-arrays
            data ready for creating plots
        """
        if self._rawdata is None:
            self.get_rawdata()
        if self._data is None:
            props = self.get_props()
            self._data = self._rawdata['sig'] * \
                props['ConversionFactor']  + props['ConversionOffset']
        return self._data

