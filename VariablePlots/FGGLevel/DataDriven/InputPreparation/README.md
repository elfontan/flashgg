# Preparation of the inputs for the data driven BDT and dedicated reweighting procedures

A data driven approach is used to describe background events coming from gJets and QCD events. The set of tools and the description of the steps needed to prepare the input files for this strategy are contained in this directory.  

The directory includes four main repositories related to the different steps used for the preparation of the inputs for the data-driven BDT training:
* `KernelEstimation`: method to prepare a fake pdf using gJets MC events to describe the minimum and maximum photon ID distributions in sideband data events.
* `TFractionFitter`: a two-dimensional template fit on minimum and maximum photon ID is performed in order to improve the description of the data provided by the two background contributions under consideration, diphoton MC and PF+FF data-driven background (as replacement of gJets + QCD events).
* `sigmaEOE_minIdPho_1Dreweighting`:
* `scaledPt_minmaxIdPho_2Dreweighting`:
* `eta_minIdPho_1Dreweighting`:

### Template fit
A two-dimensional simultaneous fit is performed on the 2D histogram of the scaled transverse momentum of minimum and maximum MVA ID photon. Two additional macros are available to perform 1D fits starting from the two separate 1D histograms: `1D_minPhoId_TFractionFitter.py` and `1D_maxPhoId_TFractionFitter.py`.

   **Available files in the repo**:
   - `TFractionFitter.C`:  
   ```
   root -l TFractionFitter.C
   ```


