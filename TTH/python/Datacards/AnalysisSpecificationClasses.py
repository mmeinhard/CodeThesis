import os
import ConfigParser
from itertools import izip
import cPickle as pickle
import fnmatch
from copy import deepcopy
import ROOT

from TTH.MEAnalysis import samples_base
from TTH.MEAnalysis.samples_base import get_files, getSitePrefix

import logging
LOG_MODULE_NAME = logging.getLogger(__name__)

# From:
# http://stackoverflow.com/questions/5389507/iterating-over-every-two-elements-in-a-list
def pairwise(iterable):
    "s -> (s0, s1), (s2, s3), (s4, s5), ..."
    a = iter(iterable)
    return izip(a, a)

def triplewise(iterable):
    "s -> (s0, s1, s2), (s3, s4, s5), (s5, s6, s7), ..."
    a = iter(iterable)
    return izip(a, a, a)

FUNCTION_TABLE = {
    "btag_LR_4b_2b_btagCSV_logit": lambda ev: ev.btag_LR_4b_2b_btagCSV_logit,
    "common_bdt": lambda ev: ev.common_bdt,
    "jetsByPt_0_eta": lambda ev: ev.jets[0].lv.Eta() if len(ev.jets)>=1 else 0.0,
    "jetsByPt_1_eta": lambda ev: ev.jets[1].lv.Eta() if len(ev.jets)>=2 else 0.0,
    "jetsByPt_2_eta": lambda ev: ev.jets[2].lv.Eta() if len(ev.jets)>=3 else 0.0,
    "jetsByPt_3_eta": lambda ev: ev.jets[3].lv.Eta() if len(ev.jets)>=4 else 0.0,
    "jetsByPt_4_eta": lambda ev: ev.jets[4].lv.Eta() if len(ev.jets)>=5 else 0.0,
    "jetsByPt_5_eta": lambda ev: ev.jets[5].lv.Eta() if len(ev.jets)>=6 else 0.0,
    "jetsByPt_0_phi": lambda ev: ev.jets[0].lv.Phi() if len(ev.jets)>=1 else 0.0,
    "jetsByPt_1_phi": lambda ev: ev.jets[1].lv.Phi() if len(ev.jets)>=2 else 0.0,
    "jetsByPt_2_phi": lambda ev: ev.jets[2].lv.Phi() if len(ev.jets)>=3 else 0.0,
    "jetsByPt_3_phi": lambda ev: ev.jets[3].lv.Phi() if len(ev.jets)>=4 else 0.0,
    "jetsByPt_4_phi": lambda ev: ev.jets[4].lv.Phi() if len(ev.jets)>=5 else 0.0,
    "jetsByPt_5_phi": lambda ev: ev.jets[5].lv.Phi() if len(ev.jets)>=6 else 0.0,
    "jetsByPt_0_mass": lambda ev: ev.jets[0].lv.M() if len(ev.jets)>=1 else 0.0,
    "jetsByPt_1_mass": lambda ev: ev.jets[1].lv.M() if len(ev.jets)>=2 else 0.0,
    "jetsByPt_2_mass": lambda ev: ev.jets[2].lv.M() if len(ev.jets)>=3 else 0.0,
    "jetsByPt_3_mass": lambda ev: ev.jets[3].lv.M() if len(ev.jets)>=4 else 0.0,
    "jetsByPt_4_mass": lambda ev: ev.jets[4].lv.M() if len(ev.jets)>=5 else 0.0,
    "jetsByPt_5_mass": lambda ev: ev.jets[5].lv.M() if len(ev.jets)>=6 else 0.0,
    "jetsByPt_0_pt": lambda ev: ev.jets[0].lv.Pt() if len(ev.jets)>=1 else 0.0,
    "jetsByPt_1_pt": lambda ev: ev.jets[1].lv.Pt() if len(ev.jets)>=2 else 0.0,
    "jetsByPt_2_pt": lambda ev: ev.jets[2].lv.Pt() if len(ev.jets)>=3 else 0.0,
    "jetsByPt_3_pt": lambda ev: ev.jets[3].lv.Pt() if len(ev.jets)>=4 else 0.0,
    "jetsByPt_4_pt": lambda ev: ev.jets[4].lv.Pt() if len(ev.jets)>=5 else 0.0,
    "jetsByPt_5_pt": lambda ev: ev.jets[5].lv.Pt() if len(ev.jets)>=6 else 0.0,
    "jetsByPt_0_btagCSV": lambda ev: ev.jets[0].btagDeepCSV if len(ev.jets)>=1 else 0.0,
    "jetsByPt_1_btagCSV": lambda ev: ev.jets[1].btagDeepCSV if len(ev.jets)>=2 else 0.0,
    "jetsByPt_2_btagCSV": lambda ev: ev.jets[2].btagDeepCSV if len(ev.jets)>=3 else 0.0,
    "jetsByPt_3_btagCSV": lambda ev: ev.jets[3].btagDeepCSV if len(ev.jets)>=4 else 0.0,
    "jetsByPt_4_btagCSV": lambda ev: ev.jets[4].btagDeepCSV if len(ev.jets)>=5 else 0.0,
    "jetsByPt_5_btagCSV": lambda ev: ev.jets[5].btagDeepCSV if len(ev.jets)>=6 else 0.0,
    "leps_0_pt": lambda ev: ev.leptons[0].lv.Pt(),
    "leps_1_pt": lambda ev: ev.leptons[1].lv.Pt(),
    "leps_0_eta": lambda ev: ev.leptons[0].lv.Eta(),
    "leps_1_eta": lambda ev: ev.leptons[1].lv.Eta(),
    "leps_0_phi": lambda ev: ev.leptons[0].lv.Phi(),
    "leps_0_mass": lambda ev: ev.leptons[0].lv.M(),
    "is_sl": lambda ev: ev.is_sl,
    "mem_DL_0w2h2t_p": lambda ev: ev.mem_DL_0w2h2t_p,
    "mem_SL_0w2h2t_p": lambda ev: ev.mem_SL_0w2h2t_p,
    "mem_SL_1w2h2t_p": lambda ev: ev.mem_SL_1w2h2t_p,
    "mem_SL_2w2h2t_p": lambda ev: ev.mem_SL_2w2h2t_p,
    "mem_DL_0w2h2t_sj_p": lambda ev: ev.mem_DL_0w2h2t_sj_p,
    "mem_SL_0w2h2t_sj_p": lambda ev: ev.mem_SL_0w2h2t_sj_p,
    "mem_SL_1w2h2t_sj_p": lambda ev: ev.mem_SL_1w2h2t_sj_p,
    "mem_SL_2w2h2t_sj_p": lambda ev: ev.mem_SL_2w2h2t_sj_p,
    "mem_DL_0w2h2t_sj_perm_higgs_p": lambda ev: ev.mem_DL_0w2h2t_sj_perm_higgs_p,
    "mem_SL_0w2h2t_sj_perm_higgs_p": lambda ev: ev.mem_SL_0w2h2t_sj_perm_higgs_p,
    "mem_SL_1w2h2t_sj_perm_higgs_p": lambda ev: ev.mem_SL_1w2h2t_sj_perm_higgs_p,
    "mem_SL_2w2h2t_sj_perm_higgs_p": lambda ev: ev.mem_SL_2w2h2t_sj_perm_higgs_p,
    "mem_SL_2w2h2t_sj_perm_top_p": lambda ev: ev.mem_SL_2w2h2t_sj_perm_top_p,
    "mem_SL_2w2h2t_sj_perm_tophiggs_p": lambda ev: ev.mem_SL_2w2h2t_sj_perm_tophiggs_p,
    "mem_FH_3w2h2t_p": lambda ev: ev.mem_FH_3w2h2t_p,
    "mem_FH_4w2h2t_p": lambda ev: ev.mem_FH_4w2h2t_p,
    "mem_FH_4w2h1t_p": lambda ev: ev.mem_FH_4w2h1t_p,
    "jetsByPt_0_qgl": lambda ev: ev.jetsByPt_0_qgl,
    "sixjetHT": lambda ev: sum([ev.jets[i].lv.Pt() for i in range(6)]),
    "centralitymass": lambda ev: ev.centralitymass,
    "min_dr_btag": lambda ev: ev.min_dr_btag,
    "mass_drpair_btag": lambda ev: ev.mass_drpair_btag,
    "mass_drpair_untag": lambda ev: ev.mass_drpair_untag,
    "mjjmin": lambda ev: ev.mjjmin,
    "log_mem_tth_3w2h2t": lambda ev: np.log10(ev.mem_tth_FH_3w2h2t_p) if ev.mem_tth_FH_3w2h2t_p>0 else 0.0,
    #"log_mem_tth_3w2h2t": lambda ev: np.log10(ev.mem_tth_FH_3w2h2t_p) if getattr(ev,"mem_tth_FH_3w2h2t_p",0)>0 else 0.0,
    "log_mem_tth_4w2h1t": lambda ev: np.log10(ev.mem_tth_FH_4w2h1t_p) if getattr(ev,"mem_tth_FH_4w2h1t_p",0)>0 else 0.0,
    "log_mem_tth_4w2h2t": lambda ev: np.log10(ev.mem_tth_FH_4w2h2t_p) if getattr(ev,"mem_tth_FH_4w2h2t_p",0)>0 else 0.0,
    "log_mem_ttbb_3w2h2t": lambda ev: np.log10(ev.mem_ttbb_FH_3w2h2t_p) if getattr(ev,"mem_ttbb_FH_3w2h2t_p",0)>0 else 0.0,
    "log_mem_ttbb_4w2h1t": lambda ev: np.log10(ev.mem_ttbb_FH_4w2h1t_p) if getattr(ev,"mem_ttbb_FH_4w2h1t_p",0)>0 else 0.0,
    "log_mem_ttbb_4w2h2t": lambda ev: np.log10(ev.mem_ttbb_FH_4w2h2t_p) if getattr(ev,"mem_ttbb_FH_4w2h2t_p",0)>0 else 0.0,
    #"log_mem_tth_3w2h2t": lambda ev: ev.log_mem_tth_3w2h2t,
    #"log_mem_tth_4w2h1t": lambda ev: ev.log_mem_tth_4w2h1t,
    #"log_mem_tth_4w2h2t": lambda ev: ev.log_mem_tth_4w2h2t,
    #"log_mem_ttbb_3w2h2t": lambda ev: ev.log_mem_ttbb_3w2h2t,
    #"log_mem_ttbb_4w2h1t": lambda ev: ev.log_mem_ttbb_4w2h1t,
    #"log_mem_ttbb_4w2h2t": lambda ev: ev.log_mem_ttbb_4w2h2t,
    "Wmass": lambda ev: ev.Wmass,
    "numJets": lambda ev: ev.numJets,
    "nBDeepCSVM": lambda ev: ev.nBDeepCSVM,
    "nBDeepFlavM" : lambda ev: ev.nBDeepFlavM,
    #"nBCSVM": lambda ev: ev.nBCSVM,
    "n_boosted_bjets": lambda ev: ev.n_boosted_bjets,
    "n_boosted_ljets": lambda ev: ev.n_boosted_ljets,
    "boosted": lambda ev: ev.boosted,
    "nPVs": lambda ev: ev.nPVs,
    "counting": 1.0,
    "mll": lambda ev: ev.mll,
    "met_pt": lambda ev: ev.met_pt,
    "met_phi": lambda ev: ev.met_phi,
    "ht": lambda ev: sum([jet.lv.Pt() for jet in ev.jets]),
    "nhiggsCandidate": lambda ev: len(ev.higgsCandidate),
    "higgsCandidate_msoftdrop": lambda ev: ev.higgsCandidate[0].msoftdrop if len(ev.higgsCandidate)>=1 else -10.0,
    "higgsCandidate_pt": lambda ev: ev.higgsCandidate[0].lv.Pt() if len(ev.higgsCandidate)>=1 else  -10.0,
    "higgsCandidate_eta": lambda ev: ev.higgsCandidate[0].lv.Eta() if len(ev.higgsCandidate)>=1 else  -10.0,
    "higgsCandidate_tau21": lambda ev: ev.higgsCandidate[0].tau21 if len(ev.higgsCandidate)>=1 else  -10.0,
    "higgsCandidate_bbtag": lambda ev: ev.higgsCandidate[0].bbtag if len(ev.higgsCandidate)>=1 else  -10.0,
    "higgsCandidate_btagL": lambda ev: max(ev.higgsCandidate[0].sj1btag,ev.higgsCandidate[0].sj2btag) if len(ev.higgsCandidate)>=1 else  -10.0,
    "higgsCandidate_btagSL": lambda ev: min(ev.higgsCandidate[0].sj1btag,ev.higgsCandidate[0].sj2btag) if len(ev.higgsCandidate)>=1 else  -10.0,
    "higgsCandidate_ptsjL": lambda ev: max(ev.higgsCandidate[0].sj1pt,ev.higgsCandidate[0].sj2pt) if len(ev.higgsCandidate)>=1 else  -10.0,
    "higgsCandidate_ptsjSL": lambda ev: min(ev.higgsCandidate[0].sj1pt,ev.higgsCandidate[0].sj2pt) if len(ev.higgsCandidate)>=1 else  -10.0,
    "ntopCandidate": lambda ev: len(ev.topCandidate),
    "topCandidate_mass": lambda ev: ev.topCandidate[0].lv.M() if len(ev.topCandidate)>=1 else -10.0,
    "topCandidate_pt": lambda ev: ev.topCandidate[0].lv.Pt() if len(ev.topCandidate)>=1 else  -10.0,
    "topCandidate_eta": lambda ev: ev.topCandidate[0].lv.Eta() if len(ev.topCandidate)>=1 else  -10.0,
    "topCandidate_tau32SD": lambda ev: ev.topCandidate[0].tau32SD if len(ev.topCandidate)>=1 else  -10.0,
    "topCandidate_fRec": lambda ev: ev.topCandidate[0].fRec if len(ev.topCandidate)>=1 else  -10.0,
    "topCandidate_delRopt": lambda ev: ev.topCandidate[0].delRopt if len(ev.topCandidate)>=1 else  -10.0,
    "topCandidate_btagL": lambda ev: max(ev.topCandidate[0].sj1btag,ev.topCandidate[0].sj2btag,ev.topCandidate[0].sj3btag) if len(ev.topCandidate)>=1 else  -10.0,
    "topCandidate_btagSL": lambda ev: min(ev.topCandidate[0].sj1btag,ev.topCandidate[0].sj2btag,ev.topCandidate[0].sj3btag) if len(ev.topCandidate)>=1 else  -10.0,
    "topCandidate_ptsjL": lambda ev: max(ev.topCandidate[0].sj1pt,ev.topCandidate[0].sj2pt,ev.topCandidate[0].sj3pt) if len(ev.topCandidate)>=1 else  -10.0,
    "topCandidate_ptsjSL": lambda ev: min(ev.topCandidate[0].sj1pt,ev.topCandidate[0].sj2pt,ev.topCandidate[0].sj3pt) if len(ev.topCandidate)>=1 else  -10.0,
    "minpt": lambda ev: ev.minpt,
    "minmass": lambda ev: ev.minmass,
    "avgpt": lambda ev: ev.avgpt,
    "avgmassbtag": lambda ev: ev.avgmassbtag,
    "avgmassnonbtag": lambda ev: ev.avgmassnonbtag,
    "avgjetmass": lambda ev: ev.avgjetmass,
    "massjetlep": lambda ev: ev.massjetlep,
    "avgbtag": lambda ev: ev.avgbtag,
    "avgbtagbtag": lambda ev: ev.avgbtagbtag,
    "avgdetabtag": lambda ev: ev.avgdetabtag,
    "avgdeta": lambda ev: ev.avgdeta,
    "avgdrbtag": lambda ev: ev.avgdrbtag,
    "avgdr": lambda ev: ev.avgdr,
    "avgdrbtagjet": lambda ev: ev.avgdrbtagjet,
    }

