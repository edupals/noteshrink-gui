from tempfile import mkdtemp
from os import path
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

    def process_files(self,output_path):
        if not self.check_files():
            return False
        temp_workspace = mkdtemp()
        cmd = ['noteshrink']
        for inputfile in self.inputfiles:
            cmd.append(inputfile)
        cmd.append("-b")
        if self.pngbasename
            cmd.append(path.join(,self.options['pngbasename']) )
        cmd.append("-o")
        cmd.append(path.join(self.options["workspace"],self.options['pdfbasename']))
        print(" ".join(cmd))
        subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
        return True
    #def process_files
