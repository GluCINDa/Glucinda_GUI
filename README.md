# GluCINDa

The tool GluCINDa takes CGM data files as input, identifies full datasets containing date, time and glucose values and writes the full datasets into output csv files.


## Requirements
Python, additional modules: chardet, csv, datetime, glob, json, openpyxl, python-magic, multiprocessing, os, pandas, pathlib, pyarrow, PySide6, PyYAML, setuptools, statistics, sys, time, traceback, unittest, xlrd


## Installation

1.  Install missing requirements
    ```bash
    pip3 install chardet csv datetime glob json openpyxl python-magic multiprocessing os pandas pathlib pyarrow PySide6 PyYAML setuptools statistics sys time traceback unittest xlrd
    ```

2.  Make sure that `git` is installed on the system

3.  Install the GluCINDa repository
    *   `cd` into the directory where you want to install GluCINDa (example: `/path_to_project/`)
        ```bash
        cd /path_to_project/
        ```
    *   Clone the repository and `cd` into it
        ```bash
        git clone https://github.com/GluCINDa/GluCINDa_GUI.git GluCINDa/
        cd GluCINDa
        git submodule init generalparser/
        git submodule init cgm_extractor/
        git submodule init data_field_adder/
        git submodule update --remote
        ```

4.  Test the installation
    Do a test run on this example, see section ‘Running GluCINDa’.


## Alternative Installation with manual Submodule Setup

1.  Install missing requirements
    ```bash
    pip3 install chardet csv datetime glob json openpyxl python-magic multiprocessing os pandas pathlib pyarrow PySide6 PyYAML setuptools statistics sys time traceback unittest xlrd
    ```

2.  Make sure that `git` is installed on the system

3.  Install the GluCINDa repository
    *   `cd` into the directory where you want to install GluCINDa (example: `/path_to_project/`)
        ```bash
        cd /path_to_project/
        ```
    *   Clone the repository, `cd` into it, and clone the *generalparser* and *cgm_extractor* repositories
        ```bash
        git clone https://github.com/GluCINDa/GluCINDa_GUI.git GluCINDa/
        cd GluCINDa
        git clone https://github.com/GluCINDa/generalparser.git generalparser/ 
        git clone https://github.com/GluCINDa/CGM_Extractor.git cgm_extractor/ 
        git clone https://github.com/GluCINDa/data_field_adder.git data_field_adder/ 
        ```

4.  Test the installation
    Do a test run on this example, see section ‘Running GluCINDa’.


## Running GluCINDa
1.  `cd` into the directory where you installed GluCINDa (example: `/path_to_project/`)
    ```bash
    cd /path_to_project/
    ```
2.  start GluCINDa
    ```bash
    python3 glucinda.py
    ```
