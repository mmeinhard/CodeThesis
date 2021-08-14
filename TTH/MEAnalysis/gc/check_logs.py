#! /usr/bin/env python
import os
import subprocess
from ROOT import TH1F, TCanvas, TFile, TObject

#samples = ["QCD300","QCD300x","QCD500","QCD500x","QCD700","QCD700x","QCD1000","QCD1500","QCD2000","TTbar","ttHbb","ttHNon"]
#samples = ["tth","tthnon","ttbar","qcd300","qcd500","qcd700","qcd1000","qcd1500","qcd2000"]
samples = ["tth"]
copy = 0
extract = 0
analyse = 1
report = 1

#se = "root://storage01.lcg.cscs.ch/pnfs/lcg.cscs.ch/cms/trivcat//store/user/dsalerno"
se = "storage01.lcg.cscs.ch" #ignored
folder = "/mnt/t3nfs01/data01/shome/dsalerno/TTH_2016/TTH_80X_M17/CMSSW_8_0_25/src/TTH/MEAnalysis/gc"

dataset = {
    "qcd300":"QCD_HT300to500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
    "QCD300x":"QCD_HT300to500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
    "qcd500":"QCD_HT500to700_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
    "QCD500x":"QCD_HT500to700_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
    "qcd700":"QCD_HT700to1000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
    "QCD700x":"QCD_HT700to1000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
    "qcd1000":"QCD_HT1000to1500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
    "qcd1500":"QCD_HT1500to2000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
    "qcd2000":"QCD_HT2000toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
    "ttbar":"TT_TuneCUETP8M1_13TeV-powheg-pythia8",
    "tth":"ttHTobb_M125_13TeV_powheg_pythia8",
    "tthnon":"ttHToNonbb_M125_13TeV_powheg_pythia8",
}

endpath = "/scratch/dsalerno/tth/80x_M17/gc_JoosepFeb_v5/"  ##CHANGE HERE!!!

