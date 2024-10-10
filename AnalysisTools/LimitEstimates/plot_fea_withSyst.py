###################################################################################
# Paper plots HIG-24-014: efficiency x acceptance plots with spline, per category #
# ------------------------------------------------------------------------------- #
#python3 plot_fea_withSyst.py --w ws_sig/CMS-HGG_sigfit_LMAnalysis_Jul2024_newSignalNtuplesNoNNLOPS_4Cat_gghSystFixed_2018_GG2H_2018_UntaggedTag_0.root  --c 0 --o /eos/user/e/elfontan/www/Hgg_veryLowMass_Paper

import ROOT
from ROOT import TLatex
import mplhep as hep
import argparse
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import CubicSpline

# Argument parsing
argparser = argparse.ArgumentParser(description='Parser used for non-default arguments', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
argparser.add_argument('--o', dest='o', default='./', help='Output directory')
argparser.add_argument('--c', dest='c', default='0', help='Category')
argparser.add_argument('--w', dest='w', default='ws_sig/CMS-HGG_sigfit_LMAnalysis_Jul2024_newSignalNtuples_4Cat_gghSyst_2018_GG2H_2018_UntaggedTag_0.root', help='Workspace')
args = argparser.parse_args()

outdir = args.o
cat = args.c
wFile = args.w

# Plotting function
def plot_spline(mhs, vals, cat, unc_spline):
    plt.style.use(hep.style.ROOT)
    fig, ax = plt.subplots(figsize=(10, 8))
    plt.scatter(mhs, vals, color='dodgerblue'if cat == '0' else 'coral' if cat == '1' else 'hotpink', marker='*', label=rf'$\epsilon \times \it{{A}}$ (Category {cat[-1]})') #s=30
    plt.plot(mhs, vals, linestyle='-', color='royalblue'if cat == '0' else 'darkorange' if cat == '1' else 'mediumvioletred', label='Spline fit') #royalblue

    # Compute the uncertainty band using the interpolated spline
    unc_vals = unc_spline(mhs)  # Get interpolated uncertainty values
    upper_bound = np.array(vals) + np.array(vals)*unc_vals/100
    lower_bound = np.array(vals) - np.array(vals)*unc_vals/100
    plt.fill_between(mhs, lower_bound, upper_bound, color='lightblue' if cat == '0' else 'lightcoral', alpha=0.5, label='Stat + Syst Unc.')

    # Setting axis labels and styles
    plt.xlabel(r"$m_{\gamma\gamma}$ [GeV]", fontsize=20)
    plt.ylabel("Efficiency x Acceptance [%]", fontsize=20)
    plt.yscale('linear')
    plt.ylim(bottom=-0.001)  
    #plt.grid(True, which='both', linestyle='--', linewidth=0.7)
    plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(lambda y, _: f'{y:.2e}')) 
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{x*100:.1f}'))                                                                                                                                   
    plt.subplots_adjust(left=0.15)  # Increased left margin

    # LaTeX annotation in the middle left
    #ax.text(0.04, 0.65, r'ggH MC ($\sigma = 1.0$, $\bf{\it{B}}$ = 100%)', fontsize=20, transform=ax.transAxes)

    # CMS label and category title
    hep.cms.text("Simulation Preliminary", loc=1)
    plt.title("2018 (13 TeV)", fontsize=22, loc='right')
    plt.legend(loc='center left', fontsize=20)
    #plt.legend(loc='lower right', fontsize=20)

    # Save the plots
    plt.savefig(f"{outdir}/feaSpline_cat{cat}_withSyst.png")
    plt.savefig(f"{outdir}/feaSpline_cat{cat}_withSyst.pdf")
    plt.clf()

# Loading the workspace
f = ROOT.TFile(wFile, "read")
w = f.Get("wsig_13TeV")

# Define mass range (10 to 70 GeV)
mhs = np.arange(10.0, 70.1, 1.0)
vals = []
masses = np.arange(10.0, 71.0, 5.0)
unc_cat0 = [8.69284669,6.91090644,7.61534648,7.0770571,6.47592256,6.57288112,6.49109399,6.6252041, 6.75470791,6.86760496,6.6694015 ,6.85669351, 7.58313381]
unc_cat1 = [6.24933697, 6.37726385, 6.35770551, 5.44307097, 7.54514615, 5.98024342, 7.0014903,  6.24873493, 8.83326622, 7.495286,   7.45359288, 7.27068053, 6.90740913]

# Interpolating the uncertainties using cubic spline
if cat == '0':
    unc_spline_cat0 = CubicSpline(masses, unc_cat0)
elif cat == '1':
    unc_spline_cat1 = CubicSpline(masses, unc_cat1)

# Extract values from the workspace
for mh in mhs:
    w.var("MH").setVal(mh)
    spline_name = f"fea_GG2H_2018_UntaggedTag_{cat[-1]}_13TeV"
    vals.append(w.function(spline_name).getVal())

# Plot the results
if cat == '0':
    plot_spline(mhs, vals, cat, unc_spline_cat0)
elif cat == '1':
    plot_spline(mhs, vals, cat, unc_spline_cat1)
