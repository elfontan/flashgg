from ROOT import *
from array import array

# Obtain spline from smoothed histogram
file_minID = TFile("minid_gjetqcd40.root", "READ")
h_minID = file_minID.Get("bkg0")
print h_minID.Integral(0,4)
print h_minID.Integral()
h_minID.GetXaxis().SetRangeUser(-0.9,0.8)
h_minID.Smooth(1, "R")

spline_x = array('f')
spline_y = array('f')
fakePDF = TSpline3(h_minID)

#for j in range(0,1901):
#  nbin = -0.9+(0.001*j)
#  eval = fakePDF.Eval(nbin)
#  spline_x.append(nbin)
#  spline_y.append(eval)
#  print j, eval

check_spline = fakePDF.Eval(0.633)
print "Spline Eval at 0.633: ",check_spline

fakePDF.SaveAs("fake.C");
gROOT.LoadMacro("fake.C++");
fakePDF_reweight = TF1("fakePDF_reweight", "fake(x)",-0.9,1.0)

print "Max Reweight: ",fakePDF_reweight.Integral(-0.7,1.0,0.000001)/fakePDF_reweight.Integral(-0.9,-0.7,0.000001)
print "Max Numerator: ",fakePDF_reweight.Integral(-0.7,1.0,0.000001)
print "Demonimator: ",fakePDF_reweight.Integral(-0.9,-0.7,0.000001)
print "1/Demonimator: ",1.0/fakePDF_reweight.Integral(-0.9,-0.7,0.000001)
