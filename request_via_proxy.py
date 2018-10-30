import platform
import requests as rq
import time,ctypes
def DelayTest():
    with open('./b.txt','r') as f:
        lines = f.readlines()
    targets = []
    for line in lines:
        ip, domain, desc = line.rstrip('\n').split(' ')
        targets.append(['http://'+ip, domain, desc])
    DoTestWin(targets, None, False, False)
    DoTestWin(targets, None, True, False)


def DoTestWin(fileList,headers,useProxy,fullDownload):
    import platform
    Win32 = platform.system() == 'Windows'
    total_size = 0.0
    count = 0
    if useProxy:
        my_proxies = {"http": "socks5://127.0.0.1:8009", "https": "socks5://127.0.0.1:8009"}
    else:
        my_proxies = None
    if Win32:
        freq = ctypes.c_longlong(0)
        t1 = ctypes.c_longlong(0)
        t2 = ctypes.c_longlong(0)
        ctypes.windll.kernel32.QueryPerformanceFrequency(ctypes.byref(freq))
        ctypes.windll.kernel32.QueryPerformanceCounter(ctypes.byref(t1))
    else:
        freq = 1
        t1 = time.time()
    for file in fileList:
        try:
            if fullDownload:
                res = rq.get(file[0], proxies=my_proxies, headers=headers,
                             stream=fullDownload, timeout=30)
                size = len(res.content)
                total_size += size / 1000.0
                count += 1
            else:
                for i in range(0, 100):
                    res=rq.get(file[0], proxies=my_proxies, headers=headers,
                                 stream=fullDownload, timeout=30)
                    count += 1
                    res.close()
        except Exception as e:
            print(e)
        else:
            if count > 0:
                if Win32:
                    ctypes.windll.kernel32.QueryPerformanceCounter(ctypes.byref(t2))
                    t=(t2.value - t1.value) / freq.value
                else:
                    t2 = time.time()
                    t = t2-t1
                if fullDownload:
                    print('Avg Speed:' + str(total_size / t) + 'KB/s with: ' +
                          str(total_size / 1000.0) + 'MB in past ' + str(t) + 's From ' +
                          str(file[1]) + ' which is ' + file[2])
                else:
                    print('Proxy Avg Delay:' + str(1000.0 *t / count) + 'ms In Past ' + str(t) + 's to ' + file[1] + ' in ' + file[2])
                if Win32:
                    ctypes.windll.kernel32.QueryPerformanceCounter(ctypes.byref(t1))
                else:
                    t1 = time.time()
                count = 0
                total_size = 0


def SpeedTestA(ip,useProxy):
        fileList=[]
        for i in range(1,3):
            url = ip+'/dl/16.7z.0'+str(i).zfill(2)
            fileList.append([url, ip, 'httpServer'])
        for i in range(1,6):
            url = ip+'/dl/256.z' + str(i).zfill(2)
            fileList.append([url, ip, 'httpServer'])
        DoTestWin(fileList, None, useProxy, True)


def SpeedTestB(placeHolder,useProxy):
    with open('./a.txt','r') as f:
        lines = f.readlines()
    fileList = []
    for line in lines:
        fileList.append(['http://'+line.rstrip('\n'),'missevan','httpServer'])
    DoTestWin(fileList,{'host':'static.missevan.com'},useProxy,True)


def main():
    #DelayTest()
    SpeedTestA('http://122.112.205.47:80', True)


if __name__ == '__main__':
    main()