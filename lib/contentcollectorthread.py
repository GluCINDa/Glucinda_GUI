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
import time
from PySide6.QtCore import QThread
from PySide6.QtCore import Signal

import lib.storage
import sys


class ContentCollectorThread(QThread):
    '''
    This class describes a collector for statistics about input dir files
    and describes the GUI states that depend on input dir changes.
    '''

    def __init__(self, runstate, path_dir, input_dir_gui_state):
        '''
        Initialization of the ContentCollectorThread class.
        '''
        super().__init__()

        self.runstate = runstate

        # check
        if len(path_dir) < 1:
            print('ERROR: ContentCollectorThread')
            sys.exit()

        self.path_dir = path_dir
        self.input_dir_gui_state = input_dir_gui_state

        self._running = False
        self._stat = None

        return


    def run(self):
        '''
        Run ContentCollectorThread.
        '''
        self._running = True
        input_dir_items = self.stat()

        if input_dir_items is False:
            return

        elif input_dir_items == -1:
            self.input_dir_gui_state.input_dir_content_labels_set_text(
                '>100000 files found (may include hidden files). '+
                'Included: supported and unsupported filetypes.', 'blue')

            self.input_dir_gui_state. \
                content_collector_group_docu_options_box_checkbox0. \
                setChecked(True)
            self.input_dir_gui_state. \
                content_collector_group_docu_options_box_checkbox1. \
                setChecked(False)
            self.input_dir_gui_state. \
                content_collector_group_export_options_box_checkbox0. \
                setChecked(False)
            self.input_dir_gui_state. \
                content_collector_group_export_options_box_checkbox1. \
                setChecked(True)
            self.input_dir_gui_state. \
                content_collector_group_export_options_box_checkbox2. \
                setChecked(False)

            return


        files_all_n = input_dir_items[0]
        files_knowntype_n = input_dir_items[1]

        if files_all_n == 1 and files_knowntype_n == 1:
            self.input_dir_gui_state.input_dir_content_labels_set_text(
                str(files_all_n)+
                ' file found (may include hidden files). '+
                str(files_knowntype_n)+
                ' with supported filetype.',
                'blue')
        elif files_all_n == 1 and files_knowntype_n == 0:
            self.input_dir_gui_state.input_dir_content_labels_set_text(
                str(files_all_n)+
                ' file found (may include hidden files). '+
                str(files_knowntype_n)+
                ' with supported filetype.',
                'blue')
        elif files_all_n > 1 and files_knowntype_n == 1:
            self.input_dir_gui_state.input_dir_content_labels_set_text(
                str(files_all_n)+
                ' files found (may include hidden files). '+
                str(files_knowntype_n)+
                ' with supported filetype.',
                'blue')
        else:
            self.input_dir_gui_state.input_dir_content_labels_set_text(
                str(files_all_n)+
                ' files found (may include hidden files). '+
                str(files_knowntype_n)+
                ' with supported filetype.',
                'blue')

        if files_knowntype_n < 100:
            self.input_dir_gui_state. \
                content_collector_group_docu_options_box_checkbox0. \
                setChecked(True)
            self.input_dir_gui_state. \
                content_collector_group_docu_options_box_checkbox1. \
                setChecked(True)
            self.input_dir_gui_state. \
                content_collector_group_export_options_box_checkbox0. \
                setChecked(False)
            self.input_dir_gui_state. \
                content_collector_group_export_options_box_checkbox1. \
                setChecked(True)
            self.input_dir_gui_state. \
                content_collector_group_export_options_box_checkbox2. \
                setChecked(True)
        else:
            self.input_dir_gui_state. \
                content_collector_group_docu_options_box_checkbox0. \
                setChecked(True)
            self.input_dir_gui_state. \
                content_collector_group_docu_options_box_checkbox1. \
                setChecked(False)
            self.input_dir_gui_state. \
                content_collector_group_export_options_box_checkbox0. \
                setChecked(False)
            self.input_dir_gui_state. \
                content_collector_group_export_options_box_checkbox1. \
                setChecked(True)
            self.input_dir_gui_state. \
                content_collector_group_export_options_box_checkbox2. \
                setChecked(False)

        return


    def stat(self):
        '''
        Determine statistics about input directory files.
        '''
        path = self.path_dir

        items_all_n = 0

        for i, f in enumerate(glob.iglob(
            path+'**'+os.sep+'*', recursive=True)):
            if i >= 100000:
                return -1

            if self._running is False:
                return False

            if os.path.isfile(f):
                items_all_n += 1


        files_csv_n = 0

        for i, f in enumerate(glob.iglob(
            path+'**'+os.sep+'*.csv', recursive=True)):
            if i > 100000:
                return False

            if self._running is False:
                return False

            if os.path.isfile(f):
                files_csv_n += 1


        files_xls_n = 0

        for i, f in enumerate(glob.iglob(
            path+'**'+os.sep+'*.xls', recursive=True)):
            if i > 100000:
                return False

            if self._running is False:
                return False

            if os.path.isfile(f):
                files_xls_n += 1


        files_xlsx_n = 0

        for i, f in enumerate(glob.iglob(
            path+'**'+os.sep+'*.xlsx', recursive=True)):
            if i > 100000:
                return False

            if self._running is False:
                return False

            if os.path.isfile(f):
                files_xlsx_n += 1


        files_knowntype_n = files_csv_n+files_xls_n+files_xlsx_n
        self._stat = [items_all_n, files_knowntype_n, 
            files_csv_n, files_xlsx_n, files_xls_n]

        return self._stat


    def stop(self):
        '''
        Stop ContentCollectorThread.
        '''
        self._running = False

        return
