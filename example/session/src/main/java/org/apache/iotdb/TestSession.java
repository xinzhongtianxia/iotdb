package org.apache.iotdb;

import java.util.ArrayList;
import java.util.Calendar;
import java.util.Date;
import java.util.List;
import java.util.Random;

import org.apache.iotdb.session.Session;
import org.apache.iotdb.tsfile.file.metadata.enums.TSDataType;
import org.apache.iotdb.tsfile.write.record.Tablet;
import org.apache.iotdb.tsfile.write.schema.IMeasurementSchema;
import org.apache.iotdb.tsfile.write.schema.MeasurementSchema;

public class TestSession {

  public static void main(String[] args) throws Exception {
    Session session = new Session("127.0.0.1", 6667, "root", "root");
    session.open();
//        session.setStorageGroup("root.sestest");
//        session.createTimeseries("root.sestest.wf01.wt01.s0", TSDataType.INT32, TSEncoding.RLE, CompressionType.SNAPPY);
//        session.createTimeseries("root.sestest.wf01.wt01.s1", TSDataType.INT32, TSEncoding.RLE, CompressionType.SNAPPY);
//        session.createTimeseries("root.sestest.wf01.wt01.s2", TSDataType.INT32, TSEncoding.RLE, CompressionType.SNAPPY);

    Date d = new Date();
    Random r = new Random(0);
    long insertCost = 0;
    for (int i = 2000; i < 4000; i++) {
//      Calendar c = Calendar.getInstance();
//      c.setTime(d);
      String deviceId = "root.sg" + i % 8 + "." + i;
//      List<List<String>> measurementsList = new ArrayList<List<String>>();
//      List<List<TSDataType>> typesList = new ArrayList<List<TSDataType>>();
//      List<List<Object>> valuesList = new ArrayList<List<Object>>();
//      List<Long> times = new ArrayList<Long>();
//      List<String> deviceIds = new ArrayList<String>();

      MeasurementSchema mes = new MeasurementSchema("s1", TSDataType.FLOAT);
      MeasurementSchema mes1 = new MeasurementSchema("is_true", TSDataType.BOOLEAN);

      List<IMeasurementSchema> schemas = new ArrayList<>();
      schemas.add(mes);
//      schemas.add(mes1);
      int rowSize = 10080;
//      int rowSize = 5080;
      Tablet ta = new Tablet(deviceId, schemas, rowSize);
      ta.rowSize = rowSize;
      for (int t = 0; t < ta.rowSize; t++) {
//					Random r=new Random();
//					 List<String> measurement = new ArrayList<>();
//					List<Object> values = new ArrayList<>(3);
//		            List<TSDataType> types = new ArrayList<>(3);
//		            times.add(c.getTimeInMillis());
//		            values.add(-2+6*r.nextFloat());
//		            types.add(TSDataType.FLOAT);
//		            values.add(true);
//		            types.add(TSDataType.BOOLEAN);
//		            measurement.add("s1");
//		            measurement.add("is_true");
//		            typesList.add(types);
//		            valuesList.add(values);
//		            deviceIds.add(deviceId);
//		            measurementsList.add(measurement);
//					c.add(Calendar.MINUTE,+i);

//					 List<String> measurement = new ArrayList<>();
//					List<Object> values = new ArrayList<>(3);
//		            List<TSDataType> types = new ArrayList<>(3);
//		           
//		            values.add(-2+6*r.nextFloat());
//		            types.add(TSDataType.FLOAT);
//		            values.add(true);
//		            types.add(TSDataType.BOOLEAN);
//		            measurement.add("s1");
//		            measurement.add("is_true");
//		            typesList.add(types);
//		            valuesList.add(values);
//		            deviceIds.add(deviceId);
//		            measurementsList.add(measurement);
//        ta.addTimestamp(t, c.getTimeInMillis());
        ta.addTimestamp(t, t);
//        ta.addValue("is_true", t, true);
//        ta.addValue("s1", t, -2 + 6 * r.nextFloat());
        ta.addValue("s1", t, -2 + 6 * 0.5f);
//        c.add(Calendar.MINUTE, +1);
      }
      long st = System.nanoTime();
      session.insertTablet(ta, true);
      insertCost += (System.nanoTime() - st);
      //session.insertRecords(deviceIds, times, measurementsList, typesList, valuesList);
    }
    session.close();
    Date d1 = new Date();
    System.out.println(d1.getTime() - d.getTime());
    System.out.println(insertCost / 1000_000);


  }

}
