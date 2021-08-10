import os
import time
import requests
from urllib3 import encode_multipart_formdata
from typing import List
import datetime
from datetime import datetime


THIS_DIR = os.path.abspath(os.path.dirname(__file__))
RESULTS_DIR = os.path.abspath(os.path.dirname(THIS_DIR))

file_list = os.listdir(RESULTS_DIR)
file_list.pop()
# print(file_list)

url = "http://127.0.0.1:8000/VQ1/file/"
headers = {
            'accept': 'application/json'
            }


def get_all_files_list():
    file_path_list = []
    for f in file_list:
        for root,dirs,files in os.walk(os.path.join(RESULTS_DIR,f)):
            if len(file_list) > 0:
                for fc in files:
                    file_path_list.append(os.path.join(root,fc))
    return file_path_list


def get_all_sensor_data_files():
    file_path_list = []
    for f in file_list:
        for root,dirs,files in os.walk(os.path.join(RESULTS_DIR,f)):
            if len(file_list) > 0:
                for fc in files:
                    if fc.endswith('sensor_data.csv'):
                        file_path_list.append(os.path.join(root,fc))
    return file_path_list


def get_today_files_list():
    D = datetime.now().strftime("%Y_%m_%d")
    file_path_list = []
    for f in file_list:
        for root,dirs,files in os.walk(os.path.join(RESULTS_DIR,f)):
            if len(file_list) > 0:
                for fc in files:
                    # print(fc)
                    if D in root:
                        file_path_list.append(os.path.join(root, fc))
    return file_path_list


def updated_files_list():
    with open('file.txt','r') as f:
        updated_files_list = f.readlines()
    for i in range(len(updated_files_list)):
        updated_files_list[i] = updated_files_list[i].strip()
    return updated_files_list


def upload_file(file_path:str):
    filename = file_path.split("results\\")[1]
    local_file_path = file_path
    with open(file_path, "r") as f:
        data = {}
        data["filestream"] = (local_file_path, f.read())
        encode_data = encode_multipart_formdata(data)
        data = encode_data[0]
        headers['Content-Type'] = encode_data[1]
        params = {"filename": filename}
        res = requests.post(url=url, headers=headers, data=data, params=params)
    return res


def upload_files_list(files_list:List):
    updated_files = updated_files_list()
    with open("file.txt","a+") as f:
        for i in files_list:
            if i in updated_files:
                print("{} is a not new file".format(i))
            else:
                res = upload_file(i)
                if res.status_code is 200:
                    print("{} upload ok".format(i))
                    f.write(i + "\n")



def update_new_files_to_server():
    local_files = get_all_files_list()
    updated_files = updated_files_list()
    print(len(local_files))
    print(len(updated_files))
    files_list_need_update = list(set(local_files).difference(set(updated_files)))
    files_list_need_different = list(set(updated_files).difference(set(local_files)))
    print(files_list_need_update)
    print(files_list_need_different)
    upload_files_list(files_list_need_update)


def update_today_files_to_server():
    files_list = get_today_files_list()
    upload_files_list(files_list)
    print("we create {} files today".format(len(files_list)))




# update_new_files_to_server()

update_today_files_to_server()

