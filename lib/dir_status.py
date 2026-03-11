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


class DirStatus():
    '''
    This class describes the current status of a working directory
    (e.g. input directory, output directory).
    '''

    def __init__(self):
        '''
        Initialization of the DirStatus class.
        '''
        self.path_dir = None  # directory path

        return


    def get_path(self):
        '''
        Get dir path.
        '''

        return self.path_dir


    def set_path(self, path_dir):
        '''
        Set new dir path.
        '''
        path_dir_ = self.clean_path(path_dir)

        if path_dir_ != self.path_dir:
            self.path_dir = path_dir_

        return


    def clean_path(self, path):
        '''
        Clean directory path.
        '''
        if len(path) >= 1:
            if path[-1] != os.sep:
                path = path+os.sep
            else:
                path = path

        return path
