kubectl --server=192.168.0.54:8080 --namespace=default delete job --all
kubectl --server=192.168.0.54:8080 create -f performance_process_deploy_with_token_tmp.yaml 