class Cut(object):
    """
    Defines a sequence of (variable, lower, upper) cuts
    that can be applied on a set of events
    """

    @staticmethod
    def string_to_cuts(s):
        cuts = []
        for cut_name, lower, upper in triplewise(s):
            cuts.append((cut_name, float(lower), float(upper)))
        return cuts

    @staticmethod
    def cuts_to_string(cuts):
        s = ""
        for cut_name, lower, upper in cuts:
            s += "{0} {1} {2}\n".format(cut_name, lower, upper)
        return s

    def __init__(self, *args, **kwargs):
        self.name = kwargs.get("name")
        self.sparsinator = kwargs.get("sparsinator", [])
        self.skim = kwargs.get("skim", None)

    @staticmethod
    def fromConfigParser(config, name):
        return Cut(
            name = name,
            sparsinator = Cut.string_to_cuts(config.get(name, "sparsinator").split()),
            skim = config.get(name, "skim")
        )

    def __str__(self):
        s = []
        for c in self.sparsinator:
            s += ["({1} <= {0} < {2})".format(*c)]
        return "AND".join(s)

    def __repr__(self):
        return str(self)

class Sample(object):
    def __init__(self, *args, **kwargs):

        #Flag to set whether in debug mode
        self.debug = kwargs.get("debug")

        #Name of sample, e.g. ttHTobb_M125_TuneCUETP8M2_ttHtranche3_13TeV-powheg-pythia8
        self.name = kwargs.get("name")

        #Schema of sample, e.g. mc, data, or mc_syst (MC that is a systematic variation)
        self.schema = kwargs.get("schema")

        #Flag if sample contains boosted information: true or false
        self.boosted = kwargs.get("boosted")

        #Name of the underlying event model, based in MEAnalysis/interface/EventModel.h
        self.treemodel = kwargs.get("treemodel")

        #Step2 files (tthbb13 output)
        self.files_load_step2 = kwargs.get("files_load_step2")

        #Step1 files (nanoAOD, optional)
        self.files_load_step1 = kwargs.get("files_load_step1", None)

        #postprocessing files (nanoAOD, optional)
        self.files_load_postproc = kwargs.get("files_load_postproc", None)

        self.step_size_sparsinator = int(kwargs.get("step_size_sparsinator"))
        self.debug_max_files = int(kwargs.get("debug_max_files"))
        self.tags = kwargs.get("tags", "").split()

        #Load the filenames for step2 (nanoAOD + tthbb13)
        #This can fail on the grid, where the stuff under src/MEAnalysis/gc is not available
        try:
            self.file_names = [getSitePrefix(fn) for fn in get_files(self.files_load_step2)]
        except Exception as e:
            LOG_MODULE_NAME.error("ERROR: could not load sample file {0}: {1}".format(self.files_load_step2, e))
            self.file_names = []

        #Load the filenames for step1 (nanoAOD)
        if self.files_load_step1 is None:
            self.file_names_step1 = self.file_names
        else:
            try:
                self.file_names_step1 = [getSitePrefix(fn) for fn in get_files(self.files_load_step1)]
            except Exception as e:
                LOG_MODULE_NAME.error("ERROR: could not load sample file {0}: {1}".format(self.files_load_step1, e))
                self.file_names_step1 = []

        self.file_names_postproc = None
        try:
            if self.files_load_postproc:
                self.file_names_postproc = [getSitePrefix(fn) for fn in get_files(self.files_load_postproc)]
        except IOError as e:
            LOG_MODULE_NAME.error("ERROR: could not load postprocessing file {0}: {1}".format(self.files_load_postproc, e))
            self.file_names_postproc = []

        #Limit list of files in debug mode
        if self.debug:
            self.file_names = self.file_names[:self.debug_max_files]

        self.ngen = int(kwargs.get("ngen"))
        self.xsec = kwargs.get("xsec")
        self.step1_tree_name = kwargs.get("step1_tree_name")


        #Normalization factors for PDF, muR, muF scale uncertainties
        #if ("ttH" in kwargs.get("name") or "TTTo" in kwargs.get("name")) and (not "up" in kwargs.get("name") and not "down" in kwargs.get("name")):
        #    self.normmuFup = kwargs.get("normmuFup")
        #    self.normmuFdown = kwargs.get("normmuFdown")
        #    self.normmuRup = kwargs.get("normmuRup")
        #    self.normmuRdown = kwargs.get("normmuRdown")

        #else:
        #    self.normmuFup = 1
        #    self.normmuFdown = 1
        #    self.normmuRup = 1
        #    self.normmuRdown = 1

        
    @staticmethod
    def fromConfigParser(config, sample_name):
        if ("ttH" in sample_name or "TTTo" in sample_name) and (not "up" in sample_name and not "down" in sample_name):
            sample = Sample(
                debug = config.getboolean("general", "debug"),
                name = sample_name,
                files_load_step2 = config.get(sample_name, "files_load_step2"),
                files_load_step1 = config.get(sample_name, "files_load_step1"),
                files_load_postproc = config.get(sample_name, "files_load_postproc"),
                schema = config.get(sample_name, "schema"),
                boosted = config.getboolean(sample_name, "boosted"),
                treemodel = config.get(sample_name, "treemodel"),
                step_size_sparsinator = config.get(sample_name, "step_size_sparsinator"),
                debug_max_files = config.get(sample_name, "debug_max_files"),
                ngen = config.getfloat(sample_name, "ngen_weight"),
                step1_tree_name = config.get(sample_name, "step1_tree_name"),
                xsec = config.getfloat(sample_name, "xsec"),
                tags = config.get(sample_name, "tags"),
                #normmuFup = config.getfloat(sample_name, "normmuFup"),
                #normmuFdown = config.getfloat(sample_name, "normmuFdown"),
                #normmuRup = config.getfloat(sample_name, "normmuRup"),
                #normmuRdown = config.getfloat(sample_name, "normmuRdown"),
            )   
        else:
            sample = Sample(
                debug = config.getboolean("general", "debug"),
                name = sample_name,
                files_load_step2 = config.get(sample_name, "files_load_step2"),
                files_load_step1 = config.get(sample_name, "files_load_step1"),
                files_load_postproc = config.get(sample_name, "files_load_postproc"),
                schema = config.get(sample_name, "schema"),
                boosted = config.getboolean(sample_name, "boosted"),
                treemodel = config.get(sample_name, "treemodel"),
                step_size_sparsinator = config.get(sample_name, "step_size_sparsinator"),
                debug_max_files = config.get(sample_name, "debug_max_files"),
                ngen = config.getfloat(sample_name, "ngen_weight"),
                step1_tree_name = config.get(sample_name, "step1_tree_name"),
                xsec = config.getfloat(sample_name, "xsec"),
                tags = config.get(sample_name, "tags"),
            )   
        return sample

    def __repr__(self):
        return "Sample(name={0})".format(self.name)

