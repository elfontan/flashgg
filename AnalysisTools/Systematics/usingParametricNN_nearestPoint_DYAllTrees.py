# --------------------------------------------------------------------------------------------------- #
# ### Low mass diphoton analysis                                                                      #
# ### Parametric neural network for signal and background classification: add score to signal samples #
# * **use the model** trained in `trainingParametricNN_nearestPoint.ipynb`                            #
# * **save NNScore in the testing trees**                                                             #
# --------------------------------------------------------------------------------------------------- #
#!/usr/bin/env python3
# coding: utf-8

from ROOT import TFile, TTree, TBranch, TList, gROOT, gSystem, TChain
import random, copy                                                                                                        
import ROOT, array, CMSGraphics, CMS_lumi                                       
import sys
import numpy as np
import math, os, h5py
import pandas as pd
import uproot
import tensorflow as tf
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Dense, Input, Layer
import sklearn
import matplotlib.pyplot as plt
import matplotlib.font_manager as font_manager
import mplhep as hep
import argparse                                                                                                        
import sys                                                                                                     
import os                                                                                                  
#gROOT.SetBatch()                                                                                    
#ROOT.gStyle.SetOptStat(0)                                                                 
#ROOT.gStyle.SetOptTitle(0)                                                                                 
#ROOT.gStyle.SetOptStat(0)                                                                 
argparser = argparse.ArgumentParser(description='Parser used for non default arguments', formatter_class=argparse.ArgumentDefaultsHelpFormatter, add_help=True)       
#argparser.add_argument('--d', dest='d', default='/eos/user/e/elfontan/DiPhotonAnalysis/diphotonBDT/Syst/SigMC_NTUPLES/', help='Input and Output Files directory')       
#argparser.add_argument('--m', dest='m', default='70', help='Mass hypothesis')

args = argparser.parse_args()                                                                   
#dir  = args.d                                                                                                             
#mass = args.m


indir = "/eos/user/e/elfontan/DiPhotonAnalysis/diphotonBDT/Zee/"
model_file = "/eos/user/e/elfontan/DiPhotonAnalysis/diphotonBDT/SignalModeling/models/model_WeightedCrossEntropyLoss_nearestPoint_newSamples_flat.h5"

######################################################
# Parametric classifier and loss function definition #
######################################################
class ParametricClassifier(Model):
    def __init__(self, input_shape, architecture=[1, 4, 1], activation='relu', name=None, **kwargs):
        super().__init__(name=name, **kwargs)
        kernel_constraint = None
        self.hidden_layers = [Dense(architecture[i+1], input_shape=(architecture[i],), activation=activation) for i in range(len(architecture)-2)]
        self.output_layer  = Dense(architecture[-1], input_shape=(architecture[-2],), activation='linear')
        self.build(input_shape)
        
    def call(self, x):
        for i, hidden_layer in enumerate(self.hidden_layers):
            x = hidden_layer(x)
        x = self.output_layer(x)
        return x

def QuadraticLoss(true, pred):
    y = true[:, 1] #taken from the true_label definition 
    w = true[:, 0] #taken from the true_label definition 
    f = pred[:, 0]
    c = 1./(1+tf.exp(f))
    return 1000*tf.reduce_mean(y*w*c**2 + (1-y)*w*(1-c)**2)
 
def WeightedCrossEntropyLoss(true, pred):
    y   = true[:, 1] #taken from the true_label definition 
    w   = true[:, 0] #taken from the true_label definition
    f   = pred[:, 0]
    return 0.1*tf.reduce_sum((1-y)*w*tf.math.log(1+tf.exp(f)) + y*w*tf.math.log(1+tf.exp(-1*f))) #activation='linear'

#####################
# Model declaration #
#####################
architecture = [11, 50, 50, 50, 1] # f(x, m) = NN(x, {w}, {b}) || f(x, m) = m * NN(x, {w}, {b})
model = ParametricClassifier(input_shape=(None, 11), architecture=architecture, activation='relu')
optimizer = tf.keras.optimizers.legacy.Adam()
print(model.summary())

model.compile(loss=WeightedCrossEntropyLoss, # QuadraticLoss
              optimizer=optimizer, 
              #metrics=['binary_accuracy']
             )

model.load_weights(model_file)

# Open the HDF5 file in read-only mode to check the content of the model
# ----------------------------------------------------------------------
with h5py.File(model_file, 'r') as file:
    # Print the keys at the root level of the HDF5 file
    print("Root keys:", list(file.keys()))
    
    print("Contents of 'dense':", list(file['dense'])) # weights and vias for each layer
    print("Contents of 'dense_1':", list(file['dense_1']))
    print("Contents of 'dense_2':", list(file['dense_2']))
    print("Contents of 'dense_3':", list(file['dense_3']))
    
    # Access a specific group or dataset within the HDF5 file
    if 'top_level_model_weights' in file:
        print("Contents of 'top_level_model_weights':", list(file['top_level_model_weights']))
    else:
        print("Group or dataset 'top_level_model_weights' not found.")
        
with h5py.File(model_file, 'r') as file:
    layer_weights = file['dense']['dense']
    print("Weights of dense layer:", layer_weights)
    
        
