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

import os

from lib.contentcollectorthread import ContentCollectorThread


class InputDirGUIState():
    '''
    This class describes the current state of the GUI section responsible
    for setting the input directory.
    '''

    def __init__(self, runstate):
        '''
        Initialization of the InputDirGUIState class.
        '''
        self.runstate = runstate
        self.content_collector_thread = None

        self.input_dir_content_labels = {}  # dict of QLabel objects

        self.content_collector_group_docu_options_box_checkbox0 = None
            # QCheckBox object

        self.content_collector_group_docu_options_box_checkbox1 = None
            # QCheckBox object

        self.content_collector_group_export_options_box_checkbox0 = None
            # QCheckBox object

        self.content_collector_group_export_options_box_checkbox1 = None
            # QCheckBox object

        self.content_collector_group_export_options_box_checkbox2 = None
            # QCheckBox object

        return


    def update_input_dir_gui_dependencies(self, import_dir):
        '''
        Update GUI elements that depend on input dir changes.
        '''
        if len(import_dir) >= 1:
            if not os.path.exists(import_dir):
                self.input_dir_content_labels_set_text(
                    'Error: Directory does not exist.', 'red')
                self.runstate.set_import_button_state(0)

            elif import_dir[-8:] == '_parsed'+os.sep:
                self.input_dir_content_labels_set_text(
                    'Warning: Selected directory seems to be an '+
                    'existing output directory.',
                    'red')

            else:
                self.input_dir_content_labels_set_text(
                    'searching ...', 'blue')

                if self.content_collector_thread is not None:
                    self.content_collector_thread.stop()
                    self.content_collector_thread.wait()
                    self.content_collector_thread = None

                if self.content_collector_thread is None:
                    self.content_collector_thread_import_dir = import_dir
                    self.content_collector_thread = ContentCollectorThread(
                        self.runstate, import_dir, self)
                    self.content_collector_thread.start()

                else:
                    print(
                        'ERROR: InputDirGUIState: '+
                        'update_input_dir_content_label')
                    sys.exit()

        return


    def input_dir_content_labels_set_text(self, text, color):
        '''
        Set text and color of GUI content label.
        '''
        for instance_id in self.input_dir_content_labels:
            self.input_dir_content_labels[instance_id].setText(text)
            self.input_dir_content_labels[instance_id].setStyleSheet(
                'color: '+str(color))

        return


    def register_input_dir_content_label(self, input_dir_content_label,
                                         instance_id):
        '''
        Set GUI content label of input dir.

        Args:
            input_dir_content_label: QLabel object

        Returns:
            None: no return value
        '''

        # check
        if instance_id in self.input_dir_content_labels:
            print('ERROR: InputDirGUIState: '+
                'register_input_dir_content_label: '+
                'instance_id in self.input_dir_content_labels')
            sys.exit()

        self.input_dir_content_labels[instance_id] = input_dir_content_label

        return


    def register_options_checkboxes(self, options_checkboxes):
        '''
        Set GUI options checkboxes.

        Args:
            options_checkboxes: list of QCheckBox objects

        Returns:
            None: no return value
        '''
        self.content_collector_group_docu_options_box_checkbox0 = \
            options_checkboxes[0]

        self.content_collector_group_docu_options_box_checkbox1 = \
            options_checkboxes[1]

        self.content_collector_group_export_options_box_checkbox0 = \
            options_checkboxes[2]

        self.content_collector_group_export_options_box_checkbox1 = \
            options_checkboxes[3]

        self.content_collector_group_export_options_box_checkbox2 = \
            options_checkboxes[4]

        return