class HistogramOutput:
    def __init__(self, hist, func, cut_name):
        self.hist = hist
        self.func = func
        self.cut_name = cut_name

    def cut(self, event):
        return event.cuts.get(self.cut_name, False)

    def fill(self, event, weight = 1.0, dooverflow = False):

        #make sure underflow is filled to first visible bin and overflow to last visible
        #Not for tagger-related variables, don't wan't default value to be filled in histogram.
        val = self.func(event)
        if dooverflow == True:
            if val < self.hist.GetBinLowEdge(1):
                val = self.hist.GetBinLowEdge(1)
            if val >= self.hist.GetBinLowEdge(self.hist.GetNbinsX()+1):
                val = self.hist.GetBinLowEdge(self.hist.GetNbinsX())
        
        if weight == 1.0:
            self.hist.Fill(val)
        else:
            self.hist.Fill(val, weight)

class CategoryCut:
    def __init__(self, cuts):
        self.cuts = cuts
            
    def cut(self, event):
        ret = True
        for cut in self.cuts:

            for cname, clow, chigh in cut.sparsinator:
                #if "jetsByPt" in cname:
                #    vint = getattr(event, "jets")
                #    if len(vint) > 5:
                #        v = vint[5].lv.Pt()
                #    else:
                #        v = 0
                #else:
                v = getattr(event, cname)
                ret = ret and (v >= clow and v < chigh)
                if not ret:
                    return False
        return ret

