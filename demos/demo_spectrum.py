#!/usr/bin/env python3
# -*- coding: utf-8 -*-
##############################################################################
# File:                demo_spectrum.py
# Created:             2018-09-13
# Last modification:   2018-09-13
# Author:              Stepan Martens <smartens@desy.de>
#                      Michael Hufschmidt <michael.hufschmidt@desy.de>
# Copyright:
# License (CC BY 4.0): https://creativecommons.org/licenses/by/4.0/deed.de
###############################################################################


from pyhaha import *                   # Environment variable $PYTHONPATH
                                       # points to relevant folder
import time

start_time = time.clock()

data_dir = './data_dir'
filename = '03_20GSs_400ns_49807_raw'  # the Base-Name

sd = ScopeData(filename, data_dir)     # create a ScopeData object
sd.print_filenames()                   # call a ScopeData method
sd.print_props()                       # call a ScopeData method

p = SpectrumPlot(sd)                   # create a standard plot object
p.make_plot()                          # create a plots with default params
#p.make_plot(2200, 3500)               # create all plots with index range
p.save_plot('plot_spectrum')           # save plot
plt.show()                             # show plot

print("\n%.2f ms" % ((time.clock() - start_time)*1e3))
