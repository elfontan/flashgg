from ROOT import *
import CMS_lumi
import ROOT, array, random, copy
from ROOT import TCanvas, TFile, TH1, TH1F, TF1, gSystem, TChain
import CMSGraphics, CMS_lumi, random, copy
from ROOT import TFile, TTree, TList
import argparse
import sys
import os

ROOT.gROOT.SetBatch()
ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetOptTitle(0)
ROOT.gStyle.SetOptStat(0)

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

# xObtain histogram files
# ----------------------
data = TFile("/eos/user/e/elfontan/DiPhotonAnalysis/diphotonBDT/NTUPLES_Oct2023/data/EGamma_D.root","READ") #Data with unweighted events, both regions
mgg = TFile("/eos/user/e/elfontan/DiPhotonAnalysis/diphotonBDT/NTUPLES_Oct2023/bkg_dipho/diPhoton_all.root","READ")
# ---- Using the new sideband file including the additional sigmaEOE weight
sideband = TFile("/eos/user/e/elfontan/DiPhotonAnalysis/diphotonBDT/NTUPLES_Oct2023/sb_newfile_sigmaEOEreweighting_ALL.root","READ")
#sideband = TFile("/eos/user/e/elfontan/DiPhotonAnalysis/diphotonBDT/reweighting/kest/output_sideband_PF_kest1D_Inclusive.root","READ")

# Get trees and create histograms for data
# ----------------------------------------
dat0 = data.Get("tagsDumper/trees/Data_13TeV_UntaggedTag_0")
sb0 = sideband.Get("tagsDumper/trees/Data_13TeV_UntaggedTag_0")
mgg0 = mgg.Get("tagsDumper/trees/mgg_bkg_13TeV_UntaggedTag_0")

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
    if not weight_histogram or not isinstance(weight_histogram, TH1):
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
# REWEIGHTING: PtToM #
# ------------------ #
#from array import array
#xbins = [0.275]
#while (xbins[-1]<7):
#    xbins.append(1.08*xbins[-1])
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
h_ptToM_sba0 = TH2F("h_ptToM_sba0", "h_ptToM_sba0", len(xbins)-1,array('f',xbins), len(xbins)-1,array('f',xbins))
h_ptToM_pre0 = TH2F("h_ptToM_pre0", "h_ptToM_pre0", len(xbins)-1,array('f',xbins), len(xbins)-1,array('f',xbins))
h_ptToM_mgg0 = TH2F("h_ptToM_mgg0", "h_ptToM_mgg0", len(xbins)-1,array('f',xbins), len(xbins)-1,array('f',xbins))
#h_ptToM_sba0 = TH2F("h_ptToM_sba0", "h_ptToM_sba0", 80, 0., 4.,  80, 0., 4.)
#h_ptToM_pre0 = TH2F("h_ptToM_pre0", "h_ptToM_pre0", 80, 0., 4.,  80, 0., 4.)
#h_ptToM_mgg0 = TH2F("h_ptToM_mgg0", "h_ptToM_mgg0", 80, 0., 4.,  80, 0., 4.)


print("----------Opening data tree")
c_dat0 = 0
for ev_dat0 in dat0:
    c_dat0 += 1
    if (not(c_dat0%20==0)): continue
    if (ev_dat0.dipho_leadIDMVA <= ev_dat0.dipho_subleadIDMVA and min(ev_dat0.dipho_leadIDMVA, ev_dat0.dipho_subleadIDMVA)>-0.7):
        fill_histograms(h_ptToM_min_pre0, ev_dat0.dipho_lead_ptoM, 1.)
        fill_histograms(h_ptToM_max_pre0, ev_dat0.dipho_sublead_ptoM, 1.)
        fill_histograms_2d(h_ptToM_pre0, ev_dat0.dipho_lead_ptoM, ev_dat0.dipho_sublead_ptoM, 1.)
    elif (ev_dat0.dipho_leadIDMVA > ev_dat0.dipho_subleadIDMVA and min(ev_dat0.dipho_leadIDMVA, ev_dat0.dipho_subleadIDMVA)>-0.7):
        fill_histograms(h_ptToM_min_pre0, ev_dat0.dipho_sublead_ptoM, 1.)
        fill_histograms(h_ptToM_max_pre0, ev_dat0.dipho_lead_ptoM, 1.)
        fill_histograms_2d(h_ptToM_pre0, ev_dat0.dipho_sublead_ptoM, ev_dat0.dipho_lead_ptoM, 1.)
