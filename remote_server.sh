#!/bin/bash

ips="ec2-52-32-163-134.us-west-2.compute.amazonaws.com
	ec2-52-34-48-36.us-west-2.compute.amazonaws.com
	ec2-35-164-213-69.us-west-2.compute.amazonaws.com
	ec2-52-25-35-204.us-west-2.compute.amazonaws.com
	ec2-34-216-70-235.us-west-2.compute.amazonaws.com"


start_one_server() {
	ip=$1
	/usr/bin/expect -c "
	set timeout 120

	echo \"start one server\"
	spawn ssh -i cse223b-19sp-j4lu.pem ec2-user@$ip

	echo \"connected\"

	send \"sudo yum -y install git\r\"
	sleep 5

	send \"rm -rf cse*\r\"
	sleep 1

	send \"git clone https://lujie1996:lu490603562@github.com/lujie1996/cse223b-project.git\r\"
	send \"cd cse223b-project\r\"
	send \"ls\r\"

	send \"sudo yum -y install python3\r\"
	sleep 10
	send \"sudo python3 -m ensurepip --default-pip\r\"
	sleep 2
	send \"sudo python3 -m pip install --upgrade pip\r\"
	sleep 20
	send \"sudo python3 -m pip install grpcio\r\"
	sleep 3
	send \"sudo python3 -m pip install grpcio-tools\r\"
	sleep 3

	send \"python3 server.py config.txt $1 5001\r\"
	
	"
}


for ip in $ips
do 
	#start_one_server $ip
	start_one_server $ip
done

python chaos_client.py upload config.txt matrix


# send "bash start_server.sh\r"
# send "python3 server.py config.txt localhost 5001\r"
# send "python3 client.py config.txt get 3"