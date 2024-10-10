#########################################################                                                                           
# Very low mass diphoton analysis: Signal MC variables  #                                                                                                           
# ----------------------------------------------------- #                                        
# python3 mc_allSamples_bdtVars.py

import CMS_lumi, CMSGraphics                        
import ROOT, array, random, copy                                                                                                                               
from ROOT import TCanvas, TFile, TH1, TH1F, TF1, gSystem, TTree, TList                                                                              
from ROOT import RooCmdArg, RooArgSet, kFALSE, RooLinkedList, kBlue, kRed, kBlack, kOpenStar, kWhite, kGray                                                      
from ROOT import gStyle, TStyle, TGraph, TGraphErrors, TMath, TMultiGraph, TLine, gPad, TGaxis, TLegend, TText, TLatex, TColor, TPaveText                  
from ROOT import TAttFill, TLegend, TRatioPlot, TPad, THStack                                                                                                 
from ROOT import kBlue, kRed, kBlack, kWhite, kAzure, kOrange, kPink, kGreen, kYellow, kCyan                                                            
from array import array                                                                                                                              
from collections import OrderedDict                                                          
import argparse                                                                                                                     
import sys                                                                                                                        
import os                                                                                
import math                                                       

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
#masses = [30, 40]
#masses = [10, 20, 30, 40, 50, 60, 70]
masses = [10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70]
list_files = []
list_trees = []
idx = 0

for m in masses: 
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
var_list = ["dipho_lead_ptoM", "dipho_sublead_ptoM", "dipho_leadEta", "dipho_subleadEta", "cosphi", "dipho_leadIDMVA", "dipho_subleadIDMVA", "sigmaMrvoM", "sigmaMwvoM", "vtxprob", "dipho_lead_sigmaEoE", "dipho_sublead_sigmaEoE", "dipho_pt", "dipho_sumpt", "NNScore", "leadPt", "subleadPt",]
#var_list = ["dipho_lead_ptoM", "dipho_sublead_ptoM", "dipho_leadEta", "dipho_subleadEta", "cosphi", "dipho_leadIDMVA", "dipho_subleadIDMVA", "sigmaMrvoM", "sigmaMwvoM", "vtxprob", "dipho_lead_sigmaEoE", "dipho_sublead_sigmaEoE", "dipho_pt", "dipho_sumpt", "dipho_mass"]
label_list = ["Leading photon p_{T}/m_{#gamma#gamma}", "Subleading photon p_{T}/m_{#gamma#gamma}", "Leading photon #eta", "Sublead photon #eta", "cosphi", "Lead #gamma IDMVA", "Sublead #gamma IDMVA", "#sigma_{RV}/m_{#gamma#gamma}", "#sigma_{WV}/m_{#gamma#gamma}", "Vtx probability", "Leading #gamma #sigma_{E}/E", "Subleading #gamma #sigma_{E}/E", "Diphoton p_{T}", "Diphoton sum p_{T}", "NN Score", "Leading photon p_{T}", "Subleading photon p_{T}"]
#"m_{#gamma#gamma}"

# Create a dictionary to store the binning information for each variable
# ----------------------------------------------------------------------
binning_info = { 
    var_list[0]: (800, 0., 4.),   #dipho_lead_ptoM
    var_list[1]: (800, 0., 4.),   #"dipho_sublead_ptoM
    #var_list[0]: (150, 0., 1.5),   #dipho_lead_ptoM
    #var_list[1]: (150, 0., 1.5),   #"dipho_sublead_ptoM
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
    var_list[14]: (100, 0., 1),   #NNScore                                                                                  
    var_list[15]: (400, 0., 200), #leadPt
    var_list[16]: (400, 0., 200)  #subleadPt                                                                                  
    #var_list[12]: (35, 0., 70.), #dipho_mass 
    #var_list[15]: (100, -1, 1)    #diphoMVA
}

listOfHistoLists = []
for m in masses:
    histolist_name = "histo_ggh_M"+str(m)+"_list"
    histolist_name = OrderedDict()
    for variable in var_list:
        nbins, xlow, xhigh = binning_info[variable]
        #print("var_list[i]", variable)
        #print("nbins = ", nbins)
        #print("xlow = ", xlow)
        #print("xhigh = ", xhigh)
        histolist_name[variable + "_ggh_M"+str(m)] = TH1F("h_" + variable + "_ggh_M"+str(m), "h_" + variable + "_ggh_M"+str(m), nbins, xlow, xhigh)
    print("----------------------------------------------------")
    print("HISTO LIST NAME IS -----> histo_ggh_M"+str(m)+"_list")
    print(histolist_name)
    listOfHistoLists.append(histolist_name)

print("---------------------------------")
output_file = TFile("histoFile_allMasses_v4.root", "RECREATE")
output_file.cd()
i = 0
for tree in list_trees:
    massValue = str(masses[i])
    print("TREE = ", tree)
    print("HISTOLIST = \t", listOfHistoLists[i])
    for variable in var_list:
        #print("VAR = ", variable)
        for ev in tree:
            h_ggh = listOfHistoLists[i][variable + "_ggh_M"+massValue]
            value = getattr(ev, variable)
            #print(value)
            h_ggh.Fill(value, ev.weight)
            #h_ggh.Fill(value, abs(ev.weight))
        h_ggh.Write()
    
    i+=1
output_file.Close()



