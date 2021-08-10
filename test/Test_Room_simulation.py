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
Sensor_flag = True

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


def record_sensor(SN,D,T,test_type,sleeptime = 10):
    file = get_file_name(SN,D,T,test_type)
    file = os.path.join(file,"sensor_data.csv")
    # print(file, "record_sensor")
    count = 0
    while thread_flag:
        count = count +1
        with open(file, "a+", newline="") as f:
            writer = csv.writer(f, delimiter=',', quoting=csv.QUOTE_NONE)
            now = datetime.now().strftime("%H:%M:%S")
            h = 55 + (random()*10.0)
            t = 21 + (random() * 2.0)
            # print(now, t,h)
            writer.writerow([now, t,h])
        sleep(sleeptime)
        if count > 32:
            break


state_dic = {
    "1": "Testing",
    "2": "Idle",
    "3": "Stop"
}


def create_folder(SN,D, T, type):
    if type == "GRAVI" or type == "SINGLE" or type == "AUTO" or type == "MICRO":
        if not os.path.exists('../results/{}/{}'.format(D, SN)):
            os.makedirs('../results/{}/{}'.format(D, SN))
        if os.path.exists('../results/{}/{}.csv'.format(D, SN)):
            os.rename('../results/{}/{}.csv'.format(D, SN),'../results/{}/{}_{}.csv'.format(D, SN, T))
    elif type == "FIXED":
        if not os.path.exists('../results/{}/{}/fixed_{}'.format(D, SN, T)):
            os.makedirs('../results/{}/{}/fixed_{}'.format(D, SN, T))
        if os.path.exists('../results/{}/{}.csv'.format(D, SN)):
            os.rename('../results/{}/{}.csv'.format(D, SN),'../results/{}/{}_{}.csv'.format(D, SN, T))
    elif type == "INCREMENT":
        if not os.path.exists('../results/{}/{}/increment_{}'.format(D, SN, T)):
            os.makedirs('../results/{}/{}/increment_{}'.format(D, SN, T))
        if os.path.exists('../results/{}/{}.csv'.format(D, SN)):
            os.rename('../results/{}/{}.csv'.format(D, SN),'../results/{}/{}_{}.csv'.format(D, SN, T))
    else:
        # print("get_file_name(SN,D, T, type)")
        raise IndexError


def get_file_name(SN,D, T, type):
    if type == "GRAVI" or type == "SINGLE" or type =="AUTO" or type =="MICRO":
        file_name = "../results/{}/{}/".format(D, SN)
    elif type == "FIXED":
        file_name = "../results/{}/{}/fixed_{}/".format(D, SN, T)
    elif type == "INCREMENT":
        file_name = "../results/{}/{}/increment_{}/".format(D, SN, T)
    else:
        # print("get_file_name(SN,D, T, type)")
        raise IndexError
    return file_name


def creat_file(SN,D,T,test_type):
    file = get_file_name(SN, D, T, test_type)
    # print(file, "creat_file")
    create_folder(SN, D, T, test_type)
    files = []
    for v in [10,20,100]:
        fn = file + str(v) + ".csv"
        files.append(fn)
        with open(fn, "a+", newline="") as f:
            writer = csv.writer(f, delimiter=',', quoting=csv.QUOTE_NONE)
            count = 0
            while True:
                if count >60:
                    break
                count = count + 1
                now = datetime.now().strftime("%H:%M:%S")

                t = 21 + (random() * 2.0)
                h1 = 55 + (random() * 10.0)
                h2 = 55 + (random() * 10.0)
                h3 = 55 + (random() * 10.0)
                h4 = 55 + (random() * 10.0)
                h5 = 55 + (random() * 10.0)
                h6 = 55 + (random() * 10.0)
                h7 = 55 + (random() * 10.0)
                h8 = 55 + (random() * 10.0)
                h9 = 55 + (random() * 10.0)
                # print(now, t, h1,h2,h3,h4,h5,h6,h7,h8,h9)
                writer.writerow([now, t, h1,h2,h3,h4,h5,h6,h7,h8,h9])
                sleep(1.9)
    files.append(file + "sensor_data.csv")
    # print(files)
    csv.register_dialect('myDialect', delimiter="/", quoting=csv.QUOTE_NONE)
    with open(file[:-16] + ".csv", 'w', newline='') as f:
        writer = csv.writer(f, delimiter=',', quoting=csv.QUOTE_NONE)
        for space in range(2):
            writer.writerow('')
        for file in files:
            f = open(file, 'r', newline='')
            csv_f = csv.reader(f)
            writer.writerow({file.upper()})
            if "sensor" in file:
                writer.writerow(["Time", "Temp(C)", "Humidity(%)"])
            for row in csv_f:
                writer.writerow(row)
            for space in range(3):
                writer.writerow('')
    # print("Created file:", file[:-16] + ".csv")
    pass


if __name__ == '__main__':
    # TH = Thread(target=record_sensor)
    # TH.start()

    while True:
        SN = "P1KS20200110" + str(randint(10,50))
        test_type = "FIXED"
        D = datetime.now().strftime("%Y_%m_%d")
        T = datetime.now().strftime('%H_%M_%S')
        create_folder(SN,D,T,test_type)

        thread_flag = True
        TH2 = Thread(target=creat_file,args=[SN,D,T,test_type])
        TH2.start()

        TH = Thread(target=record_sensor, args=[SN,D,T,test_type])
        TH.start()

        res = load_config_(config_file)
        try:
            time_delay_count = 1
            while True:
                time_delay_count = time_delay_count + 1
                room_numbr = randint(1,2)
                fixture_numbr = randint(1, 26)
                sleep(1)
                # res["flags"]["Room" + str(room_numbr)]["F" + str(fixture_numbr)] = [" "," "," "]
                res["flags"]["Room" + str(room_numbr)]["F" + str(fixture_numbr)][0] = state_dic[str(randint(1,3))]
                # res["flags"]["Room" + str(room_numbr)]["F" + str(fixture_numbr)][1] = str(21 + round(random()*2,2))
                # res["flags"]["Room" + str(room_numbr)]["F" + str(fixture_numbr)][2] = str(55 + round(random()*3,2))
                save_config_(config_file,res)
                if time_delay_count > 320:
                    break
            thread_flag = False
            TH2.join()
            TH.join()
        except Exception as e:
            thread_flag= False
            print(e)
        finally:
            thread_flag= False



