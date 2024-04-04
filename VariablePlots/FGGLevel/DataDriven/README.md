# Kernel Estimation method to extract a fake pdf

### Preparation of a fake pdf to describe the minimum and maximum photon ID distributions using gJets MC events 

   **Available files in the repo**:

   - `makeBkgGJets_newSandS_gjAll_Inclusive.py`: It can be used to prepare the histogram of the minimum photon ID distribution from gJets MC events. In this case, we consider all the gJets MC samples (= all mass ranges: [0,40] GeV, [40,80] GeV, [80,Inf] GeV). The output file is provided here as an example: `newSandS_gjAll_Inclusive.root`   

   - `histoBased_binsPhoIdMinMax_kest_pfFilter.C`: It is used to generate a workspace `w_newSandS_gjAll_Inclusive.root` including some 1D Kernel Density Functions obtained with different tunings of the parameters (mirror left, mirror right, no mirror, different values of the bandwith, ...). In this example, the mirror left case is considered with different bandwidth values.   

   - The directory `kest1D_condor_submission` contains the submission script and the executable to produce a sideband data file containing a new minimum photon ID distribution, as generated from the fake PDF saved in the workspace, and a reshaped maximum to describe the maximum photon ID in the preselection region. Follow the README in that directory to proceed.

   **Run the scripts**:
   ```
   python makeBkgGJets_newSandS_gjAll_Inclusive.py
   root -l histoBased_binsPhoIdMinMax_kest_pfFilter.C
   cd kest1D_condor_submission
   ```