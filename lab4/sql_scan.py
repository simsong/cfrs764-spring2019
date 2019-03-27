#!/usr/bin/python
#
# scan for sqlite3 databases using python2

import os
import sqlite3
import os.path
import sys

MIN_SIZE = 4096
MAGIC = b"SQLite format 3"
NOTIFY_INTERVAL=1000

import tydoc

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


def process(root):
    scanned_dirs = 0
    scanned_files = 0
    for dirpath, dirnames, filenames in os.walk(root):
        scanned_dirs += 1
        for filename in filenames:
            scanned_files += 1
            if scanned_files % NOTIFY_INTERVAL==0:
                print("Scanned dirs: {}  files: {}".format(scanned_dirs,scanned_files))
            filepath = os.path.join(dirpath, filename)
            try:
                if os.path.getsize(filepath) < MIN_SIZE:
                    continue
                if open(filepath,"rb").read(len(MAGIC)) != MAGIC:
                    continue
                print("a")
                conn = sqlite3.connect(filepath)
                print(conn)
            except sqlite3.OperationalError as r:
                continue
            except PermissionError as e:
                print(str(e))
                if os.getuid()!=0:
                    raise RuntimeError("Re-run as root")
            except FileNotFoundError as e:
                continue
            print("DATABASE FILE: {}".format(filepath))
            tables = conn.cursor().execute("select name from sqlite_master").fetchall()
            # Now print each table and a few rows
            for (name,) in tables:
                doc = tydoc.tytable()
                c = conn.cursor()
                try:
                    c.execute("SELECT COUNT(*) from {}".format(name))
                    rows = c.fetchone()[0]
                    print("Table: {}  Rows: {}".format(name,rows))
                    print("")
                    c.execute("SELECT * from {} LIMIT 5".format(name))
                    doc.add_head([info[0] for info in c.description])
                    for row in c.fetchall():
                        doc.add_data([str(s)[0:20] for s in row])
                    doc.save(sys.stdout, format='md')
                    print("")
                    print("=====================================")
                except sqlite3.OperationalError as e:
                    continue
            

if __name__=="__main__":
    import argparse
    parser = argparse.ArgumentParser(description='General customer report',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("root",help="Where to start")
    args = parser.parse_args()
    process(args.root)
