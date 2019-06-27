#!/bin/bash
#
#$ -cwd
#$ -j y
#$ -pe mpi 36
#$ -S /bin/bash

module load mpi/openmpi-x86_64
export PATH=$PATH:/share1/lsdyna
export LSTC_LICENSE=network
export LSTC_LICENSE_SERVER=10.194.60.119
mpirun -N 18 -wdir /share1/run/test /share1/lsdyna/ls-dyna_mpp_s_r11_0_0_x64_centos65_ifort160_sse2_openmpi2.1.3 i=CRUSH_analysis_All_include.k memory=300m memory2=100m