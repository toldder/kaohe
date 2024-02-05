#!/bin/bash

#安装apche,mariadb和php
apt-get update
apt-get -y install systemctl
apt-get -y install apache2
systemctl start apache2
if [ $? -ne 0 ];then
       echo "安装apache启动失败"
	exit 1
fi
# iptables -A INPUT -p tcp --dport 80 -j ACCEPT # 开放apache的端口
apt -y install mariadb-server
systemctl start mariadb
if [ $? -ne 0 ];then
       echo "mariadb启动失败"
	exit 1
fi

apt-get -y install php libapache2-mod-php php-mysql

#检查环境是否搭建成功
echo "This is the lamp environments test" > /var/www/html/index.html
systemctl restart apache2 # 重启服务加载文件内容
curl -s http://localhost/index.html | grep "This is the lamp environments test" > /dev/null # 输出结果丢弃
if [ $? -ne 0 ];then
	echo "apache have problems"
	exit 1
else
	echo "lamp environments is ok"
fi
exit 0