import time,os
import subprocess


if __name__ == '__main__':
    file_path = "/home/pi/Opentrons_Server/main.py"
    cmd = 'ps aux|grep python3'
    res = os.popen(cmd,'r')
    res = res.read()
    # print(res)
    if file_path not in res:
        res = os.system("python3 "+file_path)

