#from PhysicsTools.Heppy.physicsutils.genutils import isNotFromHadronicShower, realGenMothers, realGenDaughters, motherRef

class Particles:
    def __init__(self, tree, n):
        self.pdgId = tree.GenLepFromTop_pdgId[n];

#Only masses of particles > 10 GeV are stored in nanoAOD. Use pdg values for the others
genemass = 0.000511
genmumass = 0.1057
gentaumass = 1.777
genbmass = 4.75

def sign(number):
	return cmp(number,0)

def realGenMothers(GenParticle,gp):
    """Get the mothers of a particle X going through intermediate X -> X' chains.
       e.g. if Y -> X, X -> X' realGenMothers(X') = Y"""
    ret = []
    mom = GenParticle[gp.genPartIdxMother]
    if mom.pdgId == gp.pdgId:
        ret += realGenMothers(GenParticle,mom)
    else:
        ret.append(mom)
    return ret


### Get all generator level information


class GenLepFromTop:
	def __init__(self, GenParticle, n):
		self.pdgId = GenParticle[n].pdgId;
		self.pt = GenParticle[n].pt;
		self.eta = GenParticle[n].eta;
		self.phi = GenParticle[n].phi;
		self.status = GenParticle[n].status;
		self.charge = -sign(GenParticle[n].pdgId);
		if abs(GenParticle[n].pdgId)==13:
			self.mass = genmumass
		elif abs(GenParticle[n].pdgId)==11:
			self.mass = genemass
        #What about isPromptHard? Is it needed?
		pass

	@staticmethod
	def make_array(GenParticle):
		ret = []
		for i in range(len(GenParticle)):
		    if (abs(GenParticle[i].pdgId) in {11,13}):
		    #skip leptons from tau decays, as they are stored separately in gentauleps vector
			    if abs(GenParticle[GenParticle[i].genPartIdxMother].pdgId) != 15:
			        momids = [(m, abs(m.pdgId)) for m in realGenMothers(GenParticle,GenParticle[i])]
			        #have a look at the lepton mothers
			        for mom, momid in momids:
			            #lepton from W
			            if momid == 24:
			                wmomids = [abs(m.pdgId) for m in realGenMothers(GenParticle,mom)]
			                #W from t
			                if 6 in wmomids:
			                    #save mu,e from t->W->mu/e
			                    ret.append(i)
		return [GenLepFromTop(GenParticle, i) for i in ret]




class GenBQuarkFromTop:
	def __init__(self, GenParticle, n):
		self.pdgId = GenParticle[n].pdgId;
		self.pt = GenParticle[n].pt;
		self.eta = GenParticle[n].eta;
		self.phi = GenParticle[n].phi;
		self.status = GenParticle[n].status;
		self.charge = -sign(GenParticle[n].pdgId);
		self.mass = genbmass
        #What about isPromptHard? Is it needed?
		pass

	@staticmethod
	def make_array(GenParticle):
		ret = []
		for i in range(len(GenParticle)):		    
			if abs(GenParticle[i].pdgId) == 5:
				momids = [abs(m.pdgId) for m in realGenMothers(GenParticle,GenParticle[i])]
				if 6 in momids: 
					ret.append(i)
		return [GenBQuarkFromTop(GenParticle, i) for i in ret]


class GenLepFromTau:
	def __init__(self, GenParticle, n):
		self.pdgId = GenParticle[n].pdgId;
		self.pt = GenParticle[n].pt;
		self.eta = GenParticle[n].eta;
		self.phi = GenParticle[n].phi;
		self.status = GenParticle[n].status;
		self.charge = -sign(GenParticle[n].pdgId);
		if abs(GenParticle[n].pdgId)==13:
			self.mass = genmumass
		elif abs(GenParticle[n].pdgId)==11:
			self.mass = genemass
        #What about isPromptHard? Is it needed?
		pass

	@staticmethod
	def make_array(GenParticle):
		ret = []
		for i in range(len(GenParticle)):		
			if (abs(GenParticle[i].pdgId) in {11,13}):
				c = i
				#leptons from tau decays
				#if abs(event.GenParticle[GenParticle[i].genPartIdxMother].pdgId) == 15:
				while GenParticle[c].genPartIdxMother != -1:
					momids = [(m, abs(m.pdgId)) for m in realGenMothers(GenParticle,GenParticle[c])]
					c = GenParticle[c].genPartIdxMother
				#have a look at the lepton mothers
					for mom, momid in momids:
						#lepton from tau
						if momid == 15:
							ret.append(i)
							break
			
		return [GenLepFromTau(GenParticle, i) for i in ret]

