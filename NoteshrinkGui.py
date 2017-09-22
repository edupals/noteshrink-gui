#!/usr/bin/env python

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Pango, GdkPixbuf, Gdk, Gio, GObject,GLib

import signal
import os
import sys
import Core

import settings

signal.signal(signal.SIGINT, signal.SIG_DFL)



class NoteshrinkGui:
	
	def __init__(self):

		self.core=Core.Core.get_core()

	#def init

	def load_gui(self):
		
		builder = Gtk.Builder()
		builder.add_from_file(settings.UI_FILE)
		
		self.main_window=builder.get_object("main_window")
		self.main_window.set_title(settings.WINDOW_TITLE)
		self.main_box=builder.get_object("main_box")
		self.exit_button=builder.get_object("exit_button")
		
		self.convert_box=self.core.convert_box
		self.main_box.add(self.convert_box)

		# Add components
			
		self.set_css_info()
		self.connect_signals()
		
		self.main_window.show_all()
		
	#def load_gui

	def set_css_info(self):
		
		self.style_provider=Gtk.CssProvider()
		f=Gio.File.new_for_path(settings.CSS_FILE)
		self.style_provider.load_from_file(f)
		Gtk.StyleContext.add_provider_for_screen(Gdk.Screen.get_default(),self.style_provider,Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
		self.main_window.set_name("WINDOW")
						
	#def set_css_info					
			
	def connect_signals(self):
		
		self.main_window.connect("destroy",self.quit)
		self.exit_button.connect("clicked",self.quit)
			
	#def connect_signals

	def quit(self,widget):

		Gtk.main_quit()	
	
	#def quit

	def start_gui(self):
		
		GObject.threads_init()
		Gtk.main()
		
	#def start_gui


	
#class NoteshrinkGui


if __name__=="__main__":
	
	lap=NoteshrinkGui()
	lap.start_gui()
	
