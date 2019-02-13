# CFRS 764 Lab 2

This lab is about Disk Arbitration, BlackLight, and Encryption. We will start by using both the command line and the Disk Arbitration tool to understand how the Mac's disk arbitration system works. Then we will fire up Blacklight and continue the analysis of the DC Gallery Case. Finally, you'll take home your disk image of the USB stick and try to crack some encrypted disk partitions with John The Ripper. (That's extracredit, BTW)

Be sure to leave yourself at least an hour for the Blacklight exercise!

Well, let's have at it.

# Understanding Disk Arbitration

1. Log out of the classroom iMac log back in using the CRFS750 account and our special password.

2. Open a terminal window and use the `diskutil activity` command to monitor the activity of the disk arbitration system.

    $ diskutil activity

3. Download Disk Arbitrator from [https://github.com/aburgh/Disk-Arbitrator](https://github.com/aburgh/Disk-Arbitrator).

   1. Go to https://github.com/aburgh/Disk-Arbitrator
   2. Click on [Releases](https://github.com/aburgh/Disk-Arbitrator/releases)
   3. Download [Disk.Arbitrator-0.8.dmg](https://github.com/aburgh/Disk-Arbitrator/releases/download/v0.8.0/Disk.Arbitrator-0.8.dmg)

4. Scan [Disk.Arbitrator-0.8.dmg](https://github.com/aburgh/Disk-Arbitrator/releases/download/v0.8.0/Disk.Arbitrator-0.8.dmg) through [VirusTotal.com](https://virustotal.com) as a preventative.

5. Mount the disk and run it.

6. Disable the disk arbitration daemon.

7. Experiment with plugging and unplugging external devices.

8. Plug in the instructor-provided USB drive

9. Make a copy of it using the `dd` command, as in:

```$ sudo dd if=DEVICE of=DISKFILE.raw  bs=64k conv=noerror,sync
```
   
Where DEVICE is the name of the device (how do you find it?) and DIKSFILE.raw is your output file.

Q: How do you find the name of the device?

A:

Q: How big is the disk file?

A:

Q: Calculate the SHA1 of the disk file.  What command do you use? Show the command and your output:

A:

Q: (Extra credit) Install libewf and image the USB stick with ewfacquire. Do you get the same hash value?  Show the output and explain why it is the same or different

# Blacklight

You will need the following disk image for this assignment:

* [tracy-home-2012-07-16-final.E01](http://downloads.digitalcorpora.org/corpora/scenarios/2012-ngdc/tracy-home/tracy-home-2012-07-16-final.E01)
* [tracy-home-2012-07-16-final.E02](http://downloads.digitalcorpora.org/corpora/scenarios/2012-ngdc/tracy-home/tracy-home-2012-07-16-final.E02)

Please download the disk image in advance of class and store it on the external drive that you bring to class.

1. Start up Blacklight and create a new case on your external drive.

2. Add the Tracy Home drive, but do not do a full scan! It will take more time than we have.

3. Recall that Tracy's ex-husband put a keylogger on her computer. Can you find how it works?

Q: Please report all of the evidence you find of the keylogger:

A:

# Cracking

Did you notice that there is not one, but two encrypted disk images on the USB stick?

1. Review the web site for John the Ripper at [https://www.openwall.com/john/](https://www.openwall.com/john/).

2. You should be able to the Community Edition compiled for MacOS from [https://openwall.info/wiki/john/custom-builds#Compiled-for-Mac-OS-X](https://openwall.info/wiki/john/custom-builds#Compiled-for-Mac-OS-X). Download it.

3. You might want to check the download at VirusTotal before trusting it...

4. You'll need to use the `dmg2john` program to extract the encrypted DMG encryption key from the DMG. You'll find instructions at [https://wiki.loopback.org/display/KB/How+to+brute+force+crack+a+MacOS+disk+image](https://wiki.loopback.org/display/KB/How+to+brute+force+crack+a+MacOS+disk+image).

5. Oh, you'll also need a word list. You'll find that one of these disk images has a fairly common passphrase, while the other has one created especially for this course.

Good luck!



Q: What is on the first DMG?

A:

Q: What is the passphrase of the second DMG?

A:

Q: What did you find on the second DMG?

A:

