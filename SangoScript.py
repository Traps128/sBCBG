#!/usr/bin/python
# -*- coding: utf-8 -*-

import shlex
import subprocess
import os
import time

print "*** /!\ For simulations on Sango, check that interactive=False in LGNeurons.py ***"
print "*** and that the code to be executed has been made executable: chmod +x toto.py ***"

header = '#!/bin/bash \n\n'

execTime = time.localtime()
timeString = str(execTime[0])+'_'+str(execTime[1])+'_'+str(execTime[2])+'_'+str(execTime[3])+':'+str(execTime[4])

print 'Time:', timeString

i = 0

gmsn=4.37
gfsi=1.3
gstn=1.38
ggpe=1.3
ggpi=1.
iegpe=13.
iegpi=11.

# processes for one parameterization test:
#----------------------------------------- 
IDstring = timeString+'_%05d' %(i)

print 'Create subdirectory:',IDstring
subprocess.call(['mkdir',IDstring])
subprocess.call(['cp','LGneurons.py',IDstring+'/'])
subprocess.call(['cp','testFullBG.py',IDstring+'/'])
os.chdir(IDstring)
subprocess.call(['mkdir','log'])

# creation of the modelParams.py file that will correspond to the run at hand
mltstr = '''#!/apps/free/python/2.7.10/bin/python

# defines the value of the parameters that will be used by testFullbG.py
# generated by sangoScript.py

interactive = False

params = {'nbMSN': 2644.,
          'nbFSI':   53.,
          'nbSTN':    8.,
          'nbGPe':   25.,
          'nbGPi':   14.,
          'nbCSN': 3000.,
          'nbPTN':  100.,
          'nbCMPf':   9.,
          'GMSN':     %4.2f,
          'GFSI':     %4.2f,
          'GSTN':     %4.2f,
          'GGPe':     %4.2f,
          'GGPi':     %4.2f, 
          'IeGPe':    %3.1f,
          'IeGPi':    %3.1f,
          'inDegCSNMSN': 100.,
          'inDegPTNMSN':   1.,
          'inDegCMPfMSN':  1.,
          'inDegFSIMSN':  30., # according to Humphries et al. 2010, 30-150 FSIs->MSN                                                                                            
          'inDegMSNMSN':  70., # according to Koos et al. 2004, cited by Humphries et al., 2010, on avg 3 synpase per MSN-MSN connection                                         
          'inDegCSNFSI':  50.,
          'inDegPTNFSI':   1.,
          'inDegSTNFSI':   2.,
          'inDegGPeFSI':  25.,
          'inDegCMPfFSI':  9.,
          'inDegFSIFSI':  15., # according to Humphries et al., 2010, 13-63 FSIs->FSI                                                                                            
          'inDegPTNSTN':  25.,
          'inDegCMPfSTN':  9.,
          'inDegGPeSTN':  25.,
          'inDegCMPfGPe':  9.,
          'inDegSTNGPe':   8.,
          'inDegMSNGPe':2644.,
          'inDegGPeGPe':  25.,
          'inDegMSNGPi':2644.,
          'inDegSTNGPi':   8.,
          'inDegGPeGPi':  23.,
          'inDegCMPfGPi':  9.,
          }
''' %(gmsn,gfsi,gstn,ggpe,ggpi,iegpe,iegpi)

print 'Write modelParams.py'
paramsFile = open('modelParams.py','w')
paramsFile.writelines(mltstr)
paramsFile.close()

slurmOptions = ['#SBATCH --time=00:10:00 \n',
                '#SBATCH --partition=compute \n',
                '#SBATCH --mem-per-cpu=1G \n',
                '#SBATCH --ntasks=1 \n',
                '#SBATCH --cpus-per-task=2 \n',
                '#SBATCH --job-name=sBCBG_'+IDstring+'\n',
                '#SBATCH --input=none\n',
                '#SBATCH --output="'+IDstring+'.out" \n',
                '#SBATCH --error="'+IDstring+'.err" \n',
                '#SBATCH --mail-user=benoit.girard@isir.upmc.fr \n',
                '#SBATCH --mail-type=BEGIN,END,FAIL \n',
                ]

moduleLoad = ['module load nest/2.10 \n']

# build a parameter string strParams

# test param string:
# strParams = '2644. 53. 8. 25. 14. 3000. 100. 9. 4.37 1.3 1.38 1.3 1. 13. 11. 100. 1. 1. 30. 70. 50. 1. 2. 25. 9. 15. 25. 9. 25. 9. 8. 2644. 25. 2644. 8. 23. 9.'

# write the script file accordingly
print 'Write slurm script file'
script = open('go.slurm','w')
script.writelines(header)
script.writelines(slurmOptions)
script.writelines(moduleLoad)
script.writelines('python testFullBG.py \n')
script.close()

# execute the script file
p= []
command = 'sbatch go.slurm'
p.append(subprocess.Popen(shlex.split(command)))

os.chdir('..')
i+=1
