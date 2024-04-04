#include "RooRealVar.h"
#include "RooConstVar.h"
#include "RooArgList.h"
#include "RooDataSet.h"
#include "RooDataHist.h"
#include "RooHistPdf.h"
#include "RooGaussian.h"
#include "RooPolynomial.h"
#include "RooKeysPdf.h"
#include "RooNDKeysPdf.h"
#include "RooProdPdf.h"
#include "RooWorkspace.h"
#include "TCanvas.h"
#include "TAxis.h"
#include "TLegend.h"
#include "TH1.h"
#include "RooPlot.h"
#include <TROOT.h> 
#include <iostream>
#include <vector>
#include <string>

using namespace RooFit;
 
void histoBased_binsPhoIdMinMax_kest_pfFilter()
{
  // ------------------
  // Inputs and outputs
  // ------------------
  TFile* file = NULL;
  const std::string& indir ="./";
  const std::string& outdir ="/eos/user/e/elfontan/www/Hgg_veryLowMass_AN/paramNN/";

  // List of file paths
  // ------------------
  std::vector<std::string> file_paths = {
					 indir+"newSandS_gjAll_Inclusive.root"					 
  };

  // Create workspace to save all pdfs
  // ----------------------------------------------------                                                              
  RooWorkspace w_MinMaxPhoId("w_MinMaxPhoId", "");

  for (size_t i = 0; i < file_paths.size(); ++i) {
        const std::string& filename = file_paths[i];

        TFile* file = TFile::Open(filename.c_str(), "READ");
        if (!file || file->IsZombie()) {
            std::cerr << "Error: Unable to open the ROOT file: " << filename << std::endl;
          }
	std::cout << "File: " << filename << std::endl;
  
	TH1F* h_minIDMVA = new TH1F("h_minIDMVA", "h_minIDMVA", 38, -0.9, 1);
	h_minIDMVA = (TH1F*)file->Get("gjAll");
      
	// ----------------------------------------------------                                                           
	// Generating a fake pdf for each maximum photon ID bin                                                              
	// ----------------------------------------------------                                                              
	RooRealVar dipho_minIDMVA("dipho_minIDMVA", "dipho_minIDMVA", -0.9, 1);
	dipho_minIDMVA.setBins(38);
	
	// Binned data can be imported from ROOT THx histograms                                      
	// ----------------------------------------------------                                                
	std::string histoname = "h_dipho_minIDMVA_" + std::to_string(i);
	RooDataHist* h_dipho_minIDMVA = new RooDataHist(histoname.c_str(), histoname.c_str(), RooArgList(dipho_minIDMVA), h_minIDMVA);
	
	// Create a RooDataSet from the RooDataHist
	// ----------------------------------------
	std::string datasetname = "data_dipho_minIDMVA_" + std::to_string(i);
	RooDataSet* data_dipho_minIDMVA = new RooDataSet(datasetname.c_str(), datasetname.c_str(), RooArgList(dipho_minIDMVA));
	
	for (int bin = 1; bin <= h_minIDMVA->GetNbinsX(); ++bin) {
	  // Get the bin content and center
	  double bin_content = h_minIDMVA->GetBinContent(bin);
	  double bin_center = h_minIDMVA->GetBinCenter(bin);
	  
	  // Fill the RooDataSet with entries from this bin
	  for (int entry = 0; entry < bin_content; ++entry) {
	    dipho_minIDMVA.setVal(bin_center);
	    data_dipho_minIDMVA->add(dipho_minIDMVA); 
	  }
	}
  
	//RooPlot *frame0 = dipho_minIDMVA.frame(Title(""));
	RooPlot *frame0 = dipho_minIDMVA.frame(Title("Minimum photon ID (1D fake PDF)"));
	data_dipho_minIDMVA->plotOn(frame0);

	std::string f_name_ML = "kestML_minPhoId_" + std::to_string(i);
	std::string f_name_ML2 = "kestML2_minPhoId_" + std::to_string(i);
	std::string f_name_ML1p8 = "kestML1p8_minPhoId_" + std::to_string(i);
	std::string f_name_ML1p5 = "kestML1p5_minPhoId_" + std::to_string(i);
	std::string f_name_ML1p2 = "kestML1p2_minPhoId_" + std::to_string(i);
	std::string f_name_ML0p8 = "kestML0p8_minPhoId_" + std::to_string(i);
	std::string f_name_ML0p5 = "kestML0p5_minPhoId_" + std::to_string(i);
	std::string f_name_ML0p3 = "kestML0p3_minPhoId_" + std::to_string(i);

	RooKeysPdf kestML_minPhoId(f_name_ML.c_str(), f_name_ML.c_str(), dipho_minIDMVA, *data_dipho_minIDMVA, RooKeysPdf::MirrorLeft);
	//kestML_minPhoId.plotOn(frame0, LineWidth(3), LineStyle(kDashed), LineColor(kViolet+6));
	RooKeysPdf kestML0p3_minPhoId(f_name_ML0p3.c_str(), f_name_ML0p3.c_str(), dipho_minIDMVA, *data_dipho_minIDMVA, RooKeysPdf::MirrorLeft, 0.3);
	////kestML0p3_minPhoId.plotOn(frame0, LineWidth(3), LineStyle(kDashed), LineColor(kGreen-2));
	RooKeysPdf kestML0p5_minPhoId(f_name_ML0p5.c_str(), f_name_ML0p5.c_str(), dipho_minIDMVA, *data_dipho_minIDMVA, RooKeysPdf::MirrorLeft, 0.5);
	////kestML0p5_minPhoId.plotOn(frame0, LineWidth(2), LineColor(kCyan+2));
	RooKeysPdf kestML0p8_minPhoId(f_name_ML0p8.c_str(), f_name_ML0p8.c_str(), dipho_minIDMVA, *data_dipho_minIDMVA, RooKeysPdf::MirrorLeft, 0.8);
	//kestML0p8_minPhoId.plotOn(frame0, LineWidth(2), LineColor(kOrange-3));
	RooKeysPdf kestML1p2_minPhoId(f_name_ML1p2.c_str(), f_name_ML1p2.c_str(), dipho_minIDMVA, *data_dipho_minIDMVA, RooKeysPdf::MirrorLeft, 1.2);
	kestML1p2_minPhoId.plotOn(frame0, LineWidth(2), LineColor(kMagenta-9));
	RooKeysPdf kestML1p5_minPhoId(f_name_ML1p5.c_str(), f_name_ML1p5.c_str(), dipho_minIDMVA, *data_dipho_minIDMVA, RooKeysPdf::MirrorLeft, 1.5);
	//kestML1p5_minPhoId.plotOn(frame0, LineWidth(3), LineColor(kAzure-4));
	RooKeysPdf kestML1p8_minPhoId(f_name_ML1p8.c_str(), f_name_ML1p8.c_str(), dipho_minIDMVA, *data_dipho_minIDMVA, RooKeysPdf::MirrorLeft, 1.8);
	//kestML1p8_minPhoId.plotOn(frame0, LineWidth(2), LineColor(kCyan+2));
	RooKeysPdf kestML2_minPhoId(f_name_ML2.c_str(), f_name_ML2.c_str(), dipho_minIDMVA, *data_dipho_minIDMVA, RooKeysPdf::MirrorLeft, 2);
	//kestML2_minPhoId.plotOn(frame0, LineWidth(3), LineStyle(kDashed), LineColor(kRed-4));
	
	
	std::string c_name = "phoIdMin_kest_" + std::to_string(i);
	TCanvas *c_min = new TCanvas(c_name.c_str(), c_name.c_str(), 1200, 1000);
	c_min->cd();
	c_min->SetLeftMargin(2.5);

	frame0->SetTitle("");
	frame0->GetYaxis()->SetTitleOffset(1.4);
	frame0->GetXaxis()->SetTitle("Minimum #gamma ID");
	frame0->Draw();

	TLatex *latex2 = new TLatex();
	latex2->SetNDC();
	latex2->SetTextSize(0.4*c_min->GetTopMargin());
	latex2->SetTextFont(42);
	latex2->SetTextAlign(31);// # align right                                                                                          
	latex2->DrawLatex(0.9, 0.92,"13 TeV");
	//latex2->DrawLatex(0.9, 0.92,"96.6 fb^{-1} (13 TeV)");                                                                  
	latex2->SetTextSize(0.55*c_min->GetTopMargin());
	latex2->SetTextFont(62);
	latex2->SetTextAlign(11);// # align right                                                                                        
	latex2->DrawLatex(0.11, 0.92, "CMS"); // Out of the canvas                                                                       
	latex2->SetTextFont(42);
	latex2->SetTextSize(0.4*c_min->GetTopMargin());
	latex2->DrawLatex(0.2, 0.92, "Simulation Preliminary"); // Out of the canvas                                                        
	//latex2->DrawLatex(0.18, 0.82, "CMS"); //NORM                                                                        
	latex2->SetTextSize(0.5*c_min->GetTopMargin());
	latex2->SetTextFont(52);
	latex2->SetTextAlign(11);

	TLegend *leg_min = new TLegend(0.2,0.6,0.8,0.88);
	leg_min->SetFillColor(kWhite);
	leg_min->SetLineColor(kWhite);
	//TLegendEntry *entry0 = leg_min->AddEntry("kestML_minPhoId","Kernel estimation: mirror left","L");
	//entry0->SetLineColor(kViolet+6);
	//TLegendEntry *entry1 = leg_min->AddEntry("kestML0p8_minPhoId","Kernel estimation: mirror left, bw 0.8","L");
	//entry1->SetLineColor(kOrange-3);
	TLegendEntry *entry2 = leg_min->AddEntry("kestML1p2_minPhoId","Kernel estimation: mirror left, bw 1.2","L");
	entry2->SetLineColor(kMagenta-9);
	//TLegendEntry *entry3 = leg_min->AddEntry("kestML1p5_minPhoId","Kernel estimation: mirror left, bw 1.5","L");
	//entry3->SetLineColor(kAzure-4);
	//TLegendEntry *entry4 = leg_min->AddEntry("kestML1p8_minPhoId","Kernel estimation: mirror left, bw 1.8","L");
	//entry4->SetLineColor(kCyan+2);
	//TLegendEntry *entry5 = leg_min->AddEntry("kestML2_minPhoId","Kernel estimation: mirror left, bw 2","L");
	//entry5->SetLineColor(kRed-4);
	//TLegendEntry *entry7 = leg_min->AddEntry("kestML0p3_minPhoId","Kernel estimation: mirror left, bw 0.3","L");
	//entry7->SetLineColor(kGreen-2);
	  
	leg_min->Draw("same");
	std::string png_name = outdir+"fakePdf_gJets_all_ML1p2.png";
	std::string pdf_name = outdir+"fakePdf_gJets_all_ML1p2.pdf";
	std::string root_name = outdir+"fakePdf_gJets_all_ML1p2.root";
	//std::string png_name = outdir+"fakePdf_MaxPhoId_"+std::to_string(i)+"_ML1p2.png";
	c_min->SaveAs(png_name.c_str());  
	c_min->SaveAs(pdf_name.c_str());  
	c_min->SaveAs(root_name.c_str());  
	
	//------------------------
	// Save into ROOWorkspace
	//------------------------
	w_MinMaxPhoId.import(*data_dipho_minIDMVA);
	w_MinMaxPhoId.import(*h_dipho_minIDMVA);
	w_MinMaxPhoId.import(kestML_minPhoId);
	w_MinMaxPhoId.import(kestML0p3_minPhoId);
	w_MinMaxPhoId.import(kestML0p5_minPhoId);
	w_MinMaxPhoId.import(kestML0p8_minPhoId);
	w_MinMaxPhoId.import(kestML1p2_minPhoId);
	w_MinMaxPhoId.import(kestML1p5_minPhoId);
	w_MinMaxPhoId.import(kestML1p8_minPhoId);
	w_MinMaxPhoId.import(kestML2_minPhoId);
	//w_MinMaxPhoId.writeToFile(Form("KernelEstimation/w_ML_maxPhoId_%s_%s.root", min_maxPhoIdStr.c_str(), max_maxPhoIdStr.c_str()));
  }
  w_MinMaxPhoId.writeToFile("./test.root");
  //w_MinMaxPhoId.writeToFile("./w_newSandS_gjAll_Inclusive.root");

}

