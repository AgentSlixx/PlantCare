import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ui.ui_main import ui_run

while 1 != 2:
    ui_run()