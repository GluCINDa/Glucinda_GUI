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


class ExportFilesCleanup():
    '''
    This class handles the cleanup of unnecessary export files temporarily
    generated during processing.
    '''

    def __init__(self, runstate, export_format):
        '''
        Initialization of the ExportFilesCleanup class.
        '''
        self.runstate = runstate
        self.export_format = export_format

        self.run()

        return


    def run(self):
        '''
        Run ExportFilesCleanup.
        '''
        if 'CSV' not in self.export_format and 'all' not in self.export_format:
            combined_export_csv = \
                self.runstate.export_dir.get_path()+'parsed_all.csv'

            if os.path.isfile(combined_export_csv):
                os.unlink(combined_export_csv)


        if 'SEPARATE_FILES' not in self.export_format and \
           'all' not in self.export_format:
            single_files_dir = 'single_files_and_docs/'

            single_files = sorted(glob.iglob(
                self.runstate.export_dir.get_path()+single_files_dir+
                '*parsed*.csv'))

            for i, file in enumerate(single_files):
                if os.path.isfile(file):
                    os.unlink(file)

        return
