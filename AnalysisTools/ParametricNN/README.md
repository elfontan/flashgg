Using a parametric Neural Network (pNN) as the multivariate analyzer for diphoton event quality.
1. Input Preparation
1a. Using Kernel estimation to create a fake PDF from fitting the minimum photon ID distribution of GJet sample
1b. Reweighting of data-driven sideband and diphoton MC to match data preselection region (not yet in repo)
1c. Assigning mass hypothesis parameters using a set of mass points and nearest neighbor method
2. Training (not in repo)
3. ROC Validation and Categorization using figures of merit
3a. Validation is done using entire preselection region of data and weighted signal events
3b. Approximate Asimov significance is used as figure of merit, with signal scaled to full luminosity against data-driven background (see `plotAsimov.py`).
3c. Class 0 boundary is then determined as the average value of the NN scores that yield the highest figures of merit.