class Process(object):
    """
    Defines how an input sample should be mapped to an output histogram.
    Possibly applies cuts on the event to separate a sample into processes
    based on some event-level quantity such as ttCls
    """
    def __init__(self, *args, **kwargs):
        #Name of the input sample
        self.input_name = kwargs.get("input_name")
        #Name of the output process
        self.output_name = kwargs.get("output_name")

        #Any cuts to apply on the input sample in order to generate this process
        self.cuts = kwargs.get("cuts", [])
        self.xs_weight = kwargs.get("xs_weight", 1.0)
        self.full_name = " ".join([self.input_name, self.output_name, ",".join([c.name for c in self.cuts])])

        #extra category name, in case you want to make a distinction
        self.category_name = kwargs.get("category_name", "")

    def __repr__(self):
        s = "Process(input_name={0}, output_name={1}, cuts={2})".format(self.input_name, self.output_name, self.cuts)
        return s

    def output_path(self, category_name, discriminator_name, systematic_string=None):
        to_join = [self.output_name, category_name + self.category_name, discriminator_name]
        if systematic_string:
            to_join += [systematic_string]
        name = "__".join(to_join)
        return name
    
    def createOutputs(self, outdir, analysis, systematics, outfilter=None):
        """Creates an output dictionary with fillable objects in TDirectories based on categories and systematics. 
        
        Args:
            outdir (TYPE): Description
            analysis (TYPE): Description
            sample (TYPE): Description
            systematics (list of string): list of systematics for which to create outputs
        
        Returns:
            dict of string->output: Dictionary of fillable outputs
        """
    
        outdict_syst = {}
        outdict_cuts = {}
    
        ROOT.TH1.AddDirectory(False)
    
        for syst in systematics:
            outdict_syst[syst] = {}
            syst_str = syst
            if syst == "nominal":
                syst_str = None
            #for every category in every group
            for group_name in analysis.groups.keys():
                for category in analysis.groups[group_name]:
                    #create a new cut object that applies both the Category and Process cuts
                    category_cut = CategoryCut(
                        category.cuts
                    )
                    cut_name = (category.full_name, self.full_name)
                    if not outdict_cuts.has_key(cut_name):
                        outdict_cuts[cut_name] = category_cut
                    name = self.output_path(category.name, category.discriminator.name, syst_str)

                    #optionally create only a subset of categories
                    if outfilter:
                        if not fnmatch.fnmatch(name, outfilter):
                            LOG_MODULE_NAME.info("filtering {0} with {1}".format(name, outfilter))
                            continue

                    if not outdict_syst[syst].has_key(name):
                        h = category.discriminator.get_TH1(name)
                        outdict_syst[syst][name] = HistogramOutput(
                            h,
                            FUNCTION_TABLE[category.discriminator.func],
                            cut_name,
                        )
        return outdict_syst, outdict_cuts

