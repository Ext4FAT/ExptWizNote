#!/usr/bin/env python
# encoding: utf-8
import codecs
import os
import re
import shutil
import sqlite3
import zipfile

from bs4 import BeautifulSoup

ROOT = './WizNotes'
NOTES = './notes/'
ATTACHMENTS = './attachments/'

PYINTERPRETER = "/usr/bin/python3"
HTML2TEXT = "./lib/html2text.py"

MAX_FILENAME_LEN = 65


def is_email(str):
    emailRegex = r'^[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+){0,4}@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+){0,4}$'
    flag = re.match(emailRegex, str)
    return flag


def find_account():
    # add home
    os.environ['HOME']
    os.path.expandvars('$HOME')
    homedir = os.path.expanduser('~')
    dirs = os.listdir(homedir + '/.wiznote')
    acc = [d for d in dirs if is_email(d)]
    return acc


def data_location(acc):
    return os.path.expanduser('~') + '/.wiznote/' + acc + '/data/'


def unzip(src, dst):
    zip_file = zipfile.ZipFile(src)
    for names in zip_file.namelist():
        zip_file.extract(names, dst)
    zip_file.close()


def rm_ext_name(filename):
    print(os.path.splitext(filename))
    (shortname, extension) = os.path.splitext(filename)
    return shortname


def make_path(path):
    flag = os.path.exists(path)
    if not flag:
        os.makedirs(path)
    return flag


def read_from_db(dbname, sql):
    mydb = sqlite3.connect(dbname)
    cursor = mydb.cursor()
    cursor.execute(sql)
    table = cursor.fetchall()
    return table


def add_init_url(htmlname):
    print(htmlname)
    html = codecs.open(htmlname, 'rb', 'utf-8')
    soup = BeautifulSoup(html, "lxml")
    body = soup.body
    a_tag = body.new_tag("a", href="www.example.com")
    body.insert(0, a_tag)
    newhtml = codecs.open('new-' + htmlname, 'wb', 'utf-8')
    newhtml.write(str(soup))
    newhtml.close()
    html.close()


def wrapMarkdown(filepath, mdpath):
    pargs = [PYINTERPRETER, HTML2TEXT, '"' + filepath + '"', '1>' + '"' + mdpath + '"']
    os.system(' '.join(pargs))


def check_note_title(note_title):
    if len(note_title) > MAX_FILENAME_LEN:
        return note_title[:MAX_FILENAME_LEN]
    return note_title


def copy_notes(table):
    for row in table:
        hash, notetitle, location, url = row
        notetitle = check_note_title(notetitle)
        spath = NOTES + '{' + hash + '}'
        dpath = ROOT + location + notetitle
        '''
        if notetitle.endswith('.md'):
            dpath = dpath + '.md'
        '''
        make_path(dpath)
        if url:
            print(url)
            # addInitURL(dpath + '/index.html')
        try:
            unzip(spath, dpath)
            print('[UNZIP]\t' + spath + '->' + dpath)
            '''
            if notetitle.endswith('.md'):
                wrapMarkdown(dpath + '/index.html', ROOT + location + notetitle)
                shutil.rmtree(dpath)
            '''
        except Exception as e:
            print(e)


def copy_attachments(table):
    for row in table:
        hash, location, note_title, attname = row
        note_title = check_note_title(note_title)
        make_path(ROOT + location + note_title)
        spath = ATTACHMENTS + '{' + hash + '}' + attname
        dpath = ROOT + location + note_title + '/' + attname
        try:
            shutil.copyfile(spath, dpath)
            print('[INFO]\t' + spath)
        except Exception as e:
            print(e)
            # print('[ERROR]\t' + spath)


def export_notes(dataLoc):
    # change dir
    os.chdir(dataLoc)
    # exec sql
    sql_note = "select DOCUMENT_GUID, DOCUMENT_TITLE, DOCUMENT_LOCATION, DOCUMENT_URL from WIZ_DOCUMENT"
    sql_attach = "select ATTACHMENT_GUID, DOCUMENT_LOCATION, DOCUMENT_TITLE, ATTACHMENT_NAME from WIZ_DOCUMENT, WIZ_DOCUMENT_ATTACHMENT where  WIZ_DOCUMENT.DOCUMENT_GUID = WIZ_DOCUMENT_ATTACHMENT.DOCUMENT_GUID"
    notes = read_from_db("index.db", sql_note)
    attachments = read_from_db("index.db", sql_attach)
    # proc
    copy_notes(notes)
    copy_attachments(attachments)


def main():
    accounts = find_account()
    for acc in accounts:
        data_loc = data_location(acc)
        export_notes(data_loc)


if __name__ == "__main__":
    main()
