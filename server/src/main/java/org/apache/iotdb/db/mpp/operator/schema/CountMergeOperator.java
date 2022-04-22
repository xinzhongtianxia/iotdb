/*
 * Licensed to the Apache Software Foundation (ASF) under one
 * or more contributor license agreements.  See the NOTICE file
 * distributed with this work for additional information
 * regarding copyright ownership.  The ASF licenses this file
 * to you under the Apache License, Version 2.0 (the
 * "License"); you may not use this file except in compliance
 * with the License.  You may obtain a copy of the License at
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing,
 * software distributed under the License is distributed on an
 * "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
 * KIND, either express or implied.  See the License for the
 * specific language governing permissions and limitations
 * under the License.
 */
package org.apache.iotdb.db.mpp.operator.schema;

import org.apache.iotdb.db.mpp.operator.Operator;
import org.apache.iotdb.db.mpp.operator.OperatorContext;
import org.apache.iotdb.db.mpp.operator.process.ProcessOperator;
import org.apache.iotdb.db.mpp.sql.planner.plan.node.PlanNodeId;
import org.apache.iotdb.tsfile.file.metadata.enums.TSDataType;
import org.apache.iotdb.tsfile.read.common.block.TsBlock;
import org.apache.iotdb.tsfile.read.common.block.TsBlockBuilder;
import org.apache.iotdb.tsfile.utils.Binary;

import java.util.Arrays;
import java.util.Collections;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

public class CountMergeOperator implements ProcessOperator {

  private final PlanNodeId planNodeId;
  private final OperatorContext operatorContext;
  private boolean isFinished;

  private final List<Operator> children;

  public CountMergeOperator(
      PlanNodeId planNodeId, OperatorContext operatorContext, List<Operator> children) {
    this.planNodeId = planNodeId;
    this.operatorContext = operatorContext;
    this.children = children;
  }

  @Override
  public OperatorContext getOperatorContext() {
    return operatorContext;
  }

  @Override
  public TsBlock next() {
    isFinished = true;
    if (children.get(0) instanceof NodeTimeSeriesCountOperator) {
      return nextWithGroupByLevel();
    }
    return nextWithoutGroupByLevel();
  }

  private TsBlock nextWithoutGroupByLevel() {
    TsBlockBuilder tsBlockBuilder = new TsBlockBuilder(Collections.singletonList(TSDataType.INT32));
    int totalCount = 0;
    for (int i = 0; i < children.size(); i++) {
      TsBlock tsBlock = children.get(i).next();
      int count = tsBlock.getColumn(0).getInt(0);
      totalCount += count;
    }
    tsBlockBuilder.getTimeColumnBuilder().writeLong(0L);
    tsBlockBuilder.getColumnBuilder(0).writeInt(totalCount);
    tsBlockBuilder.declarePosition();
    return tsBlockBuilder.build();
  }

  private TsBlock nextWithGroupByLevel() {
    TsBlockBuilder tsBlockBuilder =
        new TsBlockBuilder(Arrays.asList(TSDataType.TEXT, TSDataType.INT32));
    Map<String, Integer> countMap = new HashMap<>();
    for (int i = 0; i < children.size(); i++) {
      TsBlock tsBlock = children.get(i).next();
      for (int j = 0; j < tsBlock.getPositionCount(); i++) {
        String columnName = tsBlock.getColumn(0).getBinary(j).getStringValue();
        int count = tsBlock.getColumn(1).getInt(j);
        countMap.put(columnName, countMap.getOrDefault(columnName, 0) + count);
      }
    }
    countMap.forEach(
        (column, count) -> {
          tsBlockBuilder.getTimeColumnBuilder().writeLong(0L);
          tsBlockBuilder.getColumnBuilder(0).writeBinary(new Binary(column));
          tsBlockBuilder.getColumnBuilder(1).writeInt(count);
          tsBlockBuilder.declarePosition();
        });
    return tsBlockBuilder.build();
  }

  @Override
  public boolean hasNext() {
    return !isFinished;
  }

  @Override
  public boolean isFinished() {
    return isFinished;
  }
}
