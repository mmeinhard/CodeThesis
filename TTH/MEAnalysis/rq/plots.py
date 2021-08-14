import socket
from redis import Redis
from rq import Queue, get_failed_queue
from TTH.Plotting.Datacards.AnalysisSpecificationFromConfig import analysisFromConfig
import os

import matplotlib
from matplotlib import rc
#temporarily disable true latex for fast testing
rc('text', usetex=False)
matplotlib.use('PS') #needed on T3

import TTH.Plotting.joosep.plotlib as plotlib #heplot, 
from launcher import make_workdir, waitJobs
from job import plot

#FIXME: configure all these via conf file!
procs_names = [
    ("ttH_hbb", "tt+H(bb)"),
    ("ttH_nonhbb", "tt+H(non-bb)"),
    ("ttbarOther", "tt+light"),
    ("ttbarPlusBBbar", "tt+bb"),
    ("ttbarPlus2B", "tt+2b"),
    ("ttbarPlusB", "tt+b"),
    ("ttbarPlusCCbar", "tt+cc"),
    ("diboson", "diboson"),
    ("stop", "single top"),
    ("ttv", "tt+V"),
    ("wjets", "w+jets"),
    ("dy", "dy")
]
procs = [x[0] for x in procs_names]

syst_pairs = [
    ("__CMS_puUp", "__CMS_puDown"),
#    ("__CMS_scale_jUp", "__CMS_scale_jDown"),
    ("__CMS_scaleFlavorQCD_jUp", "__CMS_scaleFlavorQCD_jDown"),
    ("__CMS_res_jUp", "__CMS_res_jDown"),
    ("__CMS_ttH_CSVcferr1Up", "__CMS_ttH_CSVcferr1Down"),
    ("__CMS_ttH_CSVcferr2Up", "__CMS_ttH_CSVcferr2Down"),
    ("__CMS_ttH_CSVhfUp", "__CMS_ttH_CSVhfDown"),
    ("__CMS_ttH_CSVhfstats1Up", "__CMS_ttH_CSVhfstats1Down"),
    ("__CMS_ttH_CSVhfstats2Up", "__CMS_ttH_CSVhfstats2Down"),
    ("__CMS_ttH_CSVjesUp", "__CMS_ttH_CSVjesDown"),
    ("__CMS_ttH_CSVlfUp", "__CMS_ttH_CSVlfDown"),
    ("__CMS_ttH_CSVlfstats1Up", "__CMS_ttH_CSVlfstats1Down"),
    ("__CMS_ttH_CSVlfstats2Up", "__CMS_ttH_CSVlfstats2Down"),
    ("__CMS_effTrigger_eUp", "__CMS_effTrigger_eDown"),
    ("__CMS_effTrigger_mUp", "__CMS_effTrigger_mDown"),
    ("__CMS_effTrigger_eeUp", "__CMS_effTrigger_emDown"),
    ("__CMS_effTrigger_mmUp", "__CMS_effTrigger_mmDown"),
    ("__CMS_effTrigger_emUp", "__CMS_effTrigger_emDown"),
    ("__CMS_ttjetsfsrUp", "__CMS_ttjetsfsrDown"),
    ("__CMS_ttjetsisrUp", "__CMS_ttjetsisrDown"),
    ("__CMS_ttjetstuneUp", "__CMS_ttjetstuneDown"),
    ("__CMS_ttjetshdampUp", "__CMS_ttjetshdampDown"),
    ("__CMS_ttH_scaleMEUp", "__CMS_ttH_scaleMEDown"),
]

def get_base_plot(basepath, outpath, analysis, category, variable):
    s = "{0}/{1}/{2}".format(basepath, analysis, category)
    ret = {
        "infile": s + ".root",
        "histname": "__".join([category, variable]),
        "category": category,
        "outname": os.path.abspath("/".join([outpath, category, variable])),
        "procs": procs_names,
        "signal_procs": ["ttH_hbb", "ttH_nonhbb"],
        "dataname": "data",
        "rebin": 1,
        "xlabel": plotlib.varnames[variable] if variable in plotlib.varnames.keys() else "PLZ add {0} to Varnames in plotlib.py".format(variable),
        "xunit": plotlib.varunits[variable] if variable in plotlib.varunits.keys() else "",
        "colors": plotlib.colors,
        "do_legend": True,
        "legend_loc": "best",
        "legend_fontsize": 10,
        "show_overflow": True,
        "title_extended": "\n" + category + r", $35.9\ \mathrm{fb}^{-1}$ (13 TeV)",
        "systematics": syst_pairs,
        "do_syst": True,
        "blindFunc": "blind_mem" if "mem" in variable else "no_blind",
        #"blindFunc": "no_blind",
        "do_tex": False 
    }
    if variable in ["numJets", "nBCSVM", "ht", "met_pt"] or variable.endswith("_pt"):
        ret["do_log"] = True
    return ret


def run_plots(workdir, analysis, path_to_files, redis_conn, qmain, qfail):
    all_jobs = []
    for cat in analysis.categories:
        outpath = os.path.abspath("/".join([workdir, "plots", cat.name, cat.discriminator.name]))
        if not os.path.exists(outpath):
            os.makedirs(outpath)

        all_jobs += [
            qmain.enqueue_call(
                func=plot,
                args=[
                    get_base_plot(
                        path_to_files, 
                        os.path.join(workdir, "plots"),
                        "",
                        cat.name,
                        cat.discriminator.name
                    )
                ],
                timeout = 20*60,
                result_ttl = 60*60,
                meta = {"retries": 0, "args": ""},
            )
        ]

    waitJobs(all_jobs, redis_conn, qmain, qfail)
    return [j.result for j in all_jobs]

if __name__ == "__main__":

    from TTH.Plotting.Datacards.AnalysisSpecificationClasses import Analysis


    import argparse
    parser = argparse.ArgumentParser(
        description='Runs the workflow'
    )
    parser.add_argument(
        '--config',
        action = "store",
        help = "Analysis configuration pickle file",
        type = str,
        required = True
    )
    parser.add_argument(
        '--hostname',
        action = "store",
        help = "Redis hostname",
        type = str,
        default = socket.gethostname()
    )
    parser.add_argument(
        '--port',
        action = "store",
        help = "Redis port",
        type = int,
        default = 6379
    )
    args = parser.parse_args()

    redis_conn = Redis(host=args.hostname, port=args.port)
    qmain = Queue("default", connection=redis_conn, async=False)  # no args implies the default queue
    qfail = get_failed_queue(redis_conn)

    analysis = Analysis.deserialize(args.config)

    workdir = make_workdir()

    run_plots(workdir, analysis, os.path.join(os.path.dirname(args.config), "categories"), redis_conn, qmain, qfail)
