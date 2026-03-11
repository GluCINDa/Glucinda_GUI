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

from lib.dir_status import DirStatus
import lib.storage


class ExportDirStatus(DirStatus):
    '''
    This class describes the current state of the running application.
    '''

    def __init__(self, runstate):
        '''
        Initialization of the ExportDirStatus class.
        '''
        self.runstate = runstate
        self.path_dir = None  # directory path

        self._dir_status = None
            # 0: directory not existing
            # 1: directory empty
            # 2: directory not empty
            # 3: directory not empty containing files or directories not
            #    associated with this software)
            # 4: directory [existing or not existing, empty or not empty]
            #    located within input_dir

        return


    def get_dir_status(self):
        '''
        Get status of export path.
        '''
        if self._dir_status is None:
            self.dir_status()

        return self._dir_status


    def set_path(self, path_dir):
        '''
        Set new directory path.
        '''
        path_dir_ = self.clean_path(path_dir)

        if path_dir_ != self.path_dir:
            self.path_dir = path_dir_
            self.dir_status()

        return


    def update(self):
        '''
        Update status of export path.
        '''
        self.dir_status()

        return


    def dir_status(self):
        '''
        Determine status of export path.

        Returns:
            self._dir_status: (0: directory not existing,
                              1: directory empty,
                              2: directory not empty,
                              3: directory not empty, containing files or
                                 directories not associated with this software
                              4: directory
                                 [existing or not existing, empty or not empty]
                                 located within input_dir)
        '''
        path = self.path_dir

        contenttypes = lib.storage.dir_contenttypes(path)
        dir_status = None
        input_dir = self.runstate.input_dir.get_path()

        if path.startswith(input_dir):
            dir_status = 4

        elif os.path.exists(path):
            content_knowntype = \
                contenttypes[1][1]+contenttypes[1][2]+contenttypes[1][3]+ \
                contenttypes[1][4]+contenttypes[1][5]+contenttypes[2][1]

            if contenttypes[0] == 0:
                dir_status = 1
            elif contenttypes[0] > 0 and contenttypes[0] == content_knowntype:
                dir_status = 2
            elif contenttypes[0] > 0 and contenttypes[0] != content_knowntype:
                dir_status = 3

        else:
            dir_status = 0

        self._dir_status = dir_status

        return self._dir_status
