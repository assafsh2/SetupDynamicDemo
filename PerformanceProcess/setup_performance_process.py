import sys
import os
import time 
import string
import subprocess
 
if __name__ == "__main__":

 if len(sys.argv) != 5:
  print 'Usgae <activity><num_of_cycles><num_of_updates_per_cycle><duration>'
  sys.exit(0)

 activity=sys.argv[1]
 num_of_cycles=sys.argv[2]
 num_of_updates_per_cycle=sys.argv[3]
 duration=sys.argv[4]

 os.system("kubectl --server=192.168.0.54:8080 --namespace=default delete job engine-performance-process")
 oldFile=open('performance_process_deploy_with_token_tmp.yaml').read()
 newFile=open('performance_process_deploy_with_token_tmp0.yaml', 'w')

 replacements={'ACTIVITY_TOKEN':activity, 'NUM_OF_CYCLES_TOKEN':num_of_cycles,
               'NUM_OF_UPDATES_PER_CYCLE_TOKEN':num_of_updates_per_cycle, 'DURATION_TOKEN':duration}
 for i in  replacements.keys():
  oldFile=oldFile.replace(i, replacements[i])
 newFile.write(oldFile)
 newFile.close
 
 cm="kubectl --server=192.168.0.54:8080 create -f performance_process_deploy_with_token_tmp0.yaml"
 print cm
 os.system(cm);

