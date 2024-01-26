import subprocess
import time
import re
import psutil
from rich.table import Table
from rich.console import Console
import getpass


def cpu_mem_use_rate():
    # 查看CPU使用率
    cpu_physic_count = psutil.cpu_count(logical=False)  # 物理CPU个数
    cpu_logic_count = psutil.cpu_count(logical=False)  # 逻辑CPU个数
    print("physical cpu counts:"+str(cpu_physic_count))
    print("logical cpu counts:"+str(cpu_logic_count))
    cpu_use_rate = psutil.cpu_percent(percpu=False)
    print("the use rate of cpu: " + str(cpu_use_rate) + "%")
    mem_use_rate = psutil.virtual_memory()  # 内存使用率
    print("the use rate of memory: "+str(mem_use_rate.percent)+"%")
    print(f"memory used:  {mem_use_rate.used/1024.0/1024.0:.2f}MB")


def get_io_delay(return_code) -> float:
    if return_code == 1:
        command = "sudo -S ./get_io_information.sh"
        tmp = subprocess.Popen(command, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                           universal_newlines=True)
        _, stderr = tmp.communicate(input=getpass.getpass("请输入sudo密码：") + '\n')
        if len(stderr) != 0:
            print("get_io_information脚本执行失败", stderr)
            return -1.0  # -1.0表示脚本执行错误
    else:
        result = subprocess.run(['bash', './get_io_information.sh'], capture_output=True, text=True)
        if result.returncode != 0:
            print("执行lamp脚本失败", result.stderr)
            return -1.0

    cmd = 'iostat -d -x 1 1 '   # -x 扩展模式，包括IO请求的响应时间。1 每隔1s显示， 1只显示一次统计信息
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    output, err = p.communicate()
    if err is not None:
        print(f"Error:{err}")
        return -1.0
    # 解析 iostat 输出结果，获取平均每秒读写延迟
    pattern = re.compile(r'\d+\.\d{2}?')
    io_delay = 0.0
    count = 0  # 磁盘的块数
    for line in output.splitlines():  # 将所得到的结果按照行切分
        match = pattern.findall(line.decode())  # 将字节解码为字符串
        if len(match) != 0:
            read_delay = float(match[4])
            write_delay = float(match[9])
            avg_delay = (read_delay + write_delay) / 2.0
            io_delay += avg_delay
            count += 1

    if count > 0:
        avg_io_delay = io_delay / count
    else:
        avg_io_delay = -2.0  # 无法获取有效IO数据
    return avg_io_delay


def io_system_info(return_code):
    # tuple,分别是read_count,write_count,read_bytes,write_bytes,read_time,write_time,默认返回所有磁盘总情况
    init_io = psutil.disk_io_counters()
    time.sleep(1)  # 等待1s，计算每秒读写次数
    current = psutil.disk_io_counters()
    read_write_count_per_sec = (current.read_count - init_io.read_count) + (current.write_count - init_io.write_count)

    # 计算IO延迟
    io_delay = get_io_delay(return_code)
    if io_delay == -1.0:
        return
    if io_delay == -2.0:
        print("无法获取有效IO信息")
        return

    table = Table(title="io_system")  # 表单形式输出
    table.add_column('information')
    table.add_column('data')
    table.add_row("read_write_count_per_sec", str(read_write_count_per_sec))
    table.add_row("io_delay", f"{io_delay:.2f}")  # 格式化字符串
    table.add_row("read_bytes", f"{current.read_bytes/1024.0:.2f}kb")
    table.add_row("write_bytes", f"{current.write_bytes/1024.0:.2f}kb")
    console = Console()
    console.print(table)


def net_info():
    # tuple,分别是bytes_sent,packets_sent,bytes_recv,packets_recv,errin,errout,dropin,dropout-丢弃的发送包的数量
    net_static = psutil.net_io_counters()
    # 计算上行流量和下行流量
    net_data = psutil.net_if_stats()
    up_bytes = 0.0
    low_bytes = 0.0
    count = 0
    for interface, status in net_data.items():  # 遍历接口
        if status.isup:  # 接口是否开启
            # 每一个接口，此时返回值是一个字典，key为接口名称,value与之前的tuple相同
            per_io_info = psutil.net_io_counters(pernic=True)[interface]
            up_bytes += per_io_info.bytes_sent
            low_bytes += per_io_info.bytes_recv
            count += 1
    if count == 0:
        print("网络错误")
        return
    upper_bytes = up_bytes/count
    lower_bytes = low_bytes/count

    table = Table(title="network")
    table.add_column('netInformation')
    table.add_column('data')
    table.add_row("总发送", f"{net_static.bytes_sent/1024.0/1024.0:.2f}MB")
    table.add_row("总接受", f"{net_static.bytes_recv/1024.0/1024.0:.2f}MB")
    table.add_row("上行流量", f"{upper_bytes/1024.0/1024.0:.2f}MB")
    table.add_row("下行流量", f"{lower_bytes/1024.0/1024.0:.2f}MB")
    console = Console()
    console.print(table)


def lamp(sudo_code):
    if sudo_code ==1:
        command_str = "sudo -S ./lamp.sh"
        tmp = subprocess.Popen(command_str, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE, universal_newlines=True)
        _, stderr = tmp.communicate(input=getpass.getpass("请输入sudo密码：") + '\n')
        if stderr is not None:
            print(stderr)
            return
    else:
        result = subprocess.run(['bash', './lamp.sh'], capture_output=True, text=True)
        if result.returncode != 0:
            print("执行lamp脚本失败",result.stderr)
            return


if __name__ == '__main__':
    # 查看运行程序的权限
    return_code = subprocess.call(['bash', './sudo.sh'])
    print("----欢迎来到宝塔命令行面板--------")
    print(" 1 查看cpu和内存使用率   2 查看I/O情况  3.查看网络流量情况 4 一键安装lamp环境 5 退出宝塔面板")
    while True:
        choice = input("请输入你的选项")
        match choice:
            case "1":
                cpu_mem_use_rate()
            case "2":
                io_system_info(return_code)
            case "3":
                net_info()
            case "4":
                print("安装lamp环境...")
                lamp(return_code)
                print("环境安装成功")
            case "5":
                break
            case _:
                print("输入错误，请重新输入")
