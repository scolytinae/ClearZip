# -*- coding: utf-8 -*-
#!/usr/bin/python

import time
import shutil
import os
import re
import argparse
import subprocess

TRASH_FILTERS = []

ARCHIVE_TYPE = 'zip'

ARCHIVE_FOLDER = '.'

PATH_7ZIP = 'C:/Program Files/7-zip/7z.exe'


def is_filtered(item, regex_list):
    """Check file name with regex"""
    try:
        for f in regex_list:
            if re.match(f, item):
                return True
        return False
    except Exception as e:
        print e.message


def files_tree_list(root_dir):
    """Create full list with file and dir names"""
    res = []

    try:
        for root, folders, files in os.walk(root_dir):
            root = root.replace('\\', '/')
            res.append(root)
            res.extend(map(lambda fname: '/'.join([root, fname]), files))
    except Exception as e:
        print e.message

    return res


def filter_to_regex(afilter):
    """Convert user filter to regex"""
    return afilter.replace('.', '\.').replace('*', '.*')


def clear_folder(folder, regex_filters):
    """Clear dir. Check files with filter and remove them"""

    def delete_item(fname):
        try:
            print 'Remove %s' % fname
            if os.path.isfile(fname):
                os.remove(fname)
            elif os.path.isdir(fname):
                shutil.rmtree(fname)
        except Exception as e:
            print e.message

    flist = files_tree_list(folder)
    for fname in flist:
        if not os.path.exists(fname):
            continue

        elif is_filtered(fname, regex_filters):
            delete_item(fname)


def make_archive(arch_name, source, atype='zip'):
    """Create folder archive"""
    spl = os.path.split(source)
    if atype == '7z':
        subprocess.call([PATH_7ZIP, 'a', arch_name, source])
    else:
        shutil.make_archive(arch_name, atype, spl[0], spl[1])


def make_archive_name(base_name):
    """Create archive name"""
    short_name = os.path.join(ARCHIVE_FOLDER, os.path.basename(base_name))
    return '%s_%s' % (short_name, time.strftime('%Y_%m_%d_%H_%M_%S'))


def load_trash_filters(fname):
    """Load filters from file"""
    try:
        with open(fname, 'r') as f:
            lines = [line.rstrip() for line in f.readlines()]
        return filter(lambda line: line and line.strip()[:1] != '#', lines)
    except Exception as e:
        print "Can't load trash filter from %s" % fname
        print e.message


def set_archive_type(atype):
    """Set archive type"""
    if atype in ['zip', 'tar', 'bztar', 'gztar', '7z']:
        global ARCHIVE_TYPE
        ARCHIVE_TYPE = atype
    else:
        raise Exception('Wrong archive type %s' % atype)


def set_archive_path(path):
    """Set folder to store archive"""
    norm = os.path.normpath(path)
    if (os.path.exists(norm)):
        global ARCHIVE_FOLDER
        ARCHIVE_FOLDER = norm
    else:
        raise Exception('Archive folder not exists %s' % norm)


def _init(args):
    if args.trash:
        global TRASH_FILTERS
        TRASH_FILTERS = load_trash_filters(args.trash)
    if args.mode:
        set_archive_type(args.mode)
    if args.dest:
        set_archive_path(args.dest)


def _get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('source', help='path to source folder')
    parser.add_argument('-d', '--dest', help='path to folder with archives', type=str)
    parser.add_argument('-t', '--trash', help='list with patterns to remove', type=str)
    parser.add_argument('-m', '--mode', help='archive mode (zip, tar, bztar, gztar, 7z)', type=str)

    return parser.parse_args()

if __name__ == "__main__":
    args = _get_arguments()
    _init(args)

    print "Prepare file list at %s" % time.strftime('%H:%M:%S')
    regex_filters = map(filter_to_regex, TRASH_FILTERS)
    print "Start clear folder at %s" % time.strftime('%H:%M:%S')
    clear_folder(args.source, regex_filters)
    print "Start archiving at %s" % time.strftime('%H:%M:%S')
    try:
        make_archive(make_archive_name(args.source), args.source, ARCHIVE_TYPE)
        print "Archive done at %s" % time.strftime('%H:%M:%S')
    except Exception as e:
        print e.message