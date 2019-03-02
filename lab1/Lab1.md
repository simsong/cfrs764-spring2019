# CFRS 764 Lab 1

In this lab we will be working with the Macbook disk image from the DC Gallery Case. We will be analyzing it from the command line, but you can also use BlackLight if you wish. (Note: we will not cover the use of BlackLight in Lab 1.)

# Background

Our main goals of this project are:

1. Mount the disk image `tracy-home-2012-07-16-final` from [https://digitalcorpora.org/](https://digitalcorpora.org/) as a read-only file system on your Mac so that you can access it using the standard Unix command-line tools `grep`, `wc`, `head`, `tail` and so on.
2. Examine the files with the file browser, the command line utilities, or emacs. 
3. View the content of some files.


## Downloading and mounting the disk image

You will need the following disk image for this assignment:

* [tracy-home-2012-07-16-final.E01](http://downloads.digitalcorpora.org/corpora/scenarios/2012-ngdc/tracy-home/tracy-home-2012-07-16-final.E01)
* [tracy-home-2012-07-16-final.E02](http://downloads.digitalcorpora.org/corpora/scenarios/2012-ngdc/tracy-home/tracy-home-2012-07-16-final.E02)

Please download the disk image in advance of class. We will be mounting the disk image. There are several ways that you can do this:

1. You can convert the disk image to a raw (e.g. dd) file and then mount it read-only. You can convert the disk image with a program such as [FTK Imager](https://accessdata.com/product-download/ftk-imager-version-4.2.0) which runs on Windows. Alternatively, you can convert it using [ewfexport](https://github.com/libyal/libewf), which can be easily installed on MacOS using [MacPorts](https://www.macports.org/) or [Homebrew](https://brew.sh/). Your instructor uses MacPorts. The converted file should be given a `.dmg` or a `.iso` extension so that it can be directly mounted using the Macintosh `hdiutil` tool, as described below.

2. You can use ewfmount (part of libewf) to "mount" the .E01 file and make a virtual raw file appear. You can then mount the virtual raw file using `hdiutil`. 

3. You can use **EW Mounter** (part of Blacklight) to mount the disk image. Documentation for EW Mounter appears in Appendix 2 (pp. 286-296) of the [2018 BlackLight User Guide](https://drive.google.com/open?id=1DPEpXdlfgUaTjRrb3i5N4VwLMS9NyLdY).

Note that in my experiments with ewfmounter on macOS 10.14.2, the mounted disk image can only be accessed by the superuser.

Here is a shell command that will export the E01 disk image to a raw file:

```
$ ewfexport -f raw -j4 -t tracy-home-2012-07-16-final -u tracy-home-2012-07-16-final.E0?
ewfexport 20171104


Export started at: Jan 13, 2019 13:28:57
This could take a while.

Status: at 7.2%
        exported 1.2 GiB (1358528512 bytes) of total 17 GiB (18639421440 bytes)
        completion in 50 second(s) with 329 MiB/s (345174471 bytes/second)


...
```

If you have created a raw disk image, you can mount it on a Mac at the location `/Volumes/tracy` using this command line:

```
$ hdiutil attach -readonly -owners on -noverify -mountpoint /Volumes/tracy tracy-home-2012-07-16-final.dmg 
/dev/disk2          	                               	/Volumes/tracy
```

If you want to try using ewfmount, below you will find a sequence that worked on your instructor's MacMini. Notice that the `hdiutil` command needs to be run as the superuser, since only the superuser has access to disk images mounted with `ewfmount`:

```
$ sudo ewfmount -X volicon=/Library/Filesystems/osxfuse.fs/Contents/Resources/Volume.icns tracy-home-2012-07-16-final.E0? /mnt
ewfmount 20171104

$ sudo ls -l /mnt/
total 18202560
-r--r--r--  1 root  wheel  18639421440 Jan 13 14:03 ewf1
$ ln -s /mnt/ewf1 /tmp/ewf1.dmg
$ sudo hdiutil attach -readonly -owners on -noverify -mountpoint /Volumes/tracy /tmp/ewf1.dmg
```

## Verifying the Mounted Disk

Once you have the file system mounted, however you have it mounted, verify that it's mounted and that you can access the following files. Note that I have it mounted at /Volumes/tracy.

$ ls -l /Volumes/tracy/var/
total 0
drwx------   2 root       wheel        68 May 25  2011 agentx/
drwxr-x---   6 _amavisd   _amavisd    204 Jun 12  2012 amavis/
drwxr-xr-x   8 daemon     wheel       272 Jun 12  2012 at/
drwx------  66 root       wheel      2244 Jul 16  2012 audit/
drwx------   2 root       wheel        68 Aug 16  2011 backups/
drwxr-xr-x  38 root       wheel      1292 Jul 11  2012 db/
drwxr-xr-x   2 root       sys          68 Aug 16  2011 empty/
drwxr-xr-x   6 root       wheel       204 Jun 14  2012 folders/
drwxr-x---   3 _jabber    _jabber     102 Jun 12  2012 jabberd/
drwxr-xr-x   3 root       wheel       102 Jun 12  2012 lib/
drwxr-xr-x  41 root       wheel      1394 Jul 16  2012 log/
drwxrwxr-x   2 root       mail         68 Aug 16  2011 mail/
drwxr-xr-x   3 root       wheel       102 Jun 12  2012 msgs/
drwxr-xr-x   5 root       wheel       170 Jun 12  2012 named/
drwxr-xr-x   2 root       wheel        68 Aug 16  2011 netboot/
drwxr-x---   2 _postgres  _postgres    68 Dec  4  2011 pgsql_socket/
drwxr-x---   7 root       wheel       238 Jun 28  2012 root/
drwxr-xr-x   4 root       wheel       136 May 25  2011 rpc/
drwxrwxr-x  25 root       daemon      850 Jul 16  2012 run/
drwxr-xr-x   2 daemon     wheel        68 Aug 16  2011 rwho/
drwxr-xr-x   7 root       wheel       238 Jun 12  2012 spool/
drwxrwxrwt   3 root       wheel       102 Jul  2  2012 tmp/
drwxr-x---   2 _amavisd   _amavisd     68 Jul 21  2011 virusmails/
drwxr-xr-x   4 root       wheel       136 Jul 15  2012 vm/
drwxr-xr-x   2 root       wheel        68 Jun 20  2011 xgrid/
drwxr-xr-x   5 root       wheel       170 Jun 12  2012 yp/
$ ls -l /Volumes/tracy/var/audit
ls: audit: Permission denied
$ sudo ls -l /Volumes/tracy/var/audit/ | head
total 636
-r--r-----  1 root  wheel    958 Jun 16  1985 19850616152718.19850616152729
-r--r-----  1 root  wheel    958 Jun 16  1985 19850616152806.19850616152824
-r--r-----  1 root  wheel  14938 Jul  2  2012 20061205082346.20120702200906
-r--r-----  1 root  wheel  87900 Jun 12  2012 20120612151305.20120612154851
-r--r-----  1 root  wheel    958 Jun 12  2012 20120612172113.20120612172152
-r--r-----  1 root  wheel  30282 Jun 12  2012 20120612190103.20120612203100
-r--r-----  1 root  wheel   6884 Jun 12  2012 20120612203111.20120612210300
-r--r-----  1 root  wheel   5477 Jun 13  2012 20120613151229.20120613172517
-r--r-----  1 root  wheel  19319 Jun 13  2012 20120613194523.20120613202847
```

As you can see, I needed to access `/var/audit` as root, since it is mode 600. If you wish, you can mount a second copy where you own all of the files, but there may still be files that you are unable to read, by changing `-owners on` to `-owners off`. However, this will make it appear that you own all of the files! So you might want to mount a second copy of the file system at `/Volumes/tracy2`. Alternatively, you can just type `sudo bash` to bring up a root shell.

## Commands we will be using

Now that you have the disk image mounted (and possibly mounted twice!)

For answering these problems, you are free to use any command line tool that you wish. The following may be especially useful. To get details on any, type `man <command>` at the command line.

* `man` --- get documentation on a command.
* `grep` --- search for lines in a file that match a given regular expression.
* `head` --- Return the first N lines of a file
* `tail` --- Return the last N lines of a file
* `awk` --- Run a program in the AWK language. 
* `cut` --- Select portions of each line of a file
* `sort` --- Sort the lines of a file
* `uniq` --- Suppress repreating lines, optionally counting the number of suppressions.
* `wc` --- Report the number of characters, words, and lines in a file
* `cat` --- Combine files.

If you haven't done so, I recommend reading the man page for each of these.

Additional command that I find useful:

* `sed` --- Stream editor.
* `emacs` --- Programmer's editor, useful for looking at any file up to ~500MB in size. Can display hexdumps, too. (You can get a tutorial by typing `C-h T`)
* `xxd` --- Another way to generate a hexdump
* `file` --- Identify a file by its magic number(s).
* `ls` --- List files

The following `grep` options may be especially useful for this problem set:

* `grep -r <pattern> <directory>` --- Recrusive grep from _directory_ for _pattern_.
* `grep -l <pattern> ...` --- Just print the names of files with matching content.

So, you might do this:

* `grep -r ‘Jan 10’  /Volumes/tracy/private/var/log` --- Search for every log file that contains `Jan 10` on a line; print that line

When you list files with the `ls`, the times are displayed in local time using the TZ environment variable. If you want to use Eastern time, this his:

    ```
    export TZ=America/New_York
    ```

* `ls -lT` --- will show full timestamps
* `ls -alT` ---  will show files beginning with dots
* `ls -alFT` --- will also show a / after directories

# Lab #1 Problems

Below is a list of questions. Each one has a code number. Turn in your answers in a file and they will be graded by your artisanal grader. 

**For each problem, please show the commands that you typed to get the answer**

## Logfile Questions

Q: What is the earliest date for a log message that appears in the logfiles?


A:



Q: In which log files this earliest date appear?

A:

Q: What is the last date on which any log entry was made. Please consider all of the log files and provide both the log file name and the date:g


A:

Q: change the time zone to UTC. What is the modification date of opendirectoryd.log.2?


A:

Q: What can we infer from these dates?

A:

Q: What is the `ls` option would print non-printable characters as a question mark?


A:

Q: Which ls option would print non-printable characters as their octal equivallents?


A:

Q: What is the option for the `cat` command that has it display non-printable characters?


A:

Q: What is a command that you could use to find out if there any files in the disk that have non-printable characters in their filenames? 


A:

Q: Are there any files on the tracy volume that have non-printable characters  in their filenames?


A:

Q: The application VirtualBox.app appears in the /Applications directory. What evidence is there is the logfiles (or elsewhere) that the VirtualBox program was run?


A:

Q: What are the 5 largest files in private/var/folders and what are they used for?


A:







Q: There are eight obvious sqlite3 databases in the /var/folders directories, apparently containing two different database types. Provide two of the filenames:


A:



Q: One of the SQLite3 databases contains a list of files. Find it and preprovide the files. What can you learn from this database?


A:











Q: The timestamps in the SQLite3 table `thumbnails` are in Apple Cocoa Core Data timestamp format. There is an [online converter](https://www.epochconverter.com/coredata) that will convert these timestamps to human-readable timestamps. For the file `/private/var/folders/15/j2xk5wls0c95jjx8f5h_00mh0000gn/C/com.apple.QuickLook.thumbnailcache/index.sqlite`, please provide the date of the first and the last thumbnail in GMT.


A:







Q: Extra credit: As of June 27, 2012, what was the previous semester's balance due at the Prufrock Preparatory School?


A:

