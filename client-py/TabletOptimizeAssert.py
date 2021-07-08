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
from iotdb.utils.IoTDBConstants import TSDataType, TSEncoding, Compressor, UseNew
from iotdb.utils.Tablet import Tablet
import random
import numpy as np
from numba import jit

# creating session connection.
ip = "127.0.0.1"
port_ = "6667"
username_ = "root"
password_ = "root"
session = Session(ip, port_, username_, password_, fetch_size=1024, zone_id="UTC+8")
session.open(False)
import time

# parameters for test
row_size = 10000
column_size = 2000


measurements_ = ["s_01", "s_02", "s_03", "s_04", "s_05", "s_06"]
data_types_ = [
    TSDataType.BOOLEAN,
    TSDataType.INT32,
    TSDataType.INT64,
    TSDataType.FLOAT,
    TSDataType.DOUBLE,
    TSDataType.TEXT,
]
one_value = [False, 10, 11, 1.1, 10011.1, "test_record"]

insert_cost = 0
st = time.perf_counter()
for i in range(0, column_size):
    device_id = "root.sg%d.%d" % (i % 8, i)
    timestamps_ = []
    values_ = []
    for t in range(0, row_size):
        timestamps_.append(t)
        # values_.append([-2 + 6 * random.random(), True])
        values_.append(one_value)

    tablet_ = Tablet(device_id, measurements_, data_types_, values_, timestamps_)
    cost_st = time.perf_counter()
    session.insert_tablet(tablet_)
    insert_cost += time.perf_counter() - cost_st

end = time.perf_counter()
print("use time: %.3f" % (end - st))
print("insert time: %.3f" % insert_cost)
print("All executions done!!")
# assert
for i in range(0, column_size):
    device_id = "root.sg%d.%d" % (i % 8, i)

    session_data_set = session.execute_query_statement("select * from " + device_id)
    session_data_set.set_fetch_size(row_size)
    while session_data_set.has_next():
        print(session_data_set.next())
    session_data_set.close_operation_handle()

session.close()

print("Assert successfully")
