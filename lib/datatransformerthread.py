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

import os
import pathlib
import sys


class DataTransformerThread(QThread):
    '''
    This class describes the thread to run the data_transformer.
    '''
    signal_finished = Signal(object)


    def __init__(self, runstate, export_format=['all'], parent=None):
        '''
        Initialization of the DataTransformerThread class.
        '''
        super().__init__(parent)

        self.runstate = runstate
        self.input_dir = self.runstate.export_dir.get_path()
        self.export_dir = self.input_dir
        self.export_format = export_format

        self.progress_var = self.runstate.parser_progress_var

        return


    def run(self):
        '''
        Run DataTransformerThread.
        '''
        data_transformer_available = self.check()

        if data_transformer_available:
            try:
                from data_transformer.data_transformer import DataTransformer

                data_transformer_ = DataTransformer(
                    self.input_dir, self.export_dir,
                    self.export_format,
                    self.progress_var,
                    self.runstate.conf)
                transformed_dir = data_transformer_.run()
                self.signal_finished.emit(transformed_dir)
            except Exception as e:
                self.runstate.add_error_message(
                    'DataTransformerThread submodule: '+str(e))
                self.signal_finished.emit('')

        else:
                self.signal_finished.emit('')

        return


    def check(self):
        '''
        Check presence of data_transformer.
        '''
        root_path = str(pathlib.Path(__file__).parent.parent)+os.sep

        if os.path.exists(root_path+'data_transformer/'):

            return True

        return False
