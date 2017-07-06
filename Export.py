#!/usr/bin/env python
# encoding: utf-8
import sys, io, os, re, shutil
import sqlite3

ROOT = '/home/idler/Desktop/OUT'
NOTES = './notes/'
ATTACHMENTS = './attachments/'

def makePath(path):
    flag = os.path.exists(path)
    if not flag: 
        os.makedirs(path)
    return flag 

def readFromDB(dbname, sql):
    mydb = sqlite3.connect(dbname)
    cursor = mydb.cursor()
    cursor.execute(sql)
    table = cursor.fetchall()
    return table

def copyNotes(table):
    for row in table:
        hash, title, location, filename = row
        makePath(ROOT + location)
        spath = NOTES + '{' + hash + '}'
        dpath = ROOT + location + filename + '.zip'
        shutil.copyfile(spath, dpath)
        print(hash, location)

def copyAttachments(table):
    for row in table:
        hash, location, notename, filename = row
        makePath(ROOT + location + notename)
        spath = ATTACHMENTS + '{' + hash + '}' + filename
        dpath = ROOT + location + notename + '/' + filename
        try:
            shutil.copyfile(spath, dpath)
        except:
            print('[ERROR]\t' + spath)
        print(dpath)

def main():
    sql_note = "select DOCUMENT_GUID, DOCUMENT_TITLE, DOCUMENT_LOCATION, DOCUMENT_NAME from WIZ_DOCUMENT"
    sql_attach = "select ATTACHMENT_GUID, DOCUMENT_LOCATION, DOCUMENT_NAME, ATTACHMENT_NAME from WIZ_DOCUMENT, WIZ_DOCUMENT_ATTACHMENT where  WIZ_DOCUMENT.DOCUMENT_GUID = WIZ_DOCUMENT_ATTACHMENT.DOCUMENT_GUID"
    notes = readFromDB("index.db", sql_note)
    copyNotes(notes)
    atttachments = readFromDB("index.db", sql_attach)
    copyAttachments(atttachments)  

if __name__ == "__main__":
    main()