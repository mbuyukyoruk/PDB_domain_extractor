import os
import sys
import argparse
from chimera import runCommand as rc
import tqdm
import subprocess
import textwrap

orig_stdout = sys.stdout

parser = argparse.ArgumentParser(prog='python PDB_domain_extractor.py',
                                 formatter_class=argparse.RawDescriptionHelpFormatter,
                                 epilog=textwrap.dedent('''\

Author: Murat Buyukyoruk

        PDB_domain_extractor help:

This script is developed to fetch domain from PDB files. 

IMPORTANT! The input PDB file should be located in the same directory as the workdir directory (type "pwd" to terminal first to get the current workdir.)  

UCSF-Chimera and Pychimera packages are required to fetch domains. Additionally, tqdm is required to provide a progress bar since some multifasta files can contain long and many sequences.

Syntax:

        pychimera PDB_domain_extractor.py -i demo_list.txt

Example Dataframe (tab separated file is required with .txt extension):

        PDB         Domain      Start       Stop
        4ncb.pdb    PIWI        461         685    
        
PDB_domain_extractor dependencies:
    
UCSF-Chimera                                            refer to https://www.cgl.ucsf.edu/chimera/data/downloads/1.17.1/linux_x86_64.html

Pychimera                                               refer to https://pypi.org/project/pychimera/0.1.1/

tqdm                                                    refer to https://pypi.org/project/tqdm/

Input Paramaters (REQUIRED):
----------------------------
	-i/--input		FASTA			Specify a list of positions of domain of interest from pdbs.

Basic Options:
--------------
	-h/--help		HELP			Shows this help text and exits the run.

Output header will contain protein accession/array no, original accession number, positions and fullname (if included in original fasta), observed stand and the information about flank in terms of which side of the gene is fetched.

      	'''))
parser.add_argument('-i', '--input', required=True, type=str, dest='filename',
                    help='Specify a list of positions of domain of interest from pdbs.\n')

results = parser.parse_args()
filename = results.filename

workdir = os.path.abspath(os.getcwd())

file_names = [fn for fn in os.listdir(".") if fn.endswith(".pdb")]

proc = subprocess.Popen("wc -l <" + filename, shell=True, stdout=subprocess.PIPE, text=True)
length = int(proc.communicate()[0].split('\n')[0])

with tqdm.tqdm(range(length-1)) as pbar:
    pbar.set_description('Reading...')
    with open(filename, 'rU') as file:
        for line in file:
            if "start" not in line.lower() or "stop" not in line.lower() or "domain" not in line.lower():
                pbar.update()
                pdb_file = line.split("\t")[0]
                if ".pdb" not in pdb_file:
                    pdb_file = pdb_file + ".pdb"
                domain = line.split("\t")[1]
                start = line.split("\t")[2]
                stop = line.split("\t")[3].split("\n")[0]
                if pdb_file in file_names:
                    rc("open " + pdb_file)
                    rc("select #0:" + start + "-" + stop)
                    rc("write selected #0 " + workdir + "/" + domain + "_" + pdb_file)
                    rc("close all")
                else:
                    sys.stdout = orig_stdout
                    print("PDB file: " + pdb_file + " not found in " + workdir)

sys.exit()
