
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
		
		self.main_window = builder.get_object("main_window")
		self.main_window.set_title(settings.WINDOW_TITLE)
		self.main_box = builder.get_object("main_box")
		self.add_file = builder.get_object("addfile_button")
		self.add_folder = builder.get_object("addfolder_button")
		self.apply = builder.get_object("apply_button")
		
		# self.convert_box=self.core.convert_box
		# self.main_box.add(self.convert_box)

		# Add components
			
		self.set_css_info()
		self.connect_signals()
		
		self.main_window.show_all()
		
	#def load_gui

	def set_css_info(self):
		self.style_provider = Gtk.CssProvider()
		f = Gio.File.new_for_path(settings.CSS_FILE)
		self.style_provider.load_from_file(f)
		Gtk.StyleContext.add_provider_for_screen(Gdk.Screen.get_default(),
									self.style_provider,
									Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
	#def set_css_info					
			
	def connect_signals(self):
		self.main_window.connect("destroy", self.quit)
		self.apply.connect("clicked", self.convert_files)
		self.add_file.connect("clicked", self.open_files_selector)
		self.add_folder.connect("clicked", self.open_folder_selector)
	#def connect_signals

	def quit(self, widget):
		Gtk.main_quit()	
	#def quit

	def start_gui(self):
		GObject.threads_init()
		Gtk.main()
	#def start_gui

	def open_files_selector(self,widget):
		dialog = Gtk.FileChooserDialog("Please choose a file", self.main_window,
			Gtk.FileChooserAction.OPEN,
			(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
			 Gtk.STOCK_OPEN, Gtk.ResponseType.OK))
		dialog.set_select_multiple(True)
		response = dialog.run()
		if response == Gtk.ResponseType.OK:
			print("Open clicked")
			self.core.noteshrink_interface.inputfiles.extend(dialog.get_filenames())
			dialog.close()
		elif response == Gtk.ResponseType.CANCEL:
			dialog.close()

	#def open_files_selector

	def open_folder_selector(self,widget):
		dialog = Gtk.FileChooserDialog("Please choose a dolder", self.main_window,
			Gtk.FileChooserAction.SELECT_FOLDER,
			(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
			 Gtk.STOCK_OPEN, Gtk.ResponseType.OK))
		self.add_folder_filters(dialog)
		response = dialog.run()
		if response == Gtk.ResponseType.OK:
			print("Open clicked")
			print("File selected: " + dialog.get_filename())
			dialog.close()
		elif response == Gtk.ResponseType.CANCEL:
			dialog.close()
	#def open_folder_selector

	def convert_files(self,widget):
		self.core.dprint("Click convert files")
		#self.core.noteshrink_interface.process_files()
	#def convert_files

	def add_folder_filters(self,widget):
		filter_folder = Gtk.FileFilter()
		filter_folder.set_name("Only folders")
		filter_folder.add_mime_type("inode/directory")
		widget.add_filter(filter_folder)
	#def add_folder_filters
	
#class NoteshrinkGui
