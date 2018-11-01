# -*- coding: utf-8 -*-
##############################################################################
# File:                file_utils.py
# Created:             2018-08-27
# Last modification:   2018-10-01
# Author:              Michael Hufschmidt <michael.hufschmidt@desy.de>
#                                         <michael@hufschmidt-web.de>
# Copyright:           (C) Michael Hufschmidt 2018
# License (CC BY 4.0): https://creativecommons.org/licenses/by/4.0/deed.de
###############################################################################

u"""
Module: file_utils
*******************
The module file_utils.py contains some general utility funktions.
For usage, simply add the following code to your Python program::

    from file_utils import *

The module contains the utility functions:

* function mount_gvfs
* function date_stamp
* function datetime_stamp
* function strings_to_ints
* function log_to_file
* function logfile
* function collect_files
* function winpath_to_linux

The module defines the global constants:

* MYHOME (my home directory)
* M_DATA_DIR (= '~/m_data/' which shold be s symlink to a gvfs share)
* RD_DATA_DIR (= '/scratch_nmsamba/' which shold be s symlink to a gvfs share)
* DATE_REGEX (regular expression for dates in ISO format)


"""
from pyhaha import *

MYHOME = os.getenv('HOME')
M_DATA_DIR  = MYHOME + '/m_data/'            # should be a symlink
RD_DATA_DIR = MYHOME + '/scratch_nmsamba/'   # should be a symlink

def mount_gvfs():
    """
    This utility function calls the shell-script ``~/bin/automount`` which
    mounts shares on ``uh2usnmserver``. No error will be sent if the script
    does not exist or the shares are already mounted. The content of this
    script could be for instance::

        #!/bin/bash
        # Script  ~/bin/automount
        gvfs-mount smb://uh2usnmserver/m_data/
        gvfs-mount smb://uh2usnmserver/scratch_nmsamba/

    """
    try:
        os.system('~/bin/automount 2> /dev/null')
    except:
        pass
    return

def date_stamp():
    """
    Returns the current date, e.g. '2017-11-30'

    *return* : string
        date in ISO-Format
    """
    return str(datetime.datetime.now())[:10]

def datetime_stamp():
    """
    Returns the current date, e.g. '2017-11-30 09:18:22'

    *return* : string
        date and time in ISO-Format
    """
    return str(datetime.datetime.now())[:19]

def strings_to_ints(in_string):
    """
    This funcion converts a string with comma separated ints
    into a list of integers. Parameters:

    *in_string* : string
        input string

    *return* : list of integers
        converted string
    """
    ints = []
    for ss in in_string.split(','):
        if (len(ss) > 0):
            i = int(ss.strip())
            ints.append(i)
    return ints

def log_to_file(msg, logfile=None):
    """
    This utility prints a message or sends it logfile which has to be
    opened before. Parameters:

    *msg* : string
        The error message to appear in the the logfile or on stdout.

    *logfile* : instance of an open text-file or None
        If logfile points to an open writeable text- file, error messages will
        be sent to that file, otherwise they will be printed to stdout.
    """
    if isinstance(logfile, io.TextIOWrapper) and logfile.mode == 'w' :
        logfile.write(msg + '\n')
    else:
        print(msg)
    return None

def logfile(file_name, title, lines, separator='\t'):
    """
    This function creates a file for logging csv data. Parameters:

    *file_name* : string
        Relative path of the output file

    *title* : string or list of strings
        The first line within the file

    *lines* : list of strings or list of list of strings
        The content, each string will be a separate line. If the line is
        a list of strings, each inner string will be printed as an item
        separated by *separator* (default '\t').
    """
    fo = open(file_name, 'w')
    if isinstance(title, list):
        zeile = ''
        for tit in title:
            zeile += tit + separator
        fo.write(zeile.rstrip(separator) + "\r\n")
    else:
        fo.write(title + '\r\n')
    for line in lines:
        if isinstance(line, list):
            zeile = ''
            for elem in line:
                zeile += str(elem) + separator
            fo.write(zeile.rstrip(separator) + "\r\n")
        else:
            fo.write(str(line) + "\r\n")
    pass
    fo.close()
    return None

