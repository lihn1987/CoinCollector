if [ `whoami` != "root" ];then
    echo "Error:This script must be run as root!"
    exit
fi
echo '{
  "registry-mirrors": [
    "https://registry.docker-cn.com",
    "http://hub-mirror.c.163.com",
    "https://docker.mirrors.ustc.edu.cn"
  ]
}' > /etc/docker/daemon.json