class GenHiggsBoson:
	def __init__(self, GenParticle, n):
		self.pdgId = GenParticle[n].pdgId;
		self.pt = GenParticle[n].pt;
		self.eta = GenParticle[n].eta;
		self.phi = GenParticle[n].phi;
		self.status = GenParticle[n].status;
		self.charge = -sign(GenParticle[n].pdgId);
		self.mass = GenParticle[n].mass;
        #What about isPromptHard? Is it needed?
		pass

	@staticmethod
	def make_array(GenParticle):
		ret = []
		for i in range(len(GenParticle)):		    
			if abs(GenParticle[i].pdgId) == 25: 
				ret.append(i)
		return [GenHiggsBoson(GenParticle, i) for i in ret]

class GenTop:
	def __init__(self, GenParticle, n):
		self.pdgId = GenParticle[n].pdgId;
		self.pt = GenParticle[n].pt;
		self.eta = GenParticle[n].eta;
		self.phi = GenParticle[n].phi;
		self.status = GenParticle[n].status;
		self.charge = -sign(GenParticle[n].pdgId);
		self.mass = GenParticle[n].mass;
        #What about isPromptHard? Is it needed?
		pass

	@staticmethod
	def make_array(GenParticle):
		ret = []
		for i in range(len(GenParticle)):		    
			if abs(GenParticle[i].pdgId) == 6: 
				ret.append(i)
		return [GenTop(GenParticle, i) for i in ret]

class GenTaus:
	def __init__(self, GenParticle, n):
		self.pdgId = GenParticle[n].pdgId;
		self.pt = GenParticle[n].pt;
		self.eta = GenParticle[n].eta;
		self.phi = GenParticle[n].phi;
		self.status = GenParticle[n].status;
		self.charge = -sign(GenParticle[n].pdgId);
		self.mass = gentaumass
        #What about isPromptHard? Is it needed?
		pass

	@staticmethod
	def make_array(GenParticle):
		ret = []
		for i in range(len(GenParticle)):	    
			if abs(GenParticle[i].pdgId) == 15:
				ret.append(i)
		return [GenTaus(GenParticle, i) for i in ret]

class GenLep:
	def __init__(self, GenParticle, n):
		self.pdgId = GenParticle[n].pdgId;
		self.pt = GenParticle[n].pt;
		self.eta = GenParticle[n].eta;
		self.phi = GenParticle[n].phi;
		self.status = GenParticle[n].status;
		self.charge = -sign(GenParticle[n].pdgId);
		if abs(GenParticle[n].pdgId)==13:
			self.mass = genmumass
		elif abs(GenParticle[n].pdgId)==11:
			self.mass = genemass
        #What about isPromptHard? Is it needed?
		pass

	@staticmethod
	def make_array(GenParticle):
		ret = []
		for i in range(len(GenParticle)):
			if abs(GenParticle[i].pdgId) in {11,13}:
				#skip leptons from tau decays, as they are stored separately in event.GenLepsFromTau
				if abs(GenParticle[GenParticle[i].genPartIdxMother].pdgId) != 15:
					ret.append(i)
		return [GenLep(GenParticle, i) for i in ret]


class GenWZQuark:
	def __init__(self, GenParticle, n):
		self.pdgId = GenParticle[n].pdgId;
		self.pt = GenParticle[n].pt;
		self.eta = GenParticle[n].eta;
		self.phi = GenParticle[n].phi;
		self.status = GenParticle[n].status;
		self.charge = -sign(GenParticle[n].pdgId);
		self.mass = GenParticle[n].mass;
        #What about isPromptHard? Is it needed?
		pass

	@staticmethod
	def make_array(GenParticle):
		ret = []
		for i in range(len(GenParticle)):	    
			if abs(GenParticle[i].pdgId) <= 5 and any([abs(m.pdgId) in {23,24} for m in realGenMothers(GenParticle,GenParticle[i])]):
				ret.append(i)
		return [GenWZQuark(GenParticle, i) for i in ret]

