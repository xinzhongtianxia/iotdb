# import argparse
# import datetime
# import random
#
# import numpy
# import pandas as pd
# import time
#
# from iotdb.Session import Session
#
# from iotdb.utils.IoTDBConstants import TSDataType
# from iotdb.utils.Tablet import Tablet
#
# # from mertic.utils.iotdb_helper import resultset_to_pandas
# # from mertic.common import setting
# from datetime import datetime
# import time
#
# def insertRecordData():
#     # session = setting.get_IoTDB_session()
#     ip = "127.0.0.1"
#     port_ = "6667"
#     username_ = "root"
#     password_ = "root"
#     session = Session(ip, port_, username_, password_, fetch_size=1024, zone_id="UTC+8")
#     session.open(False)
#     listtablet = []
#     for i in range(2000, 4000):
#         sgnum = int(i) % 8
#         k = 0
#         time = 1621250000 + i
#         json_body = [
#         ]
#         tsd=[]
#         for t in range(10080):
#             k = k + 1
#             time = 1621250000 + k * 60
#             subtsd = []
#
#             subtsd.append(int(time*1000))
#             subtsd.append(random.uniform(-2, 4))
#             subtsd.append(True)
#             tsd.append(subtsd)
#
#         # print(tsd[:,0])
#         # break
#         tsd=numpy.array(tsd)
#         device_id = "root.sg" + str(sgnum) + "." + str(i)
#         measurements = [setting.LABEL_TSD_VALUE, setting.LABEL_TSD_ISTRUE]
#         data_types = [TSDataType.FLOAT, TSDataType.BOOLEAN]
#         values = numpy.array(tsd)[:, 1:]
#         times = [int(x) for x in tsd[:, 0]]
#         tablet=Tablet(device_id,measurements,data_types,values,times)
#
#         listtablet.append(tablet)
#
#         session.insert_tablets(listtablet)
#         listtablet=[]
#
#         # session.insert_records(["root.sg"+str(sgnum)+"."+str(i)]*len(tsd),
#         #                     [int(x) for x in tsd[:,0]],
#         #                     [[setting.LABEL_TSD_VALUE, setting.LABEL_TSD_ISTRUE]]*len(tsd),
#         #                     [[TSDataType.FLOAT, TSDataType.BOOLEAN]]*len(tsd),
#         #                     numpy.array(tsd)[:,1:])
#
#     session.close()
#
#
#
# def testiotdb():
#     session = setting.get_IoTDB_session()
#     session.open(False)
#     metric_meta_data = session.execute_query_statement(
#         "select metricID, LastUpdateTime, grain, LastTimeofLocal from root.meta")
#     metric_meta_data = resultset_to_pandas(metric_meta_data)
#     del metric_meta_data['Time']
#     metric_meta_data.columns = [setting.LABEL_METRIC_ID, setting.LABEL_METRIC_LASTUPDATETIME, setting.LABEL_TSD_GRAIN,
#                                 setting.LABEL_METRIC_LASTTIMEOFLOCAL]
#     session.close()
# def queryData():
#
#     for i in range(2000,4000):
#         session = setting.get_IoTDB_session()
#         session.open(False)
#         sgnum = int(i) % 8
#
#         metric_meta_data = session.execute_query_statement(
#             "select time,value,is_true from root.sg"+str(sgnum)+"."+str(i))
#         # metric_meta_data = resultset_to_pandas(metric_meta_data)
#         # print(metric_meta_data)
#         print(i)
#         session.close()
#
# if __name__ == '__main__':
#     #args = parse_args()
#     #main(host=args.host, port=args.port)
#     #insertData()
#     #queryData(0,2000,1619193180000,1619193180000)
#     a = datetime.now()  # 获得当前时间
#     insertRecordData()
#     b = datetime.now()  # 获取当前时间
#     durn = (b - a).seconds  # 两个时间差，并以秒显示出来
#     print(durn)
#     print("--------")