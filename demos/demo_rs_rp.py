#!/usr/bin/env python3
# -*- coding: utf-8 -*-
##############################################################################
# File:                demo_rs_rp.py
# Created:             2016-10-24
# Last modification:   2018-09-13
# Author:              Michael Hufschmidt <michael.hufschmidt@desy.de>
#                                         <michael@hufschmidt-web.de>
# Copyright:           (C) Michael Hufschmidt 2016
# License (CC BY 4.0): https://creativecommons.org/licenses/by/4.0/deed.de
###############################################################################

from pyhaha import *                   # Environment variable $PYTHONPATH
                                       # points to relevant folder
my_dir = './data_dir'                  # here are all my .iv and .cv files
datafile = 'w1-pm1125-2_2013-07-24_4.cv'
ccd = ColdChuckData(datafile, my_dir)  # create a data file object
print(ccd.get_filepath())              # where the file finally was found
rs = ccd.get_rs()                      # serial resistance
rp = 1.0 / ccd.get_gp()                # parallel resistance from admittance
freqs = ccd.get_frequencies()          # all frequencies
voltages = [4, 8, 12, 14, 16, 20, 24, 26] # plot only these voltages
p = CVPlot(ccd)                        # create plot object
volt_indices = ccd.v_index(voltages)
fig = plt.figure(figsize=[11.0, 12.0])
fig.text(0.5, 0.98, p.make_title(), ha='center', va='top')
# First Subplot
plt.subplot(2, 1, 1)
plt.title('Serial Resistance versus Frequency')
for vi in volt_indices:
    v_label = "{} V".format(ccd.get_volts()[vi])
    plt.plot(freqs, rs[vi, :], label=v_label)
plt.ylabel(r'Resistance $R_s$ [$\Omega$]')
plt.loglog()
plt.legend(loc='best')
# Second Subplot
plt.subplot(2, 1, 2)
plt.title('Parallel Resistance versus Frequency')
for vi in volt_indices:
    v_label = "{} V".format(ccd.get_volts()[vi])
    plt.plot(freqs, rp[vi, :], label=v_label)
plt.xlabel('Frequency [Hz]')
plt.ylabel(r'Resistance $R_p$ [$\Omega$]')
plt.loglog()
plt.legend(loc='best')
# Show and save all
p.save_plot()                          # save plot as .pdf
plt.show()                             # show plot
