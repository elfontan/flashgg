#include <TString.h>

//write the datacard
void noNNLOPS_redTheory_manual_slidingdatacard10p_creation_cat0(){
  for (int mass=10; mass<71; mass++){
    TString mass_s;
    mass_s = Form("%iGeV_",mass);
    TString cat_s;
    TString cat_n;
    char inputShape[200];
    sprintf(inputShape,"noNNLOPS_redTheory_datacards_sliding10pdata_syst/sliding_"+mass_s+"cat0.txt");
    ofstream newcardShape;
    newcardShape.open(inputShape);
    newcardShape << Form("imax * \n");
    newcardShape << Form("jmax * \n");
    newcardShape << Form("kmax * \n");
    newcardShape << Form("------------------------------------------      \n");
    newcardShape << Form("shapes     sig cat0 ../ws_sig/CMS-HGG_sigfit_LMAnalysis_Jul2024_newSignalNtuplesNoNNLOPS_4Cat_gghSystFixed_2018_GG2H_2018_UntaggedTag_0.root wsig_13TeV:hggpdfsmrel_GG2H_2018_UntaggedTag_0_13TeV\n");
    newcardShape << Form("shapes     bkg cat0 ../ws_sliding10pdata/CMS-HGG_"+mass_s+"multipdf_UntaggedTag_0.root multipdf:CMS_hgg_UntaggedTag_0_2018_13TeV_bkgshape\n");
    newcardShape << Form("shapes     data_obs cat0 ../ws_sliding10pdata/CMS-HGG_"+mass_s+"multipdf_UntaggedTag_0.root multipdf:roohist_data_mass_UntaggedTag_0\n");
    newcardShape << Form("bin                 cat0\n");
    newcardShape << Form("observation         -1\n");
    newcardShape << Form("------------------------------------------      \n");
    newcardShape << Form("bin               cat0           cat0      \n");
    newcardShape << Form("process           sig            bkg            \n");
    newcardShape << Form("process           -1               1            \n");
    newcardShape << Form("rate              5440            1            \n");
    newcardShape << Form("------------------------------------------      \n");
    newcardShape << Form("pdfindex_UntaggedTag_0_2018_13TeV discrete      \n");
    newcardShape << Form("------------------------------------------      \n");
    newcardShape << Form("lumi                lnN             1.015    -    \n");
    newcardShape << Form("nvtx_rew                lnN             1.007    -    \n");
    newcardShape << Form("CMS_hgg_LooseMvaSF_2018   lnN   1.002    -    \n");
    newcardShape << Form("CMS_hgg_PreselSF_2018   lnN   1.047    -    \n");
    newcardShape << Form("CMS_hgg_electronVetoSF_2018   lnN   1.005    -    \n");
    newcardShape << Form("CMS_hgg_TriggerWeight_2018   lnN   1.004    -    \n");
    newcardShape << Form("CMS_hgg_SigmaEOverEShift_2018   lnN   1.054    -    \n");
    newcardShape << Form("CMS_hgg_phoIdMva_2018   lnN   1.059    -    \n");
    newcardShape << Form("------------------------------------------      \n");
    newcardShape << Form("QCDscale_ggH   lnN   1.023/0.957   -    \n");
    newcardShape << Form("alphaS_ggH   lnN   1.034    -    \n");
    newcardShape << Form("CMS_hgg_scaleWeight_0    lnN   1.021/0.965    -    \n");
    newcardShape << Form("CMS_hgg_scaleWeight_1    lnN   1.058/0.952    -    \n"); 
    newcardShape << Form("CMS_hgg_scaleWeight_2    lnN   1.070/0.914    -    \n"); 
    newcardShape << Form("------------------------------------------      \n");
    newcardShape << Form("CMS_hgg_nuisance_NonLinearity_13TeVscale    param   0.0   0.002	\n");
    newcardShape << Form("CMS_hgg_nuisance_HighR9EB_13TeVscale_2018    param   0.0   1.0	\n");
    newcardShape << Form("CMS_hgg_nuisance_HighR9EE_13TeVscale_2018    param   0.0   1.0	\n");
    newcardShape << Form("CMS_hgg_nuisance_LowR9EB_13TeVscale_2018    param   0.0   1.0	\n");
    newcardShape << Form("CMS_hgg_nuisance_LowR9EE_13TeVscale_2018    param   0.0   1.0	\n");
    newcardShape << Form("CMS_hgg_nuisance_ShowerShapeHighR9EB_13TeVscaleCorr    param   0.0   1.0	\n");
    newcardShape << Form("CMS_hgg_nuisance_ShowerShapeHighR9EE_13TeVscaleCorr    param   0.0   1.0	\n");
    newcardShape << Form("CMS_hgg_nuisance_ShowerShapeLowR9EB_13TeVscaleCorr    param   0.0   1.0	\n");
    newcardShape << Form("CMS_hgg_nuisance_ShowerShapeLowR9EE_13TeVscaleCorr    param   0.0   1.0	\n");
    newcardShape << Form("CMS_hgg_nuisance_MaterialCentralBarrel_13TeVscaleCorr    param   0.0   1.0	\n");
    newcardShape << Form("CMS_hgg_nuisance_MaterialOuterBarrel_13TeVscaleCorr    param   0.0   1.0	\n");
    newcardShape << Form("CMS_hgg_nuisance_MaterialForwardBarrel_13TeVscaleCorr    param   0.0   1.0	\n");
    newcardShape << Form("CMS_hgg_nuisance_FNUFEB_13TeVscaleCorr    param   0.0   1.0	\n");
    newcardShape << Form("CMS_hgg_nuisance_FNUFEE_13TeVscaleCorr    param   0.0   1.0	\n");
    newcardShape << Form("CMS_hgg_nuisance_HighR9EBPhi_13TeVsmear_2018    param   0.0   1.0	\n");
    newcardShape << Form("CMS_hgg_nuisance_HighR9EBRho_13TeVsmear_2018    param   0.0   1.0	\n");
    newcardShape << Form("CMS_hgg_nuisance_HighR9EERho_13TeVsmear_2018    param   0.0   1.0	\n");
    newcardShape << Form("CMS_hgg_nuisance_LowR9EBRho_13TeVsmear_2018    param   0.0   1.0	\n");
    newcardShape << Form("CMS_hgg_nuisance_LowR9EERho_13TeVsmear_2018    param   0.0   1.0	\n");
    newcardShape << Form("------------------------------------------      \n");
    newcardShape << Form("theory group = QCDscale_ggH alphaS_ggH CMS_hgg_scaleWeight_0 CMS_hgg_scaleWeight_1 CMS_hgg_scaleWeight_2\n");
    newcardShape << Form("exp group = CMS_hgg_electronVetoSF_2018 CMS_hgg_LooseMvaSF_2018 CMS_hgg_PreselSF_2018 CMS_hgg_TriggerWeight_2018 CMS_hgg_SigmaEOverEShift_2018 CMS_hgg_phoIdMva_2018\n");
    newcardShape.close();
  }
}
