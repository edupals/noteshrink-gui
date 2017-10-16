#!/usr/bin/env python
#
# $Id: setup.py,v 1.32 2010/10/17 15:47:21 ghantoos Exp $
#
#    Copyright (C) 2008-2009  Ignace Mouzannar (ghantoos) <ghantoos@ghantoos.org>
#
#    This file is part of lshell
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

from setuptools import setup
from distutils.command.build import build
import polib
import os
import shutil

package = 'noteshrinkgui'
po_folder = 'translations'
temp_mo_folder = 'build/.mo_folder'
dst_tmpl = "share/locale/{}/LC_MESSAGES/"
mo_tmpl = "build/.mo_folder/{}/{}.mo"

class Buildi18n(build):
	def run(self,*args):
		build.run(self,*args)
		self.make_mo()
	
	def make_mo(self):
		if os.path.exists(temp_mo_folder):
			shutil.rmtree(temp_mo_folder)
		os.makedirs(temp_mo_folder)
		for x in lang_list():
			aux_file = polib.pofile(os.path.join(po_folder,x + ".po"))
			aux_path = os.path.join(temp_mo_folder, x)
			os.makedirs(aux_path)
			aux_file.save_as_mofile(os.path.join(aux_path, package + ".mo"))

def lang_list():
	return [ x[:-3] for x in os.listdir(po_folder) if x[-3:] == ".po" ]

def polist():
	polist = []
	for lang in lang_list():
		polist.append( (dst_tmpl.format(lang),[ mo_tmpl.format(lang,package) ] ))
	return polist

if __name__ == '__main__':

	setup(name='noteshrink-gui',
		version='0.1',
		description='Graphic user interface for noteshrink',
		long_description="""""",
		author='Lliurex Team',
		author_email='raurodse@gmail.com',
		maintainer='Raul Rodrigo Segura',
		maintainer_email='raurodse@gmail.com',
		keywords=['software',''],
		url='https://github.com/lliurex/noteshrink',
		license='GPL',
		platforms='UNIX',
#        scripts = [''],
		packages = ['noteshrinkgui'],
		package_dir = {'noteshrinkgui':'app'},
		package_data = {'noteshrinkgui':['rsrc/*']},
		data_files = [('share/applications',['noteshrink-gui.desktop']),('share/icons/hicolor/scalable/apps',['noteshrink.svg'])] + polist() ,
		scripts = ['noteshrink-gui'],
		classifiers=[
				'Environment :: Console',
				'Intended Audience :: End Users',
				'License :: OSI Approved :: GNU General Public License v3',
				'Operating System :: POSIX',
				'Programming Language :: Python',
				],
		cmdclass = {
			'build':Buildi18n
		}
	)
