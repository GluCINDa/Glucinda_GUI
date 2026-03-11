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

class ImportButtonState():
    '''
    This class describes the current state of the import button.
    '''

    def __init__(self, runstate):
        '''
        Initialization of the ImportButtonState class.
        '''
        self.runstate = runstate
        self.label_initial = 'Run'
        self.label_multiple_runs = 'Run'
        self.label_finished = \
            "Done. For new run go back to 'Step 1'."

        self.state = None
            # 0: disabled
            # 1: enabled
            # 2: enabled, additional info text
            # 3: disabled

        return


    def get_label(self):
        '''
        Get label for import button.
        '''
        if self.runstate.runs_started_n == 0:
            label = self.label_initial
        elif self.runstate.runs_started_n == 1 and \
             (self.runstate.stage == -1 or self.runstate.stage >= 1):
            label = self.label_initial
        else:
            label = self.label_multiple_runs

        return label


    def set_state(self, button, state, text=''):
        '''
        Set state of the import button.

        Args:
            button: QPushButton object
            state:  (0: disabled, 1: enabled, 2: enabled, additional info text)
            text:   additional info text

        Returns:
            None: no return value
        '''
        if state == 1:
            button.setEnabled(True)
            button.setText(self.get_label())
            self.state = 1
        elif state == 2:
            button.setEnabled(True)
            button.setText(self.get_label()+text)
            self.state = 2
        elif state == 0:
            button.setEnabled(False)
            button.setText(self.get_label())
            self.state = 0
        elif state == 3:
            button.setEnabled(False)
            button.setText(self.label_finished)
            self.state = 3

        return
