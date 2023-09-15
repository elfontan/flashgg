# Gen Plots

# import ROOT in batch mode
import sys
oldargv = sys.argv[:]
sys.argv = [ '-b-' ]
from ROOT import *
gROOT.SetBatch(True)
sys.argv = oldargv
gStyle.SetOptStat(0)
gStyle.SetOptFit(1)
from array import array

# load FWLite C++ libraries
gSystem.Load("libFWCoreFWLite.so");
gSystem.Load("libDataFormatsFWLite.so");
#AutoLibraryLoader.enable()
FWLiteEnabler.enable()

# load FWlite python libraries
from DataFormats.FWLite import Handle, Events

gen, genLabel = Handle("GenEventInfoProduct"), ("generator")

handlePruned, prunedLabel  = Handle ("std::vector<reco::GenParticle>"), ("genParticles")
#handlePruned, prunedLabel  = Handle ("std::vector<reco::GenParticle>"), ("prunedGenParticles") # for MiniAOD

# Histograms

genmass = TH1F("genmass","genmass",120,0,60); genmass.Sumw2() #all diphotons mass
genmassfragor = TH1F("genmassfragor","genmassfragor",120,0,60); genmassfragor.Sumw2() #all diphotons passing gen fragment cut if it is an or statement instead of and
genmassfrag = TH1F("genmassfrag","genmassfrag",120,0,60); genmassfrag.Sumw2() #all diphotons passing gen fragment cut
genmassmicro = TH1F("genmassmicro","genmassmicro",120,0,60); genmassmicro.Sumw2() #all diphotons with tight photon pt filters akin to microAOD
genmasspteta = TH1F("genmasspteta","genmasspteta",120,0,60); genmasspteta.Sumw2() #all diphotons with pt 30, 18 and eta 2.5 cut

genmass.SetMaximum(7000)
genmass.SetMinimum(0)
genmassfrag.SetMaximum(7000)
genmassfrag.SetMinimum(0)
genmassmicro.SetMaximum(7000)
genmassmicro.SetMinimum(0)
genmasspteta.SetMaximum(7000)
genmasspteta.SetMinimum(0)


events = Events([
"/eos/user/a/atsatsos/mc/BkgMCGeneration/diphoton_mgg0to40_v2/wmLHEG_0_543502.0.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/diphoton_mgg0to40_v2/wmLHEG_1_543502.1.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/diphoton_mgg0to40_v2/wmLHEG_2_543502.2.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/diphoton_mgg0to40_v2/wmLHEG_3_543502.3.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/diphoton_mgg0to40_v2/wmLHEG_4_543502.4.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/diphoton_mgg0to40_v2/wmLHEG_5_543502.5.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/diphoton_mgg0to40_v2/wmLHEG_6_543502.6.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/diphoton_mgg0to40_v2/wmLHEG_7_543502.7.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/diphoton_mgg0to40_v2/wmLHEG_8_543502.8.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/diphoton_mgg0to40_v2/wmLHEG_9_543502.9.root"])

for i,event in enumerate(events):
  event.getByLabel(prunedLabel, handlePruned)
  event.getByLabel(genLabel, gen)

  #if (i%1000==0): print "Event: ",i
  print "Event: ",i
  if (i==200000): break

  if (gen.product().weight() != 0.0): w = 1.0
#  if (gen.product().weight()>0.0): w = 1.0
#  else: w = -1.0
  
  pruned = handlePruned.product()

  npho=0; 

  pho={}
  phom=TLorentzVector(0,0,0,0)

  for p in pruned :
 
    if (abs(p.pdgId())==22 and p.mother().pdgId()==22):
      if (p.pt()>3.0):
        print p.pt(), p.mother().pdgId(), p.status(), p.eta(), p.phi()
      pho[npho]=TLorentzVector(p.px(),p.py(),p.pz(),p.energy())
      if npho < 2:
        print "Photon: ", npho, "Photon pT: ", p.pt(), "Mother: ", p.mother().pdgId(), "Status: ", p.status()
      npho+=1

  if npho>=2: 
    print npho
    phom = pho[0]+pho[1]

    genmass.Fill(phom.M(),w) #diphoton mass

    if ((pho[0].Pt()>10.0 or pho[1].Pt()>10.0)): 
      genmassfragor.Fill(phom.M(),w) #fragment or statement

    if ((pho[0].Pt()>10.0 and pho[1].Pt()>10.0)):
      genmassfrag.Fill(phom.M(),w) #fragment

    if ((pho[0].Pt()>25.0 and pho[1].Pt()>15.0) or (pho[0].Pt()>15.0 and pho[1].Pt()>25.0)):
      genmassmicro.Fill(phom.M(),w) #microAOD

    if ((pho[0].Pt()>30.0 and pho[1].Pt()>18.0) or (pho[0].Pt()>18.0 and pho[1].Pt()>30.0)):
      if (abs(pho[0].Eta())<2.5 and abs(pho[1].Eta())<2.5):
        genmasspteta.Fill(phom.M(),w) #FGG ntuple cuts

print "all mass: ",genmass.Integral()
print "fragment or: ",genmassfragor.Integral()
print "fragment: ",genmassfrag.Integral()
print "uAOD pt: ",genmassmicro.Integral()
print "pT and eta cuts: ",genmasspteta.Integral()

gStyle.SetOptStat(0)
gStyle.SetOptTitle(0)

c1 = TCanvas("c1","c1",800,800)
c1.cd()

genmass.SetLineColor(2)
genmass.Draw("ehist")
genmass.SetXTitle("m_{#gamma#gamma} [GeV]")

genmassfragor.SetLineColor(7)
genmassfragor.Draw("ehistsame")
genmassfragor.SetXTitle("m_{#gamma#gamma} [GeV]")

genmassfrag.SetLineColor(3)
genmassfrag.Draw("ehistsame")
genmassfrag.SetXTitle("m_{#gamma#gamma} [GeV]")

genmassmicro.SetLineColor(4)
genmassmicro.Draw("ehistsame")
genmassmicro.SetXTitle("m_{#gamma#gamma} [GeV]")

genmasspteta.SetLineColor(6)
genmasspteta.Draw("ehistsame")
genmasspteta.SetXTitle("m_{#gamma#gamma} [GeV]")

leg = TLegend(0.6,0.75,0.9,0.9)
leg.AddEntry(genmass,"Gen Background Sample")
leg.AddEntry(genmassfragor,"Gen Background Sample, Fragment OR Cut")
leg.AddEntry(genmassfrag,"Gen Background Sample, Fragment AND Cut")
leg.AddEntry(genmassmicro,"Gen Background Sample, MicroAOD Cut")
leg.AddEntry(genmasspteta,"Gen Background Sample, pT and Eta Cut")
leg.Draw("same")

c1.SaveAs("mass_mgg040bkg_gen_22mother.png")
c1.SaveAs("mass_mgg040bkg_gen_22mother.pdf")
