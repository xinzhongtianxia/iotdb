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
from iotdb.utils.IoTDBConstants import TSDataType
from iotdb.utils.Tablet import Tablet
import random
import numpy as np
import time


def create_open_session():
    # creating session connection.
    ip = "127.0.0.1"
    port_ = "6667"
    username_ = "root"
    password_ = "root"
    session = Session(ip, port_, username_, password_, fetch_size=1024, zone_id="UTC+8")
    session.open(False)
    return session


def check_count(expect, _session, _sql):
    session_data_set = _session.execute_query_statement(_sql)
    session_data_set.set_fetch_size(1)
    get_count_line = False
    while session_data_set.has_next():
        if get_count_line:
            assert False, "select count return more than one line"
        line = session_data_set.next()
        assert expect == line.get_fields()[0].get_long_value(), "count result error"
        get_count_line = True
    if not get_count_line:
        assert False, "select count has no result"
    session_data_set.close_operation_handle()


def check_query_result(expect, _session, _sql):
    # raise Exception('not implemented')
    session_data_set = _session.execute_query_statement(_sql)
    session_data_set.set_fetch_size(1)
    idx = 0
    while session_data_set.has_next():
        line = session_data_set.next()
        assert str(line) == expect[idx], f"line {idx}: actual {str(line)} != expect ({expect[idx]})"
        idx += 1
    assert idx == len(expect), f"result rows: actual ({idx}) != expect ({len(expect)})"
    session_data_set.close_operation_handle()


def performance_test(data_types=tuple([TSDataType.FLOAT]), use_new=True, valid_result=False, row=10000, col=2000,
                     seed=0):
    session = create_open_session()
    st = time.perf_counter()
    random.seed(a=seed, version=2)
    insert_cost = 0

    VALUES_OF_TYPES = {TSDataType.BOOLEAN: True,
                       TSDataType.DOUBLE: 1.234567,
                       TSDataType.FLOAT: 1.5,
                       TSDataType.INT32: 100,
                       TSDataType.INT64: 123456789098,
                       TSDataType.TEXT: "test_record"}
    FORMAT_CHAR_OF_TYPES = {TSDataType.BOOLEAN: "?",
                            TSDataType.DOUBLE: "d",
                            TSDataType.FLOAT: "f",
                            TSDataType.INT32: "i",
                            TSDataType.INT64: "q",
                            TSDataType.TEXT: str}
    MEASUREMENT_OF_TYPES = {TSDataType.BOOLEAN: "s0",
                            TSDataType.DOUBLE: "s1",
                            TSDataType.FLOAT: "s2",
                            TSDataType.INT32: "s3",
                            TSDataType.INT64: "s4",
                            TSDataType.TEXT: "s5"}

    measurements_ = [MEASUREMENT_OF_TYPES[data_type] for data_type in data_types]

    for i in range(0, col):
        device_id = "root.sg%d.%d" % (i % 8, i)

        if not use_new:
            timestamps_ = []
            values_ = []
            for t in range(0, row):
                timestamps_.append(t)
                value_ = []
                for data_type in data_types:
                    value_.append(VALUES_OF_TYPES[data_type])
                values_.append(value_)
        else:
            timestamps_ = np.zeros(row, dtype='>q')
            values_ = [np.zeros(row, dtype=FORMAT_CHAR_OF_TYPES[data_type]) for data_type in data_types]
            for t in range(0, row):
                timestamps_[t] = t
                for j, data_type in enumerate(data_types):
                    values_[j][t] = VALUES_OF_TYPES[data_type]

        tablet_ = Tablet(device_id, measurements_, data_types, values_, timestamps_, use_new=use_new)
        cost_st = time.perf_counter()
        session.insert_tablet(tablet_)
        insert_cost += time.perf_counter() - cost_st
        if valid_result:
            # query total line
            # print("execute query for validation")
            check_count(row, session, "select count(*) from %s" % device_id)
            expect_values = "\t\t".join([str(VALUES_OF_TYPES[data_type]) for data_type in data_types])
            expect = [str(e) + "\t\t" + expect_values for e in range(row)]
            check_query_result(expect, session, f"select {','.join(measurements_)} from {device_id}")
            # print("query validation have passed")

    session.close()
    end = time.perf_counter()

    print("All executions done!!")
    print("use time: %.3f" % (end - st))
    print("insert time: %.3f" % insert_cost)


valid_result = True
use_new = True
# use_new = False
# performance_test(data_types=tuple([TSDataType.FLOAT]), use_new=use_new, valid_result=valid_result, row=3, col=2)
# performance_test(data_types=tuple([TSDataType.FLOAT]), use_new=True, valid_result=valid_result)

performance_test(
    data_types=tuple([TSDataType.BOOLEAN, TSDataType.FLOAT, TSDataType.DOUBLE, TSDataType.INT32, TSDataType.INT64]),
    use_new=use_new, valid_result=valid_result, row=3, col=3)

# performance_test(data_types=tuple([TSDataType.BOOLEAN, TSDataType.FLOAT, TSDataType.DOUBLE, TSDataType.INT32, TSDataType.INT64]), use_new=True, valid_result=valid_result)
#
# performance_test(data_types=tuple([TSDataType.BOOLEAN, TSDataType.FLOAT, TSDataType.DOUBLE, TSDataType.INT32, TSDataType.INT64, TSDataType.TEXT]), use_new=False, valid_result=valid_result)
# performance_test(data_types=tuple([TSDataType.BOOLEAN, TSDataType.FLOAT, TSDataType.DOUBLE, TSDataType.INT32, TSDataType.INT64, TSDataType.TEXT]), use_new=True, valid_result=valid_result)
