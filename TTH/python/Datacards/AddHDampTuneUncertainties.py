import json, copy, os, imp, multiprocessing, sys
import sparse, ROOT
import logging
import subprocess
from ValuesHDampTuneUncertainties import *

def add_files(indir):


    for filename in os.listdir(indir):
        if filename.endswith(".txt") and filename.startswith("shapes"): 
            st = filename[7:].split("__")
            category = st[0]
            #category = "sl_jge6_tge4_sj_only"
	    order = None
            fout = open(indir+"tmp"+filename, "w")
            f = open(indir+filename, "r")
            hdamp_ttbarOther = "CMS_ttHbb_HDAMP_ttbarOther       lnN   "
            hdamp_ttbarPlus2B = "CMS_ttHbb_HDAMP_ttbarPlus2B      lnN   "
            hdamp_ttbarPlusB = "CMS_ttHbb_HDAMP_ttbarPlusB      lnN   "
            hdamp_ttbarPlusBBbar = "CMS_ttHbb_HDAMP_ttbarPlusBBbar      lnN   "
            hdamp_ttbarPlusCCbar = "CMS_ttHbb_HDAMP_ttbarPlusCCbar      lnN   "
            tune_ttbarOther = "CMS_ttHbb_UE_ttbarOther      lnN   "
            tune_ttbarPlus2B = "CMS_ttHbb_UE_ttbarPlus2B      lnN   "
            tune_ttbarPlusB = "CMS_ttHbb_UE_ttbarPlusB      lnN   "
            tune_ttbarPlusBBbar = "CMS_ttHbb_UE_ttbarPlusBBbar      lnN   "
            tune_ttbarPlusCCbar = "CMS_ttHbb_UE_ttbarPlusCCbar      lnN   "
            written = False
            for x in f:
                if "process" in x and "ttH_hbb" in x:
                    order2 = x[8:]
                    order = order2.split()
                    for i in order:
                        if "ttbarOther" in i:
                            hdamp_ttbarOther += hdamp[category]["ttbarOther"]
                            hdamp_ttbarPlus2B += "-  "
                            hdamp_ttbarPlusB  += "-  "
                            hdamp_ttbarPlusBBbar += "-  "
                            hdamp_ttbarPlusCCbar += "-  "
                            tune_ttbarOther += tune[category]["ttbarOther"]
                            tune_ttbarPlus2B += "-  "
                            tune_ttbarPlusB += "-  "
                            tune_ttbarPlusBBbar += "-  "
                            tune_ttbarPlusCCbar += "-  "
                        elif "ttbarPlus2B" in i:
                            hdamp_ttbarOther += "-  "
                            hdamp_ttbarPlus2B += hdamp[category]["ttbarPlus2B"]
                            hdamp_ttbarPlusB  += "-  "
                            hdamp_ttbarPlusBBbar += "-  "
                            hdamp_ttbarPlusCCbar += "-  "
                            tune_ttbarOther += "-  "
                            tune_ttbarPlus2B += tune[category]["ttbarPlus2B"]
                            tune_ttbarPlusB += "-  "
                            tune_ttbarPlusBBbar += "-  "
                            tune_ttbarPlusCCbar += "-  "
                        elif i == "ttbarPlusB":
                            hdamp_ttbarOther += "-  "
                            hdamp_ttbarPlus2B += "-  "
                            hdamp_ttbarPlusB += hdamp[category]["ttbarPlusB"]
                            hdamp_ttbarPlusBBbar += "-  "
                            hdamp_ttbarPlusCCbar += "-  "
                            tune_ttbarOther += "-  "
                            tune_ttbarPlus2B += "-  "
                            tune_ttbarPlusB += tune[category]["ttbarPlusB"]
                            tune_ttbarPlusBBbar += "-  "
                            tune_ttbarPlusCCbar += "-  "
                        elif "ttbarPlusBBbar" in i:
                            hdamp_ttbarOther += "-  "
                            hdamp_ttbarPlus2B += "-  "
                            hdamp_ttbarPlusB  += "-  "
                            hdamp_ttbarPlusBBbar += hdamp[category]["ttbarPlusBBbar"]
                            hdamp_ttbarPlusCCbar += "-  "
                            tune_ttbarOther += "-  "
                            tune_ttbarPlus2B += "-  "
                            tune_ttbarPlusB += "-  "
                            tune_ttbarPlusBBbar += tune[category]["ttbarPlusBBbar"]
                            tune_ttbarPlusCCbar += "-  "
                        elif "ttbarPlusCCbar" in i:
                            hdamp_ttbarOther += "-  "
                            hdamp_ttbarPlus2B += "-  "
                            hdamp_ttbarPlusB  += "-  "
                            hdamp_ttbarPlusBBbar += "-  "
                            hdamp_ttbarPlusCCbar += hdamp[category]["ttbarPlusCCbar"]
                            tune_ttbarOther += "-  "
                            tune_ttbarPlus2B += "-  "
                            tune_ttbarPlusB += "-  "
                            tune_ttbarPlusBBbar += "-  "
                            tune_ttbarPlusCCbar += tune[category]["ttbarPlusCCbar"]
                        else:
                            hdamp_ttbarOther += "-  "
                            hdamp_ttbarPlus2B += "-  "
                            hdamp_ttbarPlusB  += "-  "
                            hdamp_ttbarPlusBBbar += "-  "
                            hdamp_ttbarPlusCCbar += "-  "
                            tune_ttbarOther += "-  "
                            tune_ttbarPlus2B += "-  "
                            tune_ttbarPlusB += "-  "
                            tune_ttbarPlusBBbar += "-  "
                            tune_ttbarPlusCCbar += "-  "

                    hdamp_ttbarOther += "\n"
                    hdamp_ttbarPlus2B += "\n"
                    hdamp_ttbarPlusB  += "\n"
                    hdamp_ttbarPlusBBbar += "\n"
                    hdamp_ttbarPlusCCbar += "\n"
                    tune_ttbarOther += "\n"
                    tune_ttbarPlus2B += "\n"
                    tune_ttbarPlusB += "\n"
                    tune_ttbarPlusBBbar += "\n" 
                    tune_ttbarPlusCCbar  += "\n"



                if "group" in x and written == False: 
                    fout.write(hdamp_ttbarOther)
                    fout.write(hdamp_ttbarPlus2B)
                    fout.write(hdamp_ttbarPlusB)
                    fout.write(hdamp_ttbarPlusBBbar)
                    fout.write(hdamp_ttbarPlusCCbar)
                    fout.write(tune_ttbarOther)
                    fout.write(tune_ttbarPlus2B)
                    fout.write(tune_ttbarPlusB)
                    fout.write(tune_ttbarPlusBBbar)
                    fout.write(tune_ttbarPlusCCbar)
                    written = True

                fout.write(x)


            f.close()
            fout.close()

            os.rename(indir+filename, indir+"no_HDAMP_UE_"  + filename)
            os.rename(indir+"tmp"+filename, indir + filename)







if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    import argparse
    parser = argparse.ArgumentParser(
        description='Merge files from "MakeCategory'
    )
    parser.add_argument(
        '--indir',
        action = "store",
        help = "Input root file",
        type = str,
        required = True
    )

    args = parser.parse_args()

    add_files(args.indir)
