from iotdb.Session import Session
from iotdb.utils.IoTDBConstants import TSDataType, TSEncoding, Compressor

# creating session connection.
ip = "127.0.0.1"
port_ = "6667"
username_ = "root"
password_ = "root"
session = Session(ip, port_, username_, password_, fetch_size=1024, zone_id="UTC+8")
session.open(False)


# setting time series.
session.create_time_series("root.dj.d_01.temperature", TSDataType.FLOAT, TSEncoding.PLAIN, Compressor.SNAPPY)
session.create_time_series("root.dj.d_01.status", TSDataType.BOOLEAN, TSEncoding.PLAIN, Compressor.SNAPPY)

# insert one record into the database.
measurements_ = ["temperature", "status"]
values_ = [19.01, True]
data_types_ = [
    TSDataType.FLOAT,
    TSDataType.BOOLEAN,
]
device_id = "root.dj.d_01"
session.insert_record(device_id, 2, measurements_, data_types_, values_)

session.execute_non_query_statement("insert into root.sg_test_01.wf02.wf01(timestamp, temperature, status) values(now(), 20.00, True)")
session.close()
