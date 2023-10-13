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
    input_file = "/eos/user/e/elfontan/DiPhotonAnalysis/diphotonBDT/NEW_BDT_TRAININGS/DefLM_MCBased/2018Data/2018EGamma.root"
    
    # Set the output file for each chunk
    output_file = f"/afs/cern.ch/work/e/elfontan/private/DiPhotonAnalysis/Sep2023_flashGG/CMSSW_12_6_5/src/condor_submission/FILES_OUTPUT/output_sideband_kest2D_chunk{process_number}.root"
    
    # Open the input file
    oldfile = TFile.Open(input_file, "read")

    if not oldfile or oldfile.IsZombie():
        print(f"Error: Unable to open the input file for chunk {process_number}.")
        return
    
    # Create a new output file
    newfile = TFile(output_file, "recreate")
    tagsDumper = newfile.mkdir("tagsDumper")
    tagsDumper.cd()
    trees = tagsDumper.mkdir("trees")
    trees.cd()
    
    oldtree = oldfile.Get("tagsDumper/trees/Data_13TeV_UntaggedTag_0")
    nentries = oldtree.GetEntries()

    # Calculate the range of entries to process for this chunk
    chunk_size = 1000
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
    
    newtree = oldtree.CloneTree(0)

    # Open the file containing the workspace
    # --------------------------------------
    ws = TFile.Open("/afs/cern.ch/work/e/elfontan/private/DiPhotonAnalysis/Sep2023_flashGG/CMSSW_12_6_5/src/KernelEstimation/w_ML_2d1d_inclusive.root")
    
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
    kest = w.pdf("kestM2d_minmaxPhoId")        
    
    # ----------------------------------------------------                                                             
    # Generating a fake pdf for each maximum photon ID bin                                                   
    # ----------------------------------------------------                                                              
    h_file = TFile.Open("/afs/cern.ch/work/e/elfontan/private/DiPhotonAnalysis/Sep2023_flashGG/CMSSW_12_6_5/src/KernelEstimation/file_histos_1DfakePdfs_from2D_10k.root")
    list_maxphoid_names = ["m0p65","m0p55","m0p45","m0p35","m0p25","m0p15","m0p05","p0p05","p0p15","p0p25","p0p35","p0p45","p0p55","p0p65","p0p75","p0p9"]
    list_maxphoid_mean = [-0.65, -0.55, -0.45, -0.35, -0.25, -0.15, -0.05, 0.05, 0.15, 0.25, 0.35, 0.45, 0.55, 0.65, 0.75, 0.9]
    list_maxphoid_min = [-0.7, -0.6, -0.5, -0.4, -0.3, -0.2, -0.1, 0.00, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8]
    list_maxphoid_max = [-0.6, -0.5, -0.4, -0.3, -0.2, -0.1, 0.00, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 1.0]
    h_kest_list = []
    
    for n in range(len(list_maxphoid_names)):
        print(n)
        histoname = "h_gendata_kest"+list_maxphoid_names[n]
        h_kest = h_file.Get(histoname)
        h_kest_list.append(h_kest)
        
    # Loop over the selected range of entries and process them
    processedEv = end_entry - start_entry
    for ev in range(start_entry, end_entry):
        if (ev%1000==0): print(ev,processedEv)
        oldtree.GetEntry(ev)
                
        #print("Original minID is = \t", min(dipho_leadIDMVA[0],dipho_subleadIDMVA[0]))
        #print("Original maxID is = \t", max(dipho_leadIDMVA[0],dipho_subleadIDMVA[0]))
        
        #if event is in sideband and also blinded
        if (min(dipho_leadIDMVA[0],dipho_subleadIDMVA[0])<-0.7 and max(dipho_leadIDMVA[0],dipho_subleadIDMVA[0])>-0.7): 
            nEvents_SB+=1
            print("Original minID SB is = \t", min(dipho_leadIDMVA[0],dipho_subleadIDMVA[0]))
            print("Original maxID SB is = \t", max(dipho_leadIDMVA[0],dipho_subleadIDMVA[0]))
        
            # Use the pdf to generate a new minimum ID
            # ----------------------------------------
            dipho_maxIDMVA.setVal(max(dipho_leadIDMVA[0],dipho_subleadIDMVA[0]))
            dipho_maxIDMVA.setConstant(True)
            dipho_minIDMVA.setConstant(False)
            dipho_minIDMVA.setRange(-0.7,max(dipho_leadIDMVA[0],dipho_subleadIDMVA[0]))
            min_fakePdf = kest.generate(RooArgSet(dipho_minIDMVA), 1)
            min_ID = min_fakePdf.get(0).getRealValue("dipho_minIDMVA")
            
            # Reweight the event
            # ------------------
            if (max(dipho_leadIDMVA[0],dipho_subleadIDMVA[0])>=list_maxphoid_min[0] and max(dipho_leadIDMVA[0],dipho_subleadIDMVA[0])<list_maxphoid_max[0]):
                h_kest_list[0].GetXaxis().SetRangeUser(-0.7, 0.5)
                num = h_kest_list[0].Integral()
                h_kest_list[0].GetXaxis().SetRangeUser(-0.9, -0.7)
                den = h_kest_list[0].Integral()
                reweight = num/den
                print("num", num, "  and den", den)
                print("reweight", reweight)
                
            elif (max(dipho_leadIDMVA[0],dipho_subleadIDMVA[0])>=list_maxphoid_min[1] and max(dipho_leadIDMVA[0],dipho_subleadIDMVA[0])<list_maxphoid_max[1]):
                h_kest_list[1].GetXaxis().SetRangeUser(-0.7, 0.5)
                num = h_kest_list[1].Integral()
                h_kest_list[1].GetXaxis().SetRangeUser(-0.9, -0.7)
                den = h_kest_list[1].Integral()
                reweight = num/den
                
            elif (max(dipho_leadIDMVA[0],dipho_subleadIDMVA[0])>=list_maxphoid_min[2] and max(dipho_leadIDMVA[0],dipho_subleadIDMVA[0])<list_maxphoid_max[2]):
                h_kest_list[2].GetXaxis().SetRangeUser(-0.7, 0.5)
                num = h_kest_list[2].Integral()
                h_kest_list[2].GetXaxis().SetRangeUser(-0.9, -0.7)
                den = h_kest_list[2].Integral()
                reweight = num/den
                
            elif (max(dipho_leadIDMVA[0],dipho_subleadIDMVA[0])>=list_maxphoid_min[3] and max(dipho_leadIDMVA[0],dipho_subleadIDMVA[0])<list_maxphoid_max[3]):
                h_kest_list[3].GetXaxis().SetRangeUser(-0.7, 0.5)
                num = h_kest_list[3].Integral()
                h_kest_list[3].GetXaxis().SetRangeUser(-0.9, -0.7)
                den = h_kest_list[3].Integral()
                reweight = num/den
                
            elif (max(dipho_leadIDMVA[0],dipho_subleadIDMVA[0])>=list_maxphoid_min[4] and max(dipho_leadIDMVA[0],dipho_subleadIDMVA[0])<list_maxphoid_max[4]):
                h_kest_list[4].GetXaxis().SetRangeUser(-0.7, 0.5)
                num = h_kest_list[4].Integral()
                h_kest_list[4].GetXaxis().SetRangeUser(-0.9, -0.7)
                den = h_kest_list[4].Integral()
                reweight = num/den
            
            elif (max(dipho_leadIDMVA[0],dipho_subleadIDMVA[0])>=list_maxphoid_min[5] and max(dipho_leadIDMVA[0],dipho_subleadIDMVA[0])<list_maxphoid_max[5]):
                h_kest_list[5].GetXaxis().SetRangeUser(-0.7, 0.5)
                num = h_kest_list[5].Integral()
                h_kest_list[5].GetXaxis().SetRangeUser(-0.9, -0.7)
                den = h_kest_list[5].Integral()
                reweight = num/den
        
            elif (max(dipho_leadIDMVA[0],dipho_subleadIDMVA[0])>=list_maxphoid_min[6] and max(dipho_leadIDMVA[0],dipho_subleadIDMVA[0])<list_maxphoid_max[6]):
                h_kest_list[6].GetXaxis().SetRangeUser(-0.7, 0.5)
                num = h_kest_list[6].Integral()
                h_kest_list[6].GetXaxis().SetRangeUser(-0.9, -0.7)
                den = h_kest_list[6].Integral()
                reweight = num/den
                
            elif (max(dipho_leadIDMVA[0],dipho_subleadIDMVA[0])>=list_maxphoid_min[7] and max(dipho_leadIDMVA[0],dipho_subleadIDMVA[0])<list_maxphoid_max[7]):
                h_kest_list[7].GetXaxis().SetRangeUser(-0.7, 0.5)
                num = h_kest_list[7].Integral()
                h_kest_list[7].GetXaxis().SetRangeUser(-0.9, -0.7)
                den = h_kest_list[7].Integral()
                reweight = num/den
                
            elif (max(dipho_leadIDMVA[0],dipho_subleadIDMVA[0])>=list_maxphoid_min[8] and max(dipho_leadIDMVA[0],dipho_subleadIDMVA[0])<list_maxphoid_max[8]):
                h_kest_list[8].GetXaxis().SetRangeUser(-0.7, 0.5)
                num = h_kest_list[8].Integral()
                h_kest_list[8].GetXaxis().SetRangeUser(-0.9, -0.7)
                den = h_kest_list[8].Integral()
                reweight = num/den
            
            elif (max(dipho_leadIDMVA[0],dipho_subleadIDMVA[0])>=list_maxphoid_min[9] and max(dipho_leadIDMVA[0],dipho_subleadIDMVA[0])<list_maxphoid_max[9]):
                h_kest_list[9].GetXaxis().SetRangeUser(-0.7, 0.5)
                num = h_kest_list[9].Integral()
                h_kest_list[9].GetXaxis().SetRangeUser(-0.9, -0.7)
                den = h_kest_list[9].Integral()
                reweight = num/den
                
            elif (max(dipho_leadIDMVA[0],dipho_subleadIDMVA[0])>=list_maxphoid_min[10] and max(dipho_leadIDMVA[0],dipho_subleadIDMVA[0])<list_maxphoid_max[10]):
                h_kest_list[10].GetXaxis().SetRangeUser(-0.7, 0.5)
                num = h_kest_list[10].Integral()
                h_kest_list[10].GetXaxis().SetRangeUser(-0.9, -0.7)
                den = h_kest_list[10].Integral()
                reweight = num/den
                
            elif (max(dipho_leadIDMVA[0],dipho_subleadIDMVA[0])>=list_maxphoid_min[11] and max(dipho_leadIDMVA[0],dipho_subleadIDMVA[0])<list_maxphoid_max[11]):
                h_kest_list[11].GetXaxis().SetRangeUser(-0.7, 0.5)
                num = h_kest_list[11].Integral()
                h_kest_list[11].GetXaxis().SetRangeUser(-0.9, -0.7)
                den = h_kest_list[11].Integral()
                reweight = num/den
        
            elif (max(dipho_leadIDMVA[0],dipho_subleadIDMVA[0])>=list_maxphoid_min[12] and max(dipho_leadIDMVA[0],dipho_subleadIDMVA[0])<list_maxphoid_max[12]):
                h_kest_list[12].GetXaxis().SetRangeUser(-0.7, 0.5)
                num = h_kest_list[12].Integral()
                h_kest_list[12].GetXaxis().SetRangeUser(-0.9, -0.7)
                den = h_kest_list[12].Integral()
                reweight = num/den
                
            elif (max(dipho_leadIDMVA[0],dipho_subleadIDMVA[0])>=list_maxphoid_min[13] and max(dipho_leadIDMVA[0],dipho_subleadIDMVA[0])<list_maxphoid_max[13]):
                h_kest_list[13].GetXaxis().SetRangeUser(-0.7, 0.5)
                num = h_kest_list[13].Integral()
                h_kest_list[13].GetXaxis().SetRangeUser(-0.9, -0.7)
                den = h_kest_list[13].Integral()
                reweight = num/den
                
            elif (max(dipho_leadIDMVA[0],dipho_subleadIDMVA[0])>=list_maxphoid_min[14] and max(dipho_leadIDMVA[0],dipho_subleadIDMVA[0])<list_maxphoid_max[14]):
                h_kest_list[14].GetXaxis().SetRangeUser(-0.7, 0.5)
                num = h_kest_list[14].Integral()
                h_kest_list[14].GetXaxis().SetRangeUser(-0.9, -0.7)
                den = h_kest_list[14].Integral()
                reweight = num/den
                
            elif (max(dipho_leadIDMVA[0],dipho_subleadIDMVA[0])>=list_maxphoid_min[15] and max(dipho_leadIDMVA[0],dipho_subleadIDMVA[0])<list_maxphoid_max[15]):
                h_kest_list[15].GetXaxis().SetRangeUser(-0.7, 0.5)
                num = h_kest_list[15].Integral()
                h_kest_list[15].GetXaxis().SetRangeUser(-0.9, -0.7)
                den = h_kest_list[15].Integral()
                reweight = num/den
            elif (max(dipho_leadIDMVA[0],dipho_subleadIDMVA[0])>=list_maxphoid_min[16] and max(dipho_leadIDMVA[0],dipho_subleadIDMVA[0])<list_maxphoid_max[16]):
                h_kest_list[15].GetXaxis().SetRangeUser(-0.7, 0.5)
                num = h_kest_list[15].Integral()
                h_kest_list[15].GetXaxis().SetRangeUser(-0.9, -0.7)
                den = h_kest_list[15].Integral()
                reweight = num/den
                
            print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> Event in sideband = ", ev)
            print("New minID is = \t", min_ID)
            print("### REWEIGHTING ###")
            print("reweight TOT = ", reweight)
            print("###################")
        
            weight[0] = weight[0] * reweight
            #print "dipho_leadIDMVA[0] = ", dipho_leadIDMVA[0]
            #print "dipho_subleadIDMVA[0] = ", dipho_subleadIDMVA[0]
            
            if (dipho_leadIDMVA[0] < dipho_subleadIDMVA[0]):         
                dipho_leadIDMVA[0] = min_ID
            else:
                dipho_subleadIDMVA[0] = min_ID
                
            newtree.Fill()
        newtree.AutoSave()
    # Close the files when done
    newfile.Close()
    oldfile.Close()
    ws.Close()
    del oldfile
    del newfile

        
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python chunk_reweight_with_kest.py <process_number>")
    else:
        process_number = int(sys.argv[1])
        main(process_number)
