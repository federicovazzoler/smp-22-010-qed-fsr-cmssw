BASE_DIR="/nfs/dust/cms/user/vazzolef/smp-22-010/qed-fsr-CMSSW/CMSSW_10_6_32_patch1/src/Configuration/smp-22-010-qed-fsr-cmssw/"

../scripts/create_condor_dag.py --dagman_area ${BASE_DIR}/condor_area/ZToEE__customLHE__Pythia8_no_MPI__NanoGEN \
                                --input_lhe_folder /pnfs/desy.de/cms/tier2/store/user/fvazzole/powheg/crab_ZToEE_NLOQCD_LOEW__1_1000/ \
                                --cmsrun_config ${BASE_DIR}/configs/customLHE__Pythia8_no_MPI__NanoGEN.py \
                                --stageout_dir davs://eoscms.cern.ch:443/eos/cms/store/group/phys_smp/ec/sin2O/FSR_studies/ZToEE/FSR_OFF \
                                --submit_job

../scripts/create_condor_dag.py --dagman_area ${BASE_DIR}/condor_area/ZToEE__customLHE__Pythia8_no_MPI_Photos__NanoGEN \
                                --input_lhe_folder /pnfs/desy.de/cms/tier2/store/user/fvazzole/powheg/crab_ZToEE_NLOQCD_LOEW__1_1000/ \
                                --cmsrun_config ${BASE_DIR}/configs/customLHE__Pythia8_no_MPI_Photos__NanoGEN.py \
                                --stageout_dir davs://eoscms.cern.ch:443/eos/cms/store/group/phys_smp/ec/sin2O/FSR_studies/ZToEE/PHOTOS_FSR \
                                --submit_job


../scripts/create_condor_dag.py --dagman_area ${BASE_DIR}/condor_area/ZToEE__customLHE__Pythia8_no_MPI_Photos_MEC_off__NanoGEN \
                                --input_lhe_folder /pnfs/desy.de/cms/tier2/store/user/fvazzole/powheg/crab_ZToEE_NLOQCD_LOEW__1_1000/ \
                                --cmsrun_config ${BASE_DIR}/configs/customLHE__Pythia8_no_MPI_Photos_MEC_off__NanoGEN.py \
                                --stageout_dir davs://eoscms.cern.ch:443/eos/cms/store/group/phys_smp/ec/sin2O/FSR_studies/ZToEE/FSR_PHOTOS_MEC_OFF \
                                --submit_job


../scripts/create_condor_dag.py --dagman_area ${BASE_DIR}/condor_area/ZToEE__customLHE__Pythia8_no_MPI_PythiaQED_alphaEMorder_0__NanoGEN \
                                --input_lhe_folder /pnfs/desy.de/cms/tier2/store/user/fvazzole/powheg/crab_ZToEE_NLOQCD_LOEW__1_1000/ \
                                --cmsrun_config ${BASE_DIR}/configs/customLHE__Pythia8_no_MPI_PythiaQED_alphaEMorder_0__NanoGEN.py \
                                --stageout_dir davs://eoscms.cern.ch:443/eos/cms/store/group/phys_smp/ec/sin2O/FSR_studies/ZToEE/FSR_PYTHIA_alphaEMorder_0 \
                                --submit_job
