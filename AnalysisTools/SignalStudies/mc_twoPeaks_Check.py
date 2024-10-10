from ROOT import *
import CMS_lumi
import ROOT, array, random, copy
from ROOT import TCanvas, TFile, TH1, TH1F, TF1, gSystem, TChain
import ROOT, array, CMSGraphics, CMS_lumi, random, copy
from ROOT import TFile, TTree, TList
from collections import OrderedDict
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

# -------------------------------------
# Obtain histogram files and get trees
# -------------------------------------
masses = [10, 20, 30, 40, 45, 50, 55, 60, 65, 70]
#masses = [5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70]
list_files = []
list_trees = []
idx = 0

for m in masses: 
    print("/eos/user/e/elfontan/DiPhotonAnalysis/diphotonBDT/NTUPLES_May2024/nearest_flat/out_ggH_M"+str(m)+"_newSamplesFlat.root")
    filename = "/eos/user/e/elfontan/DiPhotonAnalysis/diphotonBDT/NTUPLES_May2024/nearest_flat/out_ggH_M"+str(m)+"_newSamplesFlat.root"
    f = TFile.Open(filename, "READ")
    list_files.append(f)    
    ggh0 = list_files[idx].Get("tagsDumper/trees/ggh_"+str(m)+"_13TeV_UntaggedTag_0")    
    print("TREE_NAME = tagsDumper/trees/ggh_"+str(m)+"_13TeV_UntaggedTag_0")
    #ggh0 = f.Get("tagsDumper/trees/ggh_"+str(m)+"_13TeV_UntaggedTag_0")    
    list_trees.append(ggh0)
    idx += 1
print(list_trees)

# List of variables
# -----------------
var_list = ["dipho_lead_ptoM", "dipho_sublead_ptoM", "dipho_leadEta", "dipho_subleadEta", "cosphi", "dipho_leadIDMVA", "dipho_subleadIDMVA", "sigmaMrvoM", "sigmaMwvoM", "vtxprob", "dipho_lead_sigmaEoE", "dipho_sublead_sigmaEoE", "dipho_pt", "dipho_sumpt", "NNScore"]
#var_list = ["dipho_lead_ptoM", "dipho_sublead_ptoM", "dipho_leadEta", "dipho_subleadEta", "cosphi", "dipho_leadIDMVA", "dipho_subleadIDMVA", "sigmaMrvoM", "sigmaMwvoM", "vtxprob", "dipho_lead_sigmaEoE", "dipho_sublead_sigmaEoE", "dipho_pt", "dipho_sumpt", "dipho_mass"]
label_list = ["Leading photon p_{T}", "Subleading photon p_{T}", "Leading photon #eta", "Sublead photon #eta", "cosphi", "Lead #gamma IDMVA", "Sublead #gamma IDMVA", "#sigma_{RV}/m_{#gamma#gamma}", "#sigma_{WV}/m_{#gamma#gamma}", "Vtx probability", "Leading #gamma #sigma_{E}/E", "Subleading #gamma #sigma_{E}/E", "Diphoton p_{T}", "Diphoton sum p_{T}", "NN Score"]
#"m_{#gamma#gamma}"

# Create a dictionary to store the binning information for each variable
# ----------------------------------------------------------------------
binning_info = { 
    var_list[0]: (100, 0., 4.),   #dipho_lead_ptoM
    var_list[1]: (100, 0., 4.),   #"dipho_sublead_ptoM
    var_list[2]: (60, -3., 3.),   #dipho_leadEta 
    var_list[3]: (60, -3., 3.),   #dipho_subleadEta
    var_list[4]: (60, -1.0, 1.0),  #cosphi
    var_list[5]: (100, -1.,1.),   #dipho_leadIDMVA 
    var_list[6]: (100, -1.,1.),   #dipho_subleadIDMVA
    var_list[7]: (50, 0., 0.05),  #sigmaMrvoM
    var_list[8]: (50, 0., 0.05),  #sigmaMwvoM
    var_list[9]: (50, 0.9, 1.0),  #vtxprob
    var_list[10]: (50, 0., 0.05), #dipho_lead_sigmaEoE
    var_list[11]: (50, 0., 0.05), #dipho_sublead_sigmaEoE
    var_list[12]: (50, 0., 200),  #dipho_pt                                                                            
    var_list[13]: (50, 0., 200),  #dipho_sumpt                                                                                  
    var_list[14]: (50, 0., 1),   #NNScore                                                                                  
    #var_list[12]: (35, 0., 70.), #dipho_mass 
    #var_list[15]: (100, -1, 1)    #diphoMVA
}

listOfHistoLists_high = []
listOfHistoLists_low = []

for m in masses:
    histolistHigh_name = "histo_ggh_M"+str(m)+"_high_list"
    histolistLow_name = "histo_ggh_M"+str(m)+"_low_list"
    histolistHigh_name = OrderedDict()
    histolistLow_name = OrderedDict()
    for variable in var_list:
        nbins, xlow, xhigh = binning_info[variable]
        #print("var_list[i]", variable)
        #print("nbins = ", nbins)
        #print("xlow = ", xlow)
        #print("xhigh = ", xhigh)
        histolistHigh_name[variable + "_ggh_M"+str(m)] = TH1F("h_high_" + variable + "_ggh_M"+str(m), "h_high_" + variable + "_ggh_M"+str(m), nbins, xlow, xhigh)
        histolistLow_name[variable + "_ggh_M"+str(m)] = TH1F("h_low_" + variable + "_ggh_M"+str(m), "h_low_" + variable + "_ggh_M"+str(m), nbins, xlow, xhigh)
    print("----------------------------------------------------")
    print("HISTO LIST NAME (HighPeak) IS -----> histo_ggh_M"+str(m)+"_high_list")
    print(histolistHigh_name)
    print("HISTO LIST NAME (LowPeak) IS -----> histo_ggh_M"+str(m)+"_low_list")
    print(histolistLow_name)
    listOfHistoLists_high.append(histolistHigh_name)
    listOfHistoLists_low.append(histolistLow_name)

print("---------------------------------")
output_file = TFile("histoFile_doublePeakChecks.root", "RECREATE")
output_file.cd()
i = 0
for tree in list_trees:
    massValue = str(masses[i])
    print("TREE = ", tree)
    print("HISTOLIST (HighPeak) = \t", listOfHistoLists_high[i])
    print("HISTOLIST (LowPeak) = \t", listOfHistoLists_low[i])

    for variable in var_list:
        for ev in tree:
            h_ggh_high = listOfHistoLists_high[i][variable + "_ggh_M"+massValue]
            h_ggh_low = listOfHistoLists_low[i][variable + "_ggh_M"+massValue]
            value = getattr(ev, variable)
            if (ev.NNScore > 0.8):
                h_ggh_high.Fill(value, ev.weight)
            elif (ev.NNScore > 0.5 and ev.NNScore < 0.8):
                h_ggh_low.Fill(value, ev.weight)
        h_ggh_high.Write()
        h_ggh_low.Write()
    
    i+=1
output_file.Close()



