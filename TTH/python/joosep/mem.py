import ROOT
import uuid, sys, json, os, glob
from TTH.Plotting.Datacards.sparse import save_hdict

def get_mem_proba(filenames, scenario):
    probas = []
    for fn in filenames:
        fi = open(fn)
        for line in fi.readlines():
            line = line.strip()
            d = json.loads(line)

            p0 = d["output"][scenario]["tth"]
            p1 = d["output"][scenario]["ttbb"]
            p = 0.0
            if p0 > 0:
                p = p0 / (p0 + 0.1*p1)
            probas += [p]
    return probas

def make_hist(arr, bins):
    name = str(uuid.uuid4())
    h = ROOT.TH1D(name, name, *bins)
    h.Sumw2()
    for a in arr:
        h.Fill(a)
    return h

if __name__ == "__main__":
    path = sys.argv[1]
    outfile = sys.argv[2]
    hd = {}

    #Loop over the input directory
    for root, dirs, files in os.walk(path):

        #Try to find sample directories
        for sample in dirs:
            print "looking in directory", root + "/" + sample

            #find the json files
            fns = glob.glob(os.path.join(root, sample, "*.json"))
            if len(fns) == 0:
                continue
            
            #Loop over the specified MEM scenarios
            for scenario in ["CASE1", "CASE2"]:
                ps = get_mem_proba(fns, scenario)
                h = make_hist(ps, (100, 0, 1))
                hd["{0}/{1}".format(scenario, sample)] = h

    save_hdict(outfile, hd)