print("h_ptToM_pre0 Integral = ", h_ptToM_pre0.Integral())

print("----------Opening sideband tree")
c_sb0 = 0
for ev_sb0 in sb0:
    c_sb0 += 1
    #if (not(c_sb0%20==0)): continue
    print("ev_sb0.weight_sigmaEOE = ", ev_sb0.weight_sigmaEOE )
    if (ev_sb0.dipho_leadIDMVA <= ev_sb0.dipho_subleadIDMVA and min(ev_sb0.dipho_leadIDMVA, ev_sb0.dipho_subleadIDMVA)>-0.7):
        fill_histograms(h_ptToM_min_sba0, ev_sb0.dipho_lead_ptoM, ev_sb0.weight*0.0622*ev_sb0.weight_sigmaEOE)
        fill_histograms(h_ptToM_max_sba0, ev_sb0.dipho_sublead_ptoM, ev_sb0.weight*0.0622*ev_sb0.weight_sigmaEOE)
        fill_histograms_2d(h_ptToM_sba0, ev_sb0.dipho_lead_ptoM, ev_sb0.dipho_sublead_ptoM, ev_sb0.weight*0.0622*ev_sb0.weight_sigmaEOE)
    elif (ev_sb0.dipho_leadIDMVA > ev_sb0.dipho_subleadIDMVA and min(ev_sb0.dipho_leadIDMVA, ev_sb0.dipho_subleadIDMVA)>-0.7):
        fill_histograms(h_ptToM_min_sba0, ev_sb0.dipho_sublead_ptoM, ev_sb0.weight*0.0622*ev_sb0.weight_sigmaEOE)
        fill_histograms(h_ptToM_max_sba0, ev_sb0.dipho_lead_ptoM, ev_sb0.weight*0.0622*ev_sb0.weight_sigmaEOE)
        fill_histograms_2d(h_ptToM_sba0, ev_sb0.dipho_sublead_ptoM, ev_sb0.dipho_lead_ptoM, ev_sb0.weight*0.0622*ev_sb0.weight_sigmaEOE)
print("h_ptToM_sba0 Integral = ", h_ptToM_sba0.Integral())

print("----------Opening MC dipho tree")
for ev_mgg0 in mgg0:
    if (ev_mgg0.dipho_leadIDMVA <= ev_mgg0.dipho_subleadIDMVA and min(ev_mgg0.dipho_leadIDMVA, ev_mgg0.dipho_subleadIDMVA)>-0.7):
        fill_histograms(h_ptToM_min_mgg0, ev_mgg0.dipho_lead_ptoM, ev_mgg0.weight*5.9546)
        fill_histograms(h_ptToM_max_mgg0, ev_mgg0.dipho_sublead_ptoM, ev_mgg0.weight*5.9546)
        fill_histograms_2d(h_ptToM_mgg0, ev_mgg0.dipho_lead_ptoM, ev_mgg0.dipho_sublead_ptoM, ev_mgg0.weight*5.9546)
    elif (ev_mgg0.dipho_leadIDMVA > ev_mgg0.dipho_subleadIDMVA and min(ev_mgg0.dipho_leadIDMVA, ev_mgg0.dipho_subleadIDMVA)>-0.7):
        fill_histograms(h_ptToM_min_mgg0, ev_mgg0.dipho_sublead_ptoM, ev_mgg0.weight*5.9546)
        fill_histograms(h_ptToM_max_mgg0, ev_mgg0.dipho_lead_ptoM, ev_mgg0.weight*5.9546)
        fill_histograms_2d(h_ptToM_mgg0, ev_mgg0.dipho_sublead_ptoM, ev_mgg0.dipho_lead_ptoM, ev_mgg0.weight*5.9546)
