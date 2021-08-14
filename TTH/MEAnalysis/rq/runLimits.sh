#!/bin/bash

cfg=results/2017-10-21T23-13-11-879645_b91e835d-e726-4896-a3b2-96356f84e48c/analysis.pickle

for group in sl_j5_t3__btag_LR_4b_2b_btagCSV_logit sl_j5_tge4__mem_SL_1w2h2t_p sl_jge6_t3__btag_LR_4b_2b_btagCSV_logit sl_jge6_tge4__mem_SL_2w2h2t_p; do
    python $CMSSW_BASE/src/TTH/Plotting/python/Datacards/MakeLimits.py --jobtype limit --config $cfg --category $group
    python $CMSSW_BASE/src/TTH/Plotting/python/Datacards/MakeLimits.py --jobtype pulls --config $cfg --category $group
done
#python ../Plotting/python/Datacards/MakeLimits.py --jobtype syst --config cfg --category combined_test
