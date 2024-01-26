#!/bin/bash
#确保有足够的权限
if [ $(id -u) -ne 0 ];then
	echo " 请使用sudo命令运行此脚本"
	exit 1
fi
iostat
#确保存在iostat命令
if [ $? == 127 ];then
  apt-get update
  apt-get install sysstat
fi

