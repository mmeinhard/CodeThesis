from math import sqrt

class GenParticle:
    def __init__(self, tree, n):
        self.pdgId = tree.GenPart_pdgId[n];
        self.pt = tree.GenPart_pt[n];
        self.eta = tree.GenPart_eta[n];
        self.phi = tree.GenPart_phi[n];
        # nanoAOD: Mass stored for all particles with mass > 10 GeV
        # and photons with mass > 1 GeV. For other particles you can lookup from PDGID:
        # https://github.com/cms-nanoAOD/cmssw/blob/master/PhysicsTools/NanoAOD/python/genparticles_cff.py#L44
        self.mass = tree.GenPart_mass[n]
        self.status = tree.GenPart_status[n];
        self.genPartIdxMother = tree.GenPart_genPartIdxMother[n];
        pass
    @staticmethod
    def make_array(input):
        return [GenParticle(input, i) for i in range(input.nGenPart)]

class GenJet:
    def __init__(self, tree, n):
        self.pt = tree.GenJet_pt[n];
        self.eta = tree.GenJet_eta[n];
        self.phi = tree.GenJet_phi[n];
        self.mass = tree.GenJet_mass[n];
        pass
    @staticmethod
    def make_array(input):
        return [GenJet(input, i) for i in range(input.nGenJet)]



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
	#if idx == 0: #Shouldn't be needed...
	#	print "NB: realGenMothers aborted due to deep recursion"
	#	return ret
	if gp.genPartIdxMother >= 0:
		mom = GenParticle[gp.genPartIdxMother]
		if mom.pdgId == gp.pdgId:
			ret += realGenMothers(GenParticle,mom)
		else:
			ret.append(mom)
	else:
		return ret
	return ret

def allGenMothers(GenParticle,gp):
	"""Get the mothers of a particle X going through intermediate X -> X' chains.
		e.g. if Y -> X, X -> X' realGenMothers(X') = Y"""
	ret = []
	#if idx == 0: #Shouldn't be needed...
	#	print "NB: realGenMothers aborted due to deep recursion"
	#	return ret
	if gp.genPartIdxMother >= 0:
		mom = GenParticle[gp.genPartIdxMother]
		ret.append(abs(mom.pdgId))
		ret += allGenMothers(GenParticle,mom)
	else:
		return ret
	return ret

def realGenDaughters(GenParticle,gp,excludeRadiation=True):
    """Get the daughters of a particle, going through radiative X -> X' + a
       decays, either including or excluding the radiation among the daughters
       e.g. for  
                  X -> X' + a, X' -> b c 
           realGenDaughters(X, excludeRadiation=True)  = { b, c }
           realGenDaughters(X, excludeRadiation=False) = { a, b, c }"""
    ret = []
    for dau in getDaughters(GenParticle,gp):
        if dau.pdgId == gp.pdgId:
            if excludeRadiation:
                return realGenDaughters(GenParticle,dau)
            else:
                ret += realGenDaughters(GenParticle,dau)
        else:
            ret.append(dau)
	return ret

#def getDaughters(GenParticle,gp):
#	ret = []
#	for part in GenParticle:
#		if part != gp:
#			if part.genPartIdxMother == GenParticle.index(gp):
#				ret.append(part)
#	return ret

#Use this function for Delphes
def getDaughters(GenParticle,gp):
   ret = []
   idx = GenParticle.index(gp)
   for part in GenParticle:
       if part != gp:
           if part.genPartIdxMother == idx:
               ret.append(part)
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
		self.idMom = GenParticle[n].genPartIdxMother
        #What about isPromptHard? Is it needed?
		pass

	@staticmethod
	def make_array(GenParticle):
		ret = []
		for i in range(len(GenParticle)):	
			if abs(GenParticle[i].pdgId) == 5:	
				mom = GenParticle[GenParticle[i].genPartIdxMother]  
				if abs(mom.pdgId)  == 6: 
					dauids = [abs(dau.pdgId) for dau in getDaughters(GenParticle,mom)]
					if 6 not in dauids:	 
						ret.append(i) 		
		return list(set([GenBQuarkFromTop(GenParticle, i) for i in ret]))


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
				if abs(GenParticle[GenParticle[i].genPartIdxMother].pdgId) == 15:
					ret.append(i)
					break			
		return [GenLepFromTau(GenParticle, i) for i in ret]