for sample in samples: 
    print "\n",sample
    path = "work.meanalysis_"+sample+"_JoosepFeb_v5/output"
    destination = endpath+sample+"/"
    if( copy ):
        listdir = "ls "+folder+"/"+path
        p = subprocess.Popen(listdir, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

        if not os.path.exists(destination):
            os.makedirs(destination)

        for line in p.stdout.readlines(): #job_0, job_1, etc...
            directory = line.split()[0]
            if (directory.find("_")<0):
                continue
            #directory = (line.split("/")[-1]).split()[0]
            #print ""
            #print "directory ", directory
            half = directory.split("_")[1]
            num = half.strip()
            listlog = listdir+"/"+directory
            q = subprocess.Popen(listlog, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

            newlog = "job_"+num+".stdout.gz"
            logfile = "job.stdout.gz"

            if not os.path.isfile(folder+"/"+path+"/"+directory+"/"+logfile):
                newlog = "job_"+num+".stdout"
                logfile = "job.stdout"
            if not os.path.isfile(folder+"/"+path+"/"+directory+"/"+logfile):
                continue
            #print "newlog", newlog
            if( os.path.isfile(destination+"/"+newlog) ):
                print newlog, " already copied"
                continue
            stdoutfile = "job_"+num+".stdout"
            if( os.path.isfile(destination+"/"+stdoutfile) ):
                print newlog, " already extracted"
                continue
            copylog = "cp "+folder+"/"+path+"/"+directory+"/"+logfile+" /"+destination+"/"+newlog
            #print copylog
            os.system(copylog)

    if( extract ):
        r = subprocess.Popen("ls "+destination, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

        for line in r.stdout.readlines():
            zipfile = line.split()[0]
            if(zipfile.find('stdout.gz')<0):
                continue
            #print "zipfile ", zipfile
            half = zipfile.split("_")[1]
            num = half.split(".")[0]
            stdoutfile = "job_"+num+".stdout"
            #print "stdoutfile", stdoutfile
            if( os.path.isfile(destination+"/"+stdoutfile) ):
                print stdoutfile, " already extracted"
                continue
            unzip = "gunzip "+destination+"/"+zipfile
            os.system(unzip)

    if( analyse ):
        success = 0
        outf = TFile.Open(endpath+"/jobtime.root","UPDATE")
        outf.cd()
        htime_total = TH1F("htime_total","htime_total",100,0,50)

        h_0_7_322   = TH1F("h_0_7_322","h_0_7_322",300,0,300)
        h_0_7_222   = TH1F("h_0_7_222","h_0_7_222",300,0,300)
        h_0_7_122   = TH1F("h_0_7_122","h_0_7_122",300,0,300)

        h_0_8_422   = TH1F("h_0_8_422","h_0_8_422",300,0,300)    
        h_0_8_322   = TH1F("h_0_8_322","h_0_8_322",500,0,500)
        h_0_8_222   = TH1F("h_0_8_222","h_0_8_122",500,0,500)
        h_0_8_122   = TH1F("h_0_8_122","h_0_8_122",500,0,500)

        h_0_9_422   = TH1F("h_0_9_422","h_0_9_422",300,0,300)
        h_0_9_322   = TH1F("h_0_9_322","h_0_9_322",500,0,500)
        h_0_9_222   = TH1F("h_0_9_222","h_0_9_122",500,0,500)
        h_0_9_122   = TH1F("h_0_9_122","h_0_9_122",1000,0,1000)

        h_0_10_421   = TH1F("h_0_10_421","h_0_10_421",300,0,300)    
        h_0_10_321   = TH1F("h_0_10_321","h_0_10_321",300,0,300)

        h_0_11_421   = TH1F("h_0_11_421","h_0_11_421",200,0,200)    
        h_0_11_321   = TH1F("h_0_11_321","h_0_11_321",300,0,300)

        h_0_12_421   = TH1F("h_0_12_421","h_0_12_421",300,0,300)    
        h_0_12_321   = TH1F("h_0_12_321","h_0_12_321",300,0,300)

        h_1_7_322   = TH1F("h_1_7_322","h_1_7_322",300,0,300)
        h_1_7_222   = TH1F("h_1_7_222","h_1_7_222",300,0,300)
        h_1_7_122   = TH1F("h_1_7_122","h_1_7_122",300,0,300)

        h_1_8_422   = TH1F("h_1_8_422","h_1_8_422",300,0,300)    
        h_1_8_322   = TH1F("h_1_8_322","h_1_8_322",500,0,500)
        h_1_8_222   = TH1F("h_1_8_222","h_1_8_122",500,0,500)
        h_1_8_122   = TH1F("h_1_8_122","h_1_8_122",500,0,500)

        h_1_9_422   = TH1F("h_1_9_422","h_1_9_422",300,0,300)
        h_1_9_322   = TH1F("h_1_9_322","h_1_9_322",500,0,500)
        h_1_9_222   = TH1F("h_1_9_222","h_1_9_122",500,0,500)
        h_1_9_122   = TH1F("h_1_9_122","h_1_9_122",1000,0,1000)

        h_1_10_421   = TH1F("h_1_10_421","h_1_10_421",300,0,300)    
        h_1_10_321   = TH1F("h_1_10_321","h_1_10_321",300,0,300)

        h_1_11_421   = TH1F("h_1_11_421","h_1_11_421",200,0,200)    
        h_1_11_321   = TH1F("h_1_11_321","h_1_11_321",300,0,300)

        h_1_12_421   = TH1F("h_1_12_421","h_1_12_421",300,0,300)    
        h_1_12_321   = TH1F("h_1_12_321","h_1_12_321",300,0,300)

        s = subprocess.Popen("ls "+destination, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

        for line in s.stdout.readlines():
            if(line.find('stdout') > 0):
                outfile = line.split()[0]
                #print "outfile", outfile
                f = open(destination+"/"+outfile)
                lines = f.readlines()
                hypo = -1
                cat = -1
                method = -1
                sam = ""
                start = 0
                for l in lines:
                    if(l.find('FILE_NAMES') == 0):
                        for sm in samples:
                            if(l.find(dataset[sm])>0):
                                sam = sm

                    if (l.find(' INFO ') > 0):
                        if(start==0):
                            startdate = l.split()[0].split('-')
                            starttime = l.split()[1].split(',')[0].split(':')
                            start = 1
                        enddate = l.split()[0].split('-')
                        endtime = l.split()[1].split(',')[0].split(':')

                    if(l.find('hypo=0')>0):
                        hypo = 0
                    if(l.find('hypo=1')>0):
                        hypo = 1                   

                    if(l.find('fh_j7_tge5')>0 or l.find('fh_j7_t4')>0):
                        cat = 7
                    if(l.find('fh_j8_tge5')>0 or l.find('fh_j8_t4')>0):
                        cat = 8                    
                    if(l.find('fh_jge9_tge5')>0 or l.find('fh_jge9_t4')>0):
                        cat = 9
                    if(l.find('fh_j8_t3')>0 ):
                        cat = 10
                    if(l.find('fh_j7_t3')>0 ):
                        cat = 11
                    if(l.find('fh_jge9_t3')>0 ):
                        cat = 12

                    if(l.find('conf=FH_3w2h2t')>0):
                        method = 322
                    if(l.find('conf=FH_4w2h2t')>0):
                        method = 422
                    if(l.find('conf=FH_4w2h1t')>0):
                        method = 421
                    if(l.find('conf=FH_3w2h1t')>0):
                        method = 321
                    if(l.find('conf=FH_0w2w2h2t')>0):
                        method = 222
                    if(l.find('conf=FH_1w1w2h2t')>0):
                        method = 122

                    if(l.find('Job done in...............')>0):
                        half = l.split('...............')[1]
                        time = float(half.split()[0])
                        if(hypo==0):
                            if(cat==7):
                                if(method==322):
                                    h_0_7_322.Fill(time)
                                if(method==222):
                                    h_0_7_222.Fill(time)
                                if(method==122):
                                    h_0_7_122.Fill(time)
                            if(cat==8):
                                if(method==422):
                                    h_0_8_422.Fill(time)
                                if(method==322):
                                    h_0_8_322.Fill(time)
                                if(method==222):
                                    h_0_8_222.Fill(time)
                                if(method==122):
                                    h_0_8_122.Fill(time)
                            if(cat==9):
                                if(method==422):
                                    h_0_9_422.Fill(time)
                                if(method==322):
                                    h_0_9_322.Fill(time)
                                if(method==222):
                                    h_0_9_222.Fill(time)
                                if(method==122):
                                    h_0_9_122.Fill(time)
                            if(cat==10):
                                if(method==421):
                                    h_0_10_421.Fill(time)
                                if(method==321):
                                    h_0_10_321.Fill(time)
                            if(cat==11):
                                if(method==421):
                                    h_0_11_421.Fill(time)
                                if(method==321):
                                    h_0_11_321.Fill(time)
                            if(cat==12):
                                if(method==421):
                                    h_0_12_421.Fill(time)
                                if(method==321):
                                    h_0_12_321.Fill(time)
                        if(hypo==1):
                            if(cat==7):
                                if(method==322):
                                    h_1_7_322.Fill(time)
                                if(method==222):
                                    h_1_7_222.Fill(time)
                                if(method==122):
                                    h_1_7_122.Fill(time)
                            if(cat==8):
                                if(method==422):
                                    h_1_8_422.Fill(time)
                                if(method==322):
                                    h_1_8_322.Fill(time)
                                if(method==222):
                                    h_1_8_222.Fill(time)
                                if(method==122):
                                    h_1_8_122.Fill(time)
                            if(cat==9):
                                if(method==422):
                                    h_1_9_422.Fill(time)
                                if(method==322):
                                    h_1_9_322.Fill(time)
                                if(method==222):
                                    h_1_9_222.Fill(time)
                                if(method==122):
                                    h_1_9_122.Fill(time)
                            if(cat==10):
                                if(method==421):
                                    h_1_10_421.Fill(time)
                                if(method==321):
                                    h_1_10_321.Fill(time)
                            if(cat==11):
                                if(method==421):
                                    h_1_11_421.Fill(time)
                                if(method==321):
                                    h_1_11_321.Fill(time)
                            if(cat==12):
                                if(method==421):
                                    h_1_12_421.Fill(time)
                                if(method==321):
                                    h_1_12_321.Fill(time)

                    if(l.find('Looper done')==0):
                        success += 1

                # end loop over lines
                totaltime  = ((float(enddate[0])-float(startdate[0]))*365+(float(enddate[1])-float(startdate[1]))*30+(float(enddate[2])-float(startdate[2])))*24.0
                totaltime += ((float(endtime[0])-float(starttime[0]))+(float(endtime[1])-float(starttime[1]))/60.0+(float(endtime[2])-float(starttime[2]))/3600.0)
                htime_total.Fill( totaltime )

                # t = subprocess.Popen("grep 'timeto' "+destination+"/"+outfile, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

                # for line in t.stdout.readlines():
                #     if(line.find('totalJob') > 0):
                #         jobtime = line.split()[1]
                #         #print "jobtime ", float(jobtime)/3600
                #         htime.Fill(float(jobtime)/3600)

        treedir = outf.GetDirectory( sample)
        if(treedir==None):
            treedir = outf.mkdir( sample )

        treedir.cd()
        htime_total.Write("", TObject.kOverwrite)

        h_0_7_322.Write("", TObject.kOverwrite)
        h_0_7_222.Write("", TObject.kOverwrite)
        h_0_7_122.Write("", TObject.kOverwrite)
        h_0_8_422.Write("", TObject.kOverwrite)
        h_0_8_322.Write("", TObject.kOverwrite)
        h_0_8_222.Write("", TObject.kOverwrite)
        h_0_8_122.Write("", TObject.kOverwrite)
        h_0_9_422.Write("", TObject.kOverwrite)
        h_0_9_322.Write("", TObject.kOverwrite)
        h_0_9_222.Write("", TObject.kOverwrite)
        h_0_9_122.Write("", TObject.kOverwrite)
        h_0_10_421.Write("", TObject.kOverwrite)
        h_0_10_321.Write("", TObject.kOverwrite)
        h_0_11_421.Write("", TObject.kOverwrite)
        h_0_11_321.Write("", TObject.kOverwrite)
        h_0_12_421.Write("", TObject.kOverwrite)
        h_0_12_321.Write("", TObject.kOverwrite)

        h_1_7_322.Write("", TObject.kOverwrite)
        h_1_7_222.Write("", TObject.kOverwrite)
        h_1_7_122.Write("", TObject.kOverwrite)
        h_1_8_422.Write("", TObject.kOverwrite)
        h_1_8_322.Write("", TObject.kOverwrite)
        h_1_8_222.Write("", TObject.kOverwrite)
        h_1_8_122.Write("", TObject.kOverwrite)
        h_1_9_422.Write("", TObject.kOverwrite)
        h_1_9_322.Write("", TObject.kOverwrite)
        h_1_9_222.Write("", TObject.kOverwrite)
        h_1_9_122.Write("", TObject.kOverwrite)
        h_1_10_421.Write("", TObject.kOverwrite)
        h_1_10_321.Write("", TObject.kOverwrite)
        h_1_11_421.Write("", TObject.kOverwrite)
        h_1_11_321.Write("", TObject.kOverwrite)
        h_1_12_421.Write("", TObject.kOverwrite)
        h_1_12_321.Write("", TObject.kOverwrite)

        outf.Close()

        print "successful_jobs",success

    if( report ):
        outf = TFile.Open(endpath+"/jobtime.root")
        outf.cd()

        hvhbb   = outf.Get(sample+"/htime_vhbb")
        hmem    = outf.Get(sample+"/htime_mem")
        htotal  = outf.Get(sample+"/htime_total")

        hh_0_7_322   = outf.Get(sample+"/h_0_7_322")
        hh_0_7_222   = outf.Get(sample+"/h_0_7_222")
        hh_0_7_122   = outf.Get(sample+"/h_0_7_122")

        hh_0_8_422   = outf.Get(sample+"/h_0_8_422")
        hh_0_8_322   = outf.Get(sample+"/h_0_8_322")
        hh_0_8_222   = outf.Get(sample+"/h_0_8_222")
        hh_0_8_122   = outf.Get(sample+"/h_0_8_122")

        hh_0_9_422   = outf.Get(sample+"/h_0_9_422")
        hh_0_9_322   = outf.Get(sample+"/h_0_9_322")
        hh_0_9_222   = outf.Get(sample+"/h_0_9_222")
        hh_0_9_122   = outf.Get(sample+"/h_0_9_122")

        hh_0_10_421   = outf.Get(sample+"/h_0_10_421")
        hh_0_10_321   = outf.Get(sample+"/h_0_10_321")

        hh_0_11_421   = outf.Get(sample+"/h_0_11_421")
        hh_0_11_321   = outf.Get(sample+"/h_0_11_321")

        hh_0_12_421   = outf.Get(sample+"/h_0_12_421")
        hh_0_12_321   = outf.Get(sample+"/h_0_12_321")

        hh_1_7_322   = outf.Get(sample+"/h_1_7_322")
        hh_1_7_222   = outf.Get(sample+"/h_1_7_222")
        hh_1_7_122   = outf.Get(sample+"/h_1_7_122")

        hh_1_8_422   = outf.Get(sample+"/h_1_8_422")
        hh_1_8_322   = outf.Get(sample+"/h_1_8_322")
        hh_1_8_222   = outf.Get(sample+"/h_1_8_222")
        hh_1_8_122   = outf.Get(sample+"/h_1_8_122")

        hh_1_9_422   = outf.Get(sample+"/h_1_9_422")
        hh_1_9_322   = outf.Get(sample+"/h_1_9_322")
        hh_1_9_222   = outf.Get(sample+"/h_1_9_222")
        hh_1_9_122   = outf.Get(sample+"/h_1_9_122")

        hh_1_10_421   = outf.Get(sample+"/h_1_10_421")
        hh_1_10_321   = outf.Get(sample+"/h_1_10_321")

        hh_1_11_421   = outf.Get(sample+"/h_1_11_421")
        hh_1_11_321   = outf.Get(sample+"/h_1_11_321")

        hh_1_12_421   = outf.Get(sample+"/h_1_12_421")
        hh_1_12_321   = outf.Get(sample+"/h_1_12_321")

        print "\nMethod Events Mean StdDev"
        print "\n***cat7***"
        print "ttH_hypo"
        print "322", hh_0_7_322.GetEntries(), hh_0_7_322.GetMean(), hh_0_7_322.GetStdDev()
        print "222", hh_0_7_222.GetEntries(), hh_0_7_222.GetMean(), hh_0_7_222.GetStdDev()
        print "122", hh_0_7_122.GetEntries(), hh_0_7_122.GetMean(), hh_0_7_122.GetStdDev()
        print "ttbb_hypo"
        print "322", hh_1_7_322.GetEntries(), hh_1_7_322.GetMean(), hh_1_7_322.GetStdDev()
        print "222", hh_1_7_222.GetEntries(), hh_1_7_222.GetMean(), hh_1_7_222.GetStdDev()
        print "122", hh_1_7_122.GetEntries(), hh_1_7_122.GetMean(), hh_1_7_122.GetStdDev()

        print "\n***cat8***"
        print "ttH_hypo"
        print "422", hh_0_8_422.GetEntries(), hh_0_8_422.GetMean(), hh_0_8_422.GetStdDev()
        print "322", hh_0_8_322.GetEntries(), hh_0_8_322.GetMean(), hh_0_8_322.GetStdDev()
        print "222", hh_0_8_222.GetEntries(), hh_0_8_222.GetMean(), hh_0_8_222.GetStdDev()
        print "122", hh_0_8_122.GetEntries(), hh_0_8_122.GetMean(), hh_0_8_122.GetStdDev()
        print "ttbb_hypo"
        print "422", hh_1_8_422.GetEntries(), hh_1_8_422.GetMean(), hh_1_8_422.GetStdDev()
        print "322", hh_1_8_322.GetEntries(), hh_1_8_322.GetMean(), hh_1_8_322.GetStdDev()
        print "222", hh_1_8_222.GetEntries(), hh_1_8_222.GetMean(), hh_1_8_222.GetStdDev()
        print "122", hh_1_8_122.GetEntries(), hh_1_8_122.GetMean(), hh_1_8_122.GetStdDev()

        print "\n***cat9***"
        print "ttH_hypo"
        print "422", hh_0_9_422.GetEntries(), hh_0_9_422.GetMean(), hh_0_9_422.GetStdDev()
        print "322", hh_0_9_322.GetEntries(), hh_0_9_322.GetMean(), hh_0_9_322.GetStdDev()
        print "222", hh_0_9_222.GetEntries(), hh_0_9_222.GetMean(), hh_0_9_222.GetStdDev()
        print "122", hh_0_9_122.GetEntries(), hh_0_9_122.GetMean(), hh_0_9_122.GetStdDev()
        print "ttbb_hypo"
        print "422", hh_1_9_422.GetEntries(), hh_1_9_422.GetMean(), hh_1_9_422.GetStdDev()
        print "322", hh_1_9_322.GetEntries(), hh_1_9_322.GetMean(), hh_1_9_322.GetStdDev()
        print "222", hh_1_9_222.GetEntries(), hh_1_9_222.GetMean(), hh_1_9_222.GetStdDev()
        print "122", hh_1_9_122.GetEntries(), hh_1_9_122.GetMean(), hh_1_9_122.GetStdDev()

        print "\n***cat10***"
        print "ttH_hypo"
        print "421", hh_0_10_421.GetEntries(), hh_0_10_421.GetMean(), hh_0_10_421.GetStdDev()
        print "321", hh_0_10_321.GetEntries(), hh_0_10_321.GetMean(), hh_0_10_321.GetStdDev()
        print "ttbb_hypo"
        print "421", hh_1_10_421.GetEntries(), hh_1_10_421.GetMean(), hh_1_10_421.GetStdDev()
        print "321", hh_1_10_321.GetEntries(), hh_1_10_321.GetMean(), hh_1_10_321.GetStdDev()

        print "\n***cat11***"
        print "ttH_hypo"
        print "421", hh_0_11_421.GetEntries(), hh_0_11_421.GetMean(), hh_0_11_421.GetStdDev()
        print "321", hh_0_11_321.GetEntries(), hh_0_11_321.GetMean(), hh_0_11_321.GetStdDev()
        print "ttbb_hypo"
        print "421", hh_1_11_421.GetEntries(), hh_1_11_421.GetMean(), hh_1_11_421.GetStdDev()
        print "321", hh_1_11_321.GetEntries(), hh_1_11_321.GetMean(), hh_1_11_321.GetStdDev()

        print "\n***cat12***"
        print "ttH_hypo"
        print "421", hh_0_12_421.GetEntries(), hh_0_12_421.GetMean(), hh_0_12_421.GetStdDev()
        print "321", hh_0_12_321.GetEntries(), hh_0_12_321.GetMean(), hh_0_12_321.GetStdDev()
        print "ttbb_hypo"
        print "421", hh_1_12_421.GetEntries(), hh_1_12_421.GetMean(), hh_1_12_421.GetStdDev()
        print "321", hh_1_12_321.GetEntries(), hh_1_12_321.GetMean(), hh_1_12_321.GetStdDev()

        print "\n Total_mean stdev"
        print htotal.GetMean(), htotal.GetStdDev()
