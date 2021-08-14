import ROOT
import itertools
from PhysicsTools.HeppyCore.framework.analyzer import Analyzer
import copy
import math

from TTH.MEAnalysis.SubjetAnalyzerAK8 import SubjetAnalyzer
#from TTH.MEAnalysis.MulticlassAnalyzer import MulticlassAnalyzer
from TTH.MEAnalysis.WTagAnalyzer import WTagAnalyzer
from TTH.MEAnalysis.GenRadiationModeAnalyzer import GenRadiationModeAnalyzer
from TTH.MEAnalysis.GenTTHAnalyzer import GenTTHAnalyzer, GenTTHAnalyzerPre
from TTH.MEAnalysis.MEMAnalyzer import MEAnalyzer, MECategoryAnalyzer
from TTH.MEAnalysis.LeptonAnalyzer import LeptonAnalyzer
from TTH.MEAnalysis.JetAnalyzer import JetAnalyzer
from TTH.MEAnalysis.BTagLRAnalyzer import BTagLRAnalyzer
#from TTH.MEAnalysis.BtagWeightAnalyzerSubjet import BtagWeightAnalyzerSubjet
from TTH.MEAnalysis.QGLRAnalyzer import QGLRAnalyzer
from TTH.MEAnalysis.Analyzer import CounterAnalyzer, EventIDFilterAnalyzer, EventWeightAnalyzer, PrimaryVertexAnalyzer, PrefilterAnalyzer, MemoryAnalyzer, LumiListAnalyzer, PUWeightAnalyzer, TriggerWeightAnalyzer, METFilterAnalyzer
from TTH.MEAnalysis.TriggerAnalyzer import TriggerAnalyzer
from TTH.MEAnalysis.MVAVarAnalyzer import MVAVarAnalyzer
from TTH.MEAnalysis.BTagRandomizerAnalyzer import BTagRandomizerAnalyzer
from TTH.MEAnalysis.TreeVarAnalyzer import TreeVarAnalyzer
from TTH.MEAnalysis.CommonClassifierAnalyzer import CommonClassifierAnalyzer
from TTH.MEAnalysis.BtagWeightAnalyzer import BtagWeightAnalyzer
from TTH.MEAnalysis.JointLikelihoodAnalyzer import JointLikelihoodAnalyzer
from TTH.MEAnalysis.NNAnalyzer import NNAnalyzer
