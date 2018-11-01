#!/usr/bin/env python3
# -*- coding: utf-8 -*-
##############################################################################
# File:                demo_cv.py
# Created:             2016-10-17
# Last modification:   2018-09-13
# Author:              Michael Hufschmidt <michael.hufschmidt@desy.de>
#                                         <michael@hufschmidt-web.de>
# Copyright:           (C) Michael Hufschmidt 2016
# License (CC BY 4.0): https://creativecommons.org/licenses/by/4.0/deed.de
###############################################################################

from pyhaha import *                   # Environment variable $PYTHONPATH
                                       # points to relevant folder
my_dir = './data_dir'                  # here are all my .iv and .cv files
datafile = 'FTH200N_04_DiodeS_14_2015-11-05_4.cv'
ccd = ColdChuckData(datafile, my_dir)  # create a data file object
print(ccd.get_filepath())              # where the file finally was found
p = CVPlot(ccd)                        # create plot object
p.make_plot()                          # create the plot
p.save_plot()                          # save plot as .pdf
plt.show()                             # show plot
