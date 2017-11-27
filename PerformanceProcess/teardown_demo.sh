kubectl --server=192.168.0.54:8080 --namespace=default delete deploy --all
kubectl --server=192.168.0.54:8080 --namespace=default delete service --all
kubectl --server=192.168.0.54:8080 --namespace=default delete job --all
kubectl --server=192.168.0.54:8080 --namespace=default delete persistentvolumes --all
kubectl --server=192.168.0.54:8080 --namespace=default delete persistentvolumeclaim --all
