import json, copy, os, imp, multiprocessing, sys
import sparse, ROOT
import logging
from utils import fakeData
import os
import os.path
import fnmatch
import time
import itertools
import gc

# #Nota bene: this is very important!
# #need to store histograms in memory, not on disk
# ROOT.TH1.AddDirectory(False)
# ROOT.gROOT.SetBatch(True)

def make_datacard(analysis, categories, outdir, hdict):
    #split the big dictionary to category-based dictionaries
    #produce the event counts per category
    logging.getLogger('MakeCategory').info("main: producing event counts")
    event_counts = {}
    hdict_cat = {}
    for cat in categories:
        event_counts[cat.full_name] = {}
        hdict_cat[cat.full_name] = {}
        logging.getLogger('MakeCategory').info("category {0} with processes {1}".format(cat.full_name, cat.out_processes))
        for proc in cat.out_processes:
            k = "{0}__{1}__{2}".format(
                proc, cat.name, cat.discriminator.name
            )
            logging.getLogger('MakeCategory').debug("getting {0}".format(k))
            v = 0.0
            if hdict.has_key(k):
                v = hdict[k].Integral()
                if not hdict_cat[cat.full_name].has_key(k):
                    hdict_cat[cat.full_name][k] = hdict[k].Clone()
                else:
                    hdict_cat[cat.full_name][k].Add(hdict[k])
                logging.getLogger('MakeCategory').debug("I={0:.2f} N={1:.2f}".format(
                    hdict[k].Integral(), hdict[k].GetEntries())
                )
            else:
                logging.getLogger('MakeCategory').error("didn't find key {0}".format(k))
            if not event_counts[cat.full_name].has_key(proc):
                event_counts[cat.full_name][proc] = 0.0
            event_counts[cat.full_name][proc] += v

            for syst_key in filter(lambda x: x.startswith(k), hdict.keys()):
                logging.getLogger('MakeCategory').debug("getting {0} I={1:.2f} N={2:.2f}".format(
                    syst_key, hdict[syst_key].Integral(), hdict[syst_key].GetEntries()
                ))
                hdict_cat[cat.full_name][syst_key] = hdict[syst_key]

        #Remove processes that don't have any prediction
        good_procs = []
        for proc in cat.out_processes_mc:
            if event_counts[cat.full_name][proc] > 0.0:
                good_procs += [proc]
        cat.out_processes_mc = good_procs

    #catname -> file name
    category_files = {}

    #save the histograms into per-category files
    logging.getLogger('MakeCategory').info("main: saving {0} categories".format(len(categories)))
    for catname in hdict_cat.keys():
        hfile = os.path.join(outdir, "{0}.root".format(catname))
        logging.getLogger('MakeCategory').info("saving {0} histograms to {1}".format(
            len(hdict_cat[catname]), hfile)
        )
        category_files[catname] = hfile
        sparse.save_hdict(hfile, hdict_cat[catname])
    
    #add the fake data
    if analysis.do_fake_data:
        logging.getLogger('MakeCategory').info("main: adding fake data")
        for cat in categories:
            hfile = category_files[cat.full_name]
            tf = ROOT.TFile(hfile, "UPDATE")
            fakeData(tf, tf, [cat])
            tf.Close()
    else:
        for cat in categories:
            tf = ROOT.TFile(category_files[cat.full_name], "UPDATE")
            h = tf.Get("data__" + cat.full_name)
            print h
            h2 = h.Clone("data_obs__" + cat.full_name)
            tf.Write()
            tf.Close()


    #add the stat variations
    if analysis.do_stat_variations:
        logging.getLogger('MakeCategory').info("main: adding stat variations")
        from utils import makeStatVariations
        for cat in categories:
            hfile = category_files[cat.full_name]
            tf = ROOT.TFile(hfile, "UPDATE")
            stathist_names = makeStatVariations(tf, tf, [cat])
            tf.Close()
            
            #add the statistical uncertainties to the datacard specification
            for proc in cat.out_processes_mc:
                for syst in stathist_names[cat.full_name][proc]:
                    cat.shape_uncertainties[proc][syst] = 1.0
    
    from utils import PrintDatacard
    #make combine datacards (.txt) for individual categories 
    for cat in categories:
        fn = os.path.join(outdir, "shapes_{0}.txt".format(cat.full_name))
        logging.getLogger('MakeCategory').debug("main: writing shape file {0}".format(fn))
        dcof = open(fn, "w")
        PrintDatacard([cat], event_counts, category_files, dcof)
        dcof.write("# execute with\n")
        dcof.write("# combine -n {0} -M Asymptotic -t -1 {1}\n".format(cat.name, os.path.basename(fn)))
        dcof.close()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    import argparse
    parser = argparse.ArgumentParser(
        description='Creates datacards in categories based on a sparse histogram'
    )
    parser.add_argument(
        '--rootfile',
        action = "store",
        help = "Input root file",
        type = str,
        required = True
    )
    parser.add_argument(
        '--config',
        action = "store",
        help = "Analysis configuration",
        type = str,
        required = True
    )
    parser.add_argument(
        '--category',
        action = "store",
        help = "name of category or glob pattern",
        default = "*",
    )
    parser.add_argument(
        '--outdir',
        action = "store",
        help = "per-analsyis output directory (will be created)",
        default = "."
    )

    from TTH.Plotting.Datacards.AnalysisSpecificationFromConfig import analysisFromConfig
    args = parser.parse_args()
    analysis = analysisFromConfig(args.config)
  
    categories = [
        c for c in analysis.categories if fnmatch.fnmatch(c.full_name, args.category)
    ]
    if len(categories) == 0:
        print "no categories matched out of:"
        print "\n".join([c.full_name for c in analysis.categories])
    tf = ROOT.TFile(args.rootfile)

    hdict = {}
    for k in tf.GetListOfKeys():
        hdict[k.GetName()] = k.ReadObj()

    make_datacard(analysis, categories, args.outdir, hdict)
