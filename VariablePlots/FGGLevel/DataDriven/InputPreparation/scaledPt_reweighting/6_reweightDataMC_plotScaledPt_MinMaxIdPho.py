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
sideband = TFile("/eos/user/e/elfontan/DiPhotonAnalysis/diphotonBDT/NTUPLES_Oct2023/sb_newfile_sigmaEOEreweighting_ALL.root","READ")
mgg = TFile("/eos/user/e/elfontan/DiPhotonAnalysis/diphotonBDT/NTUPLES_Oct2023/bkg_dipho/diPhoton_all.root","READ")

# Reweighting function                                                                                    
# --------------------                                                                                            
def reweighting(inputFile_weights, rootFile_weights, sb_treeName, varX, varY):
    # Open the input file                                                                             
    input_file = TFile(inputFile_weights, "READ")
    if input_file.IsZombie():
        print("Error: Unable to open the input file.")
        return

    # Retrieve the weight histogram                                                                                
    weight_histogram = input_file.Get(rootFile_weights)
    if not weight_histogram or not isinstance(weight_histogram, TH2):
        print("Error: Unable to retrieve the weight histogram.")
        return
    # Get the weight from the histogram                                                                    
    bin_number_x = weight_histogram.GetXaxis().FindBin(varX)
    bin_number_y = weight_histogram.GetYaxis().FindBin(varY)
    w = weight_histogram.GetBinContent(bin_number_x, bin_number_y)

    # Close the input file                                                                        
    input_file.Close()

    return w

def fill_histograms(histogram, value, weight=1):
    n_bins = histogram.GetNbinsX()
    last_bin_content = histogram.GetBinContent(n_bins)
    last_bin_error = histogram.GetBinError(n_bins)

    if value > histogram.GetXaxis().GetXmax():
        histogram.Fill(histogram.GetXaxis().GetXmax(), weight)
        histogram.SetBinError(n_bins, TMath.Sqrt(last_bin_error ** 2 + weight))
    else:
        histogram.Fill(value, weight)

def fill_histograms_2d(histogram, value_x, value_y, weight=1):
    n_bins_x = histogram.GetNbinsX()
    n_bins_y = histogram.GetNbinsY()

    x = min(value_x, histogram.GetXaxis().GetXmax())
    y = min(value_y, histogram.GetYaxis().GetXmax())

    bin_x = histogram.GetXaxis().FindBin(x)
    bin_y = histogram.GetYaxis().FindBin(y)

    if value_x > histogram.GetXaxis().GetXmax():
        bin_x = n_bins_x

    if value_y > histogram.GetYaxis().GetXmax():
        bin_y = n_bins_y

    histogram.Fill(x, y, weight)

# ------------------ #
# PtToM REWEIGHTING  #
# ------------------ #
from array import array
xbins = [0.283]
while (xbins[-1]<7):
    xbins.append(1.09*xbins[-1])
print(xbins)
h_ptToM_min_sba0 = TH1F("h_ptToM_min_sba0", "h_ptToM_min_sba0", len(xbins)-1,array('f',xbins))
h_ptToM_min_pre0 = TH1F("h_ptToM_min_pre0", "h_ptToM_min_pre0", len(xbins)-1,array('f',xbins))
h_ptToM_min_mgg0 = TH1F("h_ptToM_min_mgg0", "h_ptToM_min_mgg0", len(xbins)-1,array('f',xbins))
h_ptToM_max_sba0 = TH1F("h_ptToM_max_sba0", "h_ptToM_max_sba0", len(xbins)-1,array('f',xbins))
h_ptToM_max_pre0 = TH1F("h_ptToM_max_pre0", "h_ptToM_max_pre0", len(xbins)-1,array('f',xbins))
h_ptToM_max_mgg0 = TH1F("h_ptToM_max_mgg0", "h_ptToM_max_mgg0", len(xbins)-1,array('f',xbins))


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
        fill_histograms(h_ptToM_min_pre0, ev_dat0.dipho_lead_ptoM, 1.)
        fill_histograms(h_ptToM_max_pre0, ev_dat0.dipho_sublead_ptoM, 1.)
    elif (ev_dat0.dipho_leadIDMVA > ev_dat0.dipho_subleadIDMVA and min(ev_dat0.dipho_leadIDMVA, ev_dat0.dipho_subleadIDMVA)>-0.7):
        fill_histograms(h_ptToM_min_pre0, ev_dat0.dipho_sublead_ptoM, 1.)
        fill_histograms(h_ptToM_max_pre0, ev_dat0.dipho_lead_ptoM, 1.)
