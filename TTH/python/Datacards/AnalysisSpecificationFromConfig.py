########################################
# Imports
########################################

import sys
from copy import deepcopy
import fnmatch

from TTH.MEAnalysis.samples_base import xsec
from TTH.Plotting.Datacards.AnalysisSpecificationClasses import Histogram, Cut, Sample, Process, DataProcess, Category, Analysis, pairwise, triplewise, make_csv_categories_abstract, make_csv_groups_abstract
from TTH.Plotting.joosep.sparsinator import TRIGGERPATH_MAP
from TTH.MEAnalysis import samples_base


########################################
# Helper Functions
########################################

def splitByTriggerPath(processes, lumi, cuts_dict):
    """
    Given a list of processes, add a cut on a trigger path (SLmu, SLele etc)
    and normalize to the given luminosity.
    """
    out = []
    _lumis = {
        "m": lumi["SingleMuon"],
        "e": lumi["SingleElectron"],
        "mm": lumi["DoubleMuon"],
        "em": lumi["MuonEG"],
        "ee": lumi["DoubleEG"],
        #"fh": lumi["BTagCSV"],
        #"bt": lumi["JetHT"],
    }

    for proc in processes:
        #Don't need to split data process
        if type(proc) is DataProcess:
            out += [proc]
            continue
        for name, trigpath in TRIGGERPATH_MAP.items():
            
            #Don't need to split data process
            if type(proc) is DataProcess:
                continue

            #Process where the trigger paths are split and then merged
            newproc = Process(
                input_name = proc.input_name,
                output_name = proc.output_name,
                xs_weight = _lumis[name] * proc.xs_weight,
                cuts = [cuts_dict["triggerPath_{0}".format(name)]] + proc.cuts,
            )

            # #Process where the trigger path is explicitly kept separate
            # newproc2 = Process(
            #     input_name = proc.input_name,
            #     output_name = proc.output_name,
            #     category_name = "_" + name,
            #     xs_weight = _lumis[name] * proc.xs_weight,
            #     cuts = [cuts_dict["triggerPath_{0}".format(name)]] + proc.cuts,
            # )
            out += [newproc]
    return out


########################################
# analysisFromConfig
########################################