class SystematicProcess(Process):
    def __init__(self, *args, **kwargs):
        super(SystematicProcess, self).__init__(self, *args, **kwargs)
        self.systematic_name = kwargs.get("systematic_name")

    def output_path(self, category_name, discriminator_name, systematic_string=None):
        return super(SystematicProcess, self).output_path(
            category_name,
            discriminator_name,
            self.systematic_name
        )
    
    def createOutputs(self, outdir, analysis, systematics, outfilter=None):
        outdict_syst = {"nominal": {}}
        outdict_cuts = {}
    
        ROOT.TH1.AddDirectory(False)
        for group_name in analysis.groups.keys():
            for category in analysis.groups[group_name]:
                #create a new cut object that applies both the Category and Process cuts
                category_cut = CategoryCut(
                    category.cuts
                )
                cut_name = (category.full_name, self.full_name)
                if not outdict_cuts.has_key(cut_name):
                    outdict_cuts[cut_name] = category_cut
                name = self.output_path(category.name, category.discriminator.name)
                
                #optionally create only a subset of categories
                if outfilter:
                    if not fnmatch.fnmatch(name, outfilter):
                        LOG_MODULE_NAME.info("filtering {0} with {1}".format(name, outfilter))
                        continue
                
                if not outdict_syst["nominal"].has_key(name):
                    h = category.discriminator.get_TH1(name)
                    outdict_syst["nominal"][name] = HistogramOutput(
                        h,
                        FUNCTION_TABLE[category.discriminator.func],
                        cut_name,
                    )
        return outdict_syst, outdict_cuts
    
    def __repr__(self):
        s = "SystematicProcess(input_name={0}, output_name={1}, systematic_name={2})".format(
            self.input_name,
            self.output_name,
            self.systematic_name
        )
        return s
            
