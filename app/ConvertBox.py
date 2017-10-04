import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Pango, GdkPixbuf, Gdk, Gio, GObject,GLib

import gettext
import Core
from urllib.parse import unquote
import magic

import threading
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
		self.mime = magic.open(magic.MAGIC_MIME)
		self.mime.load()
		self.set_name("convertbox")

	def set_background(self):
		self.background_img = Gtk.Image.new_from_file(join(settings.RSRC,"drag_and_drop.svg"))
		self.background_img.set_halign(Gtk.Align.CENTER)
		self.background_img.set_valign(Gtk.Align.CENTER)
		self.background_img.show()
		self.set_homogeneous(True)
		self.pack_start(self.background_img,False,False,0)
		self.queue_draw()

	def new_file(self,pkg_name):
		if self.mime.file(pkg_name).find("image/") != 0 :
			return 

		if self.background_img:
			self.set_homogeneous(False)
			self.background_img.hide()
		hbox = Gtk.HBox()
		hbox.set_margin_left(10)
		hbox.set_margin_right(10)
		contexto = hbox.get_style_context()
		contexto.add_class("styledboxes")

		pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(pkg_name,100,100,True)
		miniature = Gtk.Image.new_from_pixbuf(pixbuf)
		miniature.set_size_request(100,100)
		miniature.set_margin_top(4)
		miniature.set_margin_bottom(4)
		label = Gtk.Label(pkg_name)
		b = Gtk.Button()
		i = Gtk.Image.new_from_stock("gtk-delete",Gtk.IconSize.MENU)
		b.add(i)
		b.set_halign(Gtk.Align.CENTER)
		b.set_valign(Gtk.Align.CENTER)
		b.get_style_context().add_class('deletebutton')
		b.connect("clicked",self.delete_file,hbox)

		v = Gtk.VBox()
		up = Gtk.Button()
		l = Gtk.Image.new_from_stock("gtk-go-up",Gtk.IconSize.MENU)
		up.add(l)
		down = Gtk.Button()
		l1 = Gtk.Image.new_from_stock("gtk-go-down",Gtk.IconSize.MENU)
		down.add(l1)
		up.connect('clicked', self.move_element, hbox, -1)
		down.connect('clicked', self.move_element, hbox, 1)
		up.get_style_context().add_class("orderbutton")
		down.get_style_context().add_class("orderbutton")
		up.set_margin_left(5)
		up.set_margin_right(3)
		down.set_margin_left(5)
		down.set_margin_right(3)

		v.pack_start(up,False,False,0)
		v.pack_start(down,False,False,0)
		v.set_valign(Gtk.Align.CENTER)
		
		hbox.pack_start(v,False,False,0)
		hbox.pack_start(miniature,False,False,0)
		hbox.pack_start(label,False,False,0)
		hbox.pack_end(b,False,False,10)
		hbox.show_all()
		hbox.file_path = pkg_name
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
				x = bytes(unquote(x),"utf-8").decode('utf8')
				files.append(x.replace('file://',''))
		for x in files:
			if self.mime.file(x).find('inode/directory') == 0:
				self.core.noteshrink_gui.include_folder(x)
			else:
				self.new_file(x)
	#def drag_files

	def delete_file(self, widget, container):
		self.remove(container)
		if len(self.get_children()) == 1:
			self.set_homogeneous(True)
			self.background_img.show()
	#def delete_file

	def move_element(self,widget, container, position_modifier):
		position = self.child_get_property(container,'position')
		new_position = position + position_modifier if position + position_modifier != 0 else position
		self.reorder_child(container, new_position )
	#def move_element