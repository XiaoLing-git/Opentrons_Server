from ctypes import cdll
import os, json
from typing import Dict
from time import sleep
from random import randint
from random import randrange,random
import csv
from datetime import datetime
from threading import Thread


_sopen = cdll.msvcrt._sopen
_close = cdll.msvcrt._close
_SH_DENYRW = 0x10

thread_flag = True

THIS_DIR = os.path.dirname(__file__)
THIS_DIR = os.path.dirname(THIS_DIR)
config_file = os.path.join(os.path.join(os.path.join(os.path.join(\
    os.path.join(THIS_DIR,"Apps")),"Test_room"),"dependencies"),"configs.json")
print(config_file)


def load_config_(filename: str) -> Dict:
    """This function loads a given config file"""
    try:
        with open(filename, 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        print('Warning: {0} not found'.format(filename))
        data = {}
    except json.decoder.JSONDecodeError:
        print('Error: {0} is corrupt'.format(filename))
        data = {}
    return data


def save_config_(filename: str, data: str) -> Dict:
    """This function saves a given config file with data"""
    try:
        with open(filename, 'w') as file:
            json.dump(
                data, file, sort_keys=True, indent=4, separators=(',', ': ')
            )
    except FileNotFoundError:
        print('Warning: {0} not found'.format(filename))
        data = {}
    except json.decoder.JSONDecodeError:
        print('Error: {0} is corrupt'.format(filename))
        data = {}
    return data


def record_sensor(sleeptime = 20):
    while thread_flag:
        with open(".sensor_data.csv", "a+", newline="") as f:
            writer = csv.writer(f, delimiter=',', quoting=csv.QUOTE_NONE)
            now = datetime.now().strftime("%H:%M:%S")
            h = 55 + (random()*10.0)
            t = 21 + (random() * 2.0)
            print(now, t,h)
            writer.writerow([now, t,h])
        sleep(sleeptime)


state_dic = {
    "1": "Testing",
    "2": "Idle",
    "3": "Stop"
}

if __name__ == '__main__':
    TH = Thread(target=record_sensor)
    TH.start()
    res = load_config_(config_file)
    try:
        while True:
            room_numbr = randint(1,2)
            fixture_numbr = randint(1, 26)
            sleep(1)
            res["flags"]["Room" + str(room_numbr)]["F" + str(fixture_numbr)] = state_dic[str(randint(1,3))]
            save_config_(config_file,res)
    except Exception as e:
        thread_flag= False
        print(e)
    finally:
        thread_flag= False



