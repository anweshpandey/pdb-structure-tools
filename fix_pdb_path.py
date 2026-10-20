import os
import subprocess
from chimera import runCommand

# Capture the directory from which the alias was called
# This should be done before any other operations that might change the working directory
original_cwd = os.environ.get('PWD', os.getcwd())

print("*************************************************")
print("=====Directory from which alias was called=====")
print("*************************************************")

# Show the directory from which this script/alias was called
print("Working directory where alias was executed:")
print("Current directory: %s/" % original_cwd)

print("\n" + "="*50)
print("=====Directory contents where alias was called=====")
print("="*50)

# Show directory contents using ls -ltr command in the original directory
print("Running 'ls -ltr' command:")
try:
    ls_result = subprocess.check_output(['ls', '-ltr', original_cwd], universal_newlines=True)
    print(ls_result)
except subprocess.CalledProcessError as e:
    print("Error running ls -ltr: %s" % e)
    # Fallback to Python's os.listdir()
    try:
        files = os.listdir(original_cwd)
        print("Directory contents (fallback):")
        for f in files:
            print("  %s" % f)
    except OSError as e:
        print("Error listing directory: %s" % e)

print("*" * 50)

# Ask for input PDB file with full path
input_pdb = raw_input("Enter the FULL path to the input PDB file: ").strip()
while not os.path.isfile(input_pdb):
    print("File not found: %s" % input_pdb)
    input_pdb = raw_input("Enter the FULL path to the input PDB file: ").strip()

runCommand("open %s" % input_pdb)

# Ask for residues to mutate, until user presses Enter on blank line
print("Enter residue mutations (e.g., 'glu :10.A'), one per line.")
print("**********************************************************")
print("====== Press Enter on a blank line when you are done. ======")

while True:
    mutation = raw_input("> ").strip()
    if mutation == "":
        break
    runCommand("swapaa %s" % mutation)

# Show current directory again before asking for output file
print("\n" + "*" * 50)
print("=====Current directory for output file=====")
print("Current directory: %s/" % original_cwd)
print("*" * 50)

# Ask for output PDB name with full path
output_pdb = raw_input("Enter the FULL path for the output PDB file: ").strip()
output_dir = os.path.dirname(output_pdb)
if output_dir and not os.path.exists(output_dir):
    print("Directory does not exist, creating it: %s" % output_dir)
    os.makedirs(output_dir)

runCommand("write format pdb 0 %s" % output_pdb)
runCommand("stop")
