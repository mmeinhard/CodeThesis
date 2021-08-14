import matplotlib
matplotlib.use("Agg")
import ROOT
import matplotlib.pyplot as plt
#import rootpy
#from rootpy.io import root_open

from matplotlib import rc
rc('font',**{'family':'sans-serif','sans-serif':['Helvetica']})
## for Palatino and other serif fonts use:
#rc('font',**{'family':'serif','serif':['Palatino']})
rc('text', usetex=True)
matplotlib.rc("axes", labelsize=24)
matplotlib.rc("axes", titlesize=26)

colors = {
    "ttbarOther": (251, 102, 102),
    "ttbarPlusCCbar": (204, 2, -0),
    "ttbarPlusB": (153, 51, 51),
    "ttbarPlusBBbar": (102, 0, 0),
    "ttbarPlus2B": (80, 0, 0),
    "ttH": (44, 62, 167),
    "ttH_hbb": (44, 62, 167),
    "ttH_nonhbb": (90, 115, 203),
    "diboson": (42, 100, 198),
    "wjets": (102, 201, 77),
    "zjets": (102, 201, 77),
    "singlet": (235, 73, 247),
    "ttv": (204, 204, 251),
    "qcd": (102, 201, 77),
    "qcd_ht300to500"   : (102, 201, 76),
    "qcd_ht500to700"   : (102, 201, 79),
    "qcd_ht700to1000"  : (102, 201, 80),
    "qcd_ht1000to1500" : (102, 201, 81),
    "qcd_ht1500to2000" : (102, 201, 82),
    "qcd_ht2000toinf"  : (102, 201, 83),
    "dy": (0, 100, 0),
    "other": (251, 73, 255),
}
for cn, c in colors.items():
    colors[cn] = (c[0]/255.0, c[1]/255.0, c[2]/255.0)

cat_names = [ 
    ("sl_jge6_tge4__mem_SL_2w2h2t_p", "sl: $\geq$6 jets, $\geq$4 b-tags"),
    ("sl_jge6_t3__btag_LR_4b_2b_btagCSV_logit", "sl: $\geq$6 jets, 3 b-tags"),
    ("sl_j5_tge4__mem_SL_1w2h2t_p", "sl: 5 jets, $\geq$4 b-tags"),
    ("sl_j5_t3__btag_LR_4b_2b_btagCSV_logit", "sl: 5 jets, 3 b-tags"),
    ("sl_j4_tge4__mem_SL_0w2h2t_p", "sl: 4 jets, $\geq$4 b-tags"),
    ("sl_j4_t3__btag_LR_4b_2b_btagCSV_logit", "sl: 4 jets, 3 b-tags"),
    ("dl_jge4_tge4__mem_DL_0w2h2t_p", "dl: $\geq$4 jets, $\geq$4 b-tags"),
    ("dl_jge4_t3__btag_LR_4b_2b_btagCSV_logit", "dl: $\geq$4 jets, 3 b-tags"),
    ("sl_jge6_tge4_sj_only__mem_SL_2w2h2t_sj_p", "sl: $\geq$6 jets, $\geq$4 b-tags, SJ"),
    ("sl_j5_tge4_sj_only__mem_SL_1w2h2t_sj_p", "sl: 5 jets, $\geq$4 b-tags, SJ"),
    ("sl_j4_tge4_sj_only__mem_SL_0w2h2t_sj_p", "sl: 4 jets, $\geq$4 b-tags, SJ"),
    ("dl_jge4_tge4_sj_only__mem_DL_0w2h2t_sj_p", "dl: $\geq$4 jets, $\geq$4 b-tags, SJ")
]

cat = [x[0] for x in cat_names]
print cat

procs_names = [
    ("ttH_hbb", "tt+H(bb)"),
    ("ttH_nonhbb", "tt+H(non-bb)"),
    ("ttbarOther", "tt+light"),
    ("ttbarPlusBBbar", "tt+bb"),
    ("ttbarPlus2B", "tt+2b"),
    ("ttbarPlusB", "tt+b"),
    ("ttbarPlusCCbar", "tt+cc"),
    ("diboson", "diboson"),
    ("singlet", "single top"),
    ("ttv", "tt+V"),
    ("wjets", "w+jets"),
    ("dy", "dy")
]
procs = [x[0] for x in procs_names]

