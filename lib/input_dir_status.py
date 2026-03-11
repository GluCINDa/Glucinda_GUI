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
import pathlib

from lib.dir_status import DirStatus


class InputDirStatus(DirStatus):
    '''
    This class describes the current state of the running application.
    '''

    def __init__(self):
        '''
        Initialization of the InputDirStatus class.
        '''
        self.path_dir = str(pathlib.Path().absolute())+os.sep
            # import directory containing CGM data files

        self._stat = None

        return


    def get_stat(self):
        '''
        Get statistics about input directory files.
        '''
        if self._stat is None:
            self.stat()

        return self._stat


    def set_path(self, path_dir):
        '''
        Set new directory path.
        '''
        path_dir_ = self.clean_path(path_dir)

        if path_dir_ != self.path_dir:
            self.path_dir = path_dir_
            self._stat = None

        return


    def stat(self):
        '''
        Determine statistics about input directory files.
        '''
        path = self.path_dir

        files_csv = sorted(glob.glob(path+'**'+os.sep+'*.csv', recursive=True))
        files_csv_n = len(files_csv)

        files_xls = sorted(glob.glob(path+'**'+os.sep+'*.xls', recursive=True))
        files_xls_n = len(files_xls)

        files_xlsx = \
            sorted(glob.glob(path+'**'+os.sep+'*.xlsx', recursive=True))
        files_xlsx_n = len(files_xlsx)

        files_knowntype_n = files_csv_n+files_xls_n+files_xlsx_n

        items_all = sorted(
            [f for f in glob.iglob(path+'**'+os.sep+'*', recursive=True)
                if os.path.isfile(f)])
        items_all_n = len(items_all)

        self._stat = [items_all_n, files_knowntype_n, 
            files_csv_n, files_xlsx_n, files_xls_n]

        return self.stat
