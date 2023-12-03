"""Make a multipage PIPO TIFF image.

Convert a PIPO dataset to a multipage TIFF file for PIPONATOR.

This script is part of pynlomic, a Python library for nonlinear microscopy.

Copyright 2015-2022 Lukas Kontenis
Contact: dse.ssd@gmail.com
"""
# flake8: noqa
# pylint: skip-file

import sys
import os

from lkcom.util import handle_general_exception

from pynlomic.proc import convert_pipo_to_tiff_piponator
from pynlomic.dataio import get_microscopy_data_file_name

print("=== PIPONATOR TIFF converter ===", flush=True)

file_name = None
num_args = len(sys.argv)
if num_args < 2:
    file_name = get_microscopy_data_file_name()
else:
    file_name = sys.argv[1]

if file_name is None:
    print("No input provided. Specify a file name using:")
    print("\t" + os.path.basename(__file__) + " scan.dat")
    print("\nOr drag a DAT file on the script icon.\n")
else:
    try:
        print("Converting '{:s}' to TIFF...".format(file_name))

        convert_pipo_to_tiff_piponator(file_name=file_name)

    except Exception:
        handle_general_exception("Conversion failed")

input("Press any key to close this window...")
