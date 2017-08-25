INSTALLATION

Please extract this archive to a folder in your home directory.

It should create a folder dv4mini containing the following files:
-rw-r--r-- 1 uname ugroup     128 Aug 25  2016 49-dv4.rules
-rwxrwxr-x 1 uname ugroup 1743360 Mär  9 20:50 dv4mini.exe
-rwxr-xr-x 1 uname ugroup  371784 Mär 11 13:19 dv_serial
-rw-rw-r-- 1 uname ugroup       0 Mär 19 16:59 README.txt
-rw-rw-r-- 1 uname ugroup     765 Sep 28 23:06 xref.ip

Please verify the x flags have been set on dv4mini.exe and dv_serial.

After plugging in the dv4mini stick into a USB port on your computer, please 
check if you can find a new device called /dev/ttyACMx, where x is a number.

If you haven't ever had a dv4mini stick running on your Linux system or if you 
can't see the device, copy the file 49-dv4.rules to your udev configuration. 
To do that, open a terminal (STRG-ALT-T on Ubuntu Linux) and change to the
directory where you unpacked the files to. For example
cd ~/Desktop/dv4mini
Then copy the file to the new destination as root like so:
sudo cp 49-dv4.rules /etc/udev/rules.d
This command requires you to give your password.
Finally reload the udev configuration with the following command
sudo service udev reload
then unplug and reconnect the dv4mini stick to its USB port.

After that you should find the /dev/ttyACMx device.

73! de DC3AX


