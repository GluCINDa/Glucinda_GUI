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
from PySide6.QtCore import Qt
from PySide6.QtCore import QUrl
from PySide6.QtGui import QDesktopServices
from PySide6.QtWidgets import QCheckBox
from PySide6.QtWidgets import QFileDialog
from PySide6.QtWidgets import QGroupBox
from PySide6.QtWidgets import QHBoxLayout
from PySide6.QtWidgets import QLabel
from PySide6.QtWidgets import QLineEdit
from PySide6.QtWidgets import QProgressBar
from PySide6.QtWidgets import QPushButton
from PySide6.QtWidgets import QVBoxLayout
from PySide6.QtWidgets import QWidget

import lib.storage
from lib.datatransformerthread import DataTransformerThread
from lib.cgmextractorthread import CGMExtractorThread
from lib.deletefilesthread import DeleteFilesThread
from lib.export_files_cleanup import ExportFilesCleanup
from lib.generalparserthread import GeneralparserThread
from lib.progressbarthread import ProgressBarThread


class GUITab(QWidget):
    '''
    This class describes a tab (GUI) in the main application window.
    '''

    def __init__(self, mode, tabs):
        '''
        Initialization of the GUITab class.
        '''
        super().__init__()

        self.mode = mode # mode: 0:simple, 1:advanced
        self.tabs = tabs # tabs of GUIWindow
        self.runstate = None  # RunState object


        # states
        # ~~~~~~
        self.parser_running = False

        # states of GUI elements
        self.button_input_dir_state = None
                # 0: disabled
                # 1: enabled

        self.button_export_dir_state = None
                # 0: disabled
                # 1: enabled

        self.progress_bar_thread = None
        self.progress_bar_hold = True
        self.parser_progress_var = [None, None]


        # major GUI elements
        # ~~~~~~~~~~~~~~~~~~

        # step 1
        self.input_dir_box = None
        self.field_input_dir = None
        self.button_input_dir = None
        self.label_input_dir_msg = None

        # step 2
        self.export_dir_box = None
        self.field_export_dir = None
        self.button_export_dir = None
        self.label_export_dir_msg = None

        # step 3
        self.group_docu_options_box_checkbox0 = None
        self.group_docu_options_box_checkbox1 = None
        self.group_export_options_box_checkbox0 = None
        self.group_export_options_box_checkbox1 = None
        self.group_export_options_box_checkbox2 = None

        # step 4
        self.label_import_msg = None


        # labels
        # ~~~~~~

        # labels for buttons
        self.button_browse_label = 'Browse'

        # text components
        self.input_dir_txtc = 'Raw input data directory'
        self.input_dir_txt = 'raw input data directory'

        return


    def tab(self):
        '''
        Create Tab.
        '''
        layout = QVBoxLayout()


        # box for step 1
        # --------------
        group1 = QVBoxLayout()
        group1_box = QGroupBox('Step 1:   '+ \
                'Select \''+self.input_dir_txt+'\' containing CGM data files')


        # box for step 2
        # --------------
        group2 = QVBoxLayout()
        group2_box = QGroupBox('Step 2:   '+ \
                'Use default output directory or choose own')


        # box for step 3
        # --------------
        group3 = QVBoxLayout()
        group3_box = QGroupBox('Step 3:   Advanced options')


        # box for step 4
        # --------------
        group4 = QVBoxLayout()

        if self.mode == 0:
            group4_box = QGroupBox('Step 3:   Consolidate')
        elif self.mode == 1:
            group4_box = QGroupBox('Step 4:   Consolidate')


        # step 1
        # ------
        label0 = QLabel('Supported files: CSV, XLSX, XLS')

        self.field_input_dir = QLineEdit('')
        self.field_input_dir.setStyleSheet('QLineEdit { padding-left: 2px; }')
        self.field_input_dir.setPlaceholderText( \
                                    'No \''+self.input_dir_txt+'\' selected')
        self.field_input_dir.textChanged.connect(self.input_dir_changed)

        self.button_input_dir = QPushButton(self.button_browse_label)
        self.button_input_dir.clicked.connect(self.set_input_dir_gui)

        self.input_dir_box = QHBoxLayout()
        self.input_dir_box.addWidget(self.field_input_dir)
        self.input_dir_box.addWidget(self.button_input_dir)

        self.label_input_dir_msg = QLabel('')
        self.runstate.input_dir_gui_state.register_input_dir_content_label(
            self.label_input_dir_msg, self.mode)

        space1 = QLabel('')

        group1.addWidget(label0)
        group1.addLayout(self.input_dir_box)
        group1.addWidget(self.label_input_dir_msg)
        group1_box.setLayout(group1)
        layout.addWidget(group1_box)

        layout.addWidget(space1)


        # step 2
        # ------
        label1 = QLabel(
            'Output directory must be writable and empty. '+
            'If newly created, parent directory must be writable.')

        self.field_export_dir = QLineEdit('')
        self.field_export_dir.setStyleSheet('QLineEdit { padding-left: 2px; }')
        self.field_export_dir.setPlaceholderText( \
                                    'Select \''+self.input_dir_txt+'\' first')
        self.field_export_dir.textChanged.connect(self.export_dir_changed)
        self.field_export_dir.setEnabled(False)

        self.button_export_dir = QPushButton(self.button_browse_label)
        self.button_export_dir.clicked.connect(self.set_export_dir_gui)
        self.button_export_dir.setEnabled(False)

        self.export_dir_box = QHBoxLayout()
        self.export_dir_box.addWidget(self.field_export_dir)
        self.export_dir_box.addWidget(self.button_export_dir)

        self.label_export_dir_msg = QLabel('')
        metrics = self.label_export_dir_msg.fontMetrics()
        height = metrics.lineSpacing()*3
        self.label_export_dir_msg.setFixedHeight(height)
        self.label_export_dir_msg.setStyleSheet('color: red')
        self.label_export_dir_msg.setWordWrap(True)

        space2 = QLabel('')

        group2.addWidget(label1)
        group2.addLayout(self.export_dir_box)
        group2.addWidget(self.label_export_dir_msg)
        group2_box.setLayout(group2)
        layout.addWidget(group2_box)

        layout.addWidget(space2)


        # step 3
        # ------
        if self.mode == 1:
            group3_ = QHBoxLayout()

            # documentation options
            # ~~~~~~~~~~~~~~~~~~~~~
            group_docu_options = QVBoxLayout()
            group_docu_options_box = \
                QGroupBox('Documentation of parsing process as:')
            group_docu_options_box.setLayout(group_docu_options)

            group_docu_options_box_label0 = QLabel( \
                'For imports with many input files, it can \nmake sense to '+
                'export fewer documentation \nfiles to preserve storage space.')
            group_docu_options_box_label0.setWordWrap(True)
            group_docu_options_box_label0.setStyleSheet('font: italic 14px;')
            metrics = group_docu_options_box_label0.fontMetrics()
            height = metrics.lineSpacing()*3
            group_docu_options_box_label0.setFixedHeight(height)

            self.group_docu_options_box_checkbox0 = \
                QCheckBox('TXT file(s)')
            self.group_docu_options_box_checkbox1 = \
                QCheckBox('HTML file(s)')
            self.group_docu_options_box_checkbox0.setChecked(True)
            self.group_docu_options_box_checkbox1.setChecked(True)

            group_docu_options.addWidget(self.group_docu_options_box_checkbox0)
            group_docu_options.addWidget(self.group_docu_options_box_checkbox1)
            group_docu_options.addWidget(group_docu_options_box_label0)
            group_docu_options.setSpacing(0)
            group_docu_options.setContentsMargins(5, 0, 5, 0)

            group3_.addWidget(group_docu_options_box)


            # export format options
            # ~~~~~~~~~~~~~~~~~~~~~
            group_export_options = QVBoxLayout()
            group_export_options_box = QGroupBox('Export parsed CGM data as:')
            group_export_options_box.setLayout(group_export_options)

            self.group_export_options_box_checkbox0 = QCheckBox(
                    'Feather combined file\n'+
                    'WARNING: Feather files can contain\n'+
                    'sensitive system metadata.')
            self.group_export_options_box_checkbox1 = QCheckBox(
                    'CSV combined')
            self.group_export_options_box_checkbox2 = QCheckBox(
                    'Export a separate file for each\n'+
                    'input file in addition to a combined file')
            self.group_export_options_box_checkbox0.setChecked(False)
            self.group_export_options_box_checkbox1.setChecked(True)
            self.group_export_options_box_checkbox2.setChecked(True)

            group_export_options.addWidget( \
                                    self.group_export_options_box_checkbox1)
            group_export_options.addWidget( \
                                    self.group_export_options_box_checkbox0)
            group_export_options.addWidget( \
                                    self.group_export_options_box_checkbox2)
            group_export_options.setSpacing(0)
            group_export_options.setContentsMargins(5, 0, 5, 0)

            group3_.addWidget(group_export_options_box)

            group3_.addLayout(group3)

            space3 = QLabel('')

            group3_box.setLayout(group3_)
            layout.addWidget(group3_box)
            layout.addWidget(space3)

            self.runstate.input_dir_gui_state.register_options_checkboxes([
                self.group_docu_options_box_checkbox0,
                self.group_docu_options_box_checkbox1,
                self.group_export_options_box_checkbox0,
                self.group_export_options_box_checkbox1,
                self.group_export_options_box_checkbox2])


        # step 4
        # ------
        self.button_import = \
            QPushButton(self.runstate.import_button.get_label())
        self.button_import.setFixedHeight( \
                                    self.button_import.sizeHint().height()*2)
        self.button_import.setEnabled(False)
        self.button_import.clicked.connect(self.import_start)

        self.label_import_msg = QLabel('')
        metrics = self.label_import_msg.fontMetrics()
        height = metrics.lineSpacing()*2
        self.label_import_msg.setFixedHeight(height)
        self.label_import_msg.setOpenExternalLinks(False)
        self.label_import_msg.setTextInteractionFlags( \
                                Qt.TextInteractionFlag.TextBrowserInteraction)
        self.label_import_msg.linkActivated.connect(self.open_filenamanger)

        self.progress_bar = QProgressBar()
        self.progress_bar.hide()
        self.progress_bar.setRange(0, 1000)
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(False)

        self.progress_bar.setStyleSheet("""
                QProgressBar::chunk {
                    background-color: #34b233;
                    width: 20px;
                }
            """)
        
        group4.addWidget(self.button_import)
        group4.addWidget(self.progress_bar)
        group4.addWidget(self.label_import_msg)
        group4_box.setLayout(group4)
        layout.addWidget(group4_box)

        return layout


    def input_dir_changed(self):
        '''
        Perform tasks when the input directory changed.
        '''
        input_dir = self.field_input_dir.text()
        self.runstate.set_input_dir(self.clean_path(input_dir), self.mode)

        return


    def input_dir_changed_update_gui(self, import_dir):
        '''
        Update GUI state when the input directory changed.
        '''
        self.label_import_msg.setText('')

        return


    def export_dir_changed(self):
        '''
        Perform tasks when the export directory changed.
        '''
        export_dir = self.field_export_dir.text()
        self.runstate.set_export_dir(export_dir, self.mode)

        return


    def set_input_dir(self, input_dir):
        '''
        Set input directory and update GUI element.
        '''
        if input_dir != self.field_input_dir.text():
            self.field_input_dir.setText(input_dir)

        self.input_dir_changed_update_gui(input_dir)

        input_dir_ = self.runstate.input_dir.get_path()
        input_dir_rootdir = pathlib.Path(input_dir_).anchor

        if input_dir_ == '':
            export_dir = ''
        elif input_dir_ == input_dir_rootdir:
            export_dir = input_dir_+'_parsed'+os.sep
        else:
            export_dir = input_dir_[:-1]+'_parsed'+os.sep

        self.runstate.export_dir.set_path(export_dir)
        self.field_export_dir.setText(self.runstate.export_dir.get_path())
        self.field_export_dir.setEnabled(True)
        self.button_export_dir.setEnabled(True)

        return


    def set_export_dir(self):
        '''
        Set export directory and update GUI element.
        '''
        export_dir = self.runstate.export_dir.get_path()
        if export_dir != self.field_export_dir.text():
            self.field_export_dir.setText(export_dir)

        self.runstate.export_dir_gui_state.update_gui(
            self.button_import, self.label_export_dir_msg)
                # update GUI section when the export directory changed

        return


    def set_input_dir_gui(self):
        '''
        Set input directory via GUI.
        '''
        if self.runstate.input_dir.get_path() is None:
            path_start = os.sep
        else:
            path_start = self.runstate.input_dir.get_path()

        path = QFileDialog.getExistingDirectory( \
                        self, self.button_browse_label, dir=path_start)

        if path:
            if len(path) >= 1:
                self.runstate.set_input_dir(self.clean_path(path), self.mode)

        return 


    def set_export_dir_gui(self):
        '''
        Set export directory via GUI.
        '''
        if self.runstate.export_dir.get_path() is None:
            path_start = os.sep
        else:
            path_start = self.runstate.export_dir.get_path()

        path = QFileDialog.getExistingDirectory( \
                        self, self.button_browse_label, dir=path_start)

        if path:
            self.runstate.export_dir.set_path(path+os.sep)
            self.field_export_dir.setText(self.runstate.export_dir.get_path())
            self.field_export_dir.setEnabled(True)

        return 


    def import_start(self):
        '''
        Start import/parsing of CGM data files using generalparser.
        '''
        self.runstate.check_stage(0)

        export_dir_status = self.runstate.export_dir.dir_status()
            # 0: directory not existing
            # 1: directory empty
            # 2: directory not empty
            # 3: directory not empty containing files or directories not
            #    associated with this software

        if export_dir_status == 3:
            self.runstate.change_stage(-1)
            return

        if export_dir_status == 2 and self.runstate.import_button.state != 2:
                # self.runstate.import_button.state:
                # 0: disabled
                # 1: enabled
                # 2: enabled, additional info text

            return

        # disable other tab(s), buttons and fields
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        self.runstate.change_stage(1)

        if self.mode == 0:
            self.tabs.setTabEnabled(1, False)
        elif self.mode == 1:
            self.tabs.setTabEnabled(0, False)

        self.field_input_dir.setEnabled(False)
        self.field_export_dir.setEnabled(False)
        self.runstate.import_button.set_state(self.button_import, 0)
        self.set_button_export_state(0)

        if self.mode == 1:
            self.group_docu_options_box_checkbox0.setEnabled(False)
            self.group_docu_options_box_checkbox1.setEnabled(False)
            self.group_export_options_box_checkbox0.setEnabled(False)
            self.group_export_options_box_checkbox1.setEnabled(False)
            self.group_export_options_box_checkbox2.setEnabled(False)


        # show progress bar
        # ~~~~~~~~~~~~~~~~~
        self.progress_bar.show()


        # create export directory if not already existing
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        self.runstate.change_stage(2)

        if not os.path.exists(self.runstate.export_dir.get_path()):
            try:
                os.makedirs(self.runstate.export_dir.get_path())
            except Exception:
                self.label_export_dir_msg.setText( \
                        'Error: Output directory cannot be created.')
                return


        # start generalparser thread after deleting existing files in output
        # directory if necessary
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        export_format = self.get_export_format()
        self.export_format = export_format
        export_format_with_csv_and_separate_files = [f for f in export_format]

        if 'CSV' not in export_format_with_csv_and_separate_files:
            export_format_with_csv_and_separate_files.append('CSV')
        if 'SEPARATE_FILES' not in export_format_with_csv_and_separate_files:
            export_format_with_csv_and_separate_files.append('SEPARATE_FILES')

        documentation = self.get_documentation()

        generalparser_thread = GeneralparserThread(
            self.runstate, documentation=documentation, 
            export_format=export_format_with_csv_and_separate_files)
        self.runstate.set_generalparser_thread(generalparser_thread)
        self.runstate.generalparser_thread.signal_finished.connect(
            self.datatransformer_start)

        datatransformer_thread = DataTransformerThread(
            self.runstate,
            export_format=export_format_with_csv_and_separate_files)
        self.runstate.set_datatransformer_thread(datatransformer_thread)
        self.runstate.datatransformer_thread.signal_finished.connect(
            self.cgmextractort_start)

        cgmextractor_thread = CGMExtractorThread(
            self.runstate.export_dir.get_path()+'parsed_all.csv',
            self.runstate.export_dir.get_path(),
            self.runstate, self.export_format)
        self.runstate.set_cgmextractor_thread(cgmextractor_thread)
        self.runstate.cgmextractor_thread.signal_finished.connect(
            self.import_finished)

        self.label_import_msg.setStyleSheet('color: #007934')

        if export_dir_status == 2:
            self.label_import_msg.setText( \
                    'Deleting existing files in output directory ...')

            self.deletefiles_thread = \
                DeleteFilesThread(self.runstate.export_dir.get_path())
            self.deletefiles_thread.setObjectName('DeleteFilesThread')
            self.deletefiles_thread.signal_finished.connect( \
                                                    self.generalparser_start)
            self.deletefiles_thread.start()

        else:
            self.label_import_msg.setText('Parsing ...')
            self.generalparser_start()


        # start progress bar thread
        # ~~~~~~~~~~~~~~~~~~~~~~~~~
        input_dir_items = self.runstate.input_dir.get_stat()
        files_all_n = input_dir_items[0]

        if files_all_n > 0:
            self.progress_bar_thread = ProgressBarThread(
                self.runstate,
                self.progress_bar, files_all_n, 
                self.runstate.export_dir.get_path(),
                self.label_import_msg, self)
            self.progress_bar_thread.setObjectName('ProgressBarThread')

            self.progress_bar_thread.progress_bar_set.connect(
                self.progress_bar.setValue)
            self.progress_bar_thread.label_set.connect(
                self.label_import_msg.setText)
            self.progress_bar_thread.start()

        return 


    def get_documentation(self):
        '''
        Get export documentation format(s) from GUI.
        '''
        documentation_format = []

        if self.mode == 0:
            return ['all']

        if self.group_docu_options_box_checkbox0.isChecked():
            documentation_format.append('TXT')
        if self.group_docu_options_box_checkbox1.isChecked():
            documentation_format.append('HTML')
        if 'TXT' in documentation_format and 'HTML' in documentation_format:
            documentation_format = 'all'

        return documentation_format


    def get_export_format(self):
        '''
        Get export format(s) from GUI.
        '''
        export_format = []

        if self.mode == 0:
            return ['CSV', 'SEPARATE_FILES']

        if self.group_export_options_box_checkbox0.isChecked():
            export_format.append('FEATHER')
        if self.group_export_options_box_checkbox1.isChecked():
            export_format.append('CSV')
        if self.group_export_options_box_checkbox2.isChecked():
            export_format.append('SEPARATE_FILES')
        if 'FEATHER' in export_format and 'CSV' in export_format and \
           'SEPARATE_FILES' in export_format:
            export_format = ['all']

        return export_format


    def generalparser_start(self, empty=None):
        '''
        Run generalparser.
        '''
        self.runstate.change_stage(3)
        self.progress_bar_hold = False
        self.runstate.change_stage(4)
        self.runstate.generalparser_thread.start()

        return


    def datatransformer_start(self, empty=None):
        '''
        Run data_transformer.
        '''
        self.runstate.change_stage(5)
        self.runstate.change_stage(6)

        if len(self.runstate.error_messages) == 0:
            self.label_import_msg.setText( \
                                'Compiling (this may take a few minutes)')
        else:
            self.label_import_msg.setText( \
                                'Compiling (this may take a few minutes)'+ \
                                '<br />'+ \
                                self.runstate.error_messages_formatted_str)

        self.runstate.datatransformer_thread.start()

        return


    def cgmextractort_start(self, empty=None):
        '''
        Run CGM_Extractor.
        '''
        self.runstate.change_stage(7)
        self.runstate.change_stage(8)

        if len(self.runstate.error_messages) == 0:
            self.label_import_msg.setText( \
                                'Compiling (this may take a few minutes)')
        else:
            self.label_import_msg.setText( \
                                'Compiling (this may take a few minutes)'+ \
                                '<br />'+ \
                                self.runstate.error_messages_formatted_str)

        self.runstate.cgmextractor_thread.start()

        return


    def import_finished(self, parsed_dir):
        '''
        Update GUI state after import of CGM data files has finished.
        '''
        self.runstate.change_stage(9)

        if self.progress_bar_thread is not None:
            self.progress_bar_thread.stop()

        self.runstate.change_stage(10)

        export_files_cleanup = ExportFilesCleanup(
            self.runstate, self.export_format)
        self.runstate.set_export_files_cleanup(export_files_cleanup)

        self.runstate.change_stage(11)
        self.progress_bar_hold = True

        input_dir_items = self.runstate.input_dir.get_stat()
        files_all_n = input_dir_items[0]
        files_parsed_n = lib.storage.files_parsed(parsed_dir)

        if files_all_n == 0:
            print('ERROR: import_finished')

        parsed_files_stat = ''

        if files_parsed_n == 1:
            parsed_files_stat = str(files_parsed_n)+os.sep+ \
                    str(files_all_n)+' input file parsed.'
        else:
            parsed_files_stat = str(files_parsed_n)+os.sep+ \
                    str(files_all_n)+' input files parsed.'

        self.progress_bar.hide()
        self.progress_bar.setValue(0)


        # prepare for new run
        if self.mode == 0:
            self.tabs.setTabEnabled(1, True)
        elif self.mode == 1:
            self.tabs.setTabEnabled(0, True)  

        self.field_input_dir.setEnabled(True)
        self.field_export_dir.setEnabled(True)
        self.set_button_export_state(1)
        self.runstate.export_dir_gui_state.update_gui(
            self.button_import, self.label_export_dir_msg)
                # update GUI section

        self.runstate.set_import_button_state(3)

        if self.mode == 1:
            self.group_docu_options_box_checkbox0.setEnabled(True)
            self.group_docu_options_box_checkbox1.setEnabled(True)
            self.group_export_options_box_checkbox0.setEnabled(True)
            self.group_export_options_box_checkbox1.setEnabled(True)
            self.group_export_options_box_checkbox2.setEnabled(True)


        if len(self.runstate.error_messages) == 0:
            self.label_import_msg.setText(parsed_files_stat+' ' \
                                'Parsed files written to:<br />'+ \
                                '<a href="'+parsed_dir+'">'+parsed_dir+'</a>')
            self.label_import_msg.setStyleSheet('color: black')
        else:
            self.label_import_msg.setText(parsed_files_stat+' '+ \
                                '<br />'+ \
                                self.runstate.error_messages_formatted_str)
            self.label_import_msg.setStyleSheet('color: black')

        return


    def set_button_input_state(self, state):
        '''
        Set state of the input directory button.

        Args:
            state: (0: disabled, 1: enabled)

        Returns:
            None: no return value
        '''
        if state == 0:
            self.button_input_dir.setEnabled(False)
            self.button_input_dir.setText(self.button_browse_label)
            self.button_input_dir_state = 0
        elif state == 1:
            self.button_input_dir.setEnabled(True)
            self.button_input_dir.setText(self.button_browse_label)
            self.button_input_dir_state = 1

        return


    def set_button_export_state(self, state):
        '''
        Set state of the export directory button.

        Args:
            state: (0: disabled, 1: enabled)

        Returns:
            None: no return value
        '''
        if state == 0:
            self.button_export_dir.setEnabled(False)
            self.button_export_dir.setText(self.button_browse_label)
            self.button_export_dir_state = 0
        elif state == 1:
            self.button_export_dir.setEnabled(True)
            self.button_export_dir.setText(self.button_browse_label)
            self.button_export_dir_state = 1

        return


    def open_filenamanger(self, path):
        '''
        Open path in system file manager.
        '''
        QDesktopServices.openUrl(QUrl.fromLocalFile(path))

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
