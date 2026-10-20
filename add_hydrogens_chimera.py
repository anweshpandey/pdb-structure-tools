## how to run: chimera --nogui add_H2.py
import os
from chimera import runCommand as rc  # use 'rc' as shorthand for runCommand

# Gather the names of .pdb files in the folder
file_names = [fn for fn in os.listdir(".") if fn.endswith(".pdb")]

# Loop through the files, opening, processing, and closing each in turn
for fn in file_names:
    print("Processing", fn)
    base = os.path.splitext(fn)[0]  # remove .pdb extension
    rc("open " + fn)
    rc("addh")
    rc("write format pdb 0 {}_H.pdb".format(base))  # <-- works in Python 2
    rc("close all")

