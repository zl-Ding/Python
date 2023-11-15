import threading
import wmi
import psutil
import time
import numpy as np


target_cpu_utilization = 50 # 定义目标CPU利用率
allowed_deviation = 5   # 定义允许的偏差范围
total_runtime = 3600    # 定义程序运行时间（秒）

interval = 600  # 定义时间间隔（秒）

# 获取当前CPU利用率
def get_current_cpu_utilization():
    # cpu_percent = psutil.cpu_percent(interval=5,percpu=True)
    # total_cpu_percent = sum(cpu_percent)/2
    total_cpu_percent = psutil.cpu_percent(interval=5)*4.45
    return total_cpu_percent

# 获取CPU序列号
def get_cpu_serial():
    return wmi.WMI().Win32_Processor()[0].ProcessorId.strip()

# 高性能任务
def increase_cpu_usage(exit_event):

    while not exit_event.is_set():
        result = 0
        for i in range(100000):
            result += i

if __name__ == '__main__':

    start_time = time.time() # 开始时间
    end_time = start_time + total_runtime # 结束时间
    prev_time = 0

    cpu_serial = get_cpu_serial()

    cpu_usage_threads = []
    threads_num = 0
    exit_events = []

    # 开始执行程序
    while time.time() <= end_time +7:

        current_time = time.time()
        elapsed_time = current_time - start_time # 运行时间
        current_cpu_utilization = get_current_cpu_utilization()  # cpu 利用率

        # 每隔 600秒 输出
        if  elapsed_time < 3 or elapsed_time - prev_time >= interval:
            prev_time = elapsed_time
            print(f"当前系统时间: {time.ctime()}")
            print("CPU序列号: "+cpu_serial)
            print(f"当前CPU利用率: {current_cpu_utilization}%")
            print("--" * 30)

        if (current_cpu_utilization < target_cpu_utilization - allowed_deviation): # 利用率过低
            print(f"利用率过低,提高cpu利用率,当前CPU利用率{current_cpu_utilization}%.")
            # 创建一个线程来执行CPU密集任务
            exit_events.append(threading.Event())
            cpu_usage_threads.append(threading.Thread(target=increase_cpu_usage,args=(exit_events[threads_num],)))
            cpu_usage_threads[threads_num].daemon = True  # 将线程设置为守护线程，以便在程序结束时自动停止
            cpu_usage_threads[threads_num].start()
            threads_num += 1
            print(f" 线程数：{threads_num}")

        elif (current_cpu_utilization > target_cpu_utilization + allowed_deviation): # 利用率过高
            print(f"利用率过高,降低cpu利用率,当前CPU利用率{current_cpu_utilization}%.")
            # 判断超出范围时间，并确定线程数，杀死线程降低cpu利用率
            if(threads_num>0):
                threads_num -=1
                exit_events[threads_num].set() # 关闭一个线程
                exit_events.pop()
                cpu_usage_threads.pop()
            print(f" 线程数：{threads_num}")
        else:
            print(f"CPU利用率在范围45%--55%之内：{current_cpu_utilization}")
        time.sleep(1)

    print("程序执行完毕")
