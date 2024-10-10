# Using a parametric Neural Network (PNN) as the multivariate analyzer for diphoton event quality

### Input Preparation

* Kernel estimation is used to create a fake PDF from fitting the minimum photon ID distribution of GJet sample (`InputPreparation/KernelEstimation`).
* Reweighting of data-driven sideband and diphoton MC allows to match data preselection region (`InputPreparation/ReweightingProcedure`)
* Mass hypothesis parameters are assigned by using a set of mass points and nearest neighbor method (`InputPreparation/MassHypo`). 

### Training 

Jupyter Notebooks used for the training of the PNN and for adding the score to relevant samples are included in the repository `PNN_Training`.  

### ROC Validation and Categorization using figures of merit

* Validation is done using entire preselection region of data and weighted signal events.
* Approximate Asimov significance is used as figure of merit, with signal scaled to full luminosity against data-driven background (see `plotAsimov.py`).
* Class 0 boundary is then determined as the average value of the PNN scores that yield the highest figures of merit.