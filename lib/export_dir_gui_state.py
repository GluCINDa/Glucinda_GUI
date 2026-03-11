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

class ExportDirGUIState():
    '''
    This class describes the current state of the GUI section responsible
    for setting the export directory.
    '''

    def __init__(self, runstate):
        '''
        Initialization of the ExportDirGUIState class.
        '''
        self.runstate = runstate

        return


    def update_gui(self, button_import, label_export_dir_msg):
        '''
        Update GUI section.

        Args:
            button_import: QPushButton object
            label_export_dir_msg: QLabel object

        Returns:
            None: no return value
        '''
        export_dir_status = self.runstate.export_dir.update()
        export_dir_status = self.runstate.export_dir.get_dir_status()

        # export directory not existing
        if export_dir_status == 0:
            self.runstate.import_button.set_state(button_import, 1)
            label_export_dir_msg.setText(
                'Output directory will be created.')
            label_export_dir_msg.setStyleSheet('color: blue')

        # export directory empty
        elif export_dir_status == 1:
            self.runstate.import_button.set_state(button_import, 1)
            label_export_dir_msg.setText('')
            label_export_dir_msg.setStyleSheet('color: black')

        # export directory not empty
        elif export_dir_status == 2:
            self.runstate.import_button.set_state(
                button_import, 2, 
                ' and delete existing data in output directory')
            label_export_dir_msg.setText(
                'Warning: Output directory is not empty. '+ \
                'All files in existing output directory will be deleted.')
            label_export_dir_msg.setStyleSheet('color: red')

        # export directory not empty, containing files or directories not
        # associated with this software
        elif export_dir_status == 3:
            self.runstate.import_button.set_state(button_import, 0)
            label_export_dir_msg.setText(
                'Warning: Output directory is not empty and contains'+ \
                ' files or directories not created by this software.\n'+ \
                'Choose other directory or empty this folder.')
            label_export_dir_msg.setStyleSheet('color: red')

        # directory [existing or not existing, empty or not empty] located
        # within input_dir
        elif export_dir_status == 4:
            self.runstate.import_button.set_state(button_import, 0)
            label_export_dir_msg.setText(
                'Warning: Output directory cannot be located within '+ \
                'input directory.\n'+ \
                'Choose other directory.')
            label_export_dir_msg.setStyleSheet('color: red')

        else:
            raise Exception(
                'GUITab: export_dir_changed_update_gui: '+
                'invalid export_dir_status: '+
                str(export_dir_status))

        return
