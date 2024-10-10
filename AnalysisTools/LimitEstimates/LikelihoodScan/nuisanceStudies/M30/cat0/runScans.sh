combine m30_cat0.root  -M MultiDimFit --algo grid -t -1 --setParameters r=0.5 --points 1000 --setParameterRanges r=-3,3 -m 30 --freezeParameters MH --X-rtd MINIMIZER_freezeDisassociatedParams  --cminDefaultMinimizerStrategy 0 -n Default
combine m30_cat0.root  -M MultiDimFit --algo grid -t -1 --setParameters r=0.5 --points 1000 --setParameterRanges r=-3,3 -m 30 --freezeParameters MH,allConstrainedNuisances --X-rtd MINIMIZER_freezeDisassociatedParams  --cminDefaultMinimizerStrategy 0 -n AllConstrainedNuisances
combine m30_cat0.root  -M MultiDimFit --algo grid -t -1 --setParameters r=0.5 --points 1000 --setParameterRanges r=-3,3 -m 30 --freezeParameters MH --X-rtd MINIMIZER_freezeDisassociatedParams  --cminDefaultMinimizerStrategy 0 --freezeNuisanceGroups=theory  -n Theory
combine m30_cat0.root  -M MultiDimFit --algo grid -t -1 --setParameters r=0.5 --points 1000 --setParameterRanges r=-3,3 -m 30 --freezeParameters MH --X-rtd MINIMIZER_freezeDisassociatedParams  --cminDefaultMinimizerStrategy 0 --freezeNuisanceGroups=exp  -n Experimental
combine m30_cat0.root  -M MultiDimFit --algo grid -t -1 --setParameters r=0.5 --points 1000 --setParameterRanges r=-4,4 -m 30 --freezeParameters MH,allConstrainedNuisances,rgx{model_UntaggedTag.*} --X-rtd MINIMIZER_freezeDisassociatedParams  --cminDefaultMinimizerStrategy 0 -n ShapeBkg
combine m30_cat0.root  -M MultiDimFit --algo grid -t -1 --setParameters r=0.5 --points 1000 --setParameterRanges r=-4,4 -m 30 --freezeParameters MH,allConstrainedNuisances,rgx{model_UntaggedTag.*} --X-rtd MINIMIZER_freezeDisassociatedParams --freezeNuisanceGroups=theory,exp --cminDefaultMinimizerStrategy 0 -n All
