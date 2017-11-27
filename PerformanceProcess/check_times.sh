
echo "localhost time " 
date +"%Y-%m-%d %H:%M:%S,%3N"

echo "remote "
ssh -t 192.168.0.54  "echo badhat | sudo -S date +'%Y-%m-%d %H:%M:%S,%3N'"



