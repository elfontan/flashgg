//#include "setTDRStyle.C"
#include "TMath.h"
//#include "TROOT.h"
#include <TH1D.h>
#include <TH1F.h>
#include <TH1.h>
#include <TProfile.h>
#include <TStyle.h>
#include <THStack.h>
#include <TCanvas.h>
#include <TLeafF.h>
#include <TChain.h>
#include <TFile.h>
#include "TSystem.h"
#include <TChain.h>
#include "TSystem.h"
#include <TString.h>
#include <iostream>
#include <vector>
#include <TPostScript.h>
#include <iostream>
#include <iomanip>  //for precision

//==============
const int debug=1;
const int IfMCSig = 0;
const int IfBlind = 1;

const string TreeNameData = "tagsDumper/trees/Data_13TeV_UntaggedTag";
const string TreeNameQCD = "tagsDumper/trees/MC_13TeV_UntaggedTag";
const string TreeNameGJet = "tagsDumper/trees/MC_13TeV_UntaggedTag";
const string TreeNamediPho = "tagsDumper/trees/MC_13TeV_UntaggedTag";
const TString PrintInfor1="#bf{CMS} #it{} #it{Preliminary}";
const TString PrintInfor2="36.3 fb^{-1} (13TeV)";

//////////////////////////////////////

