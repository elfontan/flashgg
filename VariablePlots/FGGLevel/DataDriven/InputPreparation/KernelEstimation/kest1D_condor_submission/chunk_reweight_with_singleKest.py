#!/usr/bin/env python3                                                     

import sys
import os
from ROOT import *
import ROOT, random, copy
from ROOT import TFile, TTree, TList
from array import array

def main(process_number):
    gROOT.SetBatch(True)  # Run ROOT in batch mode    # Set the input file and chunk number                                                                                                                       
    # Set the input file for each chunk
    input_file = "/eos/user/e/elfontan/DiPhotonAnalysis/diphotonBDT/NTUPLES_Oct2023/data/EGamma_2018Data.root"
    
    # Set the output file for each chunk
    output_file = f"/afs/cern.ch/work/e/elfontan/private/DiPhotonAnalysis/Sep2023_flashGG/newFlashggRepo/CMSSW_10_6_8/src/flashgg/VariablePlots/FGGLevel/DataDriven/InputPreparation/KernelEstimation/kest1D_condor_submission/OUTPUT_FILES/test_chunk{process_number}.root"
    
    # Open the input file
    oldfile = TFile.Open(input_file, "read")

    if not oldfile or oldfile.IsZombie():
        print(f"Error: Unable to open the input file for chunk {process_number}.")
        return
    
    oldtree = oldfile.Get("tagsDumper/trees/Data_13TeV_UntaggedTag_0")
    nentries = oldtree.GetEntries()

    # Calculate the range of entries to process for this chunk
    chunk_size = 10000
    start_entry = (process_number - 1) * chunk_size
    end_entry = min(process_number * chunk_size, nentries)
    
    dipho_leadIDMVA = array('f',[0.])
    dipho_subleadIDMVA = array('f',[0.])
    weight = array('f',[0.])
    event = array('I',[0])
    oldtree.SetBranchAddress("dipho_leadIDMVA",dipho_leadIDMVA)
    oldtree.SetBranchAddress("dipho_subleadIDMVA",dipho_subleadIDMVA)
    oldtree.SetBranchAddress("weight",weight)
    oldtree.SetBranchAddress("event",event)
    
    nEvents_SB = 0
    nEvents_presel = 0
    
    # Open the file containing the workspace
    # --------------------------------------
    ws = TFile.Open("/afs/cern.ch/work/e/elfontan/private/DiPhotonAnalysis/Sep2023_flashGG/newFlashggRepo/CMSSW_10_6_8/src/flashgg/VariablePlots/FGGLevel/DataDriven/InputPreparation/KernelEstimation/w_newSandS_gjAll_Inclusive.root")    

    # Load the workspace from the file
    # --------------------------------
    w = ws.Get("w_MinMaxPhoId")
    
    if not w:
        print("Error: Could not load the workspace from the file.")
        exit(1)
        
    # Retrieve the observable variable(s) and PDFs from the workspace
    # ---------------------------------------------------------------
    dipho_minIDMVA = w.var("dipho_minIDMVA")
    dipho_maxIDMVA = w.var("dipho_maxIDMVA")
    kest0 = w.pdf("kestML1p2_minPhoId_0")

    # -----------------------------                                                             
    # Using the inclusive fake pdf                                                   
    # -----------------------------                                                              
    list_maxphoid_names = ["Inclusive"]
    list_maxphoid_min = [-0.7]
    list_maxphoid_max = [1.0]
    
    h_dipho_minIDMVA_0 = w.data("h_dipho_minIDMVA_0").createHistogram("dipho_minIDMVA")
    print("Integral = ", h_dipho_minIDMVA_0.Integral())
        
    # Create a new output file and a new tree as a clone of oldtree
    # -------------------------------------------------------------
    newfile = TFile(output_file, "recreate")
    tagsDumper = newfile.mkdir("tagsDumper")
    tagsDumper.cd()
    trees = tagsDumper.mkdir("trees")
    trees.cd()    
    newtree = oldtree.CloneTree(0)

    # Loop over the selected range of entries and process them
    # --------------------------------------------------------
    processedEv = end_entry - start_entry
    for ev in range(start_entry, end_entry):
        if (ev%1000==0): print(ev,processedEv)
        oldtree.GetEntry(ev)
                
        #print("Original minID is = \t", min(dipho_leadIDMVA[0],dipho_subleadIDMVA[0]))
        #print("Original maxID is = \t", max(dipho_leadIDMVA[0],dipho_subleadIDMVA[0]))
        
        #if event is in sideband and also blinded
        if (min(dipho_leadIDMVA[0],dipho_subleadIDMVA[0])<-0.7 and max(dipho_leadIDMVA[0],dipho_subleadIDMVA[0])>=-0.7): 
            nEvents_SB+=1
        
            # Use the pdf to generate a new minimum ID
            # ----------------------------------------
            dipho_minIDMVA.setConstant(False)
            dipho_minIDMVA.setRange(-0.7,max(dipho_leadIDMVA[0],dipho_subleadIDMVA[0]))
            
            min_fakePdf = kest0.generate(RooArgSet(dipho_minIDMVA), 1)
            min_ID = min_fakePdf.get(0).getRealValue("dipho_minIDMVA")
            h_dipho_minIDMVA_0.GetXaxis().SetRangeUser(-0.7, max(dipho_leadIDMVA[0],dipho_subleadIDMVA[0]))
            num = h_dipho_minIDMVA_0.Integral()
            h_dipho_minIDMVA_0.GetXaxis().SetRangeUser(-0.9, -0.7)
            den = h_dipho_minIDMVA_0.Integral()
            reweight = num/den
            print("==========================")
            print("num", num, "  and den", den)
            print("reweight", reweight)
                
            #print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> Event in sideband = ", ev)
            #print("Original minID SB is = \t", min(dipho_leadIDMVA[0],dipho_subleadIDMVA[0]))
            #print("Original maxID SB is = \t", max(dipho_leadIDMVA[0],dipho_subleadIDMVA[0]))
            #print("New minID is = \t", min_ID)
            #print("### REWEIGHTING ###")
            #print("reweight TOT = ", reweight)
            #print("###################")
        
            print("INITIAL WEIGHT = ", weight[0])
            weight[0] = weight[0] * reweight
            print("FINAL WEIGHT = ", weight[0])
            print("==========================")
            #print "dipho_leadIDMVA[0] = ", dipho_leadIDMVA[0]
            #print "dipho_subleadIDMVA[0] = ", dipho_subleadIDMVA[0]
            
            if (dipho_leadIDMVA[0] < dipho_subleadIDMVA[0]):         
                dipho_leadIDMVA[0] = min_ID
            else:
                dipho_subleadIDMVA[0] = min_ID
                
            newtree.Fill()
    newtree.Write()

    # Close the files when done
    # -------------------------
    newfile.Close()
    oldfile.Close()
    ws.Close()
    del oldfile
    del newfile
    del ws
    
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python chunk_reweight_with_kest.py <process_number>")
    else:
        process_number = int(sys.argv[1])
        main(process_number)
