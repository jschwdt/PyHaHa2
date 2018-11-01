#!/usr/bin/env python3
# -*- coding: utf-8 -*-
##############################################################################
# File:                demo_multi_cv.py
# Created:             2016-10-31
# Last modification:   2018-09-13
# Author:              Michael Hufschmidt <michael.hufschmidt@desy.de>
#                                         <michael@hufschmidt-web.de>
# Copyright:           (C) Michael Hufschmidt 2016
# License (CC BY 4.0): https://creativecommons.org/licenses/by/4.0/deed.de
###############################################################################

from pyhaha import *                   # Environment variable $PYTHONPATH
                                       # points to relevant folder
my_dir = './data_dir'                  # here are all my .iv and .cv files
my_files  = ['MCZ200Y_05_DiodeL_9_2012-08-08_4.cv',
             'MCZ200Y_06_DiodeL_11_2012-08-09_4.cv',
             'MCZ200Y_07_DiodeL_8_2012-08-13_4.cv']
my_labels = [r'$3\cdot 10^{13}$ neq cm${}^{-2}$',
             r'$5\cdot 10^{13}$ neq cm${}^{-2}$',
             r'$1\cdot 10^{14}$ neq cm${}^{-2}$']
ccds = []                              # list of data file objects
for my_file in my_files:
    ccd = ColdChuckData(my_file, directory=my_dir) # create an object for each
    ccds.append(ccd)                   # and collect in a list
    print(ccd.get_filepath())          # where the file finally was found
p = CVPlot(ccds)                       # create plot object
p.update_plotparams({'legend.fontsize': 'medium'})
p.make_plot(my_labels)                 # create the plot
p.save_plot()                          # save plot as .pdf
plt.show()                             # show plot
