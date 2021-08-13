import csv
import os
import time
import requests
from urllib3 import encode_multipart_formdata
from typing import Dict
import datetime
from datetime import datetime
from pydantic import BaseModel
import json


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


class file_format(BaseModel):
    fpath: str=None
    fsiez: int=None
    fmtime:float=None


class FileManager(object):
    def __init__(self,ip="127.0.0.1"):
        self.ip = ip
        self.this_dir = os.path.abspath(os.path.dirname(__file__))
        self.results_path = os.path.abspath(os.path.dirname(self.this_dir))
        self.folder_list = []
        self.log_file = os.path.join(self.this_dir,'log.json')
        self.headers = {'accept': 'application/json'}
        self.time_durtion = 40
        self.updatefolder_list()



    def updatefolder_list(self):
        self.folder_list = os.listdir(self.results_path)
        self.folder_list.pop()
        return self.folder_list


    def get_all_files_from_local(self):
        file_path_list = {}
        for f in self.folder_list:
            for root, dirs, files in os.walk(os.path.join(self.results_path, f)):
                if len(self.folder_list) > 0:
                    for fc in files:
                        file_path = os.path.join(root, fc)
                        file_inf = file_path.split("results\\")
                        file_local = file_format()
                        file_local.fpath = file_path
                        file_local.fsiez = os.path.getsize(file_path)
                        file_local.fmtime = os.path.getmtime(file_path)
                        file_path_list[file_inf[1]] = file_local
        return file_path_list


    def get_day_files_from_local(self,day):
        D = day
        today_dir = os.path.join(self.results_path, D)
        file_path_list = {}
        for root, dirs, files in os.walk(today_dir):
            if len(today_dir) > 0:
                for fc in files:
                    file_path = os.path.join(root, fc)
                    file_inf = file_path.split("results\\")
                    file_local = file_format()
                    file_local.fpath = file_path
                    file_local.fsiez = os.path.getsize(file_path)
                    file_local.fmtime = os.path.getmtime(file_path)
                    file_path_list[file_inf[1]] = file_local
        return file_path_list


    def get_all_files_from_log(self):
        log = load_config_(self.log_file)
        return log


    def get_fixture_status(self):
        D = datetime.now().strftime("%Y_%m_%d")
        today_dir = os.path.join(self.results_path,D)
        later_file = time.time()
        for root, dirs, files in os.walk(today_dir):
            for f in files:
                if 'sensor' in f:
                    file_path = os.path.join(root,f)
                    fmtime = os.path.getmtime(file_path)
                    time_interval =later_file - fmtime
                    # print(file_path)
                    if (time_interval) < self.time_durtion:
                        return ("Testing",file_path)
                    elif (time_interval) > self.time_durtion and (time_interval) < self.time_durtion *6:
                        return ("Stop",file_path)
                    else:
                        pass
        return ("Idle", None)

    def upload_file(self, file_path:str):
        url = "http://{}:8000/VQ1/file/".format(self.ip)
        filename = file_path.split("results\\")[1]
        local_file_path = file_path
        with open(file_path, "r") as f:
            data = {}
            data["filestream"] = (local_file_path, f.read())
            encode_data = encode_multipart_formdata(data)
            data = encode_data[0]
            headers = self.headers
            headers['Content-Type'] = encode_data[1]
            params = {"filename": filename}
            res = requests.post(url=url, headers=headers, data=data, params=params)
        if res.status_code is 200:
            print("{} upload done".format(file_path))
            log = self.get_all_files_from_log()
            log[filename] = {
                "filepath":file_path,
                "fsize":os.path.getsize(file_path),
                "fmtime":os.path.getmtime(file_path)
            }
            save_config_(self.log_file,log)
        return res


    def get_environment_status(self,filepath:str):
        with open(filepath,"r") as f:
            csvreader = csv.reader(f, delimiter=',', quoting=csv.QUOTE_NONE)
            start_time = None
            last_time = None
            temperature = []
            humidity = []
            count = 0
            for i in csvreader:
                if csvreader.line_num is 1:
                    start_time = i[0]
                last_time = i[0]
                temperature.append(float(i[1]))
                humidity.append(float(i[2]))
                count = csvreader.line_num
        return (start_time,last_time,sum(temperature)/count,sum(humidity)/count)


    def update_file_to_server(self,day=None):
        if day is None:
            local_files = self.get_all_files_from_local()
        else:
            local_files = self.get_day_files_from_local(day)
        log_files = self.get_all_files_from_log()
        for i in local_files:
            file_detail = log_files.get(i)
            # print(file_detail)
            if file_detail is None:
                self.upload_file(local_files[i].fpath)
            elif local_files[i].fsiez > file_detail["fsize"]:
                self.upload_file(local_files[i].fpath)
            else:
                pass

    def update_status_to_server(self, room,fixture):
        # url = "http://127.0.0.1:8000/VQ1/environment?room=1&Fixture=F1&status=Testing&temp=21&humidity=55"
        url = "http://{}:8000/VQ1/environment".format(self.ip)
        res = self.get_status()
        params = {"room": room,
                  "Fixture":fixture,
                  "status":res[0],
                  "temp":res[1],
                  "humidity":res[2]}
        res = requests.get(url=url,headers=self.headers,params=params,)
        return res

    def get_status(self):
        fixture_status = self.get_fixture_status()
        if "Idle" in fixture_status:
            return [fixture_status[0],None,None]
        else:
            env_status = self.get_environment_status(fixture_status[1])
            return [fixture_status[0], round(env_status[2],2), round(env_status[3],2)]


# fm = FileManager()
# fm.update_file_to_server()


if __name__ == '__main__':
    # ip = input("请输入IP地址:")
    # room = input("请输入房间号:")
    # fixture = input("请输入工装号:")

    ip = "127.0.0.1"
    room = 1
    fixture = "f5"

    fm = FileManager(ip)
    # fm.upload_file("C:\\Users\\opentrons\\Desktop\\Opentrons_Server\\results\\2021_08_12\\P1KS2020011021\\fixed_11_19_06\sensor_data.csv")
    fm.update_file_to_server()
    while True:
        try:
            D = datetime.now().strftime("%Y_%m_%d")
            fm.update_file_to_server(day=D)
            res = fm.update_status_to_server(room=int(room),fixture=fixture.upper())
            print(res)
            time.sleep(5)
        except Exception as e:
            print(e)

