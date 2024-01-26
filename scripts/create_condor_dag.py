#!/bin/python3

import os
import argparse
import subprocess
import re

#CERN_EOS_SITEPATH = "davs://eoscms.cern.ch:443/"

def extract_seed_from_filename(file):
  pattern = r'events_(\d+)\.root'
  match = re.search(pattern, file)
  if match:
    return match.group(1)
  else:
    raise Exception(f"No seed found for {file}")

def create_condor_submit_file(dagman_area, cmsrun_config, input_file, output_file, seed):
  condor_submit_file_dir = os.path.join(dagman_area, f"job_{seed}") 
  os.makedirs(condor_submit_file_dir, exist_ok=False)

  condor_submit_file = os.path.join(condor_submit_file_dir, "job.sub")
  with open(condor_submit_file, 'w') as f:
      f.write(f"executable = /nfs/dust/cms/user/vazzolef/smp-22-010/qed-fsr-CMSSW/CMSSW_10_6_32_patch1/src/Configuration/smp-22-010-qed-fsr-cmssw/scripts/condor_run.sh\n")
      f.write(f"arguments = \"{cmsrun_config} {input_file} {output_file} {seed}\"\n")
      f.write(f"output = {condor_submit_file_dir}/job.out\n")
      f.write(f"error = {condor_submit_file_dir}/job.err\n")
      f.write(f"log = {condor_submit_file_dir}/job.log\n")
      f.write("queue 1\n")

  return [seed, condor_submit_file]

def create_dag_file(dag_file, condor_submit_files):
  with open(dag_file, 'w') as f:
    f.write("# DAGMan file\n\n")
    f.write("MAXJOBS idle 1000\n\n")
    for submit_file in condor_submit_files:
      f.write(f"JOB job_{submit_file[0]} {submit_file[1]}\n\n")

def submit_dag(dag_file):
  subprocess.run(["condor_submit_dag", dag_file], check=True)

def parser():
  parser = argparse.ArgumentParser(description="Script to generate Condor DAGman file for subset processing and merging")
  parser.add_argument("--dagman_area", required=True, help="The dagman area")
  parser.add_argument("--input_lhe_folder", required=True, help="Path to the input LHE files folder")
  parser.add_argument("--cmsrun_config", required=True, help="Path to teh cmsrun config")
  parser.add_argument("--stageout_dir", required=True, help="Path to the stageout directory")
  parser.add_argument("--submit_job", action="store_true", help="Submit the DAGman job to Condor") 
 
  return parser.parse_args() 

def main():
  DESY_T2_SITEPATH = "root://dcache-cms-xrootd.desy.de:/"

  args = parser()
  
  os.makedirs(args.dagman_area, exist_ok=False)

  condor_submit_files = []
  for root, dirs, files in os.walk(args.input_lhe_folder):
    for file in files:
      if file.endswith(".lhe"):
        basename_input_file = os.path.splitext(os.path.basename(file))[0] + ".root"

        dagman_area = args.dagman_area
        cmsrun_config = args.cmsrun_config
        input_file = DESY_T2_SITEPATH + os.path.join(root, file)
        output_file = os.path.join(args.stageout_dir, basename_input_file)
        seed = extract_seed_from_filename(basename_input_file)      

        condor_submit_files.append(create_condor_submit_file(dagman_area, cmsrun_config, input_file, output_file, seed))

  dag_file = f"{args.dagman_area}/dagman.dag"  
  create_dag_file(dag_file, condor_submit_files)
  print("Created:", args.dagman_area)
  if args.submit_job:
    submit_dag(dag_file)

if __name__ == "__main__":
    main()

