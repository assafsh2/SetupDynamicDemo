
cd /home/badhat/YS/kubernetes-kafka
./teardown-kafka.sh /data
sudo rm -rf /data/datadir-kafka-*
sudo ntpdate -B -u 192.168.0.54  && /etc/init.d/hwclock.sh

ssh -t 192.168.0.54  "echo badhat | sudo -S /home/badhat/Templates/sudo_scripts/delete_kafka_topic.sh"

sleep 45

cd /home/badhat/YS/kubernetes-kafka
./setup-kafka.sh /data


