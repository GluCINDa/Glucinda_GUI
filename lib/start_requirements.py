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

class StartRequirements():
    '''
    This class checks the requirements for parsing start.
    '''

    def __init__(self, runstate):
        '''
        Initialization of the StartRequirements class.
        '''
        self.runstate = runstate  # RunState object

        return


    def update(self):
        '''
        Check start requirements and update run stage.
        '''
        export_dir_status = self.runstate.export_dir.get_dir_status()

        # export directory not existing
        if export_dir_status == 0:
            self.runstate.change_stage(0)

        # export directory empty
        elif export_dir_status == 1:
            self.runstate.change_stage(0)

        # export directory not empty
        elif export_dir_status == 2:
            self.runstate.change_stage(0)

        # export directory not empty, containing files or directories not
        # associated with this software
        elif export_dir_status == 3:
            self.runstate.change_stage(-1)

        # directory [existing or not existing, empty or not empty] located
        # within input_dir
        elif export_dir_status == 4:
            self.runstate.change_stage(-1)

        else:
            raise Exception(
                'StartRequirements: update: '+
                'invalid export_dir_status: '+
                str(export_dir_status))

        return
