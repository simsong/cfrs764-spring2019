# Lab #4
The original goal of Lab #4 was to explore how to use DTrace for reverse-engineering running programs. Unfortuantely, many DTrace programs no longer work, or work inconsistently. Therefore we are taking another approach. 

For Lab \#4, you should evaluate one or more reverse engineering tools by using them on two programs. 

## Pick your reverse-engineering tools

**Option #1: DTrace**

You can direclty use use the range of DTrace applications included with MacOS. I provided a list of them in class, but you can generate your own list by typing `man -k dtrace`. 

Note that DTrace commands generally need to be run as root (type `sudo
<commandname>` and even then, many of the commands no longer work
completely because of Apple's System Integrity Protection (SIP).

In hunting around the Internet, I found [http://dtrace.org/blogs/brendan/2011/10/10/top-10-dtrace-scripts-for-mac-os-x/](this blog on dtrace from 2011). It's worth reviewing, in part because it shows how you can write DTrace scripts (from the [authors' book](http://www.brendangregg.com/dtracebook/index.html). I bought the book and am happy to lend it to anyone who would like to review it, but as I indicated, many of the scripts no longer work due to SIP.

**Option #2: DTrace with a GUI**

Several programs are available that provide a GUI for some of the DTrace functionality. These include:

* **Instruments** is a program that is part of XCode. You can find it at `/Applications/Xcode.app/Contents/Applications/Instruments.app`. It's really just a front-end for DTrace. 

* **fseventer** visualizes file system access. 

**Option #3: filemon and other tools***
You can cobble together your analysis of a running program with these tools:

* [**filemon**](http://newosxbook.com/tools/filemon.html) is a program written by Jonathan Levin that hooks the OSX file monitoring API. (Note that this is different from the fsevents API). 

* [**procexp**](http://newosxbook.com/tools/procexp.html) procexp, also by Jonathan Levin, is basically a souped-up version of the top(1) command that we've used so many times. It uses system call `proc_info()` to get lots of information about running processes and shows the information with an interactive character-based GUI.

* **lsof** List of open files, by process, which we've used previously.

* **ps** List of running processes

These tools all remain powerful debugging tools, even in the world of SIP. You can use them for a lot of reverse-engineering.

## Pick a task

Once you have decided upon your reverse engineering tools, your job is to pick something to reverse engineering. Your goal is to take a program and really run it into the ground---figure out what it is doing with the tools that we have.

For example, some students had problems getting the pre-compiled verison of Volatility to find the ZIP-file plug-in, but were able to get it to work when they ran Volatility from source. If you would like to dig deeper on that, run both versions and compare the sequence of directories and files that are opened for reading. WHere are the verisons looking for their plugins --- are they looking in different locations? Does the pre-compiled version look for plugins _at all_, or do you need to speicfy a search location with the `--plugins` option?

What you decide to reverse-engineer should be something that is both
   relevant to this course and deep enough to represent a few hours of
   work. For example, if you turn in a homework that says "I ran lsof and discovered that 1000
   files are created in `/private/var/db/uuidtext/`---here is the list," that will not get full credit.

# What you should turn it:

Your lab report should contain a narrative of not less than 2 pages (not including tool output) that clearly states:

1. What you decided to target for reverse-engineering, and why it is relevant to this course.
2. What tools you used.
3. What you had your target program do.
4. What the tools reported (put the tool output in an appendix; here I want you to only include the relevant portions of the tool output).
5. How you changed the behavior of your program for a second or third run.
6. How the tool output reflected the change in the program's behavior.

Your homework should be turned in as a PDF file. You should use an appropriately sized font so that lines do not excessively wrap. Your margins should be small so as to get the maximum amount of text on the page.

