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
import pathlib


class InstallationCheck():
    '''
    This class describes a check of the GluCINDa installation.
    '''

    def __init__(self):
        '''
        Initialization of the InstallationCheck class.
        '''
        self.message = None

        return


    def check(self):
        '''
        Check the installation.
        '''
        root_path = str(pathlib.Path(__file__).parent.parent)+os.sep
        install_dir = root_path.split(os.sep)[-2]+os.sep
        check = True
        self.message = ''

        if os.path.exists(root_path+'generalparser/'):
            self.message += \
                'Module "generalparser" found.\n\n'
        else:
            check = False
            self.message += \
                'Module "generalparser" not found.\n'+ \
                'Install "generalparser" directly into '+install_dir+'.\n\n'

        if os.path.exists(root_path+'data_field_adder/'):
            self.message += \
                'Module "data_field_adder" found.\n\n'
        else:
            check = False
            self.message += \
                'Module "data_field_adder" not found.\n'+ \
                'Install "data_field_adder" directly into '+install_dir+'.\n\n'

        if os.path.exists(root_path+'cgm_extractor/'):
            self.message += \
                'Module "cgm_extractor" found.\n\n'
        else:
            check = False
            self.message += \
                'Module "cgm_extractor" not found.\n'+ \
                'Install "cgm_extractor" directly into '+install_dir+'.\n\n'


        if check is False:
            self.message = \
                'GluCINDa installation check failed:\n\n'+self.message

        return check
