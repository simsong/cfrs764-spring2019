Download the logfiles:
    
```
$ wget https://simson.net/lab1/logs.tar.gz
$ tar xfvz logs.tar.gz
$ openssl sha256 access.log.2018.txt error.log.2018.txt
SHA256(access.log.2018.txt)= e5e8aed8cfa4bc9fc735e97d7acb4de3dec39eb9785a1dab6094e1c81fd320a3
SHA256(error.log.2018.txt)= a66a609751a2f2efe72761e9ab039b8ace5b0db322ac10c733b5450c58d081d6
[nimi ~ 20:56:06]$
```

Download the SQLite3 file:

    $ wget https://simson.net/lab1/db.sqlite3.gz
    $ gunzip db.sqlite3.gz

Verify it with:

```
$ openssl sha256 db.sqlite3
SHA256(db.sqlite3)= 14ce8fd5801b16ee2a7222ae0f100253891c5c8fe6cf9909a9a09be83e991b3e
$ sqlite3 db.sqlite3
SQLite version 3.23.1 2018-04-10 17:39:29
Enter ".help" for usage hints.
sqlite> .schema
CREATE TABLE log (
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
CREATE INDEX log_ll ON log(ll);
CREATE INDEX log_ipaddr ON log(ipaddr);
CREATE INDEX log_ipaddr_ ON log(ipaddr_);
CREATE INDEX log_ident ON log(ident);
CREATE INDEX log_date ON log(date);
CREATE INDEX log_method ON log(method);
CREATE INDEX log_path ON log(path);
CREATE INDEX log_protocol ON log(protocol);
CREATE INDEX log_status ON log(status);
CREATE INDEX log_referrer ON log(referrer);
CREATE INDEX log_useragent ON log(useragent);
sqlite> select count(*) from log;
7270333
sqlite> select min(date),max(date) from log;
2018-01-01 01:24:29-08:00|2019-01-01 01:50:50-08:00
sqlite>
```