with h5py.File(model_file, 'r') as file:
    layer_weights = file['dense_1']['dense_1']
    print("Weights of dense_1 layer:", layer_weights)
    
        
with h5py.File(model_file, 'r') as file:
    layer_weights = file['dense_2']['dense_2']
    print("Weights of dense_2 layer:", layer_weights)
    
        
with h5py.File(model_file, 'r') as file:
    layer_weights = file['dense_3']['dense_3']
    print("Weights of dense_3 layer:", layer_weights)
    
####################################
# --STANDARDIZING VARIABLES RANGES #
####################################
# Make the dataset invariant for scale effects.
# Rule to transform data to be in a proper shape to apply the model

# Standardizing variables ranges: reference values used in the training
# ---------------------------------------------------------------------    
mean_REF = np.array([1.02723945e+00,5.97155929e-01,3.27149360e-01,1.40618341e-01,1.30073259e-03,1.84589661e-03,2.26421862e-02,2.87247697e-02,-2.43791035e-01,7.45146274e-01,5.09008220e+01])
std_REF = np.array([0.85487014,0.444752,0.5892425,0.59489149,0.99642843,0.95968482,0.02581517,0.02511732,0.77730978,0.26923345,16.86734849])
def standardize_dataset(data, mean, std):
    return (data - mean) / std

###########################################
# --VARIABLES USED FOR THE MODEL BUILDING #
###########################################

vars_list = [
    'dipho_lead_ptoM', 'dipho_sublead_ptoM',
    'dipho_leadIDMVA', 'dipho_subleadIDMVA',
    'dipho_leadEta', 'dipho_subleadEta',
    'sigmaMrvoM', 'sigmaMwvoM',
    'cosphi', 'vtxprob',
    'CMS_hgg_mass'
]



import ROOT
from array import array

ROOT.gROOT.SetBatch()
ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetOptTitle(0)

##########################
# Building the datasets: #
# ----------------------------------------------------------------------
# Inputs: input files and input trees, training variables, mass points #
# ----------------------------------------------------------------------
def add_nn_score_to_trees(file_names, tree_names, vars_list):    
    idx = 0
    for file_name in file_names:
        print(f"Processing file {file_name}")
        infile = ROOT.TFile.Open(file_name)

        for tree_name in tree_names:
            print(f"Processing tree {tree_name}")
            tree = infile.Get("tagsDumper/trees/" + tree_name)
            rdf = ROOT.RDataFrame(tree)
            #rdf = ROOT.RDataFrame(tree).Filter("dipho_leadIDMVA > -0.7 && dipho_subleadIDMVA > -0.7 && CMS_hgg_mass < 75.0")
            np_data = rdf.AsNumpy(vars_list)
            data_col = [np_data[var] for var in vars_list]
            data = np.column_stack(data_col)
            
            # Standardize the data
            data = standardize_dataset(data, mean_REF, std_REF)
            
            # Predict NN scores
            preds = tf.sigmoid(model.predict(data)).numpy()[:, 0]
            
            # Create the necessary directories in the output file
            newfile_data = ROOT.TFile("DY_Systematics/out_"+tree_name+".root", "recreate")
            tagsDumper = newfile_data.mkdir("tagsDumper") if not newfile_data.GetDirectory("tagsDumper") else newfile_data.GetDirectory("tagsDumper")
            trees = tagsDumper.mkdir("trees") if not tagsDumper.GetDirectory("trees") else tagsDumper.GetDirectory("trees")
            
            oldtree = infile.Get(f"tagsDumper/trees/{tree_name}")
            nentries = oldtree.GetEntries()
            print(f"nentries in {tree_name} = {nentries}")
            
            # Create a new tree with the same structure
            NNScore = array('f', [0.])
            newtree = oldtree.CloneTree(0)
            newtree.Branch("NNScore", NNScore, "NNScore/F")
            
            # Loop over the entries and fill the new tree with NNScore values
            count = 0
            for entry in oldtree:
                NNScore[0] = preds[count]
                newtree.Fill()
                count += 1
            
            # Save the new tree to the new file
            trees.cd()
            newtree.Write()
            # Close the output file
            newfile_data.Close()

        idx+=1
        # Close the input file
        infile.Close()
    
    # Close the output file
    #newfile_data.Close()


# -------------------------- #
# Call add_nn_score function #
# -------------------------- #
file_names_sig = ["/eos/user/e/elfontan/DiPhotonAnalysis/diphotonBDT/ZeeVal/dyJets2018_zeeVal_withSyst.root"]
tree_names_sig = [
    "DYToLL_13TeV_UntaggedTag_0",
    "DYToLL_13TeV_UntaggedTag_0_MvaShiftDown01sigma",
    "DYToLL_13TeV_UntaggedTag_0_MvaShiftUp01sigma",
    "DYToLL_13TeV_UntaggedTag_0_SigmaEOverEShiftDown01sigma",
    "DYToLL_13TeV_UntaggedTag_0_SigmaEOverEShiftUp01sigma"
]
add_nn_score_to_trees(file_names_sig, tree_names_sig, vars_list)
