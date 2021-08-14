import glob
from subprocess import Popen, PIPE
import sys, os

server = "t3dcachedb.psi.ch"

def xrdfs_cat(server, path):
    process = Popen(" ".join(['xrdfs', server, 'cat', path]), stdout=PIPE, stderr=PIPE, shell=True)
    stdout, stderr = process.communicate()
    return stdout.strip()

def get_files_path(server, path):
    prefix = "root://" + server
    files = [prefix + f for f in glob.glob(path + "/job_*.root")]

    input_nanoaod_files = []
    infile_outfile = {}
    for outfile in files:
        input_file = outfile.replace("out.root", "inputs.txt")
        infile_contents = xrdfs_cat(server, input_file.replace(prefix, ""))
        fns = infile_contents.split()
        print "uberftp t3se01.psi.ch 'rm {0}'".format(outfile.replace(prefix, ""))
        print "uberftp t3se01.psi.ch 'rm {0}'".format(input_file.replace(prefix, ""))
        
        if len(fns) != 1:
            raise Exception("Expected output {0} to be produced from exactly one file, but found '{1}'".format(outfile, infile_contents))
        
        filename = os.path.basename(fns[0])
        if not (filename in infile_outfile):
            infile_outfile[filename] = []
        infile_outfile[filename].append(outfile)
    
    for infile in infile_outfile.keys():
        arr = infile_outfile[infile]
        arr = sorted(arr, key=lambda x: int(os.path.basename(x).split("_")[1]))
        infile_outfile[infile] = arr
    return infile_outfile

def merge_files(server, path, infile_outfile):
    for infile, outfiles in infile_outfile.items():
        print "hadd", "root://"+server+os.path.join(path, infile), " ".join(outfiles)

path = sys.argv[1]
infile_outfile = get_files_path(server, path)
merge_files(server, path, infile_outfile)
