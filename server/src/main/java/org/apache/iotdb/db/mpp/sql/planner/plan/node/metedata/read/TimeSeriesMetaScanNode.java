package org.apache.iotdb.db.mpp.sql.planner.plan.node.metedata.read;

import org.apache.iotdb.db.metadata.path.PartialPath;
import org.apache.iotdb.db.mpp.sql.planner.plan.node.PlanNode;
import org.apache.iotdb.db.mpp.sql.planner.plan.node.PlanNodeId;

import java.util.Arrays;
import java.util.List;

import static org.apache.iotdb.commons.conf.IoTDBConstant.COLUMN_ATTRIBUTES;
import static org.apache.iotdb.commons.conf.IoTDBConstant.COLUMN_STORAGE_GROUP;
import static org.apache.iotdb.commons.conf.IoTDBConstant.COLUMN_TAGS;
import static org.apache.iotdb.commons.conf.IoTDBConstant.COLUMN_TIMESERIES;
import static org.apache.iotdb.commons.conf.IoTDBConstant.COLUMN_TIMESERIES_ALIAS;
import static org.apache.iotdb.commons.conf.IoTDBConstant.COLUMN_TIMESERIES_COMPRESSION;
import static org.apache.iotdb.commons.conf.IoTDBConstant.COLUMN_TIMESERIES_DATATYPE;
import static org.apache.iotdb.commons.conf.IoTDBConstant.COLUMN_TIMESERIES_ENCODING;

public class TimeSeriesMetaScanNode extends MetaScanNode {

  private String key;
  private String value;
  private boolean isContains;

  // if is true, the result will be sorted according to the inserting frequency of the timeseries
  private boolean orderByHeat;

  public TimeSeriesMetaScanNode(
      PlanNodeId id,
      PartialPath partialPath,
      String key,
      String value,
      int limit,
      int offset,
      boolean orderByHeat,
      boolean isContains,
      boolean isPrefixPath) {
    super(id, partialPath, limit, offset, isPrefixPath);
    this.key = key;
    this.value = value;
    this.orderByHeat = orderByHeat;
    this.isContains = isContains;
  }

  public String getKey() {
    return key;
  }

  public void setKey(String key) {
    this.key = key;
  }

  public String getValue() {
    return value;
  }

  public void setValue(String value) {
    this.value = value;
  }

  public boolean isContains() {
    return isContains;
  }

  public void setContains(boolean contains) {
    isContains = contains;
  }

  public boolean isOrderByHeat() {
    return orderByHeat;
  }

  public void setOrderByHeat(boolean orderByHeat) {
    this.orderByHeat = orderByHeat;
  }

  @Override
  public List<PlanNode> getChildren() {
    return null;
  }

  @Override
  public void addChild(PlanNode child) {}

  @Override
  public PlanNode clone() {
    return null;
  }

  @Override
  public PlanNode cloneWithChildren(List<PlanNode> children) {
    return null;
  }

  @Override
  public int allowedChildCount() {
    return NO_CHILD_ALLOWED;
  }

  @Override
  public List<String> getOutputColumnNames() {
    return Arrays.asList(
        COLUMN_TIMESERIES,
        COLUMN_TIMESERIES_ALIAS,
        COLUMN_STORAGE_GROUP,
        COLUMN_TIMESERIES_DATATYPE,
        COLUMN_TIMESERIES_ENCODING,
        COLUMN_TIMESERIES_COMPRESSION,
        COLUMN_TAGS,
        COLUMN_ATTRIBUTES);
  }
}
