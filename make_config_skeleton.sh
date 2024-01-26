#! /bin/bash

fragment=$(basename ${1})

customize="--customise_commands process.genWeightsTable.maxPdfWeights=1000"

mkdir -p configs
cmsenv
cmsDriver.py Configuration/smp-22-010-qed-fsr-cmssw/python/$(basename ${fragment}) \
             --fileout file:output.root \
             --mc \
             --eventcontent NANOAODSIM \
             --datatier NANOAOD \
             --conditions auto:mc \
             --step GEN,NANOGEN \
             --python_filename configs/${fragment%.*}.py \
             --filein /store/user/fvazzole/powheg/crab___1_100/240125_103331/0000/events_31.lhe \
             $customize \
             -n -1 \
             --no_exec
