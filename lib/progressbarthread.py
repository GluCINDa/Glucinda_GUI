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

import lib.storage

import time

from PySide6.QtCore import QThread
from PySide6.QtCore import Signal


class ProgressBarThread(QThread):
    '''
    This class describes the progress bar.
    '''
    progress_bar_set = Signal(int)
    label_set = Signal(str)


    def __init__(self, runstate, progress_bar, files_all_n, export_dir,
                 label, tab):
        '''
        Initialization of the ProgressBarThread class.
        '''
        super().__init__()

        self.runstate = runstate
        self.progress_bar = progress_bar
        self.files_all_n = files_all_n
        self.export_dir = export_dir
        self.label = label
        self.tab = tab

        return


    def run(self):
        '''
        Run ProgressBarThread.
        '''
        time.sleep(1) # avoid timing issue
        self.progress_bar_set.emit(1)

        while self.tab.progress_bar_hold is True:
            if self.isInterruptionRequested():
                return

            time.sleep(1)


        time0 = time.time()
        dt = 0.1

        for i in range(0, self.files_all_n*10000):
            if self.isInterruptionRequested():
                return

            if self.tab.progress_bar_hold is False:
                self.progress_bar_set.emit(round( \
                    self.runstate.parser_progress_var[1]/ \
                    self.files_all_n*1000))

                processed_n = self.runstate.parser_progress_var[1]
                if processed_n is None:
                    processed_n = 0

                if len(self.tab.runstate.error_messages) == 0:
                    self.label_set.emit(
                        'Parsing ('+str(processed_n)+' / '+
                        str(self.files_all_n)+' files done)')
                else:
                    self.label_set.emit(
                        'Parsing ('+str(processed_n)+' / '+
                        str(self.files_all_n)+' files done)'+
                        '<br />'+
                        self.tab.runstate.error_messages_formatted_str)

            if self.runstate.parser_progress_var[1] >= self.files_all_n:
                return

            time1 = time.time()

            if time1-time0 > 1:
                dt = 0.2
            elif time1-time0 > 5:
                dt = 0.5
            elif time1-time0 > 60:
                dt = 1
            elif time1-time0 > 600:
                dt = 2

            time.sleep(dt)

        return


    def stop(self):
        '''
        Stop ProgressBarThread.
        '''
        self.requestInterruption()

        return
