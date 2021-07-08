# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
#

# Uncomment the following line to use apache-iotdb module installed by pip3

from iotdb.Session import Session
from iotdb.utils.IoTDBConstants import TSDataType, TSEncoding, Compressor
from iotdb.utils.Tablet import Tablet

# creating session connection.
ip = "127.0.0.1"
port_ = "6667"
username_ = "root"
password_ = "root"
session = Session(ip, port_, username_, password_, fetch_size=1024, zone_id="UTC+8")
session.open(False)

# set and delete storage groups
session.set_storage_group("root.sg_test_01")
session.set_storage_group("root.sg_test_02")
session.set_storage_group("root.sg_test_03")
session.set_storage_group("root.sg_test_04")
session.delete_storage_group("root.sg_test_02")
session.delete_storage_groups(["root.sg_test_03", "root.sg_test_04"])

# setting time series.
session.create_time_series(
    "root.sg_test_01.d_01.s_01", TSDataType.BOOLEAN, TSEncoding.PLAIN, Compressor.SNAPPY
)
session.create_time_series(
    "root.sg_test_01.d_01.s_02", TSDataType.INT32, TSEncoding.PLAIN, Compressor.SNAPPY
)
session.create_time_series(
    "root.sg_test_01.d_01.s_03", TSDataType.INT64, TSEncoding.PLAIN, Compressor.SNAPPY
)

# setting multiple time series once.
ts_path_lst_ = [
    "root.sg_test_01.d_01.s_04",
    "root.sg_test_01.d_01.s_05",
    "root.sg_test_01.d_01.s_06",
    "root.sg_test_01.d_01.s_07",
    "root.sg_test_01.d_01.s_08",
    "root.sg_test_01.d_01.s_09",
]
data_type_lst_ = [
    TSDataType.FLOAT,
    TSDataType.DOUBLE,
    TSDataType.TEXT,
    TSDataType.FLOAT,
    TSDataType.DOUBLE,
    TSDataType.TEXT,
]
encoding_lst_ = [TSEncoding.PLAIN for _ in range(len(data_type_lst_))]
compressor_lst_ = [Compressor.SNAPPY for _ in range(len(data_type_lst_))]
session.create_multi_time_series(
    ts_path_lst_, data_type_lst_, encoding_lst_, compressor_lst_
)

# delete time series
session.delete_time_series(
    [
        "root.sg_test_01.d_01.s_07",
        "root.sg_test_01.d_01.s_08",
        "root.sg_test_01.d_01.s_09",
    ]
)

# checking time series
print(
    "s_07 expecting False, checking result: ",
    session.check_time_series_exists("root.sg_test_01.d_01.s_07"),
)
print(
    "s_03 expecting True, checking result: ",
    session.check_time_series_exists("root.sg_test_01.d_01.s_03"),
)

# insert one record into the database.
measurements_ = ["s_01", "s_02", "s_03", "s_04", "s_05", "s_06"]
values_ = [False, 10, 11, 1.1, 10011.1, "test_record"]
data_types_ = [
    TSDataType.BOOLEAN,
    TSDataType.INT32,
    TSDataType.INT64,
    TSDataType.FLOAT,
    TSDataType.DOUBLE,
    TSDataType.TEXT,
]

import time

st = time.perf_counter()
last_time = st
total_count = 1_000_000

for i in range(total_count):
    if i % 10000 == 0:
        now = time.perf_counter()
        print("write %d, use time: %.3f" % (i, now - last_time))
        last_time = now
    session.insert_record("root.sg_test_01.d_01", i, measurements_, data_types_, values_)
end = time.perf_counter()
# close session connection.
session.close()

print("All executions done!!")
print("write %d, total time: %.3f" % (total_count, end - st))
