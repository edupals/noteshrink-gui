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
from os.path import splitext

import settings

gettext.textdomain(settings.TEXT_DOMAIN)
_ = gettext.gettext


class ConvertBox(Gtk.VBox):
	def __init__(self):
		Gtk.VBox.__init__(self)
		self.core=Core.Core.get_core()

		builder = Gtk.Builder()
		builder.set_translation_domain(settings.TEXT_DOMAIN)
		builder.add_from_file(settings.UI_FILE)
		self.addfile = builder.get_object("addfile_button")
		self.addfolder = builder.get_object("addfolder_button")
		self.apply = builder.get_object("apply_button")
		self.pngoutput_flag = builder.get_object("png_cb")
		self.pdfoutput_flag = builder.get_object("pdf_cb")
		self.output_folder = builder.get_object("outputfolder_input")

		#self.connect_signals()
		#self.set_css_info()
		GObject.threads_init()

	def connect_signals(self):
		self.apply.connect("clicked",self.convert_files)

	def set_css_info(self):
		self.style_provider=Gtk.CssProvider()

		f=Gio.File.new_for_path(settings.CSS_FILE)
		self.style_provider.load_from_file(f)

		Gtk.StyleContext.add_provider_for_screen(Gdk.Screen.get_default(),self.style_provider,Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
		self.drop_label.set_name("OPTION_LABEL")
		self.inputfile_label.set_name("OPTION_LABEL")
		self.outputpath_label.set_name("OPTION_LABEL")
		self.outputfile_label.set_name("OUTPUT_LABEL")
		self.check_label.set_name("MSG_LABEL")

	def convert_files(self):
		print(self.output_folder)
		self.core.noteshrink_interface.process_files()


	def new_package_button(self,pkg_name):
		
		hbox=Gtk.HBox()
		label=Gtk.Label(pkg_name)
		b=Gtk.Button()
		i=Gtk.Image.new_from_file("trash.svg")
		b.add(i)
		b.set_halign(Gtk.Align.CENTER)
		b.set_valign(Gtk.Align.CENTER)
		b.set_name("DELETE_ITEM_BUTTON")
		b.connect("clicked",self.delete_package_clicked,hbox)
		hbox.pack_start(label,False,False,0)
		hbox.pack_end(b,False,False,10)
		hbox.show_all()
		label.set_margin_right(20)
		label.set_margin_left(20)
		label.set_margin_top(20)
		label.set_margin_bottom(20)
		hbox.set_name("PKG_BOX")
		self.package_list_box.pack_start(hbox,False,False,5)
		self.package_list_box.queue_draw()
		hbox.queue_draw()
 		
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