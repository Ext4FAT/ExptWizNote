#!/usr/bin/env python
# encoding: utf-8
import sys, io, os, re
import shutil

FLAGS = ['.html']
INGORE = []

def html2pdf(hpath, ppath):
    myargs = ['wkhtmltopdf', '"'+ hpath + '"', '"'+ ppath + '"']
    print(' '.join(myargs))
    os.system(' '.join(myargs))

def traversal(path):
    for item  in os.listdir(path):
        ipath = path +'/'+ item
        if os.path.isdir(ipath) and item[0] != '.':
            if item not in INGORE:
                traversal(ipath)
        if item == 'index.html':
            html2pdf(ipath, path+".pdf")
            shutil.rmtree(path)
def main():
    traversal('/home/idler/.wiznote/zyy34472@gmail.com/data/WizNotes')

if __name__ == "__main__":
    main()