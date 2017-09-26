from tempfile import mkdtemp
from os import path
from shutil import rmtree
import subprocess

import Core


class NoteshrinkInterface():
	def __init__(self):
		self.core=Core.Core.get_core()
		self.pdfoutput = True
		self.pngoutput = False
		self.pngbasename = "page"
		self.pdfbasename = "output.pdf"
		self.inputfiles = []
	#def init

	def clean_inputfiles(self):
		self.inputfiles = []
		return True
	#def clean_inputfiles

	def check_files(self):
		for f in self.inputfiles:
			if not path.exists(f):
				return False
		return True
	#def check_files

	def process_files(self,output_path):
		if not self.check_files():
			return False
		temp_workspace = mkdtemp()
		cmd = ['noteshrink']
		for inputfile in self.inputfiles:
			cmd.append(inputfile)
		cmd.append("-b")
		if self.pngoutput:
			cmd.append(path.join(output_path, self.pngbasename))
		else:
			cmd.append(path.join(temp_workspace, self.pngbasename))
		cmd.append("-o")
		if self.pdfoutput:
			cmd.append(path.join(output_path, self.pdfbasename))
		else:
			cmd.append(path.join(temp_workspace, self.pdfbasename))
		self.core.dprint(" ".join(cmd))
		subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
		rmtree(temp_workspace)
		return True
	#def process_files