print("h_ptToM_min_pre0 Integral = ", h_ptToM_min_pre0.Integral())
print("h_ptToM_max_pre0 Integral = ", h_ptToM_max_pre0.Integral())

print("----------Opening MC dipho tree")
c_mgg0 = 0
for ev_mgg0 in mgg0:
    c_mgg0 += 1
    #if (c_mgg0 == 10): break
    if (ev_mgg0.dipho_leadIDMVA <= ev_mgg0.dipho_subleadIDMVA and min(ev_mgg0.dipho_leadIDMVA, ev_mgg0.dipho_subleadIDMVA)>-0.7):
        fill_histograms(h_ptToM_min_mgg0, ev_mgg0.dipho_lead_ptoM, ev_mgg0.weight*5.9546)
        fill_histograms(h_ptToM_max_mgg0, ev_mgg0.dipho_sublead_ptoM, ev_mgg0.weight*5.9546)
    elif (ev_mgg0.dipho_leadIDMVA > ev_mgg0.dipho_subleadIDMVA and min(ev_mgg0.dipho_leadIDMVA, ev_mgg0.dipho_subleadIDMVA)>-0.7):
        fill_histograms(h_ptToM_min_mgg0, ev_mgg0.dipho_sublead_ptoM, ev_mgg0.weight*5.9546)
        fill_histograms(h_ptToM_max_mgg0, ev_mgg0.dipho_lead_ptoM, ev_mgg0.weight*5.9546)
print("h_ptToM_min_mgg0 Integral = ", h_ptToM_min_mgg0.Integral())
print("h_ptToM_max_mgg0 Integral = ", h_ptToM_max_mgg0.Integral())


# Create a new file to save the modified tree
# -------------------------------------------
new_file = TFile("/eos/user/e/elfontan/DiPhotonAnalysis/diphotonBDT/NTUPLES_Oct2023/sb_newfile_ptOverMreweighting_overflow_max7_ALL.root", "RECREATE")
tagsDumper = new_file.mkdir("tagsDumper")
tagsDumper.cd()
trees = tagsDumper.mkdir("trees")

# Clone the original tree
# -----------------------
from array import array

weight_ptOverM = array('f',[0.])
new_tree = sb0.CloneTree(0)  # 0 indicates to clone the structure only

# Create a new branch in the new tree
# -----------------------------------
new_tree.Branch("weight_ptOverM", weight_ptOverM, "weight_ptOverM/F")

print("----------Opening sideband tree")
c_sb0 = 0
for ev_sb0 in sb0:
    #if (c_sb0 == 1000): break
    c_sb0 += 1
    print("-------------------------------------------- EVENT ", c_sb0)
    #print ("ORIGINAL SB WEIGHT = ", weight[0])
    #if (not(c_sb0%20==0)): continue
    w_ptOverM = 1.
    if (ev_sb0.dipho_leadIDMVA <= ev_sb0.dipho_subleadIDMVA and min(ev_sb0.dipho_leadIDMVA, ev_sb0.dipho_subleadIDMVA)>-0.7):
        print("w_ptOverM sublead PRE = ", w_ptOverM)
        w_ptOverM = reweighting("f_ptOverM_max7_overflow_reweighting_ALL.root", "h_ratio_ptToM", "sb0", ev_sb0.dipho_lead_ptoM, ev_sb0.dipho_sublead_ptoM)
        fill_histograms(h_ptToM_min_sba0, ev_sb0.dipho_lead_ptoM, ev_sb0.weight*0.0622*ev_sb0.weight_sigmaEOE*w_ptOverM)
        fill_histograms(h_ptToM_max_sba0, ev_sb0.dipho_sublead_ptoM, ev_sb0.weight*0.0622*ev_sb0.weight_sigmaEOE*w_ptOverM)
        weight_ptOverM[0] = 1.*w_ptOverM
        print("w_ptOverM sublead POST = ", w_ptOverM)

    elif (ev_sb0.dipho_leadIDMVA > ev_sb0.dipho_subleadIDMVA and min(ev_sb0.dipho_leadIDMVA, ev_sb0.dipho_subleadIDMVA)>-0.7):
        print("w_ptOverM sublead PRE = ", w_ptOverM)
        w_ptOverM = reweighting("f_ptOverM_max7_overflow_reweighting_ALL.root", "h_ratio_ptToM", "sb0", ev_sb0.dipho_sublead_ptoM, ev_sb0.dipho_lead_ptoM)
        fill_histograms(h_ptToM_min_sba0, ev_sb0.dipho_sublead_ptoM, ev_sb0.weight*0.0622*ev_sb0.weight_sigmaEOE*w_ptOverM)
        fill_histograms(h_ptToM_max_sba0, ev_sb0.dipho_lead_ptoM, ev_sb0.weight*0.0622*ev_sb0.weight_sigmaEOE*w_ptOverM)
        weight_ptOverM[0] = 1.*w_ptOverM
        print("w_ptOverM sublead POST = ", w_ptOverM)

    new_tree.Fill()

