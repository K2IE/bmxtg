#!/usr/bin/python

## Author:  Dan Srebnick, K2DLS
##
## Version: 1.2
## Release: April 20, 2017
##
## Modified to dynamically load list of BM masters and talkgroups
##
## Version: 1.1
## Released: Janary 17, 2017
##
## Configuration moved to external config files
##
## Version: 1.0
## Originally Released: January 13, 2017
##
## Licensed under the Creative Commons Attribution + Noncommercial 3.0 License.
## Attribution Required / Noncommercial use permitted
##

import gtk
import requests
import json
from pprint import pprint
from collections import Counter
import ConfigParser
import os.path

config = ConfigParser.ConfigParser()

try:
    os.path.isfile("masters.conf")
except:
    exit("\nError: masters.conf not found\n")
else:
    config.read('masters.conf')

bm_num = config.get('My Master', 'bm_master')

## Server list
url = "http://registry.dstar.su/api/node.php"

try:
   r = requests.get(url)
except:
   exit("\nError: Can't reach BM masters list\n")

code = str(r.status_code)
if (code == "200"):
      data = json.loads(r.text)

      j = 0
      bm_master = "notfound"
      for i in data:
         if (data[j]["ID"] == bm_num):
            bm_master = data[j]["Address"]
            break
         j = j + 1
      if bm_master == "notfound":
         exit("\nError: Can't find address for master " + bm_num + "\n")
else:
   exit("\nError: Status code " + code + " while loading BM masters\n")

def press(widget):
   num = entry.get_text()
   pnum = widget.get_label()
   entry.set_text(num + pnum)

def send_press(widget):
   group = entry.get_text()
   status = bm_api(group)

##
## Define labels below.  It is ok to have definitions in this section that
## do not currently match a button, but they will not be used.
##
def send_mem(widget):

   group = ''
   tglabel  = entry.get_text()
  
   try:
       grouplabel[tglabel]
#      print "TG Label: " + tglabel
   except:
      message = " Missing TG num for " + tglabel 
      statusbar.push(context_id,message)
      entry.set_text('')
   else:
      group = str(grouplabel[tglabel])
      bm_api(group)
   
   return 0

def bm_api(group):
   url = 'http://' + bm_master + '/status/link.php?group=' + group
   r = requests.get(url)

#   debug_api(url,r)

   entry.set_text('')
   code = str(r.status_code)
   if (code == "200"):
      data = json.loads(r.text)

      if data:
#         print data["group"]
         group = str(data["group"])
         message = " Connected to TG " + group
      else:
         message = " Check BM master"

   else:
      message = " Failure: " + code

   statusbar.push(context_id,message)
   return 0

def clear_text(widget):
   entry.set_text('')
   statusbar.push(context_id," Enter TG")
 
   return 0

def debug_api(url,r):
   print "URL:             " + url
   print "HTTP Status Code:" + str(r.status_code)
   print r.headers
   print r.text
   return 0

win1 = gtk.Window()
win1.connect('destroy', lambda w: gtk.main_quit())
win1.set_default_size(250,250)
win1.set_title('BM XTG Dialer v1.2')

box = gtk.VBox()
win1.add(box)

entry = gtk.Entry()
box.pack_start(entry,False)

keypad = gtk.Table(2,2, gtk.TRUE)

a = [1,2,3,4,5,6,7,8,9,"*",0,"#" ]
x = 0
y = 0

for i in a:
   button = gtk.Button(str(i))
   button.connect("clicked",press)
   keypad.attach(button,x,x+1,y,y+1)

   x+=1
   
   if x > 2:
      x = 0
      y+=1

box.pack_start(keypad)

box2 = gtk.HBox()
box.pack_start(box2)

clear = gtk.Button("Clear")
clear.connect('clicked',clear_text)
box2.pack_start(clear)

send = gtk.Button("Send")
send.connect("clicked",send_press)
box2.pack_start(send)

box3 = gtk.HBox()
statusbar = gtk.Statusbar()
box.pack_start(statusbar)

win2 = gtk.Window()
win2.connect('destroy', lambda w: gtk.main_quit())
win2.set_default_size(250,250)
win2.set_title('BM XTG Memories')

# load talkgroups into tuples
grouplabel = {}

url = "https://api.brandmeister.network/v1.0/groups/"

try:
   r = requests.get(url)
except:
   exit("\nError: Can't reach BM groups list\n")

code = str(r.status_code)
if (code == "200"):
      data = json.loads(r.text)
      for tgid in data:
         tglabel = data[tgid]
         grouplabel[tglabel] = tgid
else:
   exit("\nError: Status code " + code + " while loading BM talkgroups\n")

## talkgroups.conf overrides BM group list when needed
try:
   with open('talkgroups.conf','r') as f:
      for line in f:
         if (not line.startswith("#") and line[0].isdigit()):
            line = line.rstrip()
            tgid, tglabel = line.split(',')
            grouplabel[tglabel] = tgid
except:
   exit("\nError: talkgroups.conf not found\n")

membox = gtk.VBox()
win2.add(membox)

mempad = gtk.Table(2,2, gtk.TRUE)

# load button names
try:
   with open('buttons.conf','r') as f:
      mem = f.read().splitlines()
except:
    exit("\nError: buttons.conf not found\n")

x = 0
y = 0

for i in mem:
   membutton = gtk.Button(i)
   membutton.connect("clicked",press)
   membutton.connect("clicked",send_mem)
   mempad.attach(membutton,x,x+1,y,y+1)

   x+=1
   
   if x > 2:
      x = 0
      y+=1

membox.pack_start(mempad)

context_id = statusbar.get_context_id("bmxtg")
statusmsg = " Master: " + bm_num + "  Enter TG"
#statusbar.push(context_id," Enter TG")
statusbar.push(context_id,statusmsg)

entry.connect("activate", send_press)

win1.show_all()
win2.show_all()

gtk.main()