print("h_ptToM_mgg0 Integral = ", h_ptToM_mgg0.Integral())

# Subtract MGG from Data Preselection
h_ptToM_dataPreselMinus_mcDipho = h_ptToM_pre0.Clone("h_ptToM_dataPreselMinus_mcDipho")
print("Pre h_ptToM_dataPreselMinus_mcDipho Integral = ", h_ptToM_dataPreselMinus_mcDipho.Integral())
h_ptToM_dataPreselMinus_mcDipho.Add(h_ptToM_mgg0, -1)
print("Post h_ptToM_dataPreselMinus_mcDipho Integral = ", h_ptToM_dataPreselMinus_mcDipho.Integral())

# Divide the result by  to compute the ratio
h_ratio_ptToM = h_ptToM_dataPreselMinus_mcDipho.Clone("h_ratio_ptToM")
print("Pre h_ratio_ptToM Integral = ", h_ratio_ptToM.Integral())
h_ratio_ptToM.Divide(h_ptToM_sba0)
print("Post h_ratio_ptToM Integral = ", h_ratio_ptToM.Integral())

c_w2 = TCanvas("c_w2","c_w2",1200,800)
c_w2.cd()
c_w2.SetLeftMargin(0.12)                     
c_w2.SetRightMargin(0.15)                     
h_ratio_ptToM.Draw("COLZ")                                       
h_ratio_ptToM.GetXaxis().SetTitle("Min ID MVA #gamma p_{T}/M")
h_ratio_ptToM.GetYaxis().SetTitle("Max ID MVA #gamma p_{T}/M")
h_ratio_ptToM.GetZaxis().SetTitle("(Data presel - MC #gamma#gamma) / SB")
#CMS lumi stuff                                                                                                      
CMS_lumi.writeExtraText = True
CMS_lumi.extraText      = "Preliminary"
CMS_lumi.lumi_sqrtS     = "1.6 fb^{-1} (13 TeV)"
#CMS_lumi.lumi_sqrtS     = "2.72 fb^{-1} (13 TeV)"                                                                                           
CMS_lumi.cmsTextSize    = 0.6
CMS_lumi.lumiTextSize   = 0.46
CMS_lumi.extraOverCmsTextSize = 0.75
CMS_lumi.relPosX = 0.12
CMS_lumi.CMS_lumi(c_w2, 0, 0)

c_w2.Update()
#c_w2.SaveAs(outputdir+"/reweighting_pt.png")
#c_w2.SaveAs(outputdir+"/reweighting_pt.pdf")
c_w2.SaveAs(outputdir+"/reweighting_scaledPt_max7_variableBinning_overflow.png")
c_w2.SaveAs(outputdir+"/reweighting_scaledPt_max7_variableBinning_overflow.pdf")


# Save the canvas with the ratio histogram to a ROOT file
outfile = TFile("f_ptOverM_max7_overflow_reweighting_ALL.root", "RECREATE")
h_ratio_ptToM.Write()

# Close the output file
outfile.Close()


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

leg = TLegend(0.23,0.5,0.73,0.88)
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
CMS_lumi.CMS_lumi(pad1, 0, 0)

c1_min.Update()
if (logScale):
    c1_min.SaveAs(outputdir+"/ptOverM_minPhoId_max7_overflow_log.png")
    c1_min.SaveAs(outputdir+"/ptOverM_minPhoId_max7_overflow_log.pdf")
else:
    c1_min.SaveAs(outputdir+"/ptOverM_minPhoId.png")
    c1_min.SaveAs(outputdir+"/ptOverM_minPhoId.pdf")



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

leg = TLegend(0.23,0.5,0.73,0.88)
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
    c1_max.SaveAs(outputdir+"/ptOverM_maxPhoId_max7_overflow_log.png")
    c1_max.SaveAs(outputdir+"/ptOverM_maxPhoId_max7_overflow_log.pdf")
else:
    c1_max.SaveAs(outputdir+"/ptOverM_maxPhoId.png")
    c1_max.SaveAs(outputdir+"/ptOverM_maxPhoId.pdf")