class DataProcess(Process):
    def __init__(self, *args, **kwargs):
        super(DataProcess, self).__init__(self, *args, **kwargs)
        self.lumi = kwargs.get("lumi", 1.0)

class Histogram:
    def __init__(self, name, func, bins):
        self.name = name
        self.func = func
        self.bins = bins

    @staticmethod
    def from_string(s):
        name, func, bins = s.split()
        return Histogram(name, func, bins)

    def to_string(self):
        return "{0} {1} {2}".format(self.name, self.func, self.bins)

    def get_binning(self):
        bs = self.bins.split(",")
        if len(bs) == 3:
            return int(bs[0]), float(bs[1]), float(bs[2])
        else:
            raise Exception("Unknown binning spec")

    def get_TH1(self, name):
        th = ROOT.TH1D(name, name, *self.get_binning())
        th.Sumw2()
        return th

class Category:
    def __init__(self, **kwargs):
        self.name = kwargs.get("name")
        self.discriminator = kwargs.get("discriminator")
        self.full_name = "{0}__{1}".format(self.name, self.discriminator.name)
        self.rebin = kwargs.get("rebin", 1)
        self.do_limit = kwargs.get("do_limit", True)

        self.scale_uncertainties = kwargs.get("scale_uncertainties", {})
        self.shape_uncertainties = kwargs.get("shape_uncertainties", {})

        self.cuts = kwargs.get("cuts", [])

        self.processes = kwargs.get("processes", [])
        self.data_processes = kwargs.get("data_processes", [])
        #self.lumi = sum([d.lumi for d in self.data_samples])

        self.signal_processes = kwargs.get("signal_processes", [])
        self.out_processes_mc = list(set([s.output_name for s in self.processes]))
        self.out_processes_data = list(set([s.output_name for s in self.data_processes]))
        self.out_processes = self.out_processes_mc + self.out_processes_data

        #[process][syst]
        self.shape_uncertainties = {}
        self.scale_uncertainties = {}

        #[syst] -> scale factor, common for all processes
        self.common_shape_uncertainties = kwargs.get("common_shape_uncertainties", {})
        self.common_scale_uncertainties = kwargs.get("common_scale_uncertainties", {})
        for proc in self.out_processes_mc:
            self.shape_uncertainties[proc] = {}
            self.scale_uncertainties[proc] = {}
            for systname, systval in self.common_shape_uncertainties.items():
                self.shape_uncertainties[proc][systname] = systval
            for systname, systval in self.common_scale_uncertainties.items():
                self.scale_uncertainties[proc][systname] = systval

        #Load the process-dependent shape uncertainties
        self.proc_shape_uncertainties = kwargs.get("shape_uncertainties", {})
        for proc, v in self.proc_shape_uncertainties.items():
            if proc not in self.shape_uncertainties.keys():
                LOG_MODULE_NAME.warning("Skipping %s for additional shape uncertainties", proc)
                continue
            self.shape_uncertainties[proc].update(v)

            
        #Load the process-dependent scale uncertainties
        self.proc_scale_uncertainties = kwargs.get("scale_uncertainties", {})
        for proc, v in self.proc_scale_uncertainties.items():
            if proc in self.scale_uncertainties:
                self.scale_uncertainties[proc].update(v)
            else:
                LOG_MODULE_NAME.debug(
                    "Could not find process {0} to update scale "
                    "uncertainties for category={1}, uncertainty={2} "
                    "make sure the category definition contains the process".format(proc, self.name, v)
                )

    
    def __str__(self):
        s = "Category(full_name={0})".format(
            self.full_name,
        )
        return s

    # # Define equality via the representation string
    # def __eq__(self,other):
    #     return self.__repr__() == other.__repr__()

    # # hash(object) = hash(representation(object))
    # def __hash__(self):
    #     return self.__repr__().__hash__()


