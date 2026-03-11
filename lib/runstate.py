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
import yaml

import lib.filesystem
from lib.export_dir_gui_state import ExportDirGUIState
from lib.input_dir_gui_state import InputDirGUIState
from lib.installation_check import InstallationCheck
from lib.export_dir_status import ExportDirStatus
from lib.import_button_state import ImportButtonState
from lib.input_dir_status import InputDirStatus
from lib.start_requirements import StartRequirements


class RunState():
    '''
    This class describes the current state of the running application.
    '''

    def __init__(self):
        '''
        Initialization of the RunState class.
        '''
        self.installation_check = InstallationCheck()


        # directories
        # ~~~~~~~~~~~
        self.installation_dir = lib.filesystem.clean_path( \
            os.path.dirname(os.path.realpath(__file__))+os.sep+'..'+os.sep)
        self.input_dir = InputDirStatus()
            # import directory containing CGM data files
        self.export_dir = ExportDirStatus(self)
            # export directory


        self.conf = {}
        self.read_conf()

        self.generalparser_thread = None  # GeneralparserThread object
        self.datatransformer_thread = None  # DataTransformerThread object
        self.cgmextractor_thread = None  # CGMExtractorThread object
        self.export_files_cleanup = None  # ExportFilesCleanup object

        self.tabs = None
        self.input_dir_gui_state = InputDirGUIState(self)
        self.export_dir_gui_state = ExportDirGUIState(self)
        self.import_button = ImportButtonState(self)
        self.error_messages = []
        self.error_messages_formatted_str = ''
        self.parser_progress_var = [None, None]

        self.stage = -1
            # run stage:
            # -1: not running, conditions for start not fulfilled
            #  0: not running, ready to start (conditions for start fulfilled)
            #  1: running
            #  2: running, started: preparation of directory structure
            #  3: running, finished: preparation of directory structure
            #  4: running, started: generalparser thread
            #  5: running, finished: generalparser thread
            #  6: running, started: data_transformer thread
            #  7: running, finished: data_transformer thread
            #  8: running, started: cgmextractor_thread thread
            #  9: running, finished: cgmextractor_thread thread
            # 10: running, started: export_files_cleanup
            # 11: running, finished: export_files_cleanup

        self.runs_started_n = 0
        self.start_requirements = StartRequirements(self)

        return


    def set_tabs(self, tabs):
        '''
        Set tabs (GUITab objects).
        '''
        self.tabs = tabs

        return


    def change_stage(self, stage):
        '''
        Change run stage.
        '''
        # checks
        if stage not in range(-1, 12) or self.stage not in range(-1, 12):
            raise Exception(
                'RunState: change_stage: stage: '+str(self.stage)+
                ', new stage: '+str(stage))

        if stage == self.stage:
            return

        elif 1 <= self.stage <= 10:
            if stage != self.stage+1:
                raise Exception(
                    'RunState: change_stage: stage: '+str(self.stage)+
                    ', new stage: '+str(stage))
        elif self.stage in (-1, 0):
            if abs(stage-self.stage) != 1:
                raise Exception(
                    'RunState: change_stage: stage: '+str(self.stage)+
                    ', new stage: '+str(stage))
        elif self.stage == 11:
            if stage not in (-1, 0):
                raise Exception(
                    'RunState: change_stage: stage: '+str(self.stage)+
                    ', new stage: '+str(stage))

        self.stage = stage

        if stage == 1:
            self.runs_started_n += 1

        return


    def check_stage(self, stage):
        '''
        Check run stage.
        '''
        if stage != self.stage:
            raise Exception(
                'RunState: check_stage: stage: '+str(self.stage)+
                ', required stage: '+str(stage))

        return


    def set_input_dir(self, input_dir, tab_id):
        '''
        Set new input dir and update the tab GUIs (GUITab objects).
        '''
        self.input_dir.set_path(input_dir)
        self.input_dir_gui_state.update_input_dir_gui_dependencies(input_dir)

        for i,tab in enumerate(self.tabs):
            tab.set_input_dir(input_dir)

        return


    def set_export_dir(self, export_dir, tab_id):
        '''
        Set new export dir and update the tab GUIs (GUITab objects).
        '''
        self.export_dir.set_path(export_dir)
        self.start_requirements.update()

        for i,tab in enumerate(self.tabs):
            tab.set_export_dir()

        return


    def set_import_button_state(self, state, text=''):
        '''
        Set new import button state and update the tab GUIs (GUITab objects).
        '''
        for i,tab in enumerate(self.tabs):
            self.import_button.set_state(tab.button_import, state, text)

        return


    def add_error_message(self, error_message):
        '''
        Add error message.
        '''
        self.error_messages.append('ERROR: '+error_message)
        self.all_error_messages_formatted()

        return


    def all_error_messages_formatted(self):
        '''
        Get all error messages combined and formatted.
        '''
        error_messages_str = '<span style="color: red;">'

        for i,error_message in enumerate(self.error_messages):
            if i > 0:
                error_messages_str += ' &nbsp; '

            error_messages_str += error_message

        error_messages_str += '</span>'
        self.error_messages_formatted_str = error_messages_str

        return error_messages_str


    def read_conf(self):
        '''
        Read config files.
        '''
        config_files = \
            sorted(glob.glob(self.installation_dir+'conf'+os.sep+'*.yaml'))

        for f in config_files:
            with open(f, 'r') as file:
                conf = yaml.safe_load(file)
                fn = f.split(os.sep)[-1]

                if fn == 'conf.yaml':
                    self.conf['conf'] = conf

        return


    def set_generalparser_thread(self, generalparser_thread):
        '''
        Set GeneralparserThread.
        '''
        from lib.generalparserthread import GeneralparserThread

        # check
        if not isinstance(generalparser_thread, GeneralparserThread):
            raise Exception('RunState: set_generalparser_thread')

        self.generalparser_thread = generalparser_thread
        self.generalparser_thread.setObjectName('GeneralparserThread')

        return


    def set_datatransformer_thread(self, datatransformer_thread):
        '''
        Set DataTransformerThread.
        '''
        from lib.datatransformerthread import DataTransformerThread

        # check
        if not isinstance(datatransformer_thread, DataTransformerThread):
            raise Exception('RunState: set_datatransformer_thread')

        self.datatransformer_thread = datatransformer_thread
        self.datatransformer_thread.setObjectName('DataTransformerThread')

        return


    def set_cgmextractor_thread(self, cgmextractor_thread):
        '''
        Set CGMExtractorThread.
        '''
        from lib.cgmextractorthread import CGMExtractorThread

        # check
        if not isinstance(cgmextractor_thread, CGMExtractorThread):
            raise Exception('RunState: set_cgmextractor_thread')

        self.cgmextractor_thread = cgmextractor_thread
        self.cgmextractor_thread.setObjectName('CGMExtractorThread')

        return


    def set_export_files_cleanup(self, export_files_cleanup):
        '''
        Set ExportFilesCleanup.
        '''
        from lib.export_files_cleanup import ExportFilesCleanup

        # check
        if not isinstance(export_files_cleanup, ExportFilesCleanup):
            raise Exception('RunState: set_export_files_cleanup')

        self.export_files_cleanup = export_files_cleanup

        return
