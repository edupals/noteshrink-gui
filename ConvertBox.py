import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Pango, GdkPixbuf, Gdk, Gio, GObject,GLib

import copy
import gettext
import Core

import Dialog
import time
import threading
import os
from os.path import splitext, join

import settings

gettext.textdomain(settings.TEXT_DOMAIN)
_ = gettext.gettext


class ConvertBox(Gtk.VBox):
	def __init__(self):
		Gtk.VBox.__init__(self)
		self.core=Core.Core.get_core()
		self.void = True
		self.background_img = None
		self.set_background()
		self.drag_dest_set(Gtk.DestDefaults.ALL, [], Gdk.DragAction.COPY)
		self.connect("drag-data-received",self.drag_files)
		self.drag_dest_add_text_targets()

	def set_background(self):
		self.background_img = Gtk.Image.new_from_stock("gtk-copy",Gtk.IconSize.MENU)
		self.background_img.set_halign(Gtk.Align.CENTER)
		self.background_img.set_valign(Gtk.Align.CENTER)
		# self.background_img.drag_dest_set(Gtk.DestDefaults.ALL, [], Gdk.DragAction.COPY)
		self.background_img.show()
		self.set_homogeneous(True)
		self.pack_start(self.background_img,False,False,0)
		self.queue_draw()

	def new_file(self,pkg_name):
		if self.background_img:
			# self.remove(self.background_img)
			# self.set_homogeneous(False)
			# self.background_img = None
			self.set_homogeneous(False)
			self.background_img.hide()
		hbox = Gtk.HBox()

		pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(pkg_name,100,100,True)
		miniature = Gtk.Image.new_from_pixbuf(pixbuf)
		miniature.set_size_request(100,100)
		label = Gtk.Label(pkg_name)
		b = Gtk.Button()
		i = Gtk.Image.new_from_file(join(settings.RSRC,"trash.svg"))
		b.add(i)
		b.set_halign(Gtk.Align.CENTER)
		b.set_valign(Gtk.Align.CENTER)
		b.set_name("DELETE_BUTTON")
		b.connect("clicked",self.delete_file,hbox,label)
		hbox.pack_start(miniature,False,False,0)
		hbox.pack_start(label,False,False,0)
		hbox.pack_end(b,False,False,10)
		hbox.show_all()
		hbox.pepito=pkg_name
		label.set_margin_right(20)
		label.set_margin_left(20)
		label.set_margin_top(20)
		label.set_margin_bottom(20)
		label.set_ellipsize(Pango.EllipsizeMode.START)
		label.set_tooltip_text(pkg_name)
		hbox.set_name("PKG_BOX")
		self.pack_start(hbox,False,False,5)
		self.queue_draw()
		hbox.queue_draw()
 	#def new_file

	def drag_files(self, widget, drag_context, x,y, data,info, time):
		text = data.get_text()
		text = text.strip().split("\r\n")
		files = []
		for x in text:
			if x.startswith('file://'):
				files.append(x.replace('file://',''))
		self.core.noteshrink_interface.inputfiles.extend(files)
		for x in files:
			self.new_file(x)
	#def drag_files

	def delete_file(self, widget, container, path ):
		self.remove(container)
		if len(self.get_children()) == 1:
			self.set_homogeneous(True)
			self.background_img.show()
		
class DropArea(Gtk.Image):

    def __init__(self,drop_param):

    	self.drop=False
    	self.commonFunc=CommonFunc()
    	self.inputpath=drop_param[0]
    	self.destpath=drop_param[1]
    	self.outputfile_label=drop_param[2]
    	self.convert_label=drop_param[3]
    	self.convert_button=drop_param[4]


    	Gtk.Image.__init__(self)
    	Gtk.Image.set_from_file(self,settings.DROP_FILE)
    	self.drag_dest_set(Gtk.DestDefaults.ALL, [], Gdk.DragAction.COPY)
       	
       	self.connect("drag-data-received", self.on_drag_data_received)
       	self.text=""

    #def __init__   	

    def on_drag_data_received(self, widget, drag_context, x,y, data,info, time):
	    
		self.drop=True
		text = data.get_text()
		text=text.strip().split("//")
		
		text[1]=text[1].replace('%20',' ')
		check=self.commonFunc.check_extension(text[1])
		self.inputpath.set_filename(text[1])
		self.inputpath.set_sensitive(False)

		if check["status"]:
			Gtk.Image.set_from_file(self,settings.DROP_CORRECT)
			
		else:

			Gtk.Image.set_from_file(self,settings.DROP_INCORRECT)
			
		param=[check['status'],check['code'],text[1],self.destpath,self.outputfile_label,self.convert_label,self.convert_button]
	
		self.commonFunc.manage_outputinfo(param)	

	#def on_drag_data_received
	
#class DropArea		