class GenBQuarkFromHiggs:
	def __init__(self, GenParticle, n):
		self.pdgId = GenParticle[n].pdgId;
		self.pt = GenParticle[n].pt;
		self.eta = GenParticle[n].eta;
		self.phi = GenParticle[n].phi;
		self.status = GenParticle[n].status;
		self.charge = -sign(GenParticle[n].pdgId);
		self.mass = genbmass
        #What about isPromptHard? Is it needed?
		pass

	@staticmethod
	def make_array(GenParticle):
		ret = []
		for i in range(len(GenParticle)): 
			if abs(GenParticle[i].pdgId) == 5:
				momids = [abs(m.pdgId) for m in realGenMothers(GenParticle,GenParticle[i])]
				if 25 in momids: 
					ret.append(i)
		return [GenBQuarkFromHiggs(GenParticle, i) for i in ret]

class GenNuFromTop:
	def __init__(self, GenParticle, n):
		self.pdgId = GenParticle[n].pdgId;
		self.pt = GenParticle[n].pt;
		self.eta = GenParticle[n].eta;
		self.phi = GenParticle[n].phi;
		self.status = GenParticle[n].status;
		self.charge = -sign(GenParticle[n].pdgId);
		#TODO: MASS IS WRONG
		self.mass = 0
        #What about isPromptHard? Is it needed?
		pass

	@staticmethod
	def make_array(GenParticle):
		ret = []
		for i in range(len(GenParticle)): 
			if abs(GenParticle[i].pdgId) in {12,14,16}:
				#skip neutrinos from tau decays, as they are stored separately in event.GenNuFromTau vector
				if abs(GenParticle[GenParticle[i].genPartIdxMother].pdgId) != 15:                     
					momids = [(m, abs(m.pdgId)) for m in realGenMothers(GenParticle,GenParticle[i])]
					#have a look at the neutrino mothers
					for mom, momid in momids:
						#neutrino from W
						if momid == 24:
							wmomids = [abs(m.pdgId) for m in realGenMothers(GenParticle,mom)]
							#W from t
							if 6 in wmomids:
								ret.append(i)
		return [GenNuFromTop(GenParticle, i) for i in ret]

class GenNu:
	def __init__(self, GenParticle, n):
		self.pdgId = GenParticle[n].pdgId;
		self.pt = GenParticle[n].pt;
		self.eta = GenParticle[n].eta;
		self.phi = GenParticle[n].phi;
		self.status = GenParticle[n].status;
		self.charge = -sign(GenParticle[n].pdgId);
		#TODO: MASS IS WRONG
		self.mass = 0
        #What about isPromptHard? Is it needed?
		pass

	@staticmethod
	def make_array(GenParticle):
		ret = []
		for i in range(len(GenParticle)):
			if abs(GenParticle[i].pdgId) in {12,14,16}:
				#skip neutrinos from tau decays, as they are stored separately in event.GenNuFromTau vector
				if abs(GenParticle[GenParticle[i].genPartIdxMother].pdgId) != 15:
					ret.append(i)
		return [GenNu(GenParticle, i) for i in ret]


class GenNuFromTau:
	def __init__(self, GenParticle, n):
		self.pdgId = GenParticle[n].pdgId;
		self.pt = GenParticle[n].pt;
		self.eta = GenParticle[n].eta;
		self.phi = GenParticle[n].phi;
		self.status = GenParticle[n].status;
		self.charge = -sign(GenParticle[n].pdgId);
		#TODO: MASS IS WRONG
		self.mass = 0
        #What about isPromptHard? Is it needed?
		pass

	@staticmethod
	def make_array(GenParticle):
		ret = []
		for i in range(len(GenParticle)):
			if abs(GenParticle[i].pdgId) in {12,14,16}:
				if abs(GenParticle[GenParticle[i].genPartIdxMother].pdgId) == 15:                     
					ret.append(i)
		return [GenNuFromTau(GenParticle, i) for i in ret]


