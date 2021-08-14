import ROOT, sys
import argparse

parser = argparse.ArgumentParser(description='Runs MEAnalysis')
parser.add_argument(
    '--infile',
    action="store",
    help="Input file to process",
    required=True
)
parser.add_argument(
    '--site',
    action="store",
    help="storage site",
    choices=["T2_CH_CSCS", "T3_CH_PSI"],
    required=False,
    default="T2_CH_CSCS"
)
parser.add_argument(
    '--maxfiles',
    action="store",
    help="max number of files",
    required=False,
    default=-1,
    type=int
)
args = parser.parse_args(sys.argv[1:])
print args

site_url = {
    "T2_CH_CSCS": "root://storage01.lcg.cscs.ch/pnfs/lcg.cscs.ch/cms/trivcat",
    "T3_CH_PSI": "root://t3dcachedb03.psi.ch/pnfs/psi.ch/cms/trivcat"
}

infile = open(args.infile).readlines()
if args.maxfiles > 0:
    infile = infile[:args.maxfiles]

bad_files = []
size = 0
goodfiles = 0
for line in infile:
    if not "root" in line:
        continue
    line = line.split()[0]
    print "trying", line
    f = None 
    try:
        f = ROOT.TFile.Open(site_url[args.site] + line)
        if not f or f.IsZombie():
            raise Exception("is zombie")
        size += f.GetSize()
        goodfiles += 1
    except Exception as e:
        print "BAD", line
        bad_files += [line]
        print e
    if f:
        f.Close()

print "bad files", len(bad_files), bad_files
print "good_files", goodfiles
print "file size", float(size)/float(goodfiles)/1024.0/1024.0
