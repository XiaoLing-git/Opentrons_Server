import os
import time
import requests
from urllib3 import encode_multipart_formdata


THIS_DIR = os.path.abspath(os.path.dirname(__file__))
RESULTS_DIR = os.path.abspath(os.path.dirname(THIS_DIR))

file_list = os.listdir(RESULTS_DIR)
file_list.pop()
print(file_list)

file_path_list = []
for f in file_list:
    for root,dirs,files in os.walk(os.path.join(RESULTS_DIR,f)):
        # print("Root:", root)
        if len(file_list) > 0:
            for fc in files:
                file_path_list.append(os.path.join(root,fc))



url = "http://127.0.0.1:8000/VQ1/file/"
headers = {
            'accept': 'application/json'
            }

for i in file_path_list:
# i = "C:\\Users\\opentrons\\Desktop\\Opentrons_Server\\results\\2021_08_06\\P1KS2020011049\\fixed_10_06_12\\sensor_data.csv"
    filename = i.split("results\\")[1]
    # print(filename)
    local_file_path = i
    # print(filename,res.content)
    with open(i,"rb") as f:
        data = {}
        data["filestream"] = (local_file_path, f.read())
        encode_data = encode_multipart_formdata(data)
        data = encode_data[0]
        headers['Content-Type'] = encode_data[1]
        params = {"filename": filename}
        res = requests.post(url=url, headers=headers, data=data, params=params)
    print(filename, res.content)
















# url = "http://127.0.0.1:8000/VQ1/file/"
#
# f = open("C:/Users/opentrons/Desktop/Opentrons_Server/results/2021_08_06/P1KS2020011049/fixed_10_06_12/sensor_data.csv",'rb')
#
#
#
#
#
# data = {}
# data["filestream"] = ("sensorsda_data.csv", f.read())
# encode_data = encode_multipart_formdata(data)
# # print(encode_data)
# data = encode_data[0]
#
# headers = {
#         'accept': 'application/json'
#     }
#
# headers['Content-Type'] = encode_data[1]
# print(headers)
#
# res = requests.post(url = url, headers =headers, data=data)
#
# print(res.content)


# data = data.decode().split('\r\n')
# for i in data:
#     print(i)



# for i in headers:
#     print(i)
