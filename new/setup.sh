if [ `whoami` != "root" ];then
    echo "Error:This script must be run as root!"
    exit
fi
apt install curl
curl -fsSL https://get.docker.com | bash -s docker --mirror Aliyun
apt install docker-compose -y

apt install python3 -y
apt install python3-pip -y
pip3 install pipreqs -y


apt install npm -y



#apt install snapd -y
#sudo snap install --classic certbot
#sudo ln -s /snap/bin/certbot /usr/bin/certbot
#certbot --server https://acme-v02.api.letsencrypt.org/directory -d "blocktools.site" -d "*.blocktools.site" --manual --preferred-challenges dns-01 certonly
