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

from PySide6.QtCore import Signal
from PySide6.QtCore import QThread

import sys

import cgm_extractor.cgm_extractor


class CGMExtractorThread(QThread):
    '''
    This class describes the thread to run CGM_Extractor.
    '''
    signal_finished = Signal(object)


    def __init__(self, input_path, export_dir, runstate, export_format,
                 parent=None):
        '''
        Initialization of the CGMExtractorThread class.
        '''
        super().__init__(parent)

        self.input_path = input_path
        self.export_dir = export_dir
        self.runstate = runstate
        self.export_format = export_format

        return


    def run(self):
        '''
        Run CGMExtractorThread.
        '''
        exp_csv = ('CSV' in self.export_format)
        exp_feather = ('FEATHER' in self.export_format)

        if ('all' in self.export_format):
            exp_csv = True
            exp_feather = True
        try:
            cgm_extractor.cgm_extractor.run( \
                self.input_path, self.export_dir, \
                exp_csv=exp_csv, \
                exp_feather= exp_feather)
            self.signal_finished.emit(self.export_dir)
        except Exception:
            self.runstate.add_error_message('CGM_Extractor submodule')
            self.signal_finished.emit(self.export_dir)

        return