def analysisFromConfig(config_file_path):
    """ Create Analysis object from cfg file """

    ########################################
    # Setup
    ########################################

    # Init config parser
    config = Analysis.getConfigParser(config_file_path)
    
    # Get information on sparse input
    lumi = {k: float(v) for (k, v) in config.items("lumi")}
    #blr_cuts = {k: float(v) for (k, v) in config.items("blr_cuts")}

    ########################################
    # Samples
    ########################################

    samples_list = config.get("samples","samples_list").split()
    samples = []
    for sample_name in samples_list:
        sample = Sample.fromConfigParser(config, sample_name)
        if config.getboolean("general", "debug"):
            sample.step_size_sparsinator = 1
        samples += [sample]

    samples_dict = {_sample.name: _sample for _sample in samples}

    ########################################
    # Cuts
    ########################################

    cuts_list = config.get("cuts","cuts_list").split()
    cuts = []
    for cut_name in cuts_list:
        cut = Cut.fromConfigParser(config, cut_name)
        cuts += [cut]

    cuts_dict = {_cut.name: _cut for _cut in cuts}

    ########################################
    # Processes
    ########################################
    
    process_lists = {}
    process_lists_original = {}
    for process_list in config.get("general","process_lists").split():
        process_lists_original[process_list] = []
        process_lists[process_list] = []


        schema =  config.get(process_list, "schema")

        for process in config.get(process_list,"processes").split():

            in_name  = config.get(process,"in")
            out_name = config.get(process,"out")
            
            if not in_name in samples_dict.keys():
                raise KeyError("process {0} needs sample {1}, but it was not defined".format(process, in_name))
            # Build cuts..
            cuts = []
            # ..Process Cut
            if config.has_option(process, "cuts"):
                for cut in config.get(process,"cuts").split():
                    cuts.append(cuts_dict[cut])

            # DATA
            if schema == "data":
                process_lists[process_list].append(
                    DataProcess(
                        input_name = in_name,
                        output_name = out_name,
                        cuts = cuts,
                        lumi = lumi[config.get(process,"lumi")]))
            # SIMULATION
            else:
                local_lumi = 1.0
                #if not splitting by trigger path, use a common lumi for every sample
                if not config.getboolean(process_list, "split_by_trigger_path"):
                    local_lumi = config.getfloat("lumi", "Common")
                 
                process_lists[process_list].append(
                    Process(
                        input_name = in_name,
                        output_name = out_name,
                        cuts = cuts,
                        xs_weight = local_lumi * samples_dict[in_name].xsec/samples_dict[in_name].ngen,
                    )
                )
        # End loop over processes

        #post-processing of processes
        #split by trigger path
        if config.getboolean(process_list, "split_by_trigger_path"):
            process_lists_original[process_list] = process_lists[process_list]
            process_lists[process_list] = splitByTriggerPath(
                process_lists[process_list],
                lumi,
                cuts_dict
            )
    # End loop over processes lists

    # Prepare the process list for the analysis object
    # TODO: check if needed since we also have per category process lists
    processes = sum([process_lists[x] for x in config.get("general", "processes").split()],[])

    #Processes in unsplit form
    processes_original = []
    for pl in process_lists_original.values():
        for proc in pl:
            processes_original.append(proc)

    ########################################
    # Categories
    ########################################

    analysis_groups = {}

    all_cats = []
    
    for group in config.get("general","analysis_groups").split():

        cats = []
        for category_name in config.get(group,"categories").split():

            template = config.get(category_name, "template")

            cut = Cut(sparsinator = Cut.string_to_cuts(config.get(category_name, "cuts").split()))

            mc_processes = sum([process_lists[x] for x in config.get(template, "mc_processes").split()], [])
            data_processes = sum([process_lists[x] for x in config.get(template, "data_processes").split()], [])
            signal_processes = config.get(template, "signal_processes").split()

            common_shape_name = config.get(template, "common_shape_uncertainties")        
            common_shape_uncertainties = {k:float(v) for k,v in config.items(common_shape_name)}

            common_scale_name = config.get(template, "common_scale_uncertainties")
            common_scale_uncertainties = {k:float(v) for k,v in config.items(common_scale_name)}        

            unique_output_processes = list(set([p.output_name for p in mc_processes]))
            
            scale_name = config.get(template, "scale_uncertainties")
            scale_uncertainties = {}
            for process, name_uncert in config.items(scale_name):
                scale_uncertainties[process] = {}
                for name, uncert in pairwise(name_uncert.split()):
                    scale_uncertainties[process][name] = uncert

            shape_name = config.get(template, "shape_uncertainties") #DS
            shape_uncertainties = {}
            for k,v in config.items(shape_name):
                shape_uncertainties[k] = {}
                for name, status in pairwise(v.split()):
                    shape_uncertainties[k][name] = float(status) #DS


            #Add any additional category-dependent scale uncertainties
            if config.has_option(category_name, "additional_scale_uncertainties"):
                for line in config.get(category_name, "additional_scale_uncertainties").strip().split("\n"):
                    name, process_pattern, uncert = line.split()
                    matching_procs = [proc for proc in unique_output_processes if fnmatch.fnmatch(proc, process_pattern)]
                    for matching_proc in matching_procs:
                        scale_uncertainties[matching_proc][name] = uncert

            if config.has_option(category_name, "rebin"):
                rebin = int(config.get(category_name,"rebin"))
            else:
                rebin = 1
            
            disc_name = config.get(category_name, "discriminator").strip()
            if len(disc_name) > 0:
                category = Category(
                    name = category_name,
                    cuts = [cut],
                    processes = mc_processes,
                    data_processes = data_processes,
                    signal_processes = signal_processes, 
                    common_shape_uncertainties = common_shape_uncertainties, 
                    common_scale_uncertainties = common_scale_uncertainties, 
                    scale_uncertainties = scale_uncertainties, 
                    shape_uncertainties = shape_uncertainties, 
                    discriminator = Histogram.from_string(disc_name),
                    rebin = rebin,
                    do_limit = True
                )
                cats.append(category)

            #a group consisting of only this category
            analysis_groups[category.full_name] = [category] 

            # Also add control variables as separate categories
            if config.has_option(category_name, "control_variables"):
                for cv in config.get(category_name, "control_variables").split('\n'):
                    if len(cv) == 0:
                        continue
                    cats.append(
                        Category(
                            name = category_name,
                            cuts = [cut],
                            processes = mc_processes,
                            data_processes = data_processes,
                            signal_processes = signal_processes, 
                            common_shape_uncertainties = common_shape_uncertainties, 
                            common_scale_uncertainties = common_scale_uncertainties, 
                            scale_uncertainties = scale_uncertainties, 
                            shape_uncertainties = shape_uncertainties, 
                            discriminator = Histogram.from_string(cv),
                            rebin = rebin,
                            do_limit = False
                    )
                )
                


            # End loop over categories
            
        analysis_groups[group] = cats
        all_cats.extend(cats)
    # End loop over groups of categories

    # If the same category is defined in multiple groups, it will exist multiple times
    # We need to define each category uniquely, so do this here via the dictionary
    all_cats_uniq = {}
    all_cats_uniq = {c.full_name: c for c in all_cats}
    all_cats = sorted(all_cats_uniq.values(), key=lambda x: x.full_name)


    ########################################
    # Put everything together
    ########################################

    analysis = Analysis(
        mem_python_config = config.get("general", "mem_python_config"),
        config = config,
        debug = config.getboolean("general", "debug"),
        samples = samples,
        cuts = cuts_dict,
        process_lists = process_lists,
        processes = processes,
        processes_unsplit = processes_original,
        process_map = processes_original,
        categories = all_cats,
        groups = analysis_groups,
        do_fake_data = config.getboolean("general", "do_fake_data"),
        do_stat_variations = config.getboolean("general", "do_stat_variations")
     )   

    return analysis

# end of analysisFromConfig


########################################
# main
########################################

if __name__ == "__main__":
    an = analysisFromConfig(sys.argv[1])
    print an
    
    print "processes"
    for proc in an.processes:
        print "  ", proc
   
    print "samples"
    for samp in an.samples:
        print "  ", samp
    
    print "categories"
    for cat in an.categories:
        print "  ", cat
