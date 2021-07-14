import psutil, socket
from collections import OrderedDict

class edge:
    def __init__(self): 
        self.ewmaoccupancy = 0
        return

    def edgeExtraction(self):
        # CPU
        cpuOccupancy = psutil.cpu_percent(interval=0.1, percpu=False)
        self.ewmaoccupancy = 0.5* cpuOccupancy + 0.5 * self.ewmaoccupancy
        self.ewmaoccupancy = round(self.ewmaoccupancy, 3)
        cpuUsage = round((psutil.cpu_count() * cpuOccupancy)/100, 3)
        cpuCore = psutil.cpu_count()
        #cpuCl = ps
        cpuClock = round(psutil.cpu_freq()[0], 3)

        # Memory (RAM)
        memory = psutil.virtual_memory()
        totalMemory = memory.total >> 20
        freeMemory = memory.available >> 20
        memoryOccupancy = round(memory.used/memory.total * 100, 3)

        # HardDisk (Storage)
        d = psutil.disk_usage(path='/')
        totalDisk = d.total >> 20
        freeDisk = d.free >> 20
        
        # IP Address
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 0))
        netAddress = s.getsockname()[0]
        userName = socket.gethostname()

        file_data = {
            "name" : userName,
            "cpuClock" : cpuClock,
            "cpuUsage" : cpuUsage,
            "cpuCore" : cpuCore,
            "cpuOccupancy" : self.ewmaoccupancy,
            "totalMemory" : totalMemory,
            "freeMemory" : freeMemory,
            "memoryOccupancy" : memoryOccupancy,
            "totalDisk" : totalDisk,
            "freeDisk" : freeDisk,
            "diskOccupancy" : d.percent,
            "netAddress" : netAddress
        }

        return file_data