class GenHiggsBoson:
	def __init__(self, GenParticle, n, genHiggsDecayMode):
		self.pdgId = GenParticle[n].pdgId;
		self.pt = GenParticle[n].pt;
		self.eta = GenParticle[n].eta;
		self.phi = GenParticle[n].phi;
		self.status = GenParticle[n].status;
		self.charge = -sign(GenParticle[n].pdgId);
		self.mass = GenParticle[n].mass;
		self.genHiggsDecayMode = genHiggsDecayMode;
        #What about isPromptHard? Is it needed?
		pass

	@staticmethod
	def make_array(GenParticle):
		ret = []
		for i in range(len(GenParticle)):		    
			if abs(GenParticle[i].pdgId) == 25: 
				dauids = [abs(dau.pdgId) for dau in getDaughters(GenParticle,GenParticle[i])]
				if 25 not in dauids:
					ret.append(i)
					dauhiggs = getDaughters(GenParticle,GenParticle[i])
					genHiggsDecayMode = abs(dauhiggs[0].pdgId) if len(dauhiggs) > 0 else 0
					genHiggsDecayMode += abs(dauhiggs[1].pdgId if len(dauhiggs) > 1 and abs(dauhiggs[1].pdgId) != abs(dauhiggs[0].pdgId) else 0) * 10000
		return [GenHiggsBoson(GenParticle, i,genHiggsDecayMode) for i in ret]

class GenTop:
	def __init__(self, GenParticle, n):
		self.pdgId = GenParticle[n].pdgId;
		self.pt = GenParticle[n].pt;
		self.eta = GenParticle[n].eta;
		self.phi = GenParticle[n].phi;
		self.status = GenParticle[n].status;
		self.charge = -sign(GenParticle[n].pdgId);
		self.mass = GenParticle[n].mass;
		self.id = n
		#Need to get top decay mode
		#go over top daughters
		decayMode = -10
		daus = getDaughters(GenParticle,GenParticle[n])
		for dau in daus:
			#found the W
			if abs(dau.pdgId) == 24:
				#find the true daughters of the W (in case of decay chain)
				W_daus = realGenDaughters(GenParticle,dau)
				decayMode = -1
				#go over the daughters of the W
				for idauw in range(len(W_daus)):
					w_dau_id = abs(W_daus[idauw].pdgId)
					#leptonic
					if w_dau_id in [11,12,13,14,15,16]:
						decayMode = 0
						break
					#hadronic
					elif w_dau_id < 6:
						decayMode = 1
						break
		self.decayMode = decayMode
		pass

	@staticmethod
	def make_array(GenParticle):
		ret = []
		for i in range(len(GenParticle)):		    
			if abs(GenParticle[i].pdgId) == 6: 
				dauids = [abs(dau.pdgId) for dau in getDaughters(GenParticle,GenParticle[i])]				
				if 6 not in dauids:
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
				if abs(GenParticle[GenParticle[i].genPartIdxMother].pdgId) not in {11,13,15}:
					momids = [(m, abs(m.pdgId)) for m in realGenMothers(GenParticle,GenParticle[i])]
					#have a look at the lepton mothers
					isW = False
					istop = False
					isWZ = False
					for mom, momid in momids:
						if momid == 24:
							isW = True
							isWZ = True
							wmomids = [(m, abs(m.pdgId)) for m in realGenMothers(GenParticle,mom)]
							for wmom, wmomid in wmomids:
								if wmomid == 6:
									istop == True
						if momid == 23:
							isWZ = True
					if istop == True or isWZ == True:	
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
		self.idMom = GenParticle[GenParticle[n].genPartIdxMother].genPartIdxMother
        #What about isPromptHard? Is it needed?
		pass

	@staticmethod
	def make_array(GenParticle):
		ret = []
		for i in range(len(GenParticle)):
			if abs(GenParticle[i].pdgId) <= 5 and abs(GenParticle[GenParticle[i].genPartIdxMother].pdgId) in [23,24]:
				ret.append(i)
		return list(set([GenWZQuark(GenParticle, i) for i in ret]))

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
			if abs(GenParticle[i].pdgId) in [3,4,5]:
				mom = GenParticle[GenParticle[i].genPartIdxMother]  
				if abs(mom.pdgId)  == 25: 
					dauids = [abs(dau.pdgId) for dau in getDaughters(GenParticle,mom)]
					if 25 not in dauids:	 
						ret.append(i) 	
		#list(set(..)) to remove hypothetic duplicates
		return list(set([GenBQuarkFromHiggs(GenParticle, i) for i in ret]))

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
					mom = GenParticle[GenParticle[i].genPartIdxMother]
					if abs(mom.pdgId) == 24:
						#wmomids = [(m, abs(m.pdgId)) for m in realGenMothers(GenParticle,mom)]
						wmomids = [abs(m.pdgId) for m in realGenMothers(GenParticle, mom)]
						if 6 in wmomids:
							#save mu,e from t->W->mu/e
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
					if GenParticle[i].pt > 20:           
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
					if GenParticle[i].pt > 20:           
						ret.append(i)
		return [GenGluonFromB(GenParticle, i) for i in ret]

class GenISRGluon:
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
                momids = allGenMothers(GenParticle,GenParticle[i])
                if 6 not in momids:
                    if 25 not in momids:
                        if GenParticle[i].pt > 10:           
                            ret.append(i)
        return [GenISRGluon(GenParticle, i) for i in ret]


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


