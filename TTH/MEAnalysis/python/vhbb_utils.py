import ROOT, math
from copy import deepcopy

def lvec(self):
    """
    Converts an object with pt, eta, phi, mass to a TLorentzVector
    """
    lv = ROOT.TLorentzVector()
#    if self.pt < 0 or abs(self.eta) > 6:
#        raise Exception("Invalid values for TLorentzVector")
    lv.SetPtEtaPhiM(self.pt, self.eta, self.phi, self.mass)
#    if abs(lv.Pt()) > 100000 or abs(lv.Eta()) > 100000:
#        raise Exception("Invalid values for TLorentzVector")
    return lv

def match_deltaR(coll1, coll2, deltaR=0.3):
    pairs = []
    for idx1, obj1 in enumerate(coll1):
        lv1 = lvec(obj1)
        for idx2, obj2 in enumerate(coll2):
            lv2 = lvec(obj2)
            dr = lv1.DeltaR(lv2)
            if dr < deltaR:
                pairs += [(idx1, idx2, dr)]
    return pairs

def remove_duplicates(coll):
    seen = set([])
    deduped = []
    for obj in coll:
        key = (obj.pt, obj.eta, obj.phi) 
        if key not in seen:
            seen.add(key)
            deduped += [obj]
        else:
            continue
    return deduped

class MET:
    def __init__(self, **kwargs):
        self.p4 = ROOT.TLorentzVector()

        _px, _py = kwargs.get("px", None), kwargs.get("py", None)
        _pt, _phi = kwargs.get("pt", None), kwargs.get("phi", None)
        tree = kwargs.get("tree", None)
        metobj = kwargs.get("metobj", None)
        systs = kwargs.get("systs", None)

        self.sumEt = 0
        self.genPt = 0
        self.genPhi = 0

        if not (_px is None or _py is None):
            self.p4.SetPxPyPzE(_px, _py, 0, math.sqrt(_px*_px + _py*_py))
            self.pt = self.p4.Pt()
            self.phi = self.p4.Phi()
            self.px = self.p4.Px()
            self.py = self.p4.Py()
        elif not (_pt is None or _phi is None):
            self.p4.SetPtEtaPhiM(_pt, 0, _phi, 0)
            self.pt = self.p4.Pt()
            self.phi = self.p4.Phi()
            self.px = self.p4.Px()
            self.py = self.p4.Py()
        elif metobj != None:
            for x in ["pt", "eta", "phi", "mass", "sumEt", "genPt", "genPhi"]:
                setattr(self, x, getattr(metobj, x, None))
            self.p4.SetPtEtaPhiM(self.pt, 0, self.phi, 0)
            self.px = self.p4.Px()
            self.py = self.p4.Py()
            if systs is not None:
               for sys in systs:
                   for sdir in ["Up", "Down"]:
                       setattr(self, "pt_corr_{0}{1}".format(sys, sdir), getattr(metobj, "pt_corr_{0}{1}".format(sys, sdir), None))
                       setattr(self, "phi_corr_{0}{1}".format(sys, sdir), getattr(metobj, "phi_corr_{0}{1}".format(sys, sdir), None))



    @staticmethod
    def make_array(event):
        return [MET(tree=event.input)]

class JetWrapper:
    """
    Needed for Heppy btagSF calculator, which expects certain functions from the jet.
    """
    def __init__(self, orig):
        self.orig = orig
    
    def __getattr__(self, attr):
        return getattr(self.__dict__["orig"], attr)
    
    def pt(self):
        return self.orig.pt
    
    def eta(self):
        return self.orig.eta

    def hadronFlavour(self):
        return self.orig.hadronFlavour

    def btag(self, algo):
        if algo == "pfCombinedInclusiveSecondaryVertexV2BJetTags":
            return self.orig.btagCSV
        elif algo == "pfCombinedMVAV2BJetTags":
            return self.orig.btagCMVA
        else:
            raise Exception("b-tag algorithm {0} undefined".format(algo))

class SystematicObject(object):
    def __init__(self, orig, variated_values):
        self.orig = orig
        for k, v in variated_values.items():
            setattr(self, k, v)

    def __getattr__(self, attr):
        return getattr(self.__dict__["orig"], attr)

def autolog(*args):
    import inspect, logging
    # Get the previous frame in the stack, otherwise it would
    # be this function!!!
    func = inspect.currentframe().f_back.f_code
    message = ", ".join(map(str, args))
    filename_last = func.co_filename.split("/")[-1]
    # Dump the message + the name of this function to the log.
    print "[%s %s:%i]: %s" % (
        func.co_name,
        filename_last,
        func.co_firstlineno,
        message
    )
