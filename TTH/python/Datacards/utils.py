import ROOT
import os

import math
from collections import OrderedDict

import logging
import sparse

def PrintDatacard(categories, event_counts, filenames, dcof):
    number_of_bins = len(categories)
    number_of_backgrounds = 0
    backgrounds = []
    #FIXME: check what happens with ttH_nonhbb
    for cat in categories:
        for proc in cat.out_processes_mc:
            backgrounds += [proc]
    backgrounds = set(backgrounds)
    number_of_backgrounds = len(backgrounds) - 1
    analysis_categories = list(set([c.full_name for c in categories]))


    dcof.write("imax {0}\n".format(number_of_bins))
    dcof.write("jmax {0}\n".format(number_of_backgrounds))
    dcof.write("kmax *\n")
    dcof.write("---------------\n")

    for cat in categories:
        dcof.write("shapes * {0} {1} $PROCESS__$CHANNEL $PROCESS__$CHANNEL__$SYSTEMATIC\n".format(
            cat.full_name,
            os.path.basename(filenames[cat.full_name])
        ))

    dcof.write("---------------\n")

    dcof.write("bin\t" +  "\t".join(analysis_categories) + "\n")
    dcof.write("observation\t" + "\t".join("-1" for _ in analysis_categories) + "\n")
    dcof.write("---------------\n")

    bins        = []
    processes_0 = []
    processes_1 = []
    rates       = []

    # Conversion:
    # Example: ttHJetTobb_M125_13TeV_amcatnloFXFX_madspin_pythia8_hbb -> ttH_hbb

    for cat in categories:
        for i_sample, sample in enumerate(cat.out_processes_mc):
            bins.append(cat.full_name)
            processes_0.append(sample)
            if sample in cat.signal_processes:
                i_sample = -i_sample
            processes_1.append(str(i_sample))
            rates.append(str(event_counts[cat.full_name][sample]))
    dcof.write("bin\t"+"\t".join(bins)+"\n")
    dcof.write("process\t"+"\t".join(processes_0)+"\n")
    dcof.write("process\t"+"\t".join(processes_1)+"\n")
    dcof.write("rate\t"+"\t".join(rates)+"\n")
    dcof.write("---------------\n")

    # Gather all shape uncerainties
    all_shape_uncerts = []
    all_scale_uncerts = []
    for cat in categories:
        for proc in cat.out_processes_mc:
            all_shape_uncerts.extend(cat.shape_uncertainties[proc].keys())
            all_scale_uncerts.extend(cat.scale_uncertainties[proc].keys())
    # Uniquify
    all_shape_uncerts = sorted(list(set(all_shape_uncerts)))
    all_scale_uncerts = sorted(list(set(all_scale_uncerts)))

    for syst in all_shape_uncerts:
        dcof.write(syst + "\t shape \t")
        for cat in categories:
            for proc in cat.out_processes_mc:
                if (cat.shape_uncertainties.has_key(proc) and
                    cat.shape_uncertainties[proc].has_key(syst)):
                    dcof.write(str(cat.shape_uncertainties[proc][syst]))
                else:
                    dcof.write("-")
                dcof.write("\t")
        dcof.write("\n")


    for syst in all_scale_uncerts:
        dcof.write(syst + "\t lnN \t")
        for cat in categories:
            for proc in cat.out_processes_mc:
                if (cat.scale_uncertainties.has_key(proc) and
                    cat.scale_uncertainties[proc].has_key(syst)):
                    dcof.write(str(cat.scale_uncertainties[proc][syst]))
                else:
                    dcof.write("-")
                dcof.write("\t")
        dcof.write("\n")


    #Add rate parameters
    dcof.write("CMS_ttHbb_bgnorm_ttbarPlusBB rateParam * ttbarPlusB 1 [-5,5]\n")
    dcof.write("CMS_ttHbb_bgnorm_ttbarPlusBB rateParam * ttbarPlus2B 1 [-5,5]\n")
    dcof.write("CMS_ttHbb_bgnorm_ttbarPlusBB rateParam * ttbarPlusBBbar 1 [-5,5]\n")
    dcof.write("CMS_ttHbb_bgnorm_ttbarPlusCCbar rateParam * ttbarPlusCCbar 1 [-5,5]\n")


    #create nuisance groups for easy manipulation
    #To be adapted
    nuisance_groups = {
        "jec": ["CMS_res_j","CMS_scaleAbsoluteMPFBias_j","CMS_scaleAbsoluteScale_j","CMS_scaleAbsoluteStat_j","CMS_scaleFlavorQCD_j","CMS_scaleFragmentation_j","CMS_scalePileUpDataMC_j","CMS_scalePileUpPtBB_j","CMS_scalePileUpPtEC1_j","CMS_scalePileUpPtRef_j","CMS_scaleRelativeBal_j","CMS_scaleRelativeFSR_j","CMS_scaleRelativeJEREC1_j","CMS_scaleRelativePtBB_j","CMS_scaleRelativePtEC1_j","CMS_scaleRelativeStatEC_j","CMS_scaleRelativeStatFSR_j","CMS_scaleSinglePionECAL_j","CMS_scaleSinglePionHCAL_j","CMS_scaleTimePtEta_j"],
        "bgnorm": ["CMS_ttHbb_bgnorm_ttbarPlusBB","CMS_ttHbb_bgnorm_ttbarPlusCCbar"],
        "pdf": ["pdf_Higgs_ttH","pdf_gg","pdf_qg","pdf_qqbar","CMS_ttHbb_PDF"],
        "QCDscale": ["QCDscale_ttH", "QCDscale_ttbar"],
        "isrfsr": ["CMS_ttHbb_FSR_ttbarOther","CMS_ttHbb_FSR_ttbarPlus2B","CMS_ttHbb_FSR_ttbarPlusB","CMS_ttHbb_FSR_ttbarPlusBBbar","CMS_ttHbb_FSR_ttbarPlusCCbar","CMS_ttHbb_ISR_ttbarOther","CMS_ttHbb_ISR_ttbarPlus2B","CMS_ttHbb_ISR_ttbarPlusB","CMS_ttHbb_ISR_ttbarPlusBBbar","CMS_ttHbb_ISR_ttbarPlusCCbar"],
        "hdampue": ["CMS_ttHbb_HDAMP_ttbarOther","CMS_ttHbb_HDAMP_ttbarPlus2B","CMS_ttHbb_HDAMP_ttbarPlusB","CMS_ttHbb_HDAMP_ttbarPlusBBbar","CMS_ttHbb_HDAMP_ttbarPlusCCbar","CMS_ttHbb_UE_ttbarOther","CMS_ttHbb_UE_ttbarPlus2B","CMS_ttHbb_UE_ttbarPlusB","CMS_ttHbb_UE_ttbarPlusBBbar","CMS_ttHbb_UE_ttbarPlusCCbar"],
        "btag": ["CMS_btag_cferr1","CMS_btag_cferr2","CMS_btag_hf","CMS_btag_hfstats1","CMS_btag_hfstats2","CMS_btag_lf","CMS_btag_lfstats1","CMS_btag_lfstats2"],
        "misc": ["CMS_effTrigger_dl","CMS_effTrigger_e","CMS_effTrigger_m","CMS_eff_e","CMS_eff_m","lumi_13TeV","CMS_ttHbb_L1PreFiring","CMS_ttHbb_PU"],
        "scale": ["CMS_ttHbb_scaleMuF","CMS_ttHbb_scaleMuR","QCDscale_V","QCDscale_VV","QCDscale_t","QCDscale_ttH","QCDscale_ttbar"]
    }
    nuisance_groups["exp"] = nuisance_groups["jec"] + nuisance_groups["btag"] + nuisance_groups["misc"] 
    #nuisance_groups["theory"] = nuisance_groups["bgnorm"] + nuisance_groups["pdf"] + nuisance_groups["QCDscale"] + nuisance_groups["isrfsr"] + nuisance_groups["tunehdamp"]
    nuisance_groups["theory"] = nuisance_groups["bgnorm"] + nuisance_groups["pdf"] + nuisance_groups["QCDscale"] + nuisance_groups["isrfsr"] + nuisance_groups["hdampue"] + nuisance_groups["scale"]
    nuisance_groups["syst"] = nuisance_groups["exp"] + nuisance_groups["theory"]

    for nuisance_group, nuisances in nuisance_groups.items():
        good_nuisances = []
        for nui in nuisances:
            if not (nui in all_scale_uncerts or nui in all_shape_uncerts):
                logging.error("unknown nuisance {0}".format(nui))
            else:
                good_nuisances += [nui]
        dcof.write("{0} group = {1}\n".format(nuisance_group, " ".join(good_nuisances)))
    
    dcof.write("* autoMCStats 0 0 1\n")
    #
    #shapename = os.path.basename(datacard.output_datacardname)
    #shapename_base = shapename.split(".")[0]
    #dcof.write("# Execute with:\n")
    #dcof.write("# combine -n {0} -M Asymptotic -t -1 {1} \n".format(shapename_base, shapename))


