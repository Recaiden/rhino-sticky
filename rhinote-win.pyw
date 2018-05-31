#!/usr/bin/env python
# Filename : rhinote.py

# Rhinote version 0.7.4  A simple "sticky notes" application; Windows version.

# Copyright 2006, 2010 by Marv Boyes - greyspace@tuxfamily.org
# http://rhinote.tuxfamily.org
# Please see the file COPYING for license details.

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.

# Thiis program is distributed in hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULR PURPOSE. See the 
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free SOftware
# Foundation, Inc., 51 Franklin St., Fifth Floor, Boston, MA  02110-1301 USA

#os.environ['TCL_LIBRARY']= r'C:\python27\tcl\tcl85'
#os.environ['TK_LIBRARY'] = r'C:\python27\tcl\tk85'

from Tkinter import *
import tkFileDialog, tkMessageBox

import os
from os import system
from os.path import expanduser

def defaultFileName(id_note):
    return "rhinote-%d.txt" %id_note

count_note = 0

def is_int(str_num):
    try:
        int(str_num)
    except ValueError:
        return False
    return True

# the root window:
def Rhinote(id_note=1):
    def on_closing():
        t.save_file()
        r.destroy()

    def configure(event):
        #canvas.delete("all")
        w, h = event.width, event.height
        #print w, h
        t.set_size(w, h)
        
    r = Tk()
    r.option_add('*font', '{Helvetica} 11')
    t = TextWidget(r, id_note = id_note, bg = '#f9f3a9', wrap = 'word', undo = True)
    global count_note
    count_note += 1
    t.focus_set()
    t.pack(fill = 'both', expand = 1)

    path_home = expanduser("~")
    path = os.path.join(path_home, ".rhinote")
    if not os.path.exists(path):
        os.mkdir(path)
    os.chdir(path)

    geostring = "%dx%d" %(t.size[0], t.size[1])
        
    #r.geometry('220x235')
    r.geometry(geostring)
    r.title('Rhinote')
    r.protocol("WM_DELETE_WINDOW", on_closing)
    r.bind("<Configure>", configure)

    if os.path.exists(os.path.join(path, defaultFileName(id_note+1))):
        Rhinote(id_note+1)

    
    r.mainloop()

# the text widget, and all of its functions:
class TextWidget(Text):
    def save_file(self, whatever = None):
        if (self.filename == ''):
            self.filename = defaultFileName(self.id_note)
            #print self.filename
            #            self.save_file_as()
            #            self.master.title('Rhinote %s' % self.filename)
            #        else:
        f = open(self.filename, 'w')
        f.write("%d %d\n" %(self.size[0], self.size[1]))
        f.write(self.get('1.0', 'end').rstrip("\r\n"))
        f.close()
        self.master.title('Rhinote %s' % self.filename)
        # Comment out the following line if you don't want a 
        # pop-up message every time you save a file:
        if self.verbose:
            tkMessageBox.showinfo('FYI', 'File Saved.')

    def set_size(self, w, h):
        self.size = (w, h)

    def save_file_as(self, whatever = None):
        self.filename = tkFileDialog.asksaveasfilename(filetypes = self._filetypes)
        f = open(self.filename, 'w')
        f.write("%d %d\n" %(self.size[0], self.size[1]))
        f.write(self.get('1.0', 'end'))
        f.close()
        # comment out the following line if you don't want a
        # pop-up message every time you save a file:
        if self.verbose:
            tkMessageBox.showinfo('FYI', 'File Saved')

    def open_file(self, whatever = None, filename = None):
        if not filename:
            self.filename = tkFileDialog.askopenfilename(filetypes = self._filetypes)
            self.master.title('Rhinote %s' % self.filename)
        else:
            self.filename = filename
            self.master.title('Rhinote %s' % self.filename)
        if not (self.filename == ''):
            f = open(self.filename, 'r')

            # line 1 is hopefully a size parameter
            line_size = f.readline()
            args_size = line_size.rstrip("\r\n").split(" ")
            if len(args_size) is 2 and is_int(args_size[0]) and is_int(args_size[1]):
                self.set_size(int(args_size[0]), int(args_size[1]))
            else:
                f.seek(0)
                
            f2 = f.read()
            
            self.delete('1.0', 'end')
            self.insert('1.0', f2)
            f.close()
            self.master.title('Rhinote %s)' % self.filename)

    def new_window(self, event):
        Rhinote(count_note+1)

    def help(self, whatever = None):
        tkMessageBox.showinfo('Rhinote Help', message = '''
Editing Commands
    Ctrl-x : Cut selected text
    Ctrl-c : Copy selected text
    Ctrl-v : Paste cut/copied text
    Ctrl-Z : Undo
    Ctrl-Shift-z : Redo

File Commands
    Ctrl-o : Open file
    Ctrl-s : Save current note
    Ctrl-a : Save current note as <filename>
    Ctrl-n : Open new Rhinote

General
    Ctrl-h : Display this help window

Rhinote version 0.7.4
Free Software distributed under the GNU General Public License
http://rhinote.tuxfamily.org
''')

    def __init__(self, master, id_note, **kw):
        Text.__init__(self, master, **kw)
        self.verbose = False
        self.bind('<Control-n>', self.new_window)
        self.bind('<Control-N>', self.new_window)
        self.bind('<Control-o>', self.open_file)
        self.bind('<Control-O>', self.open_file)
        self.bind('<Control-s>', self.save_file)
        self.bind('<Control-S>', self.save_file)
        #self.bind('<Control-a>', self.save_file_as)
        #self.bind('<Control-A>', self.save_file_as)
        self.bind('<Control-h>', self.help)
        self.bind('<Control-H>', self.help)
        self.master = master
        self.id_note = id_note
        self.filename = ''
        self._filetypes = [
        ('Text/ASCII', '*.txt'),
        ('Rhinote files', '*.rhi'),
            ('All files', '*'),
            ]
        self.size = (220, 235)
        path_home = expanduser("~")
        self.path = os.path.join(path_home, ".rhinote")
        if not os.path.exists(self.path):
            os.mkdir(self.path)
        os.chdir(self.path)

        if os.path.exists(os.path.join(self.path, defaultFileName(self.id_note))):
            self.open_file(filename = defaultFileName(id_note) )
            

# make it so:
if __name__ == '__main__':
    Rhinote()
    


