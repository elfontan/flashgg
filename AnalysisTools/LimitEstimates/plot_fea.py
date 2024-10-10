###################################################################################
# Paper plots HIG-24-014: efficiency x acceptance plots with spline, per category #
# ------------------------------------------------------------------------------- #
#python3 plot_fea.py --w ws_sig/CMS-HGG_sigfit_LMAnalysis_Jul2024_newSignalNtuples_4Cat_gghSyst_2018_GG2H_2018_UntaggedTag_1.root --c 1 --o /eos/user/e/elfontan/www/Hgg_veryLowMass_AN/SignalModeling/SYST/EffAcc/

import ROOT
from ROOT import TLatex
import mplhep as hep
import argparse
import numpy as np
import matplotlib.pyplot as plt

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
def plot_spline(mhs, vals, cat):
    plt.style.use(hep.style.ROOT)
    fig, ax = plt.subplots(figsize=(10, 8))
    plt.scatter(mhs, vals, color='dodgerblue'if cat == '0' else 'coral' if cat == '1' else 'hotpink', marker='*', label=rf'$\epsilon \times \it{{A}}$ (Category {cat[-1]})') #s=30
    plt.plot(mhs, vals, linestyle='-', color='royalblue'if cat == '0' else 'darkorange' if cat == '1' else 'mediumvioletred', label='Spline fit') #royalblue

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
    plt.savefig(f"{outdir}/feaSpline_cat{cat}.png")
    plt.savefig(f"{outdir}/feaSpline_cat{cat}.pdf")
    plt.clf()

# Loading the workspace
f = ROOT.TFile(wFile, "read")
w = f.Get("wsig_13TeV")

# Define mass range (10 to 70 GeV)
mhs = np.arange(10.0, 70.1, 1.0)
vals = []

# Extract values from the workspace
for mh in mhs:
    w.var("MH").setVal(mh)
    spline_name = f"fea_GG2H_2018_UntaggedTag_{cat[-1]}_13TeV"
    vals.append(w.function(spline_name).getVal())

# Plot the results
plot_spline(mhs, vals, cat)
