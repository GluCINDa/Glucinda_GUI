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
import sys
import time

from PySide6.QtCore import Signal
from PySide6.QtCore import QThread


class DeleteFilesThread(QThread):
    '''
    This class describes the thread to delete files.
    '''
    signal_finished = Signal(object)


    def __init__(self, path_export, parent=None):
        '''
        Initialization of the DeleteFilesThread class.
        '''
        super().__init__(parent)

        self.path_export = path_export

        return


    def run(self):
        '''
        Run DeleteFilesThread.
        '''
        files = sorted(glob.glob(self.path_export+'**'+os.sep+'*', recursive=True))

        for i,file in enumerate(files):
            fn = file.split(os.sep)[-1]

            # exit if a filetype is not associated with this software
            if os.path.isfile(file):
                if not('.csv' in fn) and not('.txt' in fn) and \
                   not('.html' in fn) and not('.feather' in fn) and \
                   not('.xlsx' in fn):
                    print(file)
                    print(fn)
                    print('ERROR: DeleteFilesThread: run')
                    sys.exit()

        for i,file in enumerate(files):
            if os.path.isfile(file):
                os.unlink(file)
                time.sleep(i*0.0001)

        self.signal_finished.emit(None)

        return