class GenGluonFromTop:
	def __init__(self, GenParticle, n):
		self.pdgId = GenParticle[n].pdgId;
		self.pt = GenParticle[n].pt;
		self.eta = GenParticle[n].eta;
		self.phi = GenParticle[n].phi;
		self.status = GenParticle[n].status;
		self.charge = -sign(GenParticle[n].pdgId);
		self.mass = 0
        #What about isPromptHard? Is it needed?
		pass

	@staticmethod
	def make_array(GenParticle):
		ret = []
		for i in range(len(GenParticle)):
			if abs(GenParticle[i].pdgId) == 21:
				if abs(GenParticle[GenParticle[i].genPartIdxMother].pdgId) == 6:                     
					ret.append(i)
		return [GenGluonFromTop(GenParticle, i) for i in ret]

class GenGluonFromB:
	def __init__(self, GenParticle, n):
		self.pdgId = GenParticle[n].pdgId;
		self.pt = GenParticle[n].pt;
		self.eta = GenParticle[n].eta;
		self.phi = GenParticle[n].phi;
		self.status = GenParticle[n].status;
		self.charge = -sign(GenParticle[n].pdgId);
		self.mass = 0
        #What about isPromptHard? Is it needed?
		pass

	@staticmethod
	def make_array(GenParticle):
		ret = []
		for i in range(len(GenParticle)):
			if abs(GenParticle[i].pdgId) == 21:
				if abs(GenParticle[GenParticle[i].genPartIdxMother].pdgId) == 5:                     
					ret.append(i)
		return [GenGluonFromB(GenParticle, i) for i in ret]


def Jet_addmc(Jet,GenJet):
    #event.injets = event.Jet
    for ij, j in enumerate(Jet):
        #Catch unmatched jets (-1) and IndexError
        if Jet[ij].genJetIdx != -1 and Jet[ij].genJetIdx < len(GenJet):
	    j.mcPt = GenJet[Jet[ij].genJetIdx].pt
	    j.mcEta = GenJet[Jet[ij].genJetIdx].eta
	    j.mcPhi = GenJet[Jet[ij].genJetIdx].phi
	    j.mcM = GenJet[Jet[ij].genJetIdx].mass
        else:
	    j.mcPt = -99
	    j.mcEta = -99
	    j.mcPhi = -99
	    j.mcM = -99
        j.mcMatchIdx = Jet[ij].genJetIdx


from PhysicsTools.HeppyCore.framework.analyzer import Analyzer
class FormatVariables(Analyzer):
    def __init__(self, cfg_ana, cfg_comp, looperName):
        super(FormatVariables, self).__init__(cfg_ana, cfg_comp, looperName)
    def process(self, event):
    	event.GenLepFromTop = GenLepFromTop.make_array(event.GenParticle)
    	event.GenBQuarkFromTop = GenBQuarkFromTop.make_array(event.GenParticle)
    	event.GenLepFromTau = GenLepFromTau.make_array(event.GenParticle)
    	event.GenHiggsBoson = GenHiggsBoson.make_array(event.GenParticle)
    	event.GenTop = GenTop.make_array(event.GenParticle)
    	event.GenTaus = GenTaus.make_array(event.GenParticle)
    	event.GenLep = GenLep.make_array(event.GenParticle)
    	event.GenWZQuark = GenWZQuark.make_array(event.GenParticle)
    	event.GenBQuarkFromH = GenBQuarkFromHiggs.make_array(event.GenParticle)
    	event.GenNuFromTop = GenNuFromTop.make_array(event.GenParticle)
    	event.GenNu = GenNu.make_array(event.GenParticle)
    	event.GenNuFromTau = GenNuFromTau.make_array(event.GenParticle)
    	event.GenGluonFromTop = GenGluonFromTop.make_array(event.GenParticle)
    	event.GenGluonFromB = GenGluonFromB.make_array(event.GenParticle)
    	Jet_addmc(event.Jet,event.GenJet)
    	event.lumi = getattr(event.input, "luminosityBlock", None)
    	event.evt = getattr(event.input, "event", None)
