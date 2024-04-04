# ------------------------------------------------------- #
# Use this script within an environment allowing python3: #
# otherwise problems related to the usage of array might  #
# happen                                                  #
# ------------------------------------------------------- #
from ROOT import * 
from ROOT import TFile, TTree, TBranch, TList, gROOT, gSystem, TChain
import random, copy
import ROOT, array, CMSGraphics, CMS_lumi
import argparse
import sys
import os

gROOT.SetBatch()
gStyle.SetOptStat(0)
gStyle.SetOptTitle(0)
gStyle.SetOptStat(0)

argparser = argparse.ArgumentParser(description='Parser used for non default arguments', formatter_class=argparse.ArgumentDefaultsHelpFormatter, add_help=True)
argparser.add_argument('--outdir', dest='outdir', default='./', help='Output dir')
argparser.add_argument('--minV', dest='minV', default='-0.9', help='Minimum Value for maxPhoId')
argparser.add_argument('--maxV', dest='maxV', default='1.0', help='Maximum Value for maxPhoId')
argparser.add_argument('--log', dest='log', default=False, help='Log scale')

args = argparser.parse_args()
outputdir = args.outdir
minValue = args.minV
maxValue = args.maxV
logScale = args.log

# Obtain histogram files
# ----------------------
data = TFile("/eos/user/e/elfontan/DiPhotonAnalysis/diphotonBDT/NTUPLES_Oct2023/data/EGamma_D.root","READ") #Data with unweighted events, both regions
sideband = TFile("/eos/user/e/elfontan/DiPhotonAnalysis/diphotonBDT/reweighting/kest/output_sideband_PF_kest1D_Inclusive.root","READ")
mgg = TFile("/eos/user/e/elfontan/DiPhotonAnalysis/diphotonBDT/NTUPLES_Oct2023/bkg_dipho/diPhoton_all.root","READ")

# ------------------------ #
# SigmaEOverE REWEIGHTING  #
# ------------------------ #
# SigmaEOverE histos
# ------------------
h_sigmaEOE_sba0 = TH1F("h_sigmaEOE_sba0", "h_sigmaEOE_sba0", 200, 0., 0.2)
h_sigmaEOE_pre0 = TH1F("h_sigmaEOE_pre0", "h_sigmaEOE_pre0", 200, 0., 0.2)
h_sigmaEOE_mgg0 = TH1F("h_sigmaEOE_mgg0", "h_sigmaEOE_mgg0", 200, 0., 0.2)
h_sigmaEOE_sba0_reweighted = TH1F("h_sigmaEOE_sba0_reweighted", "h_sigmaEOE_sba0_reweighted", 200, 0., 0.2)
bkg0 = THStack("bkg0","bkg0")

# Reweighting function
# --------------------
def reweighting(inputFile_weights, rootFile_weights, sb_treeName, var):
#def reweight_distribution(inputFile_weights, rootFile_weights, sb_fileName, sb_treeName):
    # Open the input file
    input_file = TFile(inputFile_weights, "READ")
    if input_file.IsZombie():
        print("Error: Unable to open the input file.")
        return

    # Retrieve the weight histogram
    weight_histogram = input_file.Get(rootFile_weights)
    if not weight_histogram or not isinstance(weight_histogram, TH1):
        print("Error: Unable to retrieve the weight histogram.")
        return

    ## Open the sideband file
    #sb_file = ROOT.TFile(sb_fileName, "READ")
    #if sb_file.IsZombie():
    #    print("Error: Unable to open the sideband file.")
    #    return
    ## Open the input tree
    #input_tree = input_file.Get(sb_treeName)
    #if not input_tree or not isinstance(input_tree, ROOT.TTree):
    #    print("Error: Unable to retrieve the input tree.")
    #    return

    # Get the weight from the histogram
    bin_number = weight_histogram.GetXaxis().FindBin(var)
    w = weight_histogram.GetBinContent(bin_number)
    # For demonstration purposes, let's print the weighted variable
    #print("Weighted Variable: ", var, "*", weight, " = ", var*weight)

    # Close the input file
    input_file.Close()

    return w


