python3 addMassHypothesis.py
python3 plotMassHypothesis_noWSig.py --log True --outdir /eos/user/e/elfontan/www/Hgg_veryLowMass_AN/inputPreparation/MassHyp/Oct2024_flattenedBkg 
python3 plotMassHypothesis.py --log True --outdir /eos/user/e/elfontan/www/Hgg_veryLowMass_AN/inputPreparation/MassHyp/Oct2024_flattenedBkg
python3 addMassHypothesisWeights.py
python3 plotMassHypothesisWeights_noWSig.py  --outdir /eos/user/e/elfontan/www/Hgg_veryLowMass_AN/inputPreparation/MassHyp/Oct2024_flattenedBkg
python3 plotMassHypothesisWeights.py --outdir /eos/user/e/elfontan/www/Hgg_veryLowMass_AN/inputPreparation/MassHyp/Oct2024_flattenedBkg
python3 addMassHypothesisNorms.py
python3 plotMassHypothesisNorms_noWSig.py  --outdir /eos/user/e/elfontan/www/Hgg_veryLowMass_AN/inputPreparation/MassHyp/Oct2024_flattenedBkg
python3 plotMassHypothesisNorms.py  --outdir /eos/user/e/elfontan/www/Hgg_veryLowMass_AN/inputPreparation/MassHyp/Oct2024_flattenedBkg
python3 addMassHypothesisSigNorms.py
python3 addMassHypothesisBkgNorms.py
hadd output_ParaDDFullSigBkgNorms.root output_ParaDDFullSigNorms.root output_ParaDDFullBkgNorms.root
python3 plotMassHypothesisBkgNorms_noWSig.py  --outdir /eos/user/e/elfontan/www/Hgg_veryLowMass_AN/inputPreparation/MassHyp/Oct2024_flattenedBkg
python3 plotMassHypothesisBkgNorms.py  --outdir /eos/user/e/elfontan/www/Hgg_veryLowMass_AN/inputPreparation/MassHyp/Oct2024_flattenedBkg