print("h_ptToM_min_sba0 Integral = ", h_ptToM_min_sba0.Integral())
print("h_ptToM_max_sba0 Integral = ", h_ptToM_max_sba0.Integral())

# Save the new tree to the new file
# ---------------------------------
trees.cd()  # Change to the correct directory
new_tree.Write()

# Close the files
# ---------------
new_file.Close()


bkg0_min = THStack("bkg0_min","bkg0_min")
bkg0_max = THStack("bkg0_max","bkg0_max")
# Set Maximum
if (logScale):
    bkg0_min.SetMaximum(450000)
    bkg0_max.SetMaximum(450000)
else:
    bkg0_min.SetMaximum(45000)
    bkg0_max.SetMaximum(45000)
    
#Now we draw it out                                                                                                                          
gStyle.SetOptStat(0)
gStyle.SetOptTitle(0)


####################################
# Pt Over M for minimum pho ID MVA #
####################################
c1_min = TCanvas("c1_min","c1_min",1200,1200)
c1_min.cd()
#c1_min.SetLeftMargin(0.
#upper plot pad - Data histos                                                                                                       
pad1 = TPad("pad1","pad1", 0, 0.36, 1, 1.0)
pad1.Draw()
pad1.cd()
if (logScale):
    pad1.SetLogy()                                                                                                                    
pad1.SetBottomMargin(0.01)
pad1.SetLeftMargin(1.9)

h_ptToM_min_sba0.SetLineColor(kYellow-7)
h_ptToM_min_sba0.SetFillColorAlpha(kYellow-7,0.8)
h_ptToM_min_sba0.SetLineWidth(2)

h_ptToM_min_sba0.GetYaxis().SetTitle("Events/0.5 GeV")
h_ptToM_min_sba0.GetYaxis().SetTitleSize(25)
h_ptToM_min_sba0.GetYaxis().SetTitleFont(43)
h_ptToM_min_sba0.GetYaxis().SetTitleOffset(2.25)
h_ptToM_min_sba0.GetYaxis().SetLabelFont(43)
h_ptToM_min_sba0.GetYaxis().SetLabelOffset(0.01)
h_ptToM_min_sba0.GetYaxis().SetLabelSize(25)

h_ptToM_min_mgg0.SetLineColor(kOrange-4)
h_ptToM_min_mgg0.SetFillColorAlpha(kOrange-4,0.8)
h_ptToM_min_mgg0.SetLineWidth(2)

bkg0_min.Add(h_ptToM_min_mgg0)
bkg0_min.Add(h_ptToM_min_sba0)
h_ptToM_min_sba0.GetXaxis().SetLabelOffset(1.5)
h_ptToM_min_mgg0.GetXaxis().SetLabelOffset(1.5)
h_ptToM_min_sba0.GetXaxis().SetLabelSize(0)
h_ptToM_min_mgg0.GetXaxis().SetLabelSize(0)
bkg0_min.Draw("histo")