# Get trees and create histograms for data
# ----------------------------------------
dat0 = data.Get("tagsDumper/trees/Data_13TeV_UntaggedTag_0")
mgg0 = mgg.Get("tagsDumper/trees/mgg_bkg_13TeV_UntaggedTag_0")
sb0 = sideband.Get("tagsDumper/trees/Data_13TeV_UntaggedTag_0")

print("----------Opening data tree")
c_dat0 = 0
for ev_dat0 in dat0:
    c_dat0 += 1
    #if (c_dat0 == 10): break
    if (not(c_dat0%20==0)): continue
    if (ev_dat0.dipho_leadIDMVA <= ev_dat0.dipho_subleadIDMVA and min(ev_dat0.dipho_leadIDMVA, ev_dat0.dipho_subleadIDMVA)>-0.7):
        h_sigmaEOE_pre0.Fill(ev_dat0.dipho_lead_sigmaEoE, 1.)
    elif (ev_dat0.dipho_leadIDMVA > ev_dat0.dipho_subleadIDMVA and min(ev_dat0.dipho_leadIDMVA, ev_dat0.dipho_subleadIDMVA)>-0.7):
        h_sigmaEOE_pre0.Fill(ev_dat0.dipho_sublead_sigmaEoE, 1.)
print("h_sigmaEOE_pre0 Integral = ", h_sigmaEOE_pre0.Integral())

print("----------Opening MC dipho tree")
c_mgg0 = 0
for ev_mgg0 in mgg0:
    c_mgg0 += 1
    #if (c_mgg0 == 10): break
    if (ev_mgg0.dipho_leadIDMVA <= ev_mgg0.dipho_subleadIDMVA and min(ev_mgg0.dipho_leadIDMVA, ev_mgg0.dipho_subleadIDMVA)>-0.7):
        h_sigmaEOE_mgg0.Fill(ev_mgg0.dipho_lead_sigmaEoE, ev_mgg0.weight*5.9546)
    elif (ev_mgg0.dipho_leadIDMVA > ev_mgg0.dipho_subleadIDMVA and min(ev_mgg0.dipho_leadIDMVA, ev_mgg0.dipho_subleadIDMVA)>-0.7):
        h_sigmaEOE_mgg0.Fill(ev_mgg0.dipho_sublead_sigmaEoE, ev_mgg0.weight*5.9546)
print("h_sigmaEOE_mgg0 Integral = ", h_sigmaEOE_mgg0.Integral())


# Create a new file to save the modified tree
# -------------------------------------------
new_file = TFile("/eos/user/e/elfontan/DiPhotonAnalysis/diphotonBDT/NTUPLES_Oct2023/sb_newfile_sigmaEOEreweighting_ALL.root", "RECREATE")
tagsDumper = new_file.mkdir("tagsDumper")
tagsDumper.cd()
trees = tagsDumper.mkdir("trees")

# Clone the original tree
# -----------------------
from array import array
#weight = array('f',[0.])
#event = array('I',[0])
#sb0.SetBranchAddress("weight",weight)
#sb0.SetBranchAddress("event",event)

weight_sigmaEOE = array('f',[0.])
new_tree = sb0.CloneTree(0)  # 0 indicates to clone the structure only

# Create a new branch in the new tree
# -----------------------------------
new_tree.Branch("weight_sigmaEOE", weight_sigmaEOE, "weight_sigmaEOE/F")

