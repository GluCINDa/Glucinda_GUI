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


def clean_path(path):
    """ Clean path string. """

    path_cleaned = []
    path_arr = path.split(os.sep)
    for p in path_arr:
        if p == '..':
            path_cleaned.pop()
        else:
            path_cleaned.append(p)

    path_cl = os.sep.join(path_cleaned)

    return path_cl


def create_folder(paths):
    """
    Create folder and subfolders for each entry in a list of path names.
    Input path names can contain filenames.
    """

    for path in paths:
        path_cl = clean_path(path)

        # get directory path without filename
        path_cl = path_cl.split(os.sep)
        path_cl = os.sep.join(path_cl[0:-1])

        if not os.path.exists(path_cl):
            os.makedirs(path_cl)

    return