def collect_files(base_dir, min_date='1990-01-01', valid_ext=None):
    """
    This funcion iterates recursively through all directories below *base_dir*
    and collects the filenames. Only files with
    a modification date later than *min_date* are collected. If the *fullname*
    contains 'macroscopic/', name-part before 'macroscopic/' will be removed.

    **Caveat!** A call ``collect_files(M_DATA_DIR + 'macroscopic/')`` will run
    for 9 minutes an return a list of  163 463 files
    (total size = 224 663 331 076 Bytes ~ 209 GByte).

    Parameters:

    *base_dir* : string
        Files below *base_dir* are scanned. Caution:
        If *base_dir* = M_DATA_DIR + 'macroscopic/'
        the reslut will be a list of ~80.000 items.

    *min_date* : string
        Files with a modification date < *min_date* will be ignored. Date
        format has to be YYYY-MM-DD.

    *valid_ext* : list of strings or None
        If *valid_ext* is not None, only files with an extesnion endinng
        with one of the entries in *valid_ext* will be processed. A call could
        for instance be ``(..., valid_ext=['.cv', '.iv'])``.

    *return* : list of *items*
        An *item* is a list of file properties: modification date [string],
        file-size [int], file-extension [string], filename [string] and
        fullname (= name including path below *base_dir*) [string]
    """
    count = 0
    items = []
    for root, dirs, files in os.walk(base_dir):
        for name in files:
            item = []
            ext_ok = False
            try:
                ext = name[str.rindex(name, '.'):]
            except:
                ext = ''
            if (valid_ext is None):
                ext_ok = True
            else:
                if (ext in valid_ext):
                    ext_ok = True
                else:
                    ext_ok = False
            fullname = os.path.join(root, name)
            statinfo = os.stat(fullname)
            size = int(statinfo.st_size)
            # this will result in time = 00:00:00
#            mod_date = datetime.date.fromtimestamp(statinfo.st_mtime)\
#                .strftime('%Y-%m-%d %H:%M:%S')
            mod_date = datetime.date.fromtimestamp(statinfo.st_mtime).isoformat()
            posm = fullname.find('macroscopic/')
            if (posm > 0):
                fullname = fullname[posm :]
            if (mod_date >= min_date and ext_ok):
                count += 1
                item = [mod_date, size, ext, name, fullname]
                items.append(item)
    return items

def winpath_to_linux(winpath):
    """
    This is a utility function to convert a Windows file path as stored in the
    column 'File', table 'Measurement' of the old database 'radhard' to a
    Linux path. For example
    ``winpath_to_linux('j:\macroscopic\w6\w6-pncv-2\w6-pncv-2_2013-07-26_2.cv')``
    will return
    ``M_DATA_DIR/macroscopic/w6/w6-pncv-2/w6-pncv-2_2013-07-26_2.cv'``.
    ``winpath_to_linux`` will try several linux directories for locating the file.

    Parameter:

    *winpath* : string
        Filename in Windows format

    *return* : string
        Full path in Linux format where the file can be found. The function
        will return ``None`` if the file cannot automatically be found.
    """
    linuxpath = None
    def try_fullpath(folder0, folder1, path_right):
        linuxpath = ''
        if (folder0 == 'rd_data/'):
            linuxpath = RD_DATA_DIR + folder0 + folder1 + path_right
        if (folder0 == 'macroscopic/'):
            linuxpath = M_DATA_DIR  + folder0 + folder1 + path_right
#        print('linuxpath = ', linuxpath)
        if (os.path.isfile(linuxpath)):
            return linuxpath
        else:
            return ''

    if (len(winpath) < 3):
        return None

    if (':' in winpath[0:2]):
        path = winpath.replace('\\', '/')[winpath.find(':')+2 :]
    else:
        path = winpath.replace('\\', '/')
    if ('\n' in path):
        pathlines = path.split('\n')
        try:
            path = pathlines[0] + '/' + ''.join(pathlines[2:])
        except:
            path = path.replace('\n', '/')
    folders = path.split('/')
    folder0 = (folders[0] + '/').strip()
#    print('folder0 = ' + folder0)
    path_right = ''
    if (len(folders) > 2):
        folder1 = (folders[1] + '/').strip()
        for folder in folders[2:]:
            path_right += folder + '/'
#        print('folder1 = ' + folder1)
    else:
        for folder in folders[1:]:
            path_right += folder + '/'
        folder1 = ''
    path_right = path_right.rstrip('/')
    linuxpath = try_fullpath(folder0, folder1, path_right)
    if (len(linuxpath) > 1):
        return linuxpath
    linuxpath = try_fullpath(folder0, folder1.upper(), path_right)
    if (len(linuxpath) > 1):
        return linuxpath
    linuxpath = try_fullpath(folder0, '', path_right)
    if (len(linuxpath) > 1):
        return linuxpath
    if (len(folder1) > 1):
        linuxpath = try_fullpath(folder0, folder1[0].upper() + folder1[1:], path_right)
        if (len(linuxpath) > 1):
            return linuxpath
    pass
    return None