print("----------Opening sideband tree")
c_sb0 = 0
for ev_sb0 in sb0:
    #if (c_sb0 == 1000): break
    c_sb0 += 1
    #print("-------------------------------------------- EVENT ", c_sb0)
    #print ("ORIGINAL SB WEIGHT = ", weight[0])
    #if (not(c_sb0%20==0)): continue
    w_sigmaEOE = 1
    if (ev_sb0.dipho_leadIDMVA <= ev_sb0.dipho_subleadIDMVA):
        h_sigmaEOE_sba0.Fill(ev_sb0.dipho_lead_sigmaEoE, ev_sb0.weight*0.0622)
        print("w_sigmaEOE sublead PRE = ", w_sigmaEOE)
        #w_sigmaEOE = reweighting("f_sigmaEOE_reweighting.root", "h_ratio_sigmaEOE", "sb0", ev_sb0.dipho_lead_sigmaEoE)
        w_sigmaEOE = reweighting("f_sigmaEOE_reweighting_ALL.root", "h_ratio_sigmaEOE", "sb0", ev_sb0.dipho_lead_sigmaEoE)
        h_sigmaEOE_sba0_reweighted.Fill(ev_sb0.dipho_lead_sigmaEoE, ev_sb0.weight*0.0622*w_sigmaEOE)
        weight_sigmaEOE[0] = 1.*w_sigmaEOE
        print("w_sigmaEOE sublead POST = ", w_sigmaEOE)
    elif (ev_sb0.dipho_leadIDMVA > ev_sb0.dipho_subleadIDMVA):
        print("w_sigmaEOE lead PRE = ", w_sigmaEOE )
        h_sigmaEOE_sba0.Fill(ev_sb0.dipho_sublead_sigmaEoE, ev_sb0.weight*0.0622)
        #w_sigmaEOE = reweighting("f_sigmaEOE_reweighting.root", "h_ratio_sigmaEOE", "sb0", ev_sb0.dipho_sublead_sigmaEoE)
        w_sigmaEOE = reweighting("f_sigmaEOE_reweighting_ALL.root", "h_ratio_sigmaEOE", "sb0", ev_sb0.dipho_sublead_sigmaEoE)
        print("w_sigmaEOE lead POST = ", w_sigmaEOE )
        h_sigmaEOE_sba0_reweighted.Fill(ev_sb0.dipho_sublead_sigmaEoE, ev_sb0.weight*0.0622*w_sigmaEOE)
        weight_sigmaEOE[0] = 1.*w_sigmaEOE

    new_tree.Fill()

#reweighting("f_reweighting.root", "h_ratio_sigmaEOE", "sb0", "dipho_lead_sigmaEoE")
print("h_sigmaEOE_sba0 Integral = ", h_sigmaEOE_sba0.Integral())

# Save the new tree to the new file
# ---------------------------------
trees.cd()  # Change to the correct directory
new_tree.Write()

# Close the files
# ---------------
new_file.Close()

# Set Maximum
h_sigmaEOE_sba0.SetMaximum(27000)
h_sigmaEOE_sba0_reweighted.SetMaximum(27000)
h_sigmaEOE_pre0.SetMaximum(27000)
h_sigmaEOE_mgg0.SetMaximum(27000)
bkg0.SetMaximum(27000)

#Now we draw it out                                                                                                                          
gStyle.SetOptStat(0)
gStyle.SetOptTitle(0)

c1 = TCanvas("c1","c1",1200,1200)
c1.cd()
#c1.SetLeftMargin(0.15)                                                                                                          

#upper plot pad - Data histos                                                                                                       
pad1 = TPad("pad1","pad1", 0, 0.36, 1, 1.0)
pad1.Draw()
pad1.cd()
if (logScale):
    pad1.SetLogy()                                                                                                                    
pad1.SetBottomMargin(0.01)
pad1.SetLeftMargin(1.9)

h_sigmaEOE_sba0_reweighted.SetLineColor(kYellow-7)
h_sigmaEOE_sba0_reweighted.SetFillColorAlpha(kYellow-7,0.8)
h_sigmaEOE_sba0_reweighted.SetLineWidth(2)

h_sigmaEOE_sba0_reweighted.GetYaxis().SetTitle("Events/0.001 GeV")
h_sigmaEOE_sba0_reweighted.GetYaxis().SetTitleSize(25)
h_sigmaEOE_sba0_reweighted.GetYaxis().SetTitleFont(43)
h_sigmaEOE_sba0_reweighted.GetYaxis().SetTitleOffset(2.25)
h_sigmaEOE_sba0_reweighted.GetYaxis().SetLabelFont(43)
h_sigmaEOE_sba0_reweighted.GetYaxis().SetLabelOffset(0.01)
h_sigmaEOE_sba0_reweighted.GetYaxis().SetLabelSize(25)

h_sigmaEOE_mgg0.SetLineColor(kOrange-4)
h_sigmaEOE_mgg0.SetFillColorAlpha(kOrange-4,0.8)
h_sigmaEOE_mgg0.SetLineWidth(2)

