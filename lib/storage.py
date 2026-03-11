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


'''
Module providing functions for handling of storage locations.
'''


def dir_contenttypes(path):
    '''
    Get content types of export path.
    '''
    files_csv = sorted(glob.glob(path+'**'+os.sep+'*.csv', recursive=True))
    files_csv_n = len(files_csv)

    files_txt = sorted(glob.glob(path+'**'+os.sep+'*.txt', recursive=True))
    files_txt_n = len(files_txt)

    files_html = sorted(glob.glob(path+'**'+os.sep+'*.html', recursive=True))
    files_html_n = len(files_html)

    files_feather = sorted( \
                    glob.glob(path+'**'+os.sep+'*.feather', recursive=True))
    files_feather_n = len(files_feather)

    files_xlsx = sorted(glob.glob(path+'**'+os.sep+'*.xlsx', recursive=True))
    files_xlsx_n = len(files_xlsx)

    dirnames_internal = ['single_files_and_docs', 'reports']
    dirs_internal = []

    items_all = sorted(
        [f for f in glob.iglob(path+'**'+os.sep+'*', recursive=True)
            if os.path.isfile(f)])
    items_all_n = len(items_all)

    files_all = []
    dirs_all = []

    for item in items_all:
        if os.path.isfile(item):
            files_all.append(item)

        if os.path.isdir(item):
            dirs_all.append(item)
            dirname = item.split(os.sep)[-1]

            if dirname in dirnames_internal:
                dirs_internal.append(item)

    files_all_n = len(files_all)
    dirs_internal_n = len(dirs_internal)
    dirs_all_n = len(dirs_all)

    return items_all_n, \
           [files_all_n, \
            files_csv_n, files_txt_n, files_html_n, files_feather_n, \
            files_xlsx_n, files_all], \
           [dirs_all_n, dirs_internal_n, dirs_all]


def files_parsed(path):
    '''
    Determine number of parsed files.
    '''
    files_parsed_n = 0

    if os.path.exists(path):
        files_csv = sorted(glob.glob(path+'*'+os.sep+'*parsed*.csv'))

        for file in files_csv:
            if not 'parsed_all.csv' in file:
                files_parsed_n += 1

    return files_parsed_n
