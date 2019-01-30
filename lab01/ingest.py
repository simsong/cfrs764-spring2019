#!/usr/bin/env python
"""
ingest.py:

Ingest the logfiles into the database.
This program runs under Python2 or Python3
"""

import os
import re
import sqlite3
import datetime
import socket
import struct
import time


DB_FILE = os.path.join(os.environ['HOME'],"db.sqlite3")
NOTIFY_COUNT = 1000

SQL_SCHEMA = """
CREATE TABLE IF NOT EXISTS log (
  id INTEGER PRIMARY KEY,
  ll INTEGER,
  ipaddr VARCHAR(255),
  ipaddr_ INTEGER,
  ident VARCHAR(255),
  user VARCAR(255),
  date VARCHAR(19),
  method VARCHAR(255),
  path TEXT,
  protocol VARCHAR(255),
  status INTEGER,
  size INTEGER,
  referrer VARCHAR(255),
  useragent VARCHAR(255),
  line TEXT);
CREATE INDEX IF NOT EXISTS log_ll ON log(ll);
CREATE INDEX IF NOT EXISTS log_ipaddr ON log(ipaddr);
CREATE INDEX IF NOT EXISTS log_ipaddr_ ON log(ipaddr_);
CREATE INDEX IF NOT EXISTS log_ident ON log(ident);
CREATE INDEX IF NOT EXISTS log_date ON log(date);
CREATE INDEX IF NOT EXISTS log_method ON log(method);
CREATE INDEX IF NOT EXISTS log_path ON log(path);
CREATE INDEX IF NOT EXISTS log_protocol ON log(protocol);
CREATE INDEX IF NOT EXISTS log_status ON log(status);
CREATE INDEX IF NOT EXISTS log_referrer ON log(referrer);
CREATE INDEX IF NOT EXISTS log_useragent ON log(useragent);
"""


def ip2long(ip):
    """
    Convert an IP string to long
    """
    packedIP = socket.inet_aton(ip)
    return struct.unpack("!L", packedIP)[0]


LOG_RE = re.compile(r'^(?P<ipaddr>\S+) (?P<ident>\S+) (?P<user>\S+) \[(?P<date>[\w:/]+\s[+\-]\d{4})\] '+
                    r'"(?P<method>\S+)\s?(?P<path>\S+)?\s?(?P<protocol>\S+)?" (?P<status>\d{3}|-) ' +
                    r'(?P<size>\d+|-)\s?"?(?P<referrer>[^"]*)"?\s?"?(?P<useragent>.*)?"?\s*$')


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='Compute file changes',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("--dbfile",default=DB_FILE)
    parser.add_argument("--notify",type=int, default=NOTIFY_COUNT)
    parser.add_argument("--limit", type=int, default=0)
    parser.add_argument("access_log")
    args = parser.parse_args()
    try:
        os.unlink(args.dbfile)
    except FileNotFoundError as e:
        pass

    conn = sqlite3.connect(args.dbfile)
    c = conn.cursor()
    for stmt in SQL_SCHEMA.split(";"):
        c.execute(stmt)

    file_length = os.path.getsize(args.access_log)
    chars_read  = 0
    t0 = time.time()
    with open(args.access_log,"r") as f:
        for (ll, line) in enumerate(f,1):
            chars_read += len(line)
            m = LOG_RE.search(line)
            if not m:
                print("Cannot parse line {}: {}".format(ll, line))
                continue
            date_without_tz = m.group(4)[0:m.group(4).find(' ')]
            date = datetime.datetime.strptime(date_without_tz, '%d/%b/%Y:%H:%M:%S')
            c.execute("INSERT INTO LOG "
                        "(ll,ipaddr,ipaddr_,ident,user,date,method,path,protocol,status,size,referrer,"
                        "useragent,line) "
                        "VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                        [ll, m.group('ipaddr'), ip2long( m.group('ipaddr') ),
                        m.group('ident'), m.group('user'), date,m.group('method'),
                        m.group('path'), m.group('protocol'), m.group('status'), m.group('size'),
                        m.group('referrer'), m.group('useragent'), line.strip()])
            if ll % args.notify == 0:
                frac = float(chars_read) / float(file_length)
                if frac>0:
                    elapsed = time.time() - t0
                    eta     = elapsed / frac - elapsed
                else:
                    eta     = 0
                print("%s   %5.2f  (elapsed: %5.0f; eta: %5.0f)" % (ll,frac*100.0,elapsed,eta))
                conn.commit()
            if args.limit and ll >= args.limit:
                print("Limit ({}) reached".format(args.limit))
                break
        conn.commit()

