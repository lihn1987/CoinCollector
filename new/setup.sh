if [ `whoami` != "root" ];then
    echo "Error:This script must be run as root!"
    exit
fi
apt install curl
curl -fsSL https://get.docker.com | bash -s docker --mirror Aliyun
apt install docker-compose

apt install python3
apt install python3-pip
pip3 install pipreqs