# import subprocess
# from operator import methodcaller
#
# def test_SIM():
#     pass
#
# def test_SDcard():
#     pass
#
# def test_reboot():
#     print("reboot test")
#
# def select_test():
#     test_item = {"CheckBox_SIM_test": [0, "test_SIM"],
#                  "CheckBox_SDcard_test": [0, "test_SDcard"],
#                  "CheckBox_reboot_test": [1, "test_reboot"]
#                  }
#     test_list = []
#     for i in test_item:
#         test_flag = test_item[i][0]
#         if test_flag == 1:
#             test_list.append(test_item[i][1])
#         else:
#             pass
#
#     print(test_list)
#     if test_list:
#         for func in test_list:
#             methodcaller(func)
#
# def dev():
#     device_list = subprocess.getoutput("adb get-serialno").strip().split('\n')
#     if len(device_list) == 0:
#         return 0
#     elif len(device_list) == 1 and device_list[0] != "unknown":
#         return device_list[0]
#     else:
#         return 2
#
# if __name__ == '__main__':
#     sim_state_list = {
#         "READY": 1,
#         "LOADED": "1",
#         "NOT_READY": "0",
#         "ABSENT": "0",
#         "UNKNOWN": "0"
#     }
#     print(sim_state_list['READY'] == 1)

# !/usr/bin/env python3
"""PyBluez simple example inquiry.py
Performs a simple device inquiry followed by a remote name request of each
discovered device
Author: Albert Huang <albert@csail.mit.edu>
$Id: inquiry.py 401 2006-05-05 19:07:48Z albert $
"""

# import bluetooth
#
# print("Performing inquiry...")
#
# nearby_devices = bluetooth.discover_devices(duration=8, lookup_names=True,
#                                             flush_cache=True, lookup_class=False)
#
# print("Found {} devices".format(len(nearby_devices)))
#
# for addr, name in nearby_devices:
#     try:
#         print("   {} - {}".format(addr, name))
#     except UnicodeEncodeError:
#         print("   {} - {}".format(addr, name.encode("utf-8", "replace")))
from common.pysql_connect import *

cursor, conn = conn_db()
sql = "update android_testcases set checked=%s where Case_title=%s"
rows = cursor.execute(sql, (1, 'SD卡检测'))
print(rows)
cursor.close()
conn.close()
#
# hello_dict = {'a':'1', 'b':'2', 'c':'3'}
# print(hello_dict.values())
# for i in hello_dict.items():
#     print(i[1])