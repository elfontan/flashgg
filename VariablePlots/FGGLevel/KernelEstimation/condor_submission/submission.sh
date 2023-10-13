#!/bin/bash

for i in {1..10000}; do
    condor_submit /afs/cern.ch/work/e/elfontan/private/DiPhotonAnalysis/Sep2023_flashGG/CMSSW_12_6_5/src/condor_submission/submit_job.submit i
done
