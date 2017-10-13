import sys
import os

relative_path = os.path.dirname(sys.modules[__name__].__file__)

RSRC = os.path.join(relative_path,'rsrc')
CSS_FILE = os.path.join(RSRC,'noteshrink-gui.css')
UI_FILE = os.path.join(RSRC,"noteshrink.ui")
WINDOW_TITLE = "Noteshrink"

# IMAGES
DROP_FILE = os.path.join(RSRC,"rsrc/drop_file.png")
DROP_CORRECT = os.path.join(RSRC,"rsrc/drop_file_correct.png")
DROP_INCORRECT = os.path.join(RSRC,"rsrc/drop_file_incorrect.png")


TEXT_DOMAIN = "noteshrink"
