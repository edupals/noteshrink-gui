#!/usr/bin/env python3
from setuptools import setup
from edupals.i18n import poinstaller
import sys


if __name__ == '__main__':

	pinstaller = poinstaller.PoInstaller('translations','noteshrink-gui','')
	pinstaller.build()
	polist = pinstaller.setup_install()
	setup(name='noteshrink-gui',
		version='0.1',
		description='Graphic user interface for noteshrink',
		long_description="""""",
		author='Lliurex Team',
		author_email='raurodse@gmail.com',
		maintainer='Raul Rodrigo Segura',
		maintainer_email='raurodse@gmail.com',
		keywords=['software',''],
		url='https://github.com/edupals/noteshrink-gui',
		license='GPL',
		platforms='UNIX',
#        scripts = [''],
		packages = ['noteshrinkgui'],
		package_dir = {'noteshrinkgui':'app'},
		package_data = {'noteshrinkgui':['rsrc/*']},
		data_files = [('share/applications',['noteshrink-gui.desktop']),('share/icons/hicolor/scalable/apps',['noteshrink.svg'])] + polist ,
		scripts = ['noteshrink-gui'],
		classifiers=[
				'Environment :: Console',
				'Intended Audience :: End Users',
				'License :: OSI Approved :: GNU General Public License v3',
				'Operating System :: POSIX',
				'Programming Language :: Python',
				],
	)
	pinstaller.clean()
