import ROOT, uuid

def load(filename):
    import ROOT
    ROOT.gROOT.SetBatch(True)
    tf = ROOT.TFile.Open(filename)
    return tf

def draw(args):
    import ROOT, uuid
    ROOT.gROOT.SetBatch(True)
    tf, cut, func, bins = args
    tt = tf.Get("tree")
    ROOT.gROOT.cd()
    hn = str(uuid.uuid4())
    h = ROOT.TH1D(hn, hn, *bins)
    n = tt.Draw("{0} >> {1}".format(func, hn), cut, "goff")
    return h

def add(histograms):
    import ROOT
    htot = histograms[0].Clone()
    for h in histograms[1:]:
        htot.Add(h)
    return htot

def store(args):
    import ROOT
    result, outfile = args
    of = ROOT.TFile(outfile, "RECREATE")
    of.cd()
    result.SetName("histo")
    I = result.Integral(), result.GetMean()
    of.Add(result)
    of.Write()
    of.Close()
    return I

def make_histo_graph(infiles, cut, func, bins, outfile):
    dsk = {}
    draw_tasks = []
    for ifile, inf in enumerate(infiles):
        load_task = "load-{0}".format(ifile)
        dsk[load_task] = (load, inf)
       
        draw_task = "draw-{0}".format(ifile)
        dsk[draw_task] = (draw, [load_task, cut, func, bins])
        draw_tasks += [draw_task]

    dsk["add"] = (add, draw_tasks)
    dsk["store"] = (store, ['add', outfile])
    return dsk

if __name__ == "__main__":

    from TTH.MEAnalysis.samples_base import get_files
    import dask

    infiles = get_files("datasets/Jan26/ttHTobb_M125_TuneCUETP8M2_ttHtranche3_13TeV-powheg-pythia8.txt")

    from dask.distributed import progress

    from distributed import Client
    client = Client('127.0.0.1:8786')
    
    dsk = make_histo_graph(infiles, "is_sl && numJets >=4", "jets_pt", (300, 0, 300), 'out1.root')
    out = client.get(dsk, "store", sync=True)
    print "h1", out

    dsk = make_histo_graph(infiles, "is_sl && numJets >=4", "jets_eta", (300, -2.5, 2.5), 'out2.root')
    out = client.get(dsk, "store", sync=True)
    print "h2", out
    
    dsk = make_histo_graph(infiles, "is_sl && numJets >=4", "jets_phi", (300, -2.5, 2.5), 'out3.root')
    out = client.get(dsk, "store", sync=True)
    print "h3", out
