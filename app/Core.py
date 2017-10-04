#!/usr/bin/env python

from NoteshrinkGui import NoteshrinkGui
from ConvertBox import ConvertBox
from NoteshrinkInterface import NoteshrinkInterface


class Core:
	
	singleton=None
	DEBUG=True
	
	@classmethod
	def get_core(self):
		
		if Core.singleton==None:
			Core.singleton=Core()
			Core.singleton.init()

		return Core.singleton
		
	
	def __init__(self,args=None):
		
		self.dprint("Init...")
		
	#def __init__
	
	def init(self):
		
		self.dprint("Creating ConvertBox...")
		self.convert_box = ConvertBox()

		self.dprint("Creating NoteshrinInterface...")
		self.noteshrink_interface = NoteshrinkInterface()
		
		
		# Main window must be the last one
		self.dprint("Creating NoteshrinGui...")
		self.noteshrink_gui = NoteshrinkGui()
		
		self.noteshrink_gui.load_gui()
		self.noteshrink_gui.start_gui()
		
		
	#def init
	
	
	
	def dprint(self,msg):
		
		if Core.DEBUG:
			
			print("[CORE] %s"%msg)
	
	#def  dprint