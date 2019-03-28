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

class QuickTable:
    def __init__(self):
        self.data = []

    def col(self,n):
        """Return column n as a list"""
        return [(row[n] if n<=len(row) else None) for row in self.data]

    def cols(self):
        """Return the maximum number of columns in the table."""
        return max(len(row) for row in self.data)

    def col_maxwidth(self,n):
        """Return the maximum with of column n"""
        return max( [len(e) for e in self.col(n)] )

    def add_head(self,row):
        self.data.append(row)

    def add_data(self,row):
        self.data.append(row)

    def save(self,f, format='md'):
        """Get the maximum width of each column and then typset each. Assumes one header."""
        cols = self.cols()      # it's expensive to calculate, so cache it here
        widths = [self.col_maxwidth(n) for n in range(cols)]
        fmt = "|" + "|".join([('{:' + repr(width) + '}') for width in widths]) + "|"
        for (ctr,row) in enumerate(self.data):
            # Pad this row out if it needs padding
            if len(row) < cols:
                row = row + [''] * (cols-len(row))
            f.write(fmt.format(*row))
            f.write("\n")
            # Add the lines
            if ctr==0:
                lines = ['-' * self.col_maxwidth(n) for n in range(cols)]
                f.write(fmt.format(*lines))
                f.write("\n")
            
        

def process(root,nrows=5):
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
                conn = sqlite3.connect(filepath)
            except sqlite3.OperationalError as r:
                continue
            except Exception as e:
                print(str(e))
                continue
            print("DATABASE FILE: {}".format(filepath))
            try:
                tables = conn.cursor().execute("select name from sqlite_master").fetchall()
            except sqlite3.OperationalError as e:
                print("Could not access.")
                continue
            # Now print each table and a few rows
            for (name,) in tables:
                doc = QuickTable()
                c = conn.cursor()
                try:
                    c.execute("SELECT COUNT(*) from {}".format(name))
                    rows = c.fetchone()[0]
                    print("Table: {}  Rows: {}".format(name,rows))
                    print("")
                    c.execute("SELECT * from {} LIMIT {}".format(name,nrows))
                    doc.add_head([info[0] for info in c.description])
                    for row in c.fetchall():
                        doc.add_data([repr(s)[0:20] for s in row])
                    doc.save(sys.stdout, format='md')
                    print("")
                    print("=====================================")
                except sqlite3.OperationalError as e:
                    continue
            

if __name__=="__main__":
    import argparse
    parser = argparse.ArgumentParser(description='Scan and Describe SQL databases',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("root",help="Where to start")
    parser.add_argument("--nrows",help="Number of rows to print",type=int,default=5)
    args = parser.parse_args()
    process(args.root,nrows=args.nrows)
