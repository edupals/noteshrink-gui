import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Pango, GdkPixbuf, Gdk, Gio, GObject,GLib

import copy
import gettext
import Core

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

		v = Gtk.VBox()
		up = Gtk.Button()
		l = Gtk.Label("Up")
		up.add(l)
		down = Gtk.Button()
		l1 = Gtk.Label("Down")
		down.add(l1)
		v.pack_start(up,False,False,0)
		v.pack_start(down,False,False,0)
		v.set_valign(Gtk.Align.CENTER)
		
		hbox.pack_start(miniature,False,False,0)
		hbox.pack_start(label,False,False,0)
		hbox.pack_end(b,False,False,10)
		hbox.pack_end(v,False,False,10)
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