class Analysis:
    def __init__(self, **kwargs):
        self.mem_python_config = kwargs.get("mem_python_config")
        self.config = kwargs.get("config")
        self.debug = kwargs.get("debug", False)
        self.samples = kwargs.get("samples", [])
        self.cuts = kwargs.get("cuts", {})
        self.process_lists = kwargs.get("process_lists")
        self.processes = kwargs.get("processes")
        self.processes_unsplit = kwargs.get("processes_unsplit")
        self.categories = kwargs.get("categories")

        # groups represent calls to combine, i.e. 
        # {"myCombination1": ["cat1", "cat2"] }
        # will calculate the combined limit myCombination1 of cat1 and cat2 
        self.groups = kwargs.get("groups", {})
        self.do_fake_data = kwargs.get("do_fake_data", False)
        self.do_stat_variations = kwargs.get("do_stat_variations", False)
        self.sample_d = dict([(s.name, s) for s in self.samples])

        LOG_MODULE_NAME.info("Created analysis with samples: {0}".format(",".join([s.name for s in self.samples])))
        
    def get_sample(self, sample_name):
        return self.sample_d[sample_name]

    def __repr__(self):
        s = "Analysis(processes={0}, categories={1}, groups={2})".format(
            len(self.processes),
            len(self.categories),
            len(self.groups),
        )
        return s

    @staticmethod
    def deserialize(filename):
        fi = open(filename, "rb")
        an = pickle.load(fi)
        fi.close()
        return an

    def serialize(self, filename):
        fi = open(filename, "wb")
        pickle.dump(self, fi)
        fi.close()

    @staticmethod
    def getConfigParser(config_file_name):
        config = ConfigParser.SafeConfigParser()
        config.optionxform = str # Turn on case-sensitivity
        config.read(config_file_name)
        if config.has_option("importconfig","parent"):
            parent_file_name = config.get("importconfig","parent").replace("$CMSSW_BASE", os.environ["CMSSW_BASE"])
            parent = ConfigParser.SafeConfigParser()
            parent.optionxform = str # Turn on case-sensitivity
            parent.read(parent_file_name) 
            for s in config.sections():
                if s=="importconfig":
                    continue
                for (i,v) in config.items(s):
                    if parent.get(s,i):
                        parent.set(s, i, v)
            return parent
        return config

    def __deepcopy__(self, memo):
        return self
    
def make_csv_categories_abstract(di):

    import csv
    with open('analysis_specs.csv', 'w') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=';')    

        csvwriter.writerow(['specfile', 'analysis', 'category'])
    
        # We want the analysis specification file
        # as make_csv is called from there we just take the filename of the outer stack
        import inspect
        analysis_spec_file = os.path.abspath(inspect.getouterframes(inspect.currentframe())[1][1])

        for analysis_name, analysis in di.iteritems():        

            unique_cat_names = list(set(c.name for c in analysis.categories))
            for cat_name in unique_cat_names:
                csvwriter.writerow([analysis_spec_file, analysis_name, cat_name])

    return [1]

def make_csv_groups_abstract(di):

    import csv
    with open('analysis_groups.csv', 'w') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=';')    

        csvwriter.writerow(['specfile', 'analysis', 'group'])
    
        # We want the analysis specification file
        # as make_csv is called from there we just take the filename of the outer stack    
        import inspect
        analysis_spec_file = os.path.abspath(inspect.getouterframes(inspect.currentframe())[1][1])

        for analysis_name, analysis in di.iteritems():        
            for group_name in analysis.groups.keys():
                csvwriter.writerow([analysis_spec_file, analysis_name, group_name])

    return [1]