color_list = [colors[i] for i in procs] 

# function to get the post-cut yields 
def post_cut(path, path2, cat, procs):

    N = {} 

    if not "sj" in cat:
        f = ROOT.TFile(path, "READ")
    else:
        f = ROOT.TFile(path2, "READ")

    for i in procs:

        if i=="wjets" and (cat !="sl_j5_t3" or cat !="sl_j4_t3"):
            N[i] = 0

        else: 
            if i == "ttH_nonhbb":
                pat = i + "__" + cat
                h = f.Get(pat.replace("ttH_nonhbb","ttH_hcc")).Clone()
                h2 = f.Get(pat.replace("ttH_nonhbb","ttH_hzz")).Clone()
                h3 = f.Get(pat.replace("ttH_nonhbb","ttH_hww")).Clone()
                h4 = f.Get(pat.replace("ttH_nonhbb","ttH_htt")).Clone()
                h5 = f.Get(pat.replace("ttH_nonhbb","ttH_hgg")).Clone()
                h6 = f.Get(pat.replace("ttH_nonhbb","ttH_hgluglu")).Clone()
                h7 = f.Get(pat.replace("ttH_nonhbb","ttH_hzg")).Clone()
                h.Add(h2)
                h.Add(h3)
                h.Add(h4)
                h.Add(h5)
                h.Add(h6)
                h.Add(h7)
            elif i == "ttv":
                pat = i + "__" + cat
                h = f.Get(pat.replace("ttv","ttbarZ")).Clone()
                h2 = f.Get(pat.replace("ttv","ttbarW")).Clone()
                h.Add(h2)
            elif i == "dy":
                pat = i + "__" + cat
                h = f.Get(pat.replace("dy","wjets")).Clone()
                h2 = f.Get(pat.replace("dy","zjets")).Clone()
                h.Add(h2)
            else:
                #print i + "__" + cat
                h = f.Get(i + "__" + cat)
            ent = h.Integral()
        
            N[i] = ent

    #print N
    return N

# function to plot pie charts
def pie(path, path2, cat, procs, cat_names = cat_names, procs_names = procs_names, color_list = color_list):
    matplotlib.figure.SubplotParams(wspace=0.25)
    #fig, axes = plt.subplots(nrows = 4, ncols = 2, figsize=(8,16))
    #fig, axes = plt.subplots(nrows = 2, ncols = 4, figsize=(16,8))
    fig, axes = plt.subplots(nrows = 4, ncols = 3, figsize=(15,22))

    for ax, j in zip(axes.flat[0:], cat):

        ax.set_title(cat_names[cat.index(j)][1], )
        N = post_cut(path, path2, j, procs)
        sizes = [N[i] for i in procs] 
        patches, texts = ax.pie(sizes, colors = color_list)
        ax.axis('equal')

    names = [x[1] for x in procs_names]
    #lgd = fig.legend(patches, names, bbox_to_anchor=(1.45,1.0), ncol = 1, prop={'size': 24})
    #lgd = fig.legend(patches, names, bbox_to_anchor = (.175, 0.01), loc="lower left", ncol = 5, prop={'size': 24})
    lgd = fig.legend(patches, names, bbox_to_anchor = (.175, 0.01), loc="lower left", ncol = 4, prop={'size': 24})
    #plt.show()
    plt.tight_layout()
    #plt.show()
    #plt.savefig("pie.pdf", bbox_inches = 'tight', pad_inches=0.4)
    plt.savefig("pie.pdf", bbox_inches = 'tight', pad_inches=1.8)
    #plt.savefig("pie.pdf")
    
if __name__ == "__main__":

    path = "/work/mameinha/tth/gc/sparse/Jul30_2DFactor_SLDLResolved.root"
    path2 = "/work/mameinha/tth/gc/sparse/Aug17_2DFactor_BoostedV2.root"
    pie(path, path2, cat, procs)