h_ptToM_min_pre0.SetLineWidth(2)
h_ptToM_min_pre0.SetLineColorAlpha(kBlack,0.8)
#h_ptToM_min_pre0.SetLineColorAlpha(kOrange+9,0.8)
h_ptToM_min_pre0.GetXaxis().SetLabelSize(0)
h_ptToM_min_pre0.Draw("epsame")

leg = TLegend(0.2,0.5,0.7,0.88)
leg.AddEntry(h_ptToM_min_sba0,"#gamma-jet and jet-jet (Reweighted Sideband)")
leg.AddEntry(h_ptToM_min_mgg0,"Diphoton MC")
leg.AddEntry(h_ptToM_min_pre0,"Preselection Region")
leg.SetLineWidth(0)
leg.Draw("same")

c1_min.Update()
c1_min.cd()

#lower plot pad - Ratio plot
pad2 = TPad("pad2","pad2", 0, 0.01, 1, 0.35)
pad2.SetGridy()
pad2.Draw()
pad2.cd()
pad2.SetTopMargin(0.)
pad2.SetBottomMargin(0.17)
pad2.SetLeftMargin(0.11)

#define ratio plot                                                                                                                              
rp = TH1F(h_ptToM_min_pre0.Clone("rp")) #clone the preselection region                                                                                         
rp.SetLineColor(kBlack)
rp.SetMinimum(-0.1)
rp.SetMaximum(2.1)
rp.SetStats(0)
rp.Divide(h_ptToM_min_sba0+h_ptToM_min_mgg0) #divide by sideband+mgg                                                                                                     
rp.SetMarkerStyle(24)
rp.SetTitle("")

rp.SetYTitle("Presel/(Reweighted SB + #gamma#gamma)")
rp.GetYaxis().SetNdivisions(505)
rp.GetYaxis().SetTitleSize(25)
rp.GetYaxis().SetTitleFont(43)
rp.GetYaxis().SetTitleOffset(2.25)
rp.GetYaxis().SetLabelFont(43)
rp.GetYaxis().SetLabelSize(25)

rp.SetXTitle("Min #gamma ID MVA p_{T}/M")
rp.GetXaxis().SetTitleSize(25)
rp.GetXaxis().SetTitleFont(43)
rp.GetXaxis().SetTitleOffset(3.9)
rp.GetXaxis().SetLabelFont(43)
rp.GetXaxis().SetLabelSize(25)
rp.GetXaxis().SetLabelOffset(0.02)

rp.Draw("ep")

c1_min.Update()
c1_min.cd()

#CMS lumi stuff
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

c1_min.Update()
if (logScale):
    c1_min.SaveAs(outputdir+"/ptOverM_reweighted_minPhoId_overflow_max7_log.png")
    c1_min.SaveAs(outputdir+"/ptOverM_reweighted_minPhoId_overflow_max7_log.pdf")
else:
    c1_min.SaveAs(outputdir+"/ptOverM_reweighted_minPhoId.png")
    c1_min.SaveAs(outputdir+"/ptOverM_reweighted_minPhoId.pdf")



####################################
# Pt Over M for maximum pho ID MVA #
####################################
c1_max = TCanvas("c1_max","c1_max",1200,1200)
c1_max.cd()
#c1_max.SetLeftMargin(0.
#upper plot pad - Data histos                                                                                                       
pad1 = TPad("pad1","pad1", 0, 0.36, 1, 1.0)
pad1.Draw()
pad1.cd()
if (logScale):
    pad1.SetLogy()                                                                                                                    
pad1.SetBottomMargin(0.01)
pad1.SetLeftMargin(1.9)

h_ptToM_max_sba0.SetLineColor(kYellow-7)
h_ptToM_max_sba0.SetFillColorAlpha(kYellow-7,0.8)
h_ptToM_max_sba0.SetLineWidth(2)

