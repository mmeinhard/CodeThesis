import nanoTreeClasses

from PhysicsTools.HeppyCore.framework.analyzer import Analyzer
class EventAnalyzerBoosted(Analyzer):
    def __init__(self, cfg_ana, cfg_comp, looperName):
        super(EventAnalyzerBoosted, self).__init__(cfg_ana, cfg_comp, looperName)
    def process(self, event):
        #Boosted objects
        event.HTTV2 = nanoTreeClasses.HTTV2.make_array(event.input, MC = True)
        event.HTTV2Subjet = nanoTreeClasses.HTTV2Subjet.make_array(event.input, MC = True)
        #event.FatjetCA15 = nanoTreeClasses.FatjetCA15.make_array(event.input, MC = True)
        event.FatjetCA15SoftDrop = nanoTreeClasses.FatjetCA15SoftDrop.make_array(event.input, MC = True)
        #event.FatjetCA15SoftDropSubjet = nanoTreeClasses.FatjetCA15SoftDropSubjet.make_array(event.input, MC = True)
        event.FatjetAK8 = nanoTreeClasses.FatjetAK8.make_array(event.input, MC = True)
        event.SubjetAK8 = nanoTreeClasses.SubjetAK8.make_array(event.input, MC = True)
