# Using a parametric Neural Network (PNN) as the multivariate analyzer for diphoton event quality

### Input Preparation

* Using Kernel estimation to create a fake PDF from fitting the minimum photon ID distribution of GJet sample
* Reweighting of data-driven sideband and diphoton MC to match data preselection region (not yet in repo)
* Assigning mass hypothesis parameters using a set of mass points and nearest neighbor method

### Training (not in repo)

### ROC Validation and Categorization using figures of merit

* Validation is done using entire preselection region of data and weighted signal events
* Approximate Asimov significance is used as figure of merit, with signal scaled to full luminosity against data-driven background (see `plotAsimov.py`).
* Class 0 boundary is then determined as the average value of the NN scores that yield the highest figures of merit.
