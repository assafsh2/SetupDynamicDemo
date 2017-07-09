import sys
import os
import time 
import string

def replaceTokenInFile(index,num_of_updates_per_second,stream_file,rand_file):

 name="source"+str(index)
 oldFile=open('stream_kube_dynamic_with_token.yaml', 'r')
 newFile=open(stream_file, 'w+') 

 for line in oldFile:
   if "TOKEN" in line:
    newFile.write(line.replace("TOKEN",name))
   else:
    newFile.write(line.replace("stream-dynamic","stream-dynamic"+str(index)))
    
 oldFile.close()
 newFile.close()

 oldFile=open('rand_kube_deploy_dynamic_with_token.json', 'r')
 newFile=open(rand_file, 'w+')
 
 for line in oldFile:
  if "SOURCE_NAME" in line:
    newFile.write(line.replace("SOURCE_NAME", name))
  elif "NUM_OF_UPDATES" in line:
    newFile.write(line.replace("NUM_OF_UPDATES", num_of_updates_per_second))
  else:
    newFile.write(line.replace("rand-gen-dynamic","rand-gen-dynamic"+str(index)))
   
 oldFile.close()
 newFile.close()
 

 
def deployInterface(index,num_of_updates_per_second):
 
 tmp_file_name1="stream_kube_dynamic_with_token_tmp"+str(index)+".yaml"
 os.system("cp stream_kube_dynamic_with_token.yaml "+tmp_file_name1);

 tmp_file_name2="rand_kube_deploy_dynamic_with_token_tmp"+str(index)+".json"
 os.system("cp rand_kube_deploy_dynamic_with_token.json "+tmp_file_name2);
 
 replaceTokenInFile(index,num_of_updates_per_second,tmp_file_name1,tmp_file_name2) 

 
 os.system("kubectl --server=192.168.0.51:8080 create -f "+tmp_file_name1);
 os.system("kubectl --server=192.168.0.51:8080 create -f "+tmp_file_name2);
 
if __name__ == "__main__":

  if len(sys.argv) != 3 :
   print 'Usgae <num_of_interfaces> <num_of_updates_per_second>'
   sys.exit(0)

  num_of_interfaces=sys.argv[1]
  num_of_updates_per_second=sys.argv[2]

  os.system("kubectl --server=192.168.0.51:8080 create -f engine_deployment.yaml");

  os.system("sudo rm stream_kube_dynamic_with_token_tmp*.yaml rand_kube_deploy_dynamic_with_token_tmp*.json");

  for i in range(int(num_of_interfaces)) :
    deployInterface(i,num_of_updates_per_second)
    time.sleep(1)
  





