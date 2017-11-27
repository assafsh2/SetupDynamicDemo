import sys
import os
import time 
import string
import subprocess

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

 
 os.system("kubectl --server=192.168.0.54:8080 create -f "+tmp_file_name1);
 os.system("kubectl --server=192.168.0.54:8080 create -f "+tmp_file_name2);

def deployEngine(num_of_interfaces,engine_image_tag):

 sourceNameArray=[]
 for i in range(int(num_of_interfaces)) :
  sourceNameArray.append("source"+str(i))
  if i < int(num_of_interfaces) -1 :
   sourceNameArray.append(",")


 print "".join(sourceNameArray)
 oldFile=open('engine_deployment_with_token.yaml', 'r')
 newFile=open('engine_deployment_with_token_tmp.yaml', 'w+')

 for line in oldFile:
  if "INTERFACES_NAME_TOKEN" in line:
   newFile.write(line.replace("INTERFACES_NAME_TOKEN","".join(sourceNameArray)))
  else:
   newFile.write(line.replace("IMAGE_TAG_TOKEN",engine_image_tag))

 oldFile.close()
 newFile.close()

 os.system("kubectl --server=192.168.0.54:8080 create -f engine_deployment_with_token_tmp.yaml");

def deployProcessJob(num_of_interfaces,num_of_updates_per_second):

 oldFile=open('performance_process_deploy_with_token.yaml', 'r')
 newFile=open('performance_process_deploy_with_token_tmp.yaml', 'w+')

 for line in oldFile:
  if "NUM_OF_INTERFACES_TOKEN" in line:
   newFile.write(line.replace("NUM_OF_INTERFACES_TOKEN",num_of_interfaces))
  else:
   newFile.write(line.replace("NUM_OF_UPDATES_TOKEN",num_of_updates_per_second))

 oldFile.close()
 newFile.close()


 
if __name__ == "__main__":

  if len(sys.argv) != 4 :
   print 'Usgae <num_of_interfaces> <num_of_updates_per_second><engine_image_tag>'
   sys.exit(0)

  num_of_interfaces=sys.argv[1]
  num_of_updates_per_second=sys.argv[2]
  engine_image_tag=sys.argv[3]

  os.system("./teardown_demo.sh")
  time.sleep(5)
  os.system("./restart_kafka.sh")

  os.system("kubectl --server=192.168.0.54:8080 create -f pv_engine_performance_process.yml");
  os.system("kubectl --server=192.168.0.54:8080 create -f pvc_engine_performance_process.yml");

  #os.system("kubectl --server=192.168.0.54:8080  label node 192.168.0.54 type=MASTER --overwrite=true");
  os.system("sudo rm stream_kube_dynamic_with_token_tmp*.yaml rand_kube_deploy_dynamic_with_token_tmp*.json engine_deployment_with_token_tmp.yaml");

  time.sleep(40)

  for i in range(int(num_of_interfaces)) :
    deployInterface(i,num_of_updates_per_second)
    time.sleep(1) 

  deployEngine(num_of_interfaces,engine_image_tag)

  deployProcessJob(num_of_interfaces,num_of_updates_per_second) 

