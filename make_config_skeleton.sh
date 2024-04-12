#! /bin/bash

fragment=$(basename ${1})

customize_commands="--customise_commands process.genWeightsTable.maxPdfWeights=1000"
filename=configs/${fragment%.*}.py
pruner=""
if [ "${2}" == "pruned" ]; then
   pruner="--customise PhysicsTools/NanoAOD/nanogen_cff.pruneGenParticlesNano,PhysicsTools/NanoAOD/nanogen_cff.setGenFullPrecision"
   filename=configs/${fragment%.*}_pruned.py
fi

mkdir -p configs
cmsenv
cmsDriver.py Configuration/smp-22-010-qed-fsr-cmssw/python/$(basename ${fragment}) \
             --fileout file:output.root \
             --mc \
             --eventcontent NANOAODSIM \
             --datatier NANOAOD \
             --conditions auto:mc \
             --step GEN,NANOGEN \
             --python_filename ${filename} \
             --filein /store/user/fvazzole/powheg/crab___1_100/240125_103331/0000/events_31.lhe \
             $customize_commands \
             $pruner \
             -n -1 \
             --no_exec