//void DrawMyPlots(string Object, string Selections,  string XTitle, string YUnit, string PlotName, int BinTotal, double BinXLow, double BinXHig, double RYLow, double RYHig, int LegendLR, int IfLogY, int IfBlind=0, int IfLogX=0){//for unblind
//void DrawMyPlots(string Object, string Selections,  string XTitle, string YUnit, string PlotName, int BinTotal, double BinXLow, double BinXHig, double RYLow, double RYHig, int LegendLR, int IfLogY, int IfBlind, int IfLogX=0){
//void DrawMyPlots(string Object,  string XTitle, string YUnit, string PlotName, int BinTotal, double BinXLow, double BinXHig, double RYLow, double RYHig, int LegendLR, int IfLogY, int IfBlind, int IfLogX=0){
void DrawMyPlots(string Object, string XTitle, string YUnit, string PlotName, int BinTotal, double BinXLow, double BinXHig, double RYLow, double RYHig, int LegendLR, int IfLogY, int IfLogX=0){


  TCanvas *c1 = new TCanvas("reconstruction1","reconstruction1");
  c1->SetFillColor(0);

  TLegend *legend;
  if(IfMCSig==1){
    if(LegendLR==0) legend = new TLegend(0.61,0.8,0.91,0.92);
    else if(LegendLR==1) legend = new TLegend(0.2,0.8,0.51,0.92);
    else legend = new TLegend(0.4,0.8,0.7,0.92);
  }else{
    if(LegendLR==0) legend = new TLegend(0.61,0.55,0.91,0.9);
    else if(LegendLR==1) legend = new TLegend(0.2,0.55,0.51,0.9);
    else legend = new TLegend(0.4,0.7,0.7,0.9);
  }
  legend->SetFillColor(0);
  //====add root file
  TChain *Data_Tree=new TChain(TreeNameData.c_str());
  TChain *MCGG_Tree=new TChain(TreeNamediPho.c_str());
  TChain *MCGJ_Tree=new TChain(TreeNameGJet.c_str());
  TChain *MCJJ_Tree=new TChain(TreeNameQCD.c_str());

  //====================
  Data_Tree->Add("./FinalTrees/Data_2016legacy.root");
  MCGG_Tree->Add("./FinalTrees/output_DiPhotonJetsBox.root");
  MCGJ_Tree->Add("./FinalTrees/output_GJet.root");
  MCJJ_Tree->Add("./FinalTrees/output_QCD.root");

  //=========entries================
  int entries_Data = Data_Tree->GetEntries();
  if(debug==1) cout <<"JTao: nEntries_Data = "<<entries_Data<<endl;
  c1->cd();
  //=================
  char *myLimits= new char[100];
  sprintf(myLimits,"(%d,%f,%f)",BinTotal,BinXLow,BinXHig);
  TString Taolimits(myLimits);

  TString Cut;
  TString Cut1;
  TString Cut2;
  TString Cut3;

  //  ----- data Cut  --------
    //Cut = "weight * ( ( mass>65. && mass<70.) || ( mass>110. && mass<120.0 ) )"; // low mass 2016Legacy Aamir// for Blinded
    Cut = "weight * ( ( mass>65. && mass<120.0 ) )"; // low mass 2016Legacy Aamir //for unBlinded
     if (Object=="mass") Cut = "weight * ( mass>65. && mass<120.0 )"; // low mass 2017 & 2018 & 2016 Legacy

  // DiPhotonJetsBox cut
    //Cut1 = "weight * ( ( mass>65. && mass<70.) || ( mass>110. && mass<120.0 ) )"; // low mass 2016 Legacy // for Blinded
    Cut1 = "weight * ( ( mass>65. && mass<120.0 ) )"; // low mass 2016 Legacy // for unBlinded
    if (Object=="mass")Cut1 = "weight * ( mass>65. && mass<120.0 )"; // low mass 2016 Legacy
    //if(IfMC_SideBand==1) Cut1 = Cut;

  // jet-jet cut
    //Cut2 = "weight * ( mass>65. && mass<120.0 && ( leadMatchType !=1 && subleadMatchType !=1 ) )";
    //if(IfMC_SideBand==1)  Cut2 = "weight * ( ( (mass>65. && mass<70.0 ) || (mass>110. && mass<120.0) ) && ( leadMatchType !=1 && subleadMatchType !=1 ) )";
    //Cut2 = "weight * ( ( (mass>65. && mass<70.0 ) || (mass>110. && mass<120.0) ) && ( leadMatchType !=1 && subleadMatchType !=1 ) )"; //low mass 2016Legacy Aamir// for Blinded
    Cut2 = "weight * ( ( (mass>65. &&  mass<120.0) ) && ( leadMatchType !=1 && subleadMatchType !=1 ) )"; //low mass 2016Legacy Aamir// for unBlinded
    if(Object=="mass")  Cut2 = "weight * (mass>65. && mass<120.0 && ( leadMatchType !=1 && subleadMatchType !=1 ) )";
    //Case = "both fake";

  // photon-jet cut
    //Cut3 = "weight * ( mass>65. && mass<120.0 && ( ( leadMatchType ==1 && subleadMatchType !=1 ) || ( leadMatchType !=1 && subleadMatchType ==1 ) ) )";
    //if(IfMC_SideBand==1) Cut3 = "weight * ( ( (mass>65. && mass<70.0 ) || (mass>110. && mass<120.0) ) && ( ( leadMatchType ==1 && subleadMatchType !=1 ) || ( leadMatchType !=1 && subleadMatchType ==1 ) ) )";
    //Cut3 = "weight * ( ( (mass>65. && mass<70.0 ) || (mass>110. && mass<120.0) ) && ( ( leadMatchType ==1 && subleadMatchType !=1 ) || ( leadMatchType !=1 && subleadMatchType ==1 ) ) )"; //low mass 2016Legacy Aamir// for Blinded
    Cut3 = "weight * ( ( (mass>65. && mass<120.0) ) && ( ( leadMatchType ==1 && subleadMatchType !=1 ) || ( leadMatchType !=1 && subleadMatchType ==1 ) ) )"; //low mass 2016Legacy Aamir// for unBlinded
    if(Object=="mass") Cut3 = "weight * ( mass>65. && mass<120.0  && ( ( leadMatchType ==1 && subleadMatchType !=1 ) || ( leadMatchType !=1 && subleadMatchType ==1 ) ) )";
    //Case = "1 fake";

  //====data=======
  TString variable_Data = Object + ">>Histo_Data_temp" + Taolimits;
/*  //string dataSelection = Selections;
  //string dataSelection = "(mass>65 && mass<120)";
  string dataSelection = "(mass>65 && mass<70) || (mass>110 && mass<120)";

  string dataSelection = "";
  if(Object=="mass"){
  	dataSelection = "weight*(mass>65. && mass<120.)";}
  else{
  	dataSelection = "weight*(mass>65. && mass<70. || mass>115. && mass<120.)";} 
*/
  //Data_Tree->Draw(variable_Data, dataSelection.c_str());
  Data_Tree->Draw(variable_Data, Cut);
  TH1F *h_data = (TH1F*)gDirectory->Get("Histo_Data_temp");
  h_data->SetTitle("");
  c1->Clear();
  double Ntot_Data=h_data->Integral();
  if( debug==1 ) cout<<"JTao: N_Data= "<<Ntot_Data<<endl;
  //Float_t scale_Data = 1.0/Ntot_Data;
  h_data->Sumw2();
  //h_data->Scale(1);

  ///====================================================
       //TH1F *hff_MC = new TH1F("hff_MC","", BinTotal,BinXLow,BinXHig)   //TH1F *hff_MC = new TH1F("hff_MC","", BinTotal,BinXLow,BinXHig);

    //string MCSelections = Selections;
    //string MCSelections = "(mass>65 && mass<120)";
    //string MCSelections = "(mass>65 && mass<70) || (mass>110 && mass<120)";
    //string PPSelections = "41.529*weight*lumiFactor*(" + MCSelections + " )";
    //string PPSelections = "36.3*weight*(" + MCSelections + " )";
    //string PPSelections = "weight*(" + MCSelections + " )";

    TH1F *h_MC = new TH1F("h_MC","", BinTotal,BinXLow,BinXHig);
    TH1F *hpp_MC= new TH1F("hpp_MC","", BinTotal,BinXLow,BinXHig);  
    TH1F *hpf_MC= new TH1F("hpf_MC","", BinTotal,BinXLow,BinXHig);
    TH1F *hff_MC= new TH1F("hff_MC","", BinTotal,BinXLow,BinXHig);

    // === DiPhotonBox =====
    TString variable_pp = Object + ">>hpp_temp" + Taolimits;
    //MCGG_Tree->Draw(variable_pp, PPSelections.c_str());
    MCGG_Tree->Draw(variable_pp, Cut1);
    hpp_MC = (TH1F*)gDirectory->Get("hpp_temp");
    c1->Clear();
    hpp_MC->Scale(1.3); //JTao test
    float Npp = hpp_MC->Integral();
    cout<<"JTao: total pp : "<<Npp<<" with raw entries from the tree "<<MCGG_Tree->GetEntries()<<endl;
/* 
    string PFPreSel = "( (leadMatchType == 1 && subleadMatchType != 1) || (leadMatchType != 1 && subleadMatchType == 1) )";
    //string PFSelections = "41.529*weight*lumiFactor*(" + MCSelections + " && " + PFPreSel + ")";
    //string PFSelections = "36.3*weight*(" + MCSelections + " && " + PFPreSel + ")";
    string PFSelections = "weight*(" + MCSelections + " && " + PFPreSel + ")";
*/  

    TString variable_gjpf = Object + ">>hgjpf_temp" + Taolimits;
    //MCGJ_Tree->Draw(variable_gjpf, PFSelections.c_str());
    MCGJ_Tree->Draw(variable_gjpf, Cut3);
    TH1F *hgjpf_MC = (TH1F*)gDirectory->Get("hgjpf_temp");
    c1->Clear();
    
    TString variable_jjpf = Object + ">>hjjpf_temp" + Taolimits;
    //MCJJ_Tree->Draw(variable_jjpf, PFSelections.c_str());
    MCJJ_Tree->Draw(variable_jjpf, Cut3);
    TH1F *hjjpf_MC = (TH1F*)gDirectory->Get("hjjpf_temp");
    c1->Clear();

    hpf_MC->Add(hgjpf_MC, 1.0);
    hpf_MC->Add(hjjpf_MC, 1.0);
    
    float Npf=hpf_MC->Integral();
    cout<<"JTao: total pf : "<<hgjpf_MC->Integral()<<" from GJet and "<<hjjpf_MC->Integral()<<" from QCD!"<<endl;
    cout<<"JTao: total pf : "<<Npf<<" from GJet+QCD !"<<endl;
/*
    string FFPreSel = "(leadMatchType != 1 && subleadMatchType != 1)";
    //string FFSelections = "41.529*weight*lumiFactor*(" + MCSelections + " && " + FFPreSel + " )";
    //string FFSelections = "36.3*weight*(" + MCSelections + " && " + FFPreSel + " )";
    string FFSelections = "weight*(" + MCSelections + " && " + FFPreSel + " )";
*/  
    TString variable_gjff = Object + ">>hgjff_temp" + Taolimits;
    //MCGJ_Tree->Draw(variable_gjff, FFSelections.c_str());
    MCGJ_Tree->Draw(variable_gjff, Cut2);
    TH1F *hgjff_MC = (TH1F*)gDirectory->Get("hgjff_temp");
    c1->Clear();
   
    TString variable_jjff = Object + ">>hjjff_temp" + Taolimits;
    //MCJJ_Tree->Draw(variable_jjff, FFSelections.c_str());
    MCJJ_Tree->Draw(variable_jjff, Cut2);
    TH1F *hjjff_MC = (TH1F*)gDirectory->Get("hjjff_temp");
    c1->Clear();
 
    hff_MC->Add(hgjff_MC, 1.0);
    hff_MC->Add(hjjff_MC, 1.0);

    float Nff=hff_MC->Integral();
    cout<<"JTao: total ff : "<<hgjff_MC->Integral()<<" from GJet and "<<hjjff_MC->Integral()<<" from QCD!"<<endl;
    cout<<"JTao: total ff : "<<Nff<<" from GJet+QCD!"<<endl;

    h_MC->Add(hpp_MC, 1.0);
    h_MC->Add(hpf_MC, 1.0);
    h_MC->Add(hff_MC, 1.0);

  //=============
  double Ntot_MC=h_MC->Integral();
  if( debug==1 ) cout<<"JTao: N_MC= "<<Ntot_MC<<endl;
  Float_t scale_MC = Ntot_Data*1.0/Ntot_MC;
  h_MC->Sumw2();

  h_MC->Scale(scale_MC);
  hpp_MC->Scale(scale_MC);
  hpf_MC->Scale(scale_MC);
  hff_MC->Scale(scale_MC);

  cout<<"JTao: MC SF = "<<scale_MC<<endl;
  //double Ntot_MCXSW=h_MC->Integral();
  //if( debug==1 ) cout<<"JTao: Weighted N_MC= "<<Ntot_MCXSW<<endl;

  if( debug==1 ) cout<<"JTao: start to add the MC for THStack! " << endl;

    //=====add a histogram to the stack
   THStack *hs = new THStack("hs","");
    hs->Add(hpp_MC);
    hs->Add(hpf_MC);
    hs->Add(hff_MC);
  if( debug==1 ) cout<<"JTao: after THStack adding! " << endl;

  //===================
  double maxY=max(h_data->GetMaximum(),h_MC->GetMaximum());
  double minY=min(h_data->GetMinimum(),h_MC->GetMinimum());
  minY = 0.9*minY; 
  if(minY<1.) minY=0.1;
  h_data->GetYaxis()->SetRangeUser(minY, 1.2*maxY);
  //h_data->SetMaximum(1.2*maxY);
  if(IfLogY==1) h_data->GetYaxis()->SetRangeUser(0.2, 100.*maxY);
  //-------------------------------------
  TH1F *histoRatio = new TH1F(*h_data);
  histoRatio->Divide(h_data, h_MC, 1., 1.);
  if(IfLogX==1){
    double minX= BinXLow, maxX=BinXHig;
    if(minX<0.0015) minX=0.0015;
    if(maxX<minX)  maxX=1.1*minX;
    h_data->GetXaxis()->SetRangeUser(minX, maxX);
    histoRatio->GetXaxis()->SetRangeUser(minX, maxX);
  }

  //===================
  TH1F *h_MCErr = new TH1F("h_MCErr","", BinTotal,BinXLow,BinXHig);
  double Chi2=0.;
  for(int ibin=0; ibin<BinTotal; ibin++){
   float Nd = h_data->GetBinContent(ibin+1);
    float NdErr = h_data->GetBinError(ibin+1);
    float Nm = h_MC->GetBinContent(ibin+1);
    float NmErr = h_MC->GetBinError(ibin+1);
    if (Nm!=0){
    histoRatio->SetBinError(ibin+1, NdErr/Nm);}
    h_MCErr->SetBinContent(ibin+1, 1.);
    float RelErr = Nm>0.?NmErr*1.0/Nm:0.0;
    h_MCErr->SetBinError(ibin+1, RelErr);
    
    Chi2 += fabs(NmErr)>1e-9?(Nm-Nd)*(Nm-Nd)*1.0/(NmErr*NmErr):0.0;
    //===
      if(IfBlind==1){
       float x=BinXLow + (ibin+1)*(BinXHig-BinXLow)*1.0/BinTotal;
        //if( (x<87 && x>70) || (x> 93 && x<115) ) {
        if( (x<88 && x>70) || (x> 93 && x<116) ) {
	h_data->SetBinContent(ibin+1, 0.0);
	histoRatio->SetBinContent(ibin+1, 0.0);
      }
    }
     }
  cout<<"JTao: chi2 = "<<Chi2<<endl;


  h_data->SetLineColor(1);
  h_data->SetFillColor(0);
  h_data->SetLineStyle(1);
  h_data->SetLineWidth(2);
  h_data->GetXaxis()->SetTitle(XTitle.c_str());
  double WidthBin=(BinXHig-BinXLow)/BinTotal;
  //TString TitleY( Form("A.U. / %.2g GeV",WidthBin) );
  //TString TitleY( Form("No. of Entries in data / %.2g GeV",WidthBin) );
  //TString TitleY = "A.U";
  string PreTitleY( Form("Entries / %.2g ",WidthBin) );
  string TitleY =  PreTitleY + YUnit;
  h_data->GetYaxis()->SetTitle(TitleY.c_str());

  h_data->SetTitleSize(0.05,"X");
  h_data->SetTitleSize(0.06,"Y");
  //h_data->SetTitleOffset(1.3, "Y");
  h_data->SetTitleOffset(1.1, "Y");

  h_data->SetMarkerColor(kBlack);
  h_data->SetMarkerSize(1.0);
  h_data->SetMarkerStyle(20);
 
  h_MC->SetFillColor(kOrange+10);
  h_MC->SetLineColor(kOrange+10);
  h_MC->SetFillColor(kOrange+10); 
  h_MC->SetFillStyle(3244); //3001,3005
  h_MC->SetLineStyle(1);
  h_MC->SetLineWidth(2);
  h_MC->SetMarkerColor(17);

  h_MCErr->SetLineColor(kOrange+10);
  h_MCErr->SetLineStyle(1);
  h_MCErr->SetLineWidth(2);
  h_MCErr->SetFillColor(kOrange+10); //2
  h_MCErr->SetFillStyle(3244); //3001, 3005

  legend->AddEntry(h_data,"data","pe");

    hpp_MC->SetFillColor(2);
    hpp_MC->SetMarkerStyle(0);
    hpp_MC->SetLineColor(2);
    hpp_MC->SetLineStyle(1);
    hpp_MC->SetLineWidth(2);
    hpf_MC->SetFillColor(4);
    hpf_MC->SetMarkerStyle(0);
    hpf_MC->SetLineColor(4);
    hpf_MC->SetLineStyle(1);
    hpf_MC->SetLineWidth(2);

    hff_MC->SetFillColor(5);
    hff_MC->SetMarkerStyle(0);
    hff_MC->SetLineColor(5);
    hff_MC->SetLineStyle(1);
    hff_MC->SetLineWidth(2);
   
    legend->AddEntry(hpp_MC,"#gamma-#gamma","f");
    legend->AddEntry(hpf_MC,"#gamma-jet","f");
    legend->AddEntry(hff_MC,"jet-jet","f");
    legend->AddEntry(h_MC,"MC stat. unc.","f");
  
  gPad->SetTickx(1);
  gPad->SetTicky(1);
  gPad->SetLeftMargin(0.18);
  gPad->SetBottomMargin(0.15);
  gPad->SetTopMargin(0.05);
  gPad->SetRightMargin(0.05);

  c1->SetFrameBorderSize(0);
  c1->SetFrameBorderMode(0);
  h_data->GetXaxis()->SetLabelColor(0);
  h_data->SetNdivisions(510 ,"X");

  TLatex * tex1 = new TLatex(0.2,0.87, PrintInfor1); //0.88
  if(LegendLR==1) tex1 = new TLatex(0.65, 0.87, PrintInfor1);
  tex1->SetNDC();
  tex1->SetTextFont(42);
  tex1->SetTextSize(0.045);
  tex1->SetLineWidth(2);

  TLatex * tex2 = new TLatex(0.20,0.81, PrintInfor2); //0.82
  if(LegendLR==1)  tex2 = new TLatex(0.65,0.81, PrintInfor2); 
  tex2->SetNDC();
  tex2->SetTextFont(42);
  tex2->SetTextSize(0.045);
  tex2->SetLineWidth(2);

 
  string Prenameplots="DataMC_"+PlotName;

  if(IfMCSig == 1){
    Prenameplots="DataMCSig_"+PlotName;

    h_data->Draw("PE1");
    legend->Draw("same");
    h_MC->Draw("Histsame");

    tex1->Draw();
    tex2->Draw();
  }else{

    //prepare 2 pads
    const Int_t nx=1;
    const Int_t ny=2;
    const Double_t x1[2] = {0.0,0.0};
    const Double_t x2[2] = {1.0,1.0};
    //const Double_t y1[] = {1.0,0.3};
    //const Double_t y2[] = {0.3,0.00};
    const Double_t y1[2] = {0.3,0.0};
    const Double_t y2[2] = {1.0,0.3};
    Float_t psize[2];
    TPad *pad;
    const char *myname = "c";
    char *name2 = new char [strlen(myname)+6];
    Int_t n = 0;
    for (int iy=0;iy<ny;iy++) {
      for (int ix=0;ix<nx;ix++) {
	n++;
	sprintf(name2,"%s_%d",myname,n);
	if(ix==0){
	  gStyle->SetPadLeftMargin(.166);
	}else{
	  gStyle->SetPadLeftMargin(.002);
	  gStyle->SetPadTopMargin(.002);
	}

	if(iy==0){//upper
	  gStyle->SetPadTopMargin(0.05*(1./0.7)); // 0.05
	  gStyle->SetPadBottomMargin(.02);
	}
	if(iy==(ny-1)){//lower pad
	  gStyle->SetPadTopMargin(.05);
	  //gStyle->SetPadBottomMargin(.13*(1./0.3));
	  gStyle->SetPadBottomMargin(.40);


	}
	pad = new TPad(name2,name2,x1[ix],y1[iy],x2[ix],y2[iy]);
	pad->SetNumber(n);
	pad->Draw();
	psize[iy]=y1[iy]-y2[iy];
	//if(iy>0 )pad->SetGrid(kTRUE);
      }// end of loop over x
    }// end of loop over y
    delete [] name2;

    //===Drawing====

    c1->cd(1);
    gPad->SetLogy(IfLogY);
    gPad->SetLogx(IfLogX);
    gPad->SetTickx(1);
    gPad->SetTicky(1);
    //=========
    h_data->Draw("PE1");
    legend->Draw("same");
    if(IfMCSig != 1) hs->Draw("hist,same");
    h_MC->Draw("E2,same");
    h_data->Draw("samePE1");
    h_data->Draw("Axissame");

    tex1->Draw();
    tex2->Draw();

    ///====
    TLine *Line1 = new TLine(h_data->GetBinLowEdge(1),1,h_data->GetBinLowEdge(h_data->GetNbinsX())+ h_data->GetBinWidth(h_data->GetNbinsX()),1);
    Line1->SetLineColor(1);
    Line1->SetLineWidth(2);
    Line1->SetLineStyle(4);

    //TH1F *histoRatio = new TH1F(*h_data);
    //histoRatio->Divide(h_data, h_MC, 1., 1.);
    histoRatio->SetLineColor(1);
    histoRatio->SetLineStyle(1);
    histoRatio->SetLineWidth(2);
    histoRatio->SetMarkerColor(1);
    histoRatio->SetMarkerStyle(20);

    c1->cd(2);
    gPad->SetLogy(0);
    gPad->SetLogx(IfLogX);
    //gPad->SetLogx(0);
    histoRatio->SetTitleOffset(1,"X");
    histoRatio->SetTitleSize(0.12,"X");
    histoRatio->SetLabelSize(0.1,"X");
    histoRatio->GetXaxis()->SetTitle(XTitle.c_str());
    histoRatio->GetYaxis()->SetTitle("data/MC");
    //histoRatio->SetTitleOffset(0.5,"Y");
    histoRatio->SetTitleOffset(0.4,"Y");
    //histoRatio->SetTitleSize(0.12,"Y");
    histoRatio->SetTitleSize(0.14,"Y");
    histoRatio->SetLabelSize(0.1,"Y");
    histoRatio->SetLabelColor(1,"X");
    histoRatio->GetYaxis()->CenterTitle();
    //histoRatio->SetNdivisions(505 ,"Y");
    histoRatio->SetNdivisions(510 ,"X");

    gPad->SetTickx(1);
    gPad->SetTicky(1);
 
    histoRatio->GetXaxis()->SetTickLength(0.08);
    histoRatio->GetYaxis()->SetTickLength(0.06);
    histoRatio->GetYaxis()->SetNdivisions(503);
  
    histoRatio->SetMinimum(RYLow);
    histoRatio->SetMaximum(RYHig);
    histoRatio->Draw("PE1");
    h_MCErr->Draw("E2,same");
    histoRatio->Draw("samePE1");
    Line1->Draw("same");
  }

  //===================================
  string pngplots= Prenameplots + ".png";
  c1->Print(pngplots.c_str());

  string pdfplots= Prenameplots + ".pdf";
  c1->Print(pdfplots.c_str());
  //c1->Clear();
  //legend->Clear();
 
}


