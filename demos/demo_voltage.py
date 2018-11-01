#!/usr/bin/env python3
# -*- coding: utf-8 -*-
##############################################################################
# File:                demo_voltage.py
# Created:             2018-08-23
# Last modification:   2018-09-13
# Author:
###############################################################################

from pyhaha import *                   # Environment variable $PYTHONPATH
                                       # points to relevant folder
my_dir = './data_dir'                  # here are all my .iv and .cv files
datafile = 'Ketek-2018_01_PM3315-WB-C0_3_2018-08-23_1.iv'
ccd = ColdChuckData(datafile, my_dir)  # create a data file object
print(ccd.get_filepath())              # where the file finally was found
p = VoltagePlot(ccd)                   # create plot object
p.make_plot()                          # create the plot
p.save_plot()                          # save plot as .pdf
plt.show()                             # show plot
