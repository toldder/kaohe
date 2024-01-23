import threading
import time
import psutil
from rich.progress import Progress
from rich.table import Table
from rich.console import Console


def cpu_mem_use_rate():
    # 查看CPU使用率
    cpu_count = psutil.cpu_count(logical=False)  # 逻辑CPU个数
    cpu_use_rate = psutil.cpu_percent(percpu=False)
    mem_use_rate = psutil.virtual_memory().percent  # 内存使用率
    with Progress() as progress:
        old_cpu = cpu_use_rate
        old_mem = mem_use_rate
        print("cpu个数："+str(cpu_count))
        task1 = progress.add_task('[red]CPU_use_rate', total=100)
        task2 = progress.add_task('[green]mem_use_rate', total=100)
        progress.update(task1, advance=cpu_use_rate)  # 初识进度显示位置
        progress.update(task2, advance=mem_use_rate)
        while not progress.finished:
            cpu_use_rate = psutil.cpu_percent(percpu=False)
            mem_use_rate = psutil.virtual_memory().percent
            progress.update(task1, advance=cpu_use_rate-old_cpu)  # 进度条前进的距离
            progress.update(task2, advance=mem_use_rate-old_mem)
            time.sleep(0.02)  # 每隔0.02s刷新一次
            old_cpu = cpu_use_rate
            old_mem = mem_use_rate


def io_system_info():
    # tuple,分别是read_count,write_count,read_bytes,write_bytes,read_time,write_time,默认返回所有磁盘总情况
    io_system = psutil.disk_io_counters()
    table = Table(title="io_system")  # 表单形式输出
    table.add_column('information')
    table.add_column('data')
    table.add_row("read_count", str(io_system.read_count))
    table.add_row("write_count", str(io_system.write_count))
    table.add_row("read_bytes", str(io_system.read_bytes))
    table.add_row("write_bytes", str(io_system.write_bytes))
    console = Console()
    console.print(table)


def net_info():
    # tuple,分别是bytes_sent,packets_sent,bytes_recv,packets_recv,errin,errout,dropin,dropout-丢弃的发送包的数量
    net_static = psutil.net_io_counters()
    table = Table(title="network")
    table.add_column('netInformation')
    table.add_column('data')
    table.add_row("bytes_sent", str(net_static.bytes_sent))
    table.add_row("packets_sent", str(net_static.packets_sent))
    table.add_row("bytes_recv", str(net_static.bytes_recv))
    table.add_row("packets_recv", str(net_static.packets_recv))
    console = Console()
    console.print(table)


if __name__ == '__main__':
    thread1 = threading.Thread(target=cpu_mem_use_rate)
    io_system_info()
    net_info()
    thread1.start()
