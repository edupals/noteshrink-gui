
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Pango, GdkPixbuf, Gdk, Gio, GObject,GLib

import signal
import os
import sys
import threading
import gettext

import Core

import settings

signal.signal(signal.SIGINT, signal.SIG_DFL)
gettext.textdomain("noteshrink-gui")
_ = gettext.gettext

class NoteshrinkGui:

	def __init__(self):

		self.core=Core.Core.get_core()

	#def init

	def load_gui(self):
		
		builder = Gtk.Builder()
		builder.set_translation_domain('noteshrink-gui')
		builder.add_from_file(settings.UI_FILE)
		
		self.main_window = builder.get_object("main_window")
		self.viewport = builder.get_object("listfiles_vp")

		# Toolbar widgets
		self.add_file = builder.get_object("addfile_button")
		self.add_folder = builder.get_object("addfolder_button")
		self.apply = builder.get_object("apply_button")
		self.apply1 = builder.get_object("apply_button1")
		self.box4 = builder.get_object("box4")

		# Options widgets
		self.png_output = builder.get_object("png_cb")
		self.pdf_format = builder.get_object("pdf_cl")
		self.pdf_output = builder.get_object("pdf_cb")
		self.output_path = builder.get_object("outputfolder_input")
		
		self.convert_box = self.core.convert_box
		self.viewport.add(self.convert_box)

		self.progressbar = builder.get_object("progressbar")
		# Add components
		self.set_default_values()
		self.set_css_info()
		self.connect_signals()
		
		self.main_window.show_all()
		
	#def load_gui

	def set_default_values(self):
		self.main_window.set_title(settings.WINDOW_TITLE)
		self.main_window.set_default_size(900,550)
		self.png_output.set_active(self.core.noteshrink_interface.pngoutput)
		self.pdf_output.set_active(self.core.noteshrink_interface.pdfoutput)
		self.pdf_format.set_active(0)
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
		self.png_output.connect("toggled",self.toggle_png_output)
		self.pdf_output.connect("toggled",self.toggle_pdf_output)
		self.pdf_format.connect("changed",self.changed_pdf_format)
	#def connect_signals

	def toggle_pdf_output(self,widget):
		self.core.noteshrink_interface.pdfoutput = not self.core.noteshrink_interface.pdfoutput
	#def toggle_pdf_output

	def toggle_png_output(self,widget):
		self.core.noteshrink_interface.pngoutput = not self.core.noteshrink_interface.pngoutput
	#def toggle_png_output

	def changed_pdf_format(self,widget):
		option = self.pdf_format.get_active_id()
		self.core.noteshrink_interface.pdfmulti = False if option == "single" else True
	#def changed_pdf_format

	def quit(self, widget):
		Gtk.main_quit()	
	#def quit

	def start_gui(self):
		GObject.threads_init()
		Gtk.main()
	#def start_gui

	def open_files_selector(self,widget):
		dialog = Gtk.FileChooserDialog(_("Please choose a file"), self.main_window,
										Gtk.FileChooserAction.OPEN,
										(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
			 							Gtk.STOCK_OPEN, Gtk.ResponseType.OK))
		dialog.set_select_multiple(True)
		response = dialog.run()
		if response == Gtk.ResponseType.OK:
			self.core.dprint("Open clicked")
			files = dialog.get_filenames()
			for x in files:
				self.convert_box.new_file(x)
			dialog.close()
		elif response == Gtk.ResponseType.CANCEL:
			dialog.close()

	#def open_files_selector

	def open_folder_selector(self,widget):
		dialog = Gtk.FileChooserDialog(_("Please choose a folder"), self.main_window,
			Gtk.FileChooserAction.SELECT_FOLDER,
			(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
			 Gtk.STOCK_OPEN, Gtk.ResponseType.OK))
		self.add_folder_filters(dialog)
		response = dialog.run()
		if response == Gtk.ResponseType.OK:
			self.core.dprint("Open Folder clicked")
			self.include_folder(dialog.get_filename())
			dialog.close()
		elif response == Gtk.ResponseType.CANCEL:
			dialog.close()
	#def open_folder_selector

	def convert_files(self,widget):

		self.core.dprint("Click convert files")
		self.apply1.set_sensitive(False)
		self.box4.set_sensitive(False)
		t = threading.Thread(target=self.execute_command)
		t.daemon = True
		t.start()
		GLib.timeout_add(200,self.convert_listener,t)
	#def convert_files

	def execute_command(self):
		self.core.noteshrink_interface.clean_inputfiles()
		for x in self.convert_box.get_children():
			if type(x) == type(Gtk.HBox()):
				self.core.noteshrink_interface.inputfiles.append(x.file_path)
		self.core.noteshrink_interface.process_files(self.output_path.get_filename())


	def convert_listener(self,t):
		self.progressbar.pulse()
		thread_status = t.is_alive()
		if not thread_status:
			self.progressbar.set_fraction(1.0)
			self.apply.set_sensitive(True)
			self.apply1.set_sensitive(True)
			self.box4.set_sensitive(True)
		return thread_status


	def add_folder_filters(self,widget):
		filter_folder = Gtk.FileFilter()
		filter_folder.set_name("Only folders")
		filter_folder.add_mime_type("inode/directory")
		widget.add_filter(filter_folder)
	#def add_folder_filters
	
	def include_folder(self,path):
		for root, dirs, files in os.walk(path):
			for x in files:
				self.convert_box.new_file(os.path.join(root,x))

#class NoteshrinkGui
