#!/usr/bin/env python
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
