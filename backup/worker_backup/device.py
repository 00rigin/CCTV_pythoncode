import cv2
import imutils
import time
from multiprocessing import Process, Queue

class device:
    def __init__(self):
        self._url = {
            "192.168.0.4" : 'rtsp://admin:coco2006!@192.168.0.4:554/0/profile2/media.smp',
            "192.168.0.6" : 'rtsp://admin:coco2006!@192.168.0.6:554/0/profile2/media.smp',
            "192.168.0.12" : 'rtsp://coco:coco2006!@192.168.0.12:88/videoMain',
            "192.168.0.9" : 'rtsp://coco:coco2006!@192.168.0.9:88/videoMain',
            "192.168.0.14" : 'rtsp://coco:coco2006!@192.168.0.14:88/videoMain',
            "192.168.0.15" : 'rtsp://coco:coco2006!@192.168.0.15:88/videoMain'
        }
        self.connectedDevice = []
        self.processList = []
        self.queueList = []
        self.createDevice("192.168.0.14")
        self.createDevice("192.168.0.15")
        return

    def camera(self, url, q):
        cap = cv2.VideoCapture(url)
        prevTime = 0

        while True:
            # extract context of device
            ret, frame = cap.read()
            curTime = time.time()
            sec = curTime - prevTime
            prevTime = curTime
            framesize = 1920 * len(frame) * 8 * 3
            quality = len(frame)
            bitra = framesize/(sec*1000)
            bitrate = round(bitra, 3)

            # descript the context
            data = [quality, bitrate, 37.61972, 127.060886]

            # insert the data in queue
            q.put(data)

            time.sleep(1)
        
            

    def createDevice(self, deviceUrl):
        # find the url
        url = self._url[deviceUrl]

        #create subprocess and queue
        q = Queue()
        subProcess = Process(target = self.camera, args=(url, q))
        subProcess.start()

        # append process and queue to list for management
        self.processList.append(subProcess)
        self.queueList.append(q)
        self.connectedDevice.append(deviceUrl)

    def terminateDevice(self, url):
        # find the url
        index = 0
        for deviceUrl in self.connectedDevice:
            if url == deviceUrl:
                break
            index+=1

        #
        subProcess = self.processList[index]
        del self.processList[index]
        subProcess.terminate()

        q = self.queueList[index]
        del self.queueList[index]
        q.close()

        del self.connectedDevice[index]

    def deviceExtraction(self):
        i=0
        result = {
            "connectedDevice" : self.connectedDevice,
            "videoQuality" :[],
            "videoRate" :[],
            "latitude" :[],
            "longitude":[]
        }

        for q in self.queueList:
            result['videoQuality'].append(0.0)
            result['videoRate'].append(0.0)
            result['latitude'].append(37.61972)
            result['longitude'].append(127.060886)
            
            if(q.qsize()>0):
                for value in iter(q.get, None): 
                    result['videoQuality'][i] = value[0]
                    result['videoRate'][i] = value[1]
                    result['latitude'][i] = value[2]
                    result['longitude'][i] = value[3]
                    if(q.qsize()<=0):
                        break            
            i+=1


        return result

