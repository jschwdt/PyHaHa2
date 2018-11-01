#!/usr/bin/env python3
# -*- coding: utf-8 -*-
##############################################################################
# File:                demo_iv.py
# Created:             2016-10-13
# Last modification:   2018-09-13
# Author:              Michael Hufschmidt <michael.hufschmidt@desy.de>
#                                         <michael@hufschmidt-web.de>
# Copyright:           (C) Michael Hufschmidt 2016
# License (CC BY 4.0): https://creativecommons.org/licenses/by/4.0/deed.de
###############################################################################

from pyhaha import *                   # Environment variable $PYTHONPATH
                                       # points to relevant folder
my_dir = './data_dir'                  # here are all my .iv and .cv files
datafile = 'FTH200N_04_DiodeS_14_2015-11-06_7.iv'
ccd = ColdChuckData(datafile, my_dir)  # create a data file object
print(ccd.get_filepath())              # where the file finally was found
p = IVPlot(ccd)                        # create plot object
p.make_plot()                          # create the plot
# plt.semilogy()                       # optional
p.save_plot()                          # save plot as .pdf
plt.show()                             # show plot
