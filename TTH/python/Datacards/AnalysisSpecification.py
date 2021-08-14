#!/usr/bin/env python
#The production of the datacards follows the following pattern:
#Each final limit, (e.g. full ttH limit) corresponds to an Analysis.
#Each Analysis is made of Groups, which are made of Categories.
import os

from TTH.Plotting.Datacards.AnalysisSpecificationClasses import make_csv_categories_abstract, make_csv_groups_abstract

from TTH.Plotting.Datacards.AnalysisSpecificationFromConfig import analysisFromConfig

analyses = {} 
#for config in ["config_sl.cfg", "config_dl.cfg", "config_fh.cfg"]:
config ="/work/mameinha/testcrab/CMSSW_10_2_15_patch2/src/TTH/MEAnalysis/data/default_Boosted_btag.cfg"
analysis = analysisFromConfig(os.path.join(os.environ["CMSSW_BASE"],
                                                 "src/TTH/Plotting/python/Datacards",
                                                 config))
sparsefile = "/work/mameinha/testcrab/CMSSW_10_2_15_patch2/src/TTH/Plotting/python/tthbbwork/DifferentChecks/out_fulleta_fixed_merged.root"
#sparsefile = "/mnt/t3nfs01/data01/shome/mameinha/testcrab/CMSSW_10_2_15_patch2/src/TTH/Plotting/python/tthbbwork/DifferentChecks/out_test_scale_rescaledata.root"
def make_csv_categories_abstract(analysis):

    import csv
    with open('analysis_specs.csv', 'w') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=';')

        csvwriter.writerow(['sparsefile', 'config', 'category','cat','variable'])

        # We want the analysis specification file
        # as make_csv is called from there we just take the filename of the outer stack
        import inspect
        analysis_spec_file = os.path.abspath(inspect.getouterframes(inspect.currentframe())[1][1])

        #for analysis_name, analysis in di.iteritems():        

        unique_cat_names = list(set(c.name for c in analysis.categories))
        #for cat_name in unique_cat_names:
        for cat in analysis.categories:
            csvwriter.writerow([sparsefile, config, cat.full_name, cat.name, cat.full_name.split('__')[1]])

    return [1]

def make_csv_groups_abstract(analysis):

    import csv
    with open('analysis_groups.csv', 'w') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=';')

        csvwriter.writerow(['specfile', 'analysis', 'group'])

        # We want the analysis specification file
        # as make_csv is called from there we just take the filename of the outer stack    
        import inspect
        analysis_spec_file = os.path.abspath(inspect.getouterframes(inspect.currentframe())[1][1])

        #for analysis_name, analysis in di.iteritems():        
        for group_name in analysis.groups.keys():
            csvwriter.writerow([analysis_spec_file, config, group_name])

    return [1]


def main():
    print "Printing all analyses", analysis

    #write out all categories that we want to create
    make_csv_categories_abstract(analysis)

    #write out all the combine groups
    make_csv_groups_abstract(analysis)


if __name__ == "__main__":
    main()

