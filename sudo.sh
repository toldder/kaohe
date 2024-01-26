#!/bin/bash
#确保有足够的权限
if [ $(id -u) -ne 0 ];then
	echo " 请使用sudo命令运行此脚本"
	exit 1
fi
