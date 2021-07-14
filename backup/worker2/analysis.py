import requests
import psutil, getpass, json, socket, threading
import math
#import Gputil as gp
import os
from collections import OrderedDict

class analysis:

    def __init__(self, object):
        self.object = object # 분석대상
        #### AI context ####
        self.objectList = ["Human","Car", "Fire", "Knife"]
        self.AI_context = {"DetectObject": [["Human","Car"],"Fire","Knife"],
                           "CPU": [0, 0, 0],
                           "Memory": [0, 0, 0]
                           }

        return

    def analysisExtraction(self):
        ### 분석대상 ###
        # Fire
        # Human/car
        # Knife

        cpuUsage = (psutil.cpu_count() * psutil.cpu_percent(interval=0.1, percpu=False)) / 100
        cpuCore = psutil.cpu_count()
        cpuOccupancy = psutil.cpu_percent(interval=0.1, percpu=False)
        cpuClock = psutil.cpu_freq()[0]
        memory = psutil.virtual_memory()
        totalMemory = memory.total
        memUsage = memory.used
        freeMemory = memory.available
        memoryOccupancy = memory.used / memory.total * 100
        d = psutil.disk_usage(path='/')
        totalDisk = d.total
        freeDisk = d.free
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 0))
        netAddress = s.getsockname()[0]
        # print(s)
        userName = socket.gethostname()

        objectIndex = self.objectList.index(self.object) - 1 # Find object resource data index
        if(objectIndex<0): objectIndex=0 # human/car 사용

        ## Pycharm 만 켜져 있을때 사용률 제외함
        self.AI_context["CPU"][objectIndex] = round(cpuUsage - 0.1, 3)
        self.AI_context["Memory"][objectIndex] = round(
            (memUsage - 2806722560) / math.pow(2, 20))  # byte->Mb

        file_data = self.AI_context

        # Display
        # os.system('clear')
        # print("----------------")
        # print("  CPU  |  MEM  ")
        # print(" %.2f%% | %.2f%% " % (cpuOccupancy, memoryOccupancy))
        # print("----------------")
        # print("totalCPU : " + str(cpuCore))
        # print("cpuUsage : " + str(cpuUsage))
        # # print("cpuOccupancy :"+ str(cpuOccupancy))
        # print("totalMemory :" + str(totalMemory))
        # print("memoryUsage : " + str(memUsage))
        # print("freeMemory :" + str(freeMemory))
        # # print("memoryOccupancy :"+ str(memoryOccupancy))
        # # print(gp.showUtilization())
        # print("----------------")

        return  file_data