void DrawDataMCPlotsVar_2016Legacy(){

  gROOT->ProcessLine(".x hggPaperStyle.C");
  gStyle->SetOptStat(0);
  gStyle->SetOptFit(111);	

//void DrawMyPlots(string Object, string Selections,  string XTitle, string YUnit, string PlotName, int BinTotal, double BinXLow, double BinXHig, double RYLow, double RYHig, int LegendLR, int IfLogY, int IfBlind, int IfLogX=0){

  //All
  cout<<"============================All========================"<<endl;
  //string BasicSelections="(mass>93 && mass<98)";

  //string BasicSelections="(mass>65 && mass<120) && (result>-0.364 && result<0.334)";
  string BasicSelections="(mass>65 && mass<120)";// only for mass plot (for blinded) and for all the plots if Unblinded
  //string BasicSelections="(mass>65 && mass<70) || (mass>110 && mass<120)";//for all the plots except "mass" plot (for side bands) Blinded

//DrawMyPlots("mass", BasicSelections, "m_{#gamma#gamma} (GeV)", "GeV",  "Diphoton_Mass", 55, 65., 120., 0.5, 2.0, 0, 0, 1); //per 1GeV
//DrawMyPlots("mass", BasicSelections, "m_{#gamma#gamma} (GeV)", "GeV",  "Diphoton_Mass", 110, 65., 120., 0.5, 2.0, 0, 0, 1); // per 0.5 GeV

//Aamir Start Draw
//DrawMyPlots("mass", BasicSelections, "m_{#gamma#gamma} (GeV)", "GeV",  "Diphoton_Mass", 110, 65., 120., 0.5, 2.0, 0, 0, 1); // per 0.5 GeV //Blinded
//DrawMyPlots("mass", BasicSelections, "m_{#gamma#gamma} (GeV)", "GeV",  "Diphoton_Mass", 110, 65., 120., 0.5, 1.5, 0, 0, 0); // per 0.5 GeV //UnBlinded for mass
//DrawMyPlots("result", BasicSelections, "DiphotonBDT score ", "",  "DiphotonBDT_score", 50, -1., 1., 0., 2.0, 0, 0, 0);

//DrawMyPlots("result",  "DiphotonBDT score ", "",  "DiphotonBDT_score", 50, -1., 1., 0.5, 1.5, 0, 0, 0);
//DrawMyPlots("mass", "m_{#gamma#gamma} (GeV)", "GeV",  "Diphoton_Mass", 110, 65., 120., 0.5, 1.5, 0, 0, 0); // per 0.5 GeV
DrawMyPlots("result",  "DiphotonBDT score ", "",  "DiphotonBDT_score", 50, -1., 1., 0., 2.0, 0, 0);
DrawMyPlots("leadeta", "#eta^{(1)} ", "",  "leadeta", 60, -3., 3., 0., 2.0, 0, 0);
DrawMyPlots("subleadeta", "#eta^{(2)} ", "",  "subleadeta", 60, -3., 3., 0., 2.0, 0, 0);
DrawMyPlots("leadmva", "lead PhotonIDMVA ", "",  "leadmva", 50, -1., 1., 0., 2.0, 0, 0);
DrawMyPlots("subleadmva", "sublead PhotonIDMVA ", "",  "subleadmva", 50, -1., 1., 0., 2.0, 0, 0);
DrawMyPlots("leadptom", "P_T^{(1)}/M_{#gamma#gamma} ", "",  "leadPToM", 50, 0., 1., 0., 2.0, 0, 0);
DrawMyPlots("subleadptom", "P_T^{(2)}/M_{#gamma#gamma} ", "",  "subleadPToM", 50, 0., 1., 0., 2.0, 0, 0);
DrawMyPlots("vtxprob", "p_{vertex} ", "",  "pvertex", 50, 0., 1.0, 0., 2.0, 0, 0);

//DrawMyPlots("CosPhi", "Cos(#Delta #Phi) ", "",  "cosphi", 50, -1., 1., 0., 2.0, 0, 0);
DrawMyPlots("CosPhi", "Cos(#Delta #Phi) ", "",  "cosphi", 50, -1., 1., 0., 2.0, 0, 1); //for log plot
DrawMyPlots("sigmarv", "#sigma_{rv} ", "",  "sigmarv", 25, 0., 0.05, 0., 2.0, 0, 0);
DrawMyPlots("sigmawv", "#sigma_{wv} ", "",  "sigmawv", 25, 0., 0.05, 0., 2.0, 0, 0);


/*DrawMyPlots("mass", BasicSelections, "m_{#gamma#gamma} (GeV)", "GeV",  "Diphoton_Mgg_2017_untagged2_bin110", 110, 65., 120., 0.5, 2.0, 0, 0, 0);
DrawMyPlots("mass", BasicSelections, "m_{#gamma#gamma} (GeV)", "GeV",  "Diphoton_Mgg_2017_untagged2_bin55_blind", 55, 65., 120., 0.5, 2.0, 0, 0, 1);
 DrawMyPlots("mass", BasicSelections, "m_{#gamma#gamma} (GeV)", "GeV",  "Diphoton_Mgg_2017_untagged2_bin110_blind", 110, 65., 120., 0.5, 2.0, 0, 0, 1);*/
 //DrawMyPlots("mass", BasicSelections, "m_{#gamma#gamma} (GeV)", "GeV",  "Diphoton_Mgg_2017_test_bin110_lumi_93", 110, 65., 120., 0.5, 2.0, 0, 0, 0);
//DrawMyPlots("subleadptom", BasicSelections, " P_T^{(2)}/M_{#gamma#gamma} ", "",  "subleadptcut_2017_bins40_DataSideBands_test", 40, 0., 1., 0., 2.0, 0, 0, 1);
  //DrawMyPlots("bdtLow2017Pray", BasicSelections, "DiphotonBDT score Pray", "",  "DiphotonBDT_score_Pray", 100, -1., 1., 0., 2.0, 0, 0, 1);*/
/*  DrawMyPlots("result", BasicSelections, "DiphotonBDT score ", "",  "DiphotonBDT_score_2017_unblinded_lumi_9.", 50, -1., 1., 0., 2.0, 0, 0, 1);
  DrawMyPlots("leadeta", BasicSelections, "#eta^{(1)} ", "",  "leadeta_2017_bins60_unblinded_lumi_9.", 60, -3., 3., 0., 2.0, 0, 0, 1);
  DrawMyPlots("subleadeta", BasicSelections, "#eta^{(2)} ", "",  "subleadeta_2017_bins60_unblinded_lumi_9.", 60, -3., 3., 0., 2.0, 0, 0, 1);
  DrawMyPlots("leadmva", BasicSelections, "lead PhotonIDMVA ", "",  "leadmva_2017_bins50_unblinded_lumi_9.", 50, -1., 1., 0., 2.0, 0, 0, 1);
  DrawMyPlots("subleadmva", BasicSelections, "sublead PhotonIDMVA ", "",  "subleadmva_2017_bins50_unblinded_lumi_9.", 50, -1., 1., 0., 2.0, 0, 0, 1);
  DrawMyPlots("leadptom", BasicSelections, "P_T^{(1)}/M_{#gamma#gamma} ", "",  "leadptcut_2017_bins50_unblinded_lumi_9.", 50, 0., 1., 0., 2.0, 0, 0, 1);
  DrawMyPlots("subleadptom", BasicSelections, " P_T^{(2)}/M_{#gamma#gamma} ", "",  "subleadptcut_2017_bins20_unblinded_lumi_9.", 20, 0.2, 0.6, 0., 2.0, 0, 0, 1);
  DrawMyPlots("vtxprob", BasicSelections, "p_{vertex} ", "",  "pvertex_2017_bins50_unblinded_lumi_9.", 50, 0., 1.0, 0., 2.0, 0, 0, 1);
  DrawMyPlots("CosPhi", BasicSelections, "Cos(#Delta #Phi) ", "",  "cosphi_2017_bins50_unblinded_lumi_9.", 50, -1., 1., 0., 2.0, 0, 1, 1);
  DrawMyPlots("sigmarv", BasicSelections, "#sigma_{rv} ", "",  "sigmarv_2017_bins50_unblinded_lumi_9.", 50, 0., 0.05, 0., 2.0, 0, 0, 1);
  DrawMyPlots("sigmawv", BasicSelections, "#sigma_{wv} ", "",  "sigmawv_2017_bins50_unblinded_lumi_9.", 50, 0., 0.05, 0., 2.0, 0, 0, 1);
*/
}
