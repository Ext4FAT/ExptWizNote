#!/usr/bin/env python
# encoding: utf-8
import sys, io, os, re, zipfile

FLAGS = ['.zip']

INGORE = []

def Unzip(path):
    abs_path = os.path.abspath(path)
    base_path = abs_path[:-len('.zip')]

    if os.path.isdir(base_path):
        pass
    else:
        os.mkdir(base_path)

    zip_file = zipfile.ZipFile(abs_path)

    for names in zip_file.namelist():
        zip_file.extract(names, base_path)

    zip_file.close()



def Traversal(path):
    for item  in os.listdir(path):
        ipath = path +'/'+ item
        if os.path.isdir(ipath) and item[0] != '.':
            if item not in INGORE:
                Traversal(ipath)
        for flag in FLAGS:
            if item[-len(flag):] == flag:
                Unzip(ipath)
                Traversal(ipath[:-len('.zip')])

def main():
    paths = ['.']
    if len(sys.argv) > 1:
        paths = sys.argv[1:]
    for p in paths:
        Traversal(p)


if __name__ == "__main__":
    main()
