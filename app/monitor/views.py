# -*- coding: utf-8 -*-

import os
import time
import sys
import datetime
import socket
import psutil 
import re
import json
from flask import request, jsonify

from . import system_monitor
from run import app


@system_monitor.route("/baseinfo")
def base_info():
    """
    :return:
    """
    hostname = socket.gethostname()
    user_conn = len(psutil.users())
    start_time = datetime.datetime.fromtimestamp(psutil.boot_time()).strftime("%Y-%m-%d %H:%M:%S")
    now_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
#    sys_runtime = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time() - psutil.boot_time()))
    result = re.search(r"up\s+(.*?\,.*?),", os.popen('uptime').readline())
    sys_runtime = result.group(1)
    process = os.popen('ps -ef |wc -l').read().strip()
    value = {"hostname":hostname,"user_conn":user_conn,"sys_start_time":start_time,"now_time":now_time,"sys_runtime":sys_runtime,"process":process}

    return jsonify(value)


@system_monitor.route("/cpuinfo")
def cpu_info():
    ave_load = os.popen('uptime').readline().split(":")[-1].split()
    ave_load = ' '.join(ave_load) #CPU平均负载
    #以下四项值都是获取的瞬时值
    user_time = psutil.cpu_times().user  #用户态使用CPU时间
    sys_time = psutil.cpu_times().system #系统态使用CPU时间
    idle_time = psutil.cpu_times().idle #CPU空闲时间
    iowait_time = psutil.cpu_times().iowait #IO等待时间
    total_cpu = 0
    for i in range(len(psutil.cpu_times())):
        total_cpu += psutil.cpu_times()[i] 
    user_use = str(round(user_time / total_cpu * 100,2)) + '%'
    sys_use = str(round(sys_time / total_cpu * 100,2)) + '%'
    idle = str(round(idle_time / total_cpu * 100,2)) + '%'
    iowait = str(round(iowait_time / total_cpu * 100,2)) + '%'
    cpu_pre = str(psutil.cpu_percent(app.config["CPUT"])) + "%"
    logical_cpu = psutil.cpu_count()
    pyhsical_cpu = psutil.cpu_count(logical=False)
    #获取CPU使用最高的前十行
    #top10 = len(os.popen('ps aux|grep -v PID|sort -rn -k +3|head -10').readlines())
#    dic1 = {"ave_load":ave_load,"user_use":user_use,"sys_use":sys_use,"idle":idle,"iowait":iowait,"cpu_pre":cpu_pre,"logical_cpu":logical_cpu,"pyhsical_cpu":pyhsical_cpu}
    l1,l2,l3,l4,l5,l6 = [],[],[],[],[],[]
    i = 0
    while i < 10:
        #user = os.popen('ps aux|grep -v PID|sort -rn -k +4|head').readlines().[info].split()[0]
        #pid = int(os.popen('ps aux|grep -v PID|sort -rn -k +3|head -10').readlines()[i].split()[1])
        #a = os.popen('ps aux |sort -k3 -nr').readlines()[i].split()
        try:
            info = ''
            info = psutil.Process(int(os.popen("ps aux|grep -v PID|sort -rn -k +3").readlines()[i].split()[1]))
            #if bool(info):
            #pid = psutil.Process(int(os.popen('ps aux|grep -v PID|sort -rn -k +3').readlines()[i].split()[1])).pid
            pid = info.pid
            user = info.username()
            process_name = info.name()
            cpu_use = str(info.cpu_percent()) + '%'
            status = info.status()
            l1.append(user)
            l2.append(pid)
            l3.append(cpu_use)
            l4.append(process_name)
            l5.append(status)
            i += 1
        except:
            pass
    c0 = []
    l = ["user","pid","cpu_use","process_name","status"]
    cpu_value = list(zip(l1,l2,l3,l4,l5))
    cpu_len = len(cpu_value)
    for i in range(cpu_len):
        c0.append(dict(zip(l,cpu_value[i])))
#def cpu():
#以下获取的是逻辑CPU的瞬时值
    with open('/proc/stat','r') as f:
        cpu_item = f.readlines()
    cpu_number,cpu_use = [],[]
    for i in cpu_item:
        if re.search("^cpu[0-9]{1,}",i):
            cpu_info = i
            cpu_info = cpu_info.split(' ')
            #cpu_number = cpu_info[0]
            cpu_number.append(cpu_info[0])
            cpu_total = 0
            for num in cpu_info:
                if num.isdigit():
                    cpu_total += float(num)
                cpu_free = float(cpu_info[4])
            cpu_u = str(round((1 - cpu_free / cpu_total) * 100 ,2)) + '%'
            cpu_list = cpu_u.split()
            cpu_str = ''.join(cpu_list)
            cpu_use.append(cpu_str)
    c1 = []
    cpu_l = ["cpu_number","cpu_use"]
    cpu_v = list(zip(cpu_number,cpu_use))
    cpu_len = len(cpu_v)
    for i in range(cpu_len):
        c1.append(dict(zip(cpu_l,cpu_v[i])))
    value =   {
                "ave_load":ave_load,
                "user_use":user_use,
                "sys_use":sys_use,
                "idle":idle,
                "iowait":iowait,
                "cpu_pre":cpu_pre,
                "logical_cpu":logical_cpu,
                "pyhsical_cpu":pyhsical_cpu,
                "logical_cpu_use":c1,
                "cpu_top10":c0
              }
    return jsonify(value)


