# level0

1.**cpu和内存使用情况**都调用了psutil库里面的函数，使用psutil库里的cpu_count统计物理cpu和逻辑cpu个数，使用cou_percent统计cpu使用率，virtual_memory函数统计内存使用率，used函数统计内存已经使用的大小

2.**I/O**采用了pustil中的disk_io_counters统计了io的**每秒读写次数**，采用了psutil库里的函数，**io延迟**是采用了subprocess库里函数，结合shell脚本一起执行计算得出，在使用shell脚本进行输出io情况后，又采用了正则表达式对输出结果进行了筛选计算，并采用rich库中的表单形式输出每秒读写次数，io延迟，写入流量，读流量

3.**流量情况**采用了psutil库中的net_io_counters统计总发送，总接受，上行流量和下行流量。且也采用了rich库中的表单形式进行输出

# level1

编写了dockerfile文件

# level2

pull该镜像的命令

```
docker pull witch6/winter_test:3.10
```

**关于docker中容器中运行该程序的一些问题**

容器中输出io的情况耗费时间有时候特别长，在容器中安装lamp环境是启动mariadb服务器会失败

# level 3

编写了安装lamp环境的shell脚本

