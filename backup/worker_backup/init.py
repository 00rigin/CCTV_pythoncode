from edge import edge
from device import device
import requests
import json, schedule, time
import http.server
import threading
from queue import Queue
from urllib.parse import urlparse, parse_qs

q = Queue()
worker = edge()
camera = device()

class HTTPRequestHandler(http.server.BaseHTTPRequestHandler):
    def __init__(self, request, client_address, server):
        self.qu = server.qu
        http.server.BaseHTTPRequestHandler.__init__(self, request, client_address, server)

    def do_GET(self):
        self.response(200, 'hello')

    def response(self, status_code, body):
        self.send_response(status_code)

        parsed_path = urlparse(self.path)
        data = parse_qs(parsed_path.query)

        self.send_header('Content-type', 'text/plain; charset-utf-8')
        self.end_headers()

        # insert the data in queue
        self.qu.put(data)


def main():
    # create thread
    thread = threading.Thread(target=HTTPserver, args=(q, ))
    thread.start()

    #
    schedule.every().second.do(jsonEncryption)

    while True:
        schedule.run_pending()
        time.sleep(1)

def HTTPserver(qu):
    ADDRESS = '192.168.0.2', 8000
    listener = http.server.HTTPServer(ADDRESS, HTTPRequestHandler)
    listener.qu = qu
    listener.serve_forever()

def jsonEncryption():
    # collaboration control
    data = {
        "terresult" : ['1'],
        "result" : ['2'],
        "camera": ['3']
    }
    if q.qsize() > 0:
        data = q.get()

    if data['terresult'][0] == '192.168.0.2':
        camera.terminateDevice(data['camera'][0])
    elif data['result'][0] == '192.168.0.2':
        camera.createDevice(data['camera'][0])

    # context extraction
    context = extraction()
    # regular formatting
    value = formatting(context)

    with open('context.json', 'w', encoding="utf-8") as make_file:
        json.dump(value, make_file, ensure_ascii=False, indent="\t")
    contextShare(context)

def contextShare(data):
    params = data
    response = requests.get('http://192.168.0.5:8000', params=params)
    # print(data)

def extraction():
    edgeData = worker.edgeExtraction()
    deviceData = camera.deviceExtraction()
    deviceData.update(edgeData)
    return deviceData

def formatting(data):
    print(data)
    result = {
        "name" : data['name'],
        "EdgeServer" : {
            "netAddress" : data['netAddress'],
            "CPU" : {
                "cpuClock" : data['cpuClock'],
                "cpuUsage" : data['cpuUsage'],
                "cpuCore" : data['cpuCore'],
                "cpuOccupancy" : data['cpuOccupancy']
            },
            "RAM" : {
                "totalMemory" : data['totalMemory'],
                "freeMemory" : data['freeMemory'],
                "memoryOccupancy" : data['memoryOccupancy'],
            },
            "Storage" : {
                "totalDisk" : data['totalDisk'],
                "freeDisk" : data['freeDisk'],
                "diskOccuapncy" : data['diskOccupancy']
            },
            "connectedDevice" : len(data['videoQuality'])
        },
        "Device" : {
            "cameraIp":data['connectedDevice'],
            "videoQuality" : data['videoQuality'],
            "videoRate" : data['videoRate'],
            "deviceGPS" : {
                "latitude" : data['latitude'],
                "longitude" : data['longitude']
            }
        }
    }

    return result

if __name__ == "__main__":
    main()

