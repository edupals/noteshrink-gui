from tempfile import mkdtemp
from os import path 
from shutil import rmtree, move
import subprocess

import Core


class NoteshrinkInterface():
	def __init__(self):
		self.core=Core.Core.get_core()
		self.pdfoutput = True
		self.pngoutput = False
		self.pdfmulti = False
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
		destbasepng = path.join(temp_workspace, self.pngbasename)
		if self.pdfoutput and self.pdfmulti:
			for x in self.inputfiles:
				filename_wihout_extension = path.basename(path.splitext(x)[0])

				validpdf = self.get_valid_name(path.join(output_path, filename_wihout_extension + '.pdf' ))
				cmd = ['noteshrink', '-o', '{}'.format(validpdf),'-b', destbasepng, x]
				subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
				if self.pngoutput:
					self.safe_move(destbasepng + "0000.png",path.join(output_path,filename_wihout_extension + '.png'))
		else:
			cmd = ['noteshrink','-K','-b',destbasepng,'-o']
			if self.pdfoutput:
				cmd.append(self.get_valid_name(path.join(output_path, self.pdfbasename)))
			else:
				cmd.append(path.join(temp_workspace, self.pdfbasename))

			for inputfile in self.inputfiles:
				cmd.append('{}'.format(inputfile))
			cosa = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
			if self.pngoutput:
				for i in range(0,len(self.inputfiles)):
					filename_wihout_extension = path.basename(path.splitext(self.inputfiles[i])[0])
					self.safe_move(destbasepng + "{:04d}.png".format(i), path.join(output_path,filename_wihout_extension + '.png'))

		rmtree(temp_workspace)
		return True
	#def process_files

	def get_valid_name(self, absname):
		(path_without_extension, extension) = path.splitext(absname)
		aux_decorator = ""
		while True:
			if not path.exists(path_without_extension + aux_decorator + extension):
				break
			if aux_decorator == "":
				aux_decorator = "1"
			else:
				aux_decorator = str(int(aux_decorator) + 1)
		return path_without_extension + aux_decorator + extension
	#def get_valid_name

	def safe_move(self,orig,dest):
		valid_name = self.get_valid_name(dest)
		move(orig,valid_name)
	#def safe_move