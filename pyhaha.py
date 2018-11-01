# -*- coding: utf-8 -*-
##############################################################################
# File:                pyhaha.py
# Created:             2018-08-27
# Last modification:   2018-10-01
# Author:              Michael Hufschmidt <michael.hufschmidt@desy.de>
#                                         <michael@hufschmidt-web.de>
# Copyright:           (C) Michael Hufschmidt 2018
# License (CC BY 4.0): https://creativecommons.org/licenses/by/4.0/deed.de
###############################################################################

u"""
Module: pyhaha
**************
pyhaha.py is the base module. Here all other modules and imports are loaded,
and some general constants are defined.
For usage, simply add the following code to your Python program::

    from pyhaha import *

The following modules are required and will always be loaded:

* os
* sys
* re (for regular expressions)
* csv (for CSV files)
* numpy as np (for multidimensional arrays, linear algebra, ...)
* cmath
* collections (for OrderedDict)
* lxml.etree as et (for XML parsers)
* matplotlib.pyplot as plt
* matplotlib.colors as colors
* string
* io
* datetime
* time

The following project modules are imported:

* cold_chuck_tools.py
* transient_tools.py
* pyhaha_plots
* cold_chuck_plots.py
* transient_plots.py
* file_utils.py
"""
import os
import sys
import re               # for regular expressions
import csv              # for CSV files
import numpy as np      # NumPy (multidimensional arrays, linear algebra, ...)
import cmath            # complex math
import collections
import lxml.etree as et  # for XML parsing
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import string
import io
import datetime
import time

from cold_chuck_tools import *
from transient_tools import *
from pyhaha_plots import *
from cold_chuck_plots import *
from transient_plots import *
from file_utils import *
