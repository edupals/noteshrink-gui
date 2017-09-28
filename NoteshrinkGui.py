
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
		self.viewport = builder.get_object("listfiles_vp")

		# Toolbar widgets
		self.add_file = builder.get_object("addfile_button")
		self.add_folder = builder.get_object("addfolder_button")
		self.apply = builder.get_object("apply_button")
		self.apply1 = builder.get_object("apply_button1")

		# Options widgets
		self.output_png = builder.get_object("png_cb")
		self.output_pdf = builder.get_object("pdf_cb")
		self.output_path = builder.get_object("outputfolder_input")
		
		self.convert_box = self.core.convert_box
		self.viewport.add(self.convert_box)

		# Add components
		self.set_default_values()
		self.set_css_info()
		self.connect_signals()
		
		self.main_window.show_all()
		
	#def load_gui

	def set_default_values(self):
		self.main_window.set_title(settings.WINDOW_TITLE)
		self.main_window.set_default_size(900,400)
		self.output_png.set_active(self.core.noteshrink_interface.pngoutput)
		self.output_pdf.set_active(self.core.noteshrink_interface.pdfoutput)
		self.output_path.set_filename(GLib.get_user_special_dir(GLib.USER_DIRECTORY_DOCUMENTS))
	#def set_default_values


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
		self.apply1.connect("clicked", self.convert_files)
		self.add_file.connect("clicked", self.open_files_selector)
		self.add_folder.connect("clicked", self.open_folder_selector)
		self.output_pdf.connect("toggled",self.toggle_pdf_output)
		self.output_png.connect("toggled",self.toggle_png_output)
	#def connect_signals

	def toggle_pdf_output(self,widget):
		self.core.noteshrink_interface.pdfoutput = not self.core.noteshrink_interface.pdfoutput
	#def toggle_pdf_output

	def toggle_png_output(self,widget):
		self.core.noteshrink_interface.pngoutput = not self.core.noteshrink_interface.pngoutput
	#def toggle_png_output

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
			files = dialog.get_filenames()
			self.core.noteshrink_interface.inputfiles.extend(files)
			for x in files:
				self.convert_box.new_file(x)
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
		for x in self.convert_box.get_children():
			if type(x) == type(Gtk.HBox()):
				print(x)
		# self.core.noteshrink_interface.process_files(self.output_path.get_filename())
	#def convert_files

	def add_folder_filters(self,widget):
		filter_folder = Gtk.FileFilter()
		filter_folder.set_name("Only folders")
		filter_folder.add_mime_type("inode/directory")
		widget.add_filter(filter_folder)
	#def add_folder_filters
	
#class NoteshrinkGui
