#! /bin/bash

# Check if arguments are provided
if [ "$#" != 4 ]; then
  echo "Usage: $0 <cmsrun_config> <input_file> <output_file> <input_seed>"
  exit 1
fi

cmsrun_config=${1}
input_file=${2}
output_file=${3} #gfal-copy -p crab.log davs://eoscms.cern.ch:443/eos/cms/store/group/phys_smp/ec/sin2O/testfoldr/crab.log
input_seed=${4}

print_message() {
  local caller_function="${FUNCNAME[1]}"
  local message="$1"
  local severity="$2"

  case "$severity" in
    INFO)
      echo -e "\e[97mINFO $(date +"%d-%b-%Y %H:%M:%S %Z") [${caller_function}]: ${message}\e[0m"  # White color for INFO
      ;;
    WARNING)
      echo -e "\e[93mWARNING $(date +"%d-%b-%Y %H:%M:%S %Z") [${caller_function}]: ${message}\e[0m"  # Yellow color for WARNING
      ;;
    ERROR)
      echo -e "\e[91mERROR $(date +"%d-%b-%Y %H:%M:%S %Z") [${caller_function}]: ${message}\e[0m"  # Red color for ERROR
      ;;
    *)
      echo -e "\e[91mERROR $(date +"%d-%b-%Y %H:%M:%S %Z") [${caller_function}]: Invalid severity level: $severity"
      ;;
  esac
}

setup_environment() {
  # Setup the environment
  source /cvmfs/grid.desy.de/etc/profile.d/grid-ui-env.sh
  export X509_USER_PROXY=~/.globus/x509up

  MDL_ver=cmssw/slc7_amd64_gcc900
  source /etc/profile.d/modules.sh
  module use -a /afs/desy.de/group/cms/modulefiles/
  module purge
  module load ${MDL_ver}
  
  cmsenv() {
    eval "$(scramv1 runtime -sh)"
  }
  export -f cmsenv
}

check_proxy_certificate_validity() {
  local threshold_hours=10
  
  # Check if the proxy certificate file exists
  if [ ! -f "${X509_USER_PROXY}" ]; then
    print_message "user proxy certificate not found at ${X509_USER_PROXY}. Please use 'voms-proxy-init --rfc --voms cms --valid 192:00 -out ~/.globus/x509up'" ERROR
    exit 1
  fi
  
  validity_output=$(openssl x509 -checkend 0 -noout -in "${X509_USER_PROXY}")
  validity_check_status=$?
  
  if [ "${validity_check_status}" -ne 0 ]; then
    print_message "certificate has expired or is not valid. Please use 'voms-proxy-init --rfc --voms cms --valid 192:00 -out ~/.globus/x509up' to recreate it." ERROR
    exit 1
  fi
  
  # Calculate the time remaining in seconds
  time_left_seconds=$(openssl x509 -in "${X509_USER_PROXY}" -noout -enddate | cut -d '=' -f 2- | xargs -I {} date '+%s' -d {})
  
  # Calculate the time remaining in hours
  time_left_hours=$(( (time_left_seconds - $(date '+%s')) / 3600 ))
  
  # Check if the time remaining is greater than the threshold
  if [ "${time_left_hours}" -gt "${threshold_hours}" ]; then
    print_message "certificate is still valid and has more than ${threshold_hours} hours remaining." INFO
  else
    print_message "certificate is still valid but has less than ${threshold_hours} hours remaining." ERROR
    exit 1
  fi
}

stageout_output() {
  local input_file="${1}"
  local output_directory="${2}"

  print_message "starting stageout" INFO

  if [ ! -f "${input_file}" ]; then
    print_message "'${input_file}' does not exist" ERROR
    exit 1
  fi
 
  gfal-copy -t 86400 -rpf "${input_file}" "${output_directory}/$(basename "${input_file}")"

  wait

  if gfal-ls "${output_directory}/$(basename "${input_file}")" &> /dev/null; then
    print_message "stageout completed to ${output_directory}/$(basename "${input_file}")" INFO
  else
    print_message "stageout failed" ERROR
    exit 1
  fi
}

run() {
  local cmsrun_config="${1}"
  local input_file="${2}"
  local output_file="${3}"
  local input_seed=${4}

  print_message "cmsRun started" INFO  
  (cmsenv; cmsRun ${cmsrun_config} inputFile=${input_file} outputFile=${temp_out} seed=${input_seed})
  if [ "$?" != 0 ]; then
    print_message "cmsRun failed" ERROR
    exit 1
  fi
  print_message "cmsRun finished" INFO  
}

job() {
  local cmsrun_config="${1}"
  local input_file="${2}"
  local output_file="${3}"
  local input_seed=${4}

  local working_folder=$(mktemp -d)
  local temp_out=${working_folder}/$(basename ${output_file})

  setup_environment
  
  check_proxy_certificate_validity

  run ${cmsrun_config} ${input_file} ${temp_out} ${input_seed}
  wait

  stageout_output "${temp_out}" "$(dirname "${output_file}")"

  print_message "job finished" INFO
 
  exit 0
}

job ${cmsrun_config} ${input_file} ${output_file} ${input_seed}
