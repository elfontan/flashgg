# ---------------- #
# Likelihood scans #
# ---------------- #
# python3 compPlot_LLscan.py  --s1 higgsCombineDefault.MultiDimFit.mH50.root --s2 higgsCombineShapeBkg.MultiDimFit.mH50.root  --output /eos/user/e/elfontan/www/Hgg_veryLowMass_AN/Syst/LikelihoodScan/ -- m 50 --c 1 --input nuisanceStudies/M50/cat1
# -------------------------------------------------------------------------------------------------------------------------- #

#!/bin/bash

# Define arrays for masses and categories
masses=(30 50 70)
categories=(0 1 01)

# Base output directory
base_output_dir="/eos/user/e/elfontan/www/Hgg_veryLowMass_AN/Syst/LikelihoodScan/"

# Define the different s2 options
s2_options=(
  #"higgsCombineTheory.MultiDimFit"
  #"higgsCombineExperimental.MultiDimFit"
  #"higgsCombineAllConstrainedNuisances.MultiDimFit"
  "higgsCombineAll.MultiDimFit"
  #"higgsCombineShapeBkg.MultiDimFit"
)

# Loop over each mass
for mass in "${masses[@]}"; do
  # Loop over each category
  for category in "${categories[@]}"; do
    # Define input directory based on mass and category
    input_dir="/afs/cern.ch/work/e/elfontan/private/DiPhotonAnalysis/StatisticalAnalysis/CMSSW_11_3_4/src/Combine/SlidingWindows/LikelihoodScan/nuisanceStudies/M${mass}/cat${category}/"

    # Loop over each s2 option
    for s2 in "${s2_options[@]}"; do
      # Construct the s1 and s2 filenames with the current mass
      s1_file="higgsCombineDefault.MultiDimFit.mH${mass}.root"
      s2_file="${s2}.mH${mass}.root"

      # Execute the Python script with the current parameters
      python3 compPlot_LLscan.py \
        --s1 "${s1_file}" \
        --s2 "${s2_file}" \
        --output "${base_output_dir}/" \
        --m "${mass}" \
        --c "${category}" \
        --input "${input_dir}"
    done
  done
done

