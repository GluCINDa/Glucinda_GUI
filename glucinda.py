# This file is part of GluCINDa.
#
# GluCINDa (© 2025 Medical University of Graz. All rights reserved.) is licensed under the
# EUPL v. 1.2.
# You may use, modify, and distribute this software under the terms of the EUPL.
#
# The EUPL is internationally recognized and written in neutral terms which ensures its
# broad applicability. It is not limited to the EU and can be used worldwide as it is
# formulated in such a way that it can be applied in different legal systems. The EUPL is
# also compatible with many other widely used open source licenses. This facilitates the
# integration and use of EUPL-licensed software in international projects.
#
# GluCINDa is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# EUPL and README-file for more details.
#
# You should have received a copy of the EUPL along with GluCINDa. If not, see
# <https://eupl.eu/1.2/en/>.
#
# The software (including all related documentation) shall be used by/communicated in
# compliance with the export control laws in force. In this respect, the use
# by/communication to persons/countries restricted by regulatory authorities (according to the classification/intended use) is strictly prohibited.
#

import glob
import os
import pathlib
import sys
import time
import traceback

from multiprocessing import freeze_support
from PySide6.QtCore import Qt
from PySide6.QtCore import QThread
from PySide6.QtCore import Signal
from PySide6.QtCore import QUrl
from PySide6.QtWidgets import QApplication
from PySide6.QtWidgets import QCheckBox
from PySide6.QtWidgets import QGroupBox
from PySide6.QtWidgets import QLabel
from PySide6.QtWidgets import QLineEdit
from PySide6.QtWidgets import QPushButton
from PySide6.QtWidgets import QTabWidget
from PySide6.QtWidgets import QTextEdit
from PySide6.QtWidgets import QVBoxLayout
from PySide6.QtWidgets import QWidget

try:
    from .lib import storage
    from .lib.installation_check import InstallationCheck
    from .lib.runstate import RunState
except ImportError:  # Standalone execution as script
    from lib import storage
    from lib.installation_check import InstallationCheck
    from lib.runstate import RunState

class GUIWindow(QWidget):
    '''
    This class describes the GUI window of GluCINDa.
    '''

    def __init__(self):
        '''
        Initialization of the GUI window.
        '''
        super().__init__()

        self.runstate = RunState()
        self.tabs = None  # tabs of GUIWindow
        self.tab0 = None
        self.tab1 = None
        self.references_button = None

        if self.check_installation() is False:
            return
        
        self.open()

        return


    def open(self):
        '''
        Open GUI window.
        '''
        from lib.guitab import GUITab

        self.setWindowTitle('GluCINDa')
        self.setGeometry(200, 100, 750, 800)  # dx, dy, width, height
        self.layout = QVBoxLayout(self)


        # create tabs
        self.tabs = QTabWidget()
        self.tab0 = GUITab(0, self.tabs)
        self.tab1 = GUITab(1, self.tabs)
        self.tabs.addTab(self.tab0, 'Simple')
        self.tabs.addTab(self.tab1, 'Advanced')
        self.runstate.set_tabs([self.tab0, self.tab1])
        self.tab0.runstate = self.runstate
        self.tab1.runstate = self.runstate

        tab0_layout = self.tab0.tab()
        self.tab0.setLayout(tab0_layout)

        tab1_layout = self.tab1.tab()
        self.tab1.setLayout(tab1_layout)

        self.layout.addWidget(self.tabs)


        self.space0 = QLabel('')
        self.layout.addWidget(self.space0)


        # add references box
        root_path = str(pathlib.Path(__file__).parent)+os.sep
        reference_file = root_path+'reference.txt'

        if os.path.isfile(reference_file):
            self.references_box(reference_file, self.layout)

        return


    def references_box(self, reference_file, layout):
        '''
        Create and add references box.
        '''
        with open(reference_file, 'r') as f:
            self.references_txt = f.read()

        references_label = QLabel('If you use this software, please cite:')
        layout.addWidget(references_label)

        references_box = QTextEdit(self.references_txt)
        references_box.setReadOnly(True)

        metrics = references_box.fontMetrics()
        height = metrics.lineSpacing()*4
        references_box.setFixedHeight(height)
        layout.addWidget(references_box)

        self.references_button = QPushButton('Copy citation to clipboard')
        self.references_button.clicked.connect(self.references_copy)
        layout.addWidget(self.references_button)

        return


    def references_copy(self):
        '''
        Copy references to clipboard.
        '''
        clipboard = QApplication.clipboard()
        clipboard.setText(self.references_txt)

        return


    def check_installation(self):
        '''
        Check the GluCINDa installation.
        '''
        check = self.runstate.installation_check

        if check.check() is False:
            print(check.message)

            self.setWindowTitle('GluCINDa')
            self.setGeometry(200, 100, 750, 800)  # dx, dy, width, height
            self.layout = QVBoxLayout(self)

            group_box = QGroupBox('GluCINDa installation check')
            group = QVBoxLayout()

            label = QLabel(check.message)
            group.addWidget(label)
            group_box.setLayout(group)

            self.layout.addWidget(group_box)

            return False

        return True


def exception(exception_type, exception_value, traceback_):
    '''
    Handling of general exceptions
    '''
    print('ERROR:')
    traceback.print_exception(exception_type, exception_value, traceback_)
    sys.exit()

    return

def main():
    freeze_support()
    sys.excepthook = exception

    application = QApplication(sys.argv)
    gui = GUIWindow()
    gui.show()
    sys.exit(application.exec())

if __name__ == "__main__":
    main()