h_ptToM_max_sba0.GetYaxis().SetTitle("Events/0.5 GeV")
h_ptToM_max_sba0.GetYaxis().SetTitleSize(25)
h_ptToM_max_sba0.GetYaxis().SetTitleFont(43)
h_ptToM_max_sba0.GetYaxis().SetTitleOffset(2.25)
h_ptToM_max_sba0.GetYaxis().SetLabelFont(43)
h_ptToM_max_sba0.GetYaxis().SetLabelOffset(0.01)
h_ptToM_max_sba0.GetYaxis().SetLabelSize(25)

h_ptToM_max_mgg0.SetLineColor(kOrange-4)
h_ptToM_max_mgg0.SetFillColorAlpha(kOrange-4,0.8)
h_ptToM_max_mgg0.SetLineWidth(2)

bkg0_max.Add(h_ptToM_max_mgg0)
bkg0_max.Add(h_ptToM_max_sba0)
h_ptToM_max_sba0.GetXaxis().SetLabelOffset(1.5)
h_ptToM_max_mgg0.GetXaxis().SetLabelOffset(1.5)
h_ptToM_max_sba0.GetXaxis().SetLabelSize(0)
h_ptToM_max_mgg0.GetXaxis().SetLabelSize(0)
bkg0_max.Draw("histo")

h_ptToM_max_pre0.SetLineWidth(2)
h_ptToM_max_pre0.SetLineColorAlpha(kBlack,0.8)
#h_ptToM_max_pre0.SetLineColorAlpha(kOrange+9,0.8)
h_ptToM_max_pre0.GetXaxis().SetLabelSize(0)
h_ptToM_max_pre0.Draw("epsame")

leg = TLegend(0.2,0.5,0.7,0.88)
leg.AddEntry(h_ptToM_max_sba0,"#gamma-jet and jet-jet (Reweighted Sideband)")
leg.AddEntry(h_ptToM_max_mgg0,"Diphoton MC")
leg.AddEntry(h_ptToM_max_pre0,"Preselection Region")
leg.SetLineWidth(0)
leg.Draw("same")

c1_max.Update()
c1_max.cd()

#lower plot pad - Ratio plot
pad2 = TPad("pad2","pad2", 0, 0.01, 1, 0.35)
pad2.SetGridy()
pad2.Draw()
pad2.cd()
pad2.SetTopMargin(0.)
pad2.SetBottomMargin(0.17)
pad2.SetLeftMargin(0.11)

#define ratio plot                                                                                                                              
rp = TH1F(h_ptToM_max_pre0.Clone("rp")) #clone the preselection region                                                                                         
rp.SetLineColor(kBlack)
rp.SetMinimum(-0.1)
rp.SetMaximum(2.1)
rp.SetStats(0)
rp.Divide(h_ptToM_max_sba0+h_ptToM_max_mgg0) #divide by sideband+mgg                                                                                                     
rp.SetMarkerStyle(24)
rp.SetTitle("")

rp.SetYTitle("Presel/(Reweighted SB + #gamma#gamma)")
rp.GetYaxis().SetNdivisions(505)
rp.GetYaxis().SetTitleSize(25)
rp.GetYaxis().SetTitleFont(43)
rp.GetYaxis().SetTitleOffset(2.25)
rp.GetYaxis().SetLabelFont(43)
rp.GetYaxis().SetLabelSize(25)

rp.SetXTitle("Max #gamma ID MVA p_{T}/M")
rp.GetXaxis().SetTitleSize(25)
rp.GetXaxis().SetTitleFont(43)
rp.GetXaxis().SetTitleOffset(3.9)
rp.GetXaxis().SetLabelFont(43)
rp.GetXaxis().SetLabelSize(25)
rp.GetXaxis().SetLabelOffset(0.02)

rp.Draw("ep")

c1_max.Update()
c1_max.cd()

#CMS lumi stuff
CMS_lumi.CMS_lumi(pad1, 0, 0)

c1_max.Update()
if (logScale):
    c1_max.SaveAs(outputdir+"/ptOverM_reweighted_maxPhoId_overflow_max7_log.png")
    c1_max.SaveAs(outputdir+"/ptOverM_reweighted_maxPhoId_overflow_max7_log.pdf")
else:
    c1_max.SaveAs(outputdir+"/ptOverM_reweighted_maxPhoId.png")
    c1_max.SaveAs(outputdir+"/ptOverM_reweighted_maxPhoId.pdf")
