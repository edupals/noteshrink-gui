#
# Regular cron jobs for the noteshrink-gui package
#
0 4	* * *	root	[ -x /usr/bin/noteshrink-gui_maintenance ] && /usr/bin/noteshrink-gui_maintenance
