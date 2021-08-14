import ROOT, sys

arg = sys.argv[1].strip()
d = None
if ":" in sys.argv[1]:
    fn, d = sys.argv[1].split(":")
    tf = ROOT.TFile(fn)
    d = tf.Get(d)
else:
    fn = sys.argv[1]
    tf = ROOT.TFile(fn)
    d = tf

for k in d.GetListOfKeys():
    o = k.ReadObj()
    cn = o.__class__.__name__
    if cn.startswith("TH"):
        print o.GetName(), o.Integral(), o.GetEntries(), o.GetMean(), o.GetRMS()
