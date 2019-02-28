# Memory analysis on the Mac

Memory forensics requires two steps:

1. Acquiring memory (although in some cases you can analyze live memory)
2. Analyzing the memory you have required.

Apple has made it systematically harder to analyze memory over the years. Early MacOS systems contained a device called `/dev/pmem` that you could use to access physical memory. This device was removed from the operating system several years ago.

For years the go-to memory analysis framework has been Volatility. Then several years ago there was a split in the memory forensics community, and Google created a fork called Rekall Forensics. Rekall had advantages over Volatility, but it has largely been abandoned by its creators.

Google also developed a memory acquisition tool called osxpmem. The osxpmem tool includes a kernel ext ension called `MacPmem.kext` that recreates the `/dev/pmem` device, and a tool called `osxpmem` that reads the device and creates a memory dump. `osxpmem` can create memory files in three formats: `map`, an AFF4Map object, `elf` (and ELF stream), and `raw`). The latest OSX pmem tool is available as part of something called Velociraptor and can be downloaded from [https://github.com/Velocidex/c-aff4](https://github.com/Velocidex/c-aff4).

In this lab, you will create the memory image of a Mac that contains a known process that is downloading a file from a remote computer. You will then examine the memory image to see if you can locate the following:

1. The process doing the downloading.
2. The name or IP address of the computer that you are downloading from.
3. The local file that is open and that is receiving the file being downloaded.

This lab has three goals. First, you will learn how to construct a forensic image so that an artifact can be found. This sort of principled examination is important when you are testing and validating forensic tools, and is an essential part of digital forensics research. Second, you will learn how to make a memory acquisition on one or more Mac operating systems using one or more techniques. And lastly, you will learn how to find artifacts in a memory image. 

To assist you in creating this image, I have created a program that is running at [https://simson.net/bigfile.cgi](https://simson.net/bigfile.cgi) which will download a file approximately 300K in size over the course of 30 minutes. The idea is that you can download this URL using `curl` of Safari and the connection will stay open long enough while you are making the memory image.

# Preparing the forensic image.

We will do our initial forensic examination with an El Capitan Virtual Machine running inside VMWare. Create a machine with the following characteristics:

* VMWare Fusion running El Capitan (MacOS 10.11) (I used 10.11.6)
* 2GB of RAM
* 40GB Disk
* Username `user` password `user`

1. Log into the virtual machine, bring up the Terminal application.
Inside the terminal, type:

```
curl https://simson.net/bigfile.cgi -o bigfile.txt
```

2. You can monitor the progress of the download by opening up another Terminal window and typing:

```
tail -f bigfile.txt
```

3. While the download is happening, suspend the virtual machine.

4. Right-click on the name of the virtual machine in the VMWare Fusion title bar and you will see the path to the virtual machine package. Open the containing folder. Right-click on the vmware package in the finder and chose "Show Package Contents" to view the individual files. Alternatively, go to the command line and list the files in the package with the `ls -l` command. You should see something that looks like this:

```
[nimi /Volumes/SanDiskSSD/macOS 10.11 (El Capitan).vmwarevm 08:10:21]$ ls -l
total 13551596
-rw-r--r--  1 simsong  staff  11590107136 Feb 24 08:07 Virtual Disk.vmdk
drwxr-xr-x  3 simsong  staff          102 Feb 24 08:07 caches/
-rw-------  1 simsong  staff   2147483648 Feb 24 08:08 macOS 10.11 (El Capitan)-6cd268bd.vmem
-rw-------  1 simsong  staff    138263946 Feb 24 08:07 macOS 10.11 (El Capitan)-6cd268bd.vmss
-rw-------  1 simsong  staff       270840 Feb 24 07:56 macOS 10.11 (El Capitan).nvram
-rw-r--r--  1 simsong  staff          645 Feb 24 07:56 macOS 10.11 (El Capitan).plist
-rw-r--r--  1 simsong  staff            0 Feb 23 21:10 macOS 10.11 (El Capitan).vmsd
-rwxr-xr-x  1 simsong  staff         3133 Feb 24 08:07 macOS 10.11 (El Capitan).vmx
drwxrwxrwx  3 simsong  staff          102 Feb 23 21:10 macOS 10.11 (El Capitan).vmx.lck/
-rw-r--r--  1 simsong  staff          382 Feb 24 07:56 macOS 10.11 (El Capitan).vmxf
-rw-r--r--  1 simsong  staff         1006 Feb 24 08:07 startMenu.plist
-rw-r--r--  1 simsong  staff       384651 Feb 24 07:56 vmware-0.log
-rw-r--r--  1 simsong  staff       300028 Feb 24 08:08 vmware.log
[nimi /Volumes/SanDiskSSD/macOS 10.11 (El Capitan).vmwarevm 08:10:22]$
```

Not surprisingly, the `.vmem` file is the virtual memory of the 2GB virtual machine (which is why it is exactly 2^31 bytes in size, while the `.vmss` file is the VMWare Suspended State.

# Analyzing the forensic image with Volatility

Volatility is the currently the most popular memory forensics tool because of the wide number of analyses it can perform and its easy extensibility. Most analyses are performed with plugins that perform a specific feature. The Mac-specific plugins being with `mac_`.

Volatility requires a profile that matches your kernel.

* [Volatility Wiki on using it with the Mac](https://github.com/volatilityfoundation/volatility/wiki/Mac)
* [Download a pre-built copy of Volatility 2.6](https://www.volatilityfoundation.org/releases)
* [Download a pre-built Mac profile](https://github.com/volatilityfoundation/volatility/wiki/Mac#download-pre-built-profiles)
* [ElCapitan MacOS 10.11 profiles](https://github.com/volatilityfoundation/profiles/tree/master/Mac/10.11)

The easiest way forward is to download the prebuild Volatility and the prebuilt profiles. If you download the source, you'll need to make sure that all of the various Python dependencies are installed. That's a lot of work!

You can download volatility and the profiles by typing:

```
curl http://downloads.volatilityfoundation.org/releases/2.6/volatility_2.6_mac64_standalone.zip -o volatility_2.6_mac64_standalone.zip
unzip volatility_2.6_mac64_standalone.zip
git clone https://github.com/volatilityfoundation/profiles.git
```

You must then install the Mac profiles for 10.11; you can do that with this command:

```
cp profiles/Mac/10.1/* volatility_2.6_mac64_standalone/plugins/overlays/mac
```

Verify that they are installed with this command (it will take a while):

```
volatility_2.6_mac64_standalone/volatility_2.6_mac64_standalone --info | grep -i mac
```

## What to hand in:

Hand in a Microsoft Word file describing:
- What you did.
- Output from Volatility's `mac_psaux` showing your download command

hint: try `volatility_2.6_mac64_standalone/volatility_2.6_mac64_standalone -f <memory_file> ps_aux`

then try: `volatility_2.6_mac64_standalone/volatility_2.6_mac64_standalone -f <memory_file> ps_aux | grep curl`

or:

then try: `volatility_2.6_mac64_standalone/volatility_2.6_mac64_standalone -f <memory_file> ps_aux | grep 208.113.173.77`

- Output from Volatility's  `mac_netstat` showing the open TCP connection.

- Output from Volatility's  `mac_lsof` showing the relevant open files.

# Moving from a B+ to an A
Simply following the instructions above will get you a B+ on the homework. If you want an A, you'll need to do something additional.

## Option #1: Capturing images with osxpmem
You can download version 2.1 of osxpmem under the Rekall Release 1.5.1. Furka from [https://github.com/google/rekall/releases](https://github.com/google/rekall/releases).

* Here is an article about using osxpmem: http://www.computerpi.com/mac-ram-acquisition/

## Option #2: Try using Rekall
If you are interesetd in going deeper, give the Rekall Forensics package a try.
You will find instructions at [http://www.rekall-forensic.com/releases](http://www.rekall-forensic.com/releases).

## Option #3: Try building your own Volatility profile.

## Option #4: Put another process in the memory image

## Option #5: Do something else with memory forensics (for example, run bulk_extractor)

Write up what you did and add it to your homework.