def makeStatVariations(tf, of, categories):
    """
    Given an input TFile and an output TFile, produces the histograms for
    bin-by-bin variations for the given categories.
    """
    ret = {}
    tf.cd()
    for cat in categories:
        ret[cat.full_name] = {}
        for proc in cat.out_processes_mc:
            ret[cat.full_name][proc] = []
            hn = "{0}__{1}__{2}".format(proc, cat.name, cat.discriminator.name)
            h = tf.Get(hn)
            h = h.Clone()
            for ibin in range(1, h.GetNbinsX() + 1):
                systname = "CMS_ttH_{0}_{1}_Bin{2}".format(proc, cat.full_name, ibin)
                ret[cat.full_name][proc] += [systname]
                for sigma, sdir in [(+1, "Up"), (-1, "Down")]:
                    systname_sdir = proc + "__" + cat.full_name + "__" + systname + sdir
                    hvar = h.Clone(systname_sdir)
                    delta = hvar.GetBinError(ibin)
                    c = hvar.GetBinContent(ibin) + sigma*delta
                    if c <= 10**-5 and h.Integral() > 0:
                        c = 10**-5
                    hvar.SetBinContent(ibin, c)
                    #tf.Add(hvar)
                    hvar.Write("", ROOT.TObject.kOverwrite)
    #tf.Write()
    return ret
#end of makeStatVariations

def fakeData(infile, outfile, categories):
    dircache = {}
    for cat in categories:

        #get first nominal histogram
        hn = "{0}__{1}__{2}".format(
            cat.out_processes_mc[0], cat.name, cat.discriminator.name
        )
        h = infile.Get(hn)
        if not h or h.IsZombie():
            raise Exception("Could not get histo {0}".format(hn)) 
        h = h.Clone()

        #Get and add the rest of the nominal histograms
        for proc in cat.out_processes_mc[1:]:
            name = "{0}__{1}__{2}".format(
                proc, cat.name, cat.discriminator.name
            )
            h2 = infile.Get(name)
            if not h2:
                logging.error("could not get histo {0}".format(name))
                continue
            h.Add(h2)

        outname = "data_obs__{0}__{1}".format(cat.name, cat.discriminator.name)
        dircache[outname] = h

    # End of loop over categories

    outfile.cd()
    for (k, v) in dircache.items():
        v.SetName(k)
        v.SetDirectory(outfile)
        outfile.Append(v, True)
    outfile.Write()
#end of fakeData