bkg0.Add(h_sigmaEOE_mgg0)
bkg0.Add(h_sigmaEOE_sba0_reweighted)
h_sigmaEOE_sba0_reweighted.GetXaxis().SetLabelOffset(1.5)
h_sigmaEOE_mgg0.GetXaxis().SetLabelOffset(1.5)
h_sigmaEOE_sba0_reweighted.GetXaxis().SetLabelSize(0)
h_sigmaEOE_mgg0.GetXaxis().SetLabelSize(0)
bkg0.Draw("histo")

h_sigmaEOE_pre0.SetLineWidth(2)
h_sigmaEOE_pre0.SetLineColorAlpha(kBlack,0.8)
#h_sigmaEOE_pre0.SetLineColorAlpha(kOrange+9,0.8)
h_sigmaEOE_pre0.GetXaxis().SetLabelSize(0)
h_sigmaEOE_pre0.Draw("epsame")

leg = TLegend(0.2,0.5,0.7,0.88)
leg.AddEntry(h_sigmaEOE_sba0_reweighted,"#gamma-jet and jet-jet (Reweighted Sideband)")
leg.AddEntry(h_sigmaEOE_mgg0,"Diphoton MC")
leg.AddEntry(h_sigmaEOE_pre0,"Preselection Region")
leg.SetLineWidth(0)
leg.Draw("same")

c1.Update()
c1.cd()

#lower plot pad - Ratio plot
pad2 = TPad("pad2","pad2", 0, 0.01, 1, 0.35)
pad2.SetGridy()
pad2.Draw()
pad2.cd()
pad2.SetTopMargin(0.)
pad2.SetBottomMargin(0.17)
pad2.SetLeftMargin(0.11)

#define ratio plot                                                                                                                              
rp = TH1F(h_sigmaEOE_pre0.Clone("rp")) #clone the preselection region                                                                                         
rp.SetLineColor(kBlack)
rp.SetMinimum(0.5)
rp.SetMaximum(1.9)
rp.SetStats(0)
rp.Divide(h_sigmaEOE_sba0_reweighted+h_sigmaEOE_mgg0) #divide by sideband+mgg                                                                                                     
rp.SetMarkerStyle(24)
rp.SetTitle("")

rp.SetYTitle("Reweighted SB/Presel")
rp.GetYaxis().SetNdivisions(505)
rp.GetYaxis().SetTitleSize(25)
rp.GetYaxis().SetTitleFont(43)
rp.GetYaxis().SetTitleOffset(2.25)
rp.GetYaxis().SetLabelFont(43)
rp.GetYaxis().SetLabelSize(25)

rp.SetXTitle("Min #gamma ID MVA #sigma_{E}/E")
rp.GetXaxis().SetTitleSize(25)
rp.GetXaxis().SetTitleFont(43)
rp.GetXaxis().SetTitleOffset(3.9)
rp.GetXaxis().SetLabelFont(43)
rp.GetXaxis().SetLabelSize(25)
rp.GetXaxis().SetLabelOffset(0.02)

rp.Draw("ep")

c1.Update()
c1.cd()

#CMS lumi stuff
CMS_lumi.writeExtraText = True
CMS_lumi.extraText      = "Preliminary"
CMS_lumi.lumi_sqrtS     = "1.6 fb^{-1} (13 TeV)"
#CMS_lumi.lumi_sqrtS     = "2.72 fb^{-1} (13 TeV)"
CMS_lumi.cmsTextSize    = 0.6
CMS_lumi.lumiTextSize   = 0.46
CMS_lumi.extraOverCmsTextSize = 0.75
CMS_lumi.relPosX = 0.12
CMS_lumi.CMS_lumi(pad1, 0, 0)

c1.Update()
if (logScale):
    c1.SaveAs(outputdir+"/sigmaEoE_minPhoId_reweighted_log.png")
    c1.SaveAs(outputdir+"/sigmaEoE_minPhoId_reweighted_log.pdf")
else:
    c1.SaveAs(outputdir+"/sigmaEoE_minPhoId_reweighted.pdf")
    c1.SaveAs(outputdir+"/sigmaEoE_minPhoId_reweighted.png")

print("MGG: ", h_sigmaEOE_mgg0.Integral())
print("Reweighted sigmaEOE minPhoId: ", h_sigmaEOE_sba0_reweighted.Integral())
print("Preselection region: ", h_sigmaEOE_pre0.Integral())