@system_monitor.route("/memoryinfo")
def memory_info():
    total_mem = str(round(psutil.virtual_memory().total / 1024 /1024/1024)) + 'G'
    use_mem = str(round(psutil.virtual_memory().used / 1024 /1024/1024)) + 'G'
    mem_percent = str(psutil.virtual_memory().percent) + '%'
    free_mem = str(round(psutil.virtual_memory().free / 1024 /1024/1024)) + 'G'
    swap_mem = str(round(psutil.swap_memory().total / 1024 /1024/1024)) + "G"
    swap_use = str(round(psutil.swap_memory().used / 1024 /1024/1024 )) + 'G'
    swap_free = str(round(psutil.swap_memory().free / 1024 /1024/1024))  + 'G'
    swap_percent = str(psutil.swap_memory().percent) + '%'
 #获取memory使用最高的前十行
    #top10 = len(os.popen('ps aux|grep -v PID|sort -rn -k +4|head -10').readlines())
#    dic1 = {"ave_load":ave_load,"user_use":user_use,"sys_use":sys_use,"idle":idle,"iowait":iowait,"cpu_pre":cpu_pre,"logical_cpu":logical_cpu,"pyhsical_cpu":pyhsical_cpu}
    l1,l2,l3,l4,l5,l6 = [],[],[],[],[],[]
    i = 0
    while i < 10:
        #user = os.popen('ps aux|grep -v PID|sort -rn -k +4|head').readlines().[info].split()[0]
        #pid = int(os.popen('ps aux|grep -v PID|sort -rn -k +4|head -10').readlines()[i].split()[1])
        try:
            info = psutil.Process(int(os.popen('ps aux|grep -v PID|sort -rn -k +4').readlines()[i].split()[1]))
            pid = info.pid
            user = info.username()
            process_name = info.name()
            mem_use = str(round(info.memory_percent(),2)) + '%'
            status = info.status()
            l1.append(user)
            l2.append(pid)
            l3.append(mem_use)
            l4.append(process_name)
            l5.append(status)
            i += 1
        except:
            pass
        continue
    m0 = []
    l = ["user","pid","mem_use","process_name","status"]
    mem_value = list(zip(l1,l2,l3,l4,l5))
    mem_len = len(mem_value)
    for i in range(mem_len):
        m0.append(dict(zip(l,mem_value[i])))
 
    value =  {
               "total_mem":total_mem,
               "use_mem":use_mem,
               "free_mem":free_mem,
               "mem_percent":mem_percent,
               "swap_mem":swap_mem,
               "swap_use":swap_use,
               "swap_free":swap_free,
               "swap_percent":swap_percent,
               "mem_top10":m0
             }
    return jsonify(value)


@system_monitor.route("/diskinfo")
def disk_info():
    #print("\033[31mdisk_info:\033[0m")
    #print("disk%-10s total%-10s free%-10s used%-10s percent%-10s"%('','(G)','(G)','(G)','(%)'))
    disk_num = int(''.join(os.popen("ls /dev/sd[a-z]|wc -l").readlines()[0].split()))
    d1,d2,d3,d4,d5 = [],[],[],[],[]
    disk_total,disk_used,disk_free = 0,0,0
    disk_len = len(psutil.disk_partitions())
    for info in range(disk_len):
        disk = psutil.disk_partitions()[info][1]
        if len(disk) < 10:
            d1.append(disk)
            total = str(round(psutil.disk_usage(disk).total /1024/1024/1024)) + 'G'
            total_num = psutil.disk_usage(disk).total
            disk_total  += total_num
            free = str(round(psutil.disk_usage(disk).free /1024/1024/1024)) + 'G'
            disk_free += psutil.disk_usage(disk).free
            used = str(round(psutil.disk_usage(disk).used /1024/1024/1024)) + 'G'
            disk_used += psutil.disk_usage(disk).used
            percent = str(psutil.disk_usage(disk).percent) + '%'
            d2.append(total)
            d3.append(free)
            d4.append(used)
            d5.append(percent)
    disk_used_percent = str(round(disk_used / disk_total * 100,2)) + '%'
    disk_free_percent = str(round(disk_free / disk_total * 100,2)) + '%'
    disk_total = str(round(disk_total /1024/1024/1024)) + "G"
    disk_free = str(round(disk_free /1024/1024/1024)) + "G"
    disk_used = str(round(disk_used /1024/1024/1024)) + "G"
    d0 = []
    d = ["mount","total","free","used","percent"]
    disk_value = list(zip(d1,d2,d3,d4,d5))
    disk_len = len(disk_value)
    for i in range(disk_len):
        d0.append(dict(zip(d,disk_value[i])))
    value =  {
               "disk":[
                        {"disk_num":disk_num},
                        {"disk_total":disk_total},
                        {"disk_free":disk_free},
                        {"disk_used":disk_used},
                        {"disk_used_percent":disk_used_percent},
                        {"disk_free_percent":disk_free_percent}
                      ],
               "partitions":d0
             }
    return jsonify(value)