/*
 * Licensed to the Apache Software Foundation (ASF) under one
 * or more contributor license agreements.  See the NOTICE file
 * distributed with this work for additional information
 * regarding copyright ownership.  The ASF licenses this file
 * to you under the Apache License, Version 2.0 (the
 * "License"); you may not use this file except in compliance
 * with the License.  You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing,
 * software distributed under the License is distributed on an
 * "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
 * KIND, either express or implied.  See the License for the
 * specific language governing permissions and limitations
 * under the License.
 */

package org.apache.iotdb.db.query.expression.binary;

import org.apache.iotdb.db.query.expression.Expression;
import org.apache.iotdb.db.query.expression.ExpressionType;
import org.apache.iotdb.db.query.udf.core.reader.LayerPointReader;
import org.apache.iotdb.db.query.udf.core.transformer.ArithmeticBinaryTransformer;
import org.apache.iotdb.db.query.udf.core.transformer.ArithmeticDivisionTransformer;
import org.apache.iotdb.tsfile.utils.ReadWriteIOUtils;

import java.nio.ByteBuffer;

public class DivisionExpression extends BinaryExpression {

  public DivisionExpression(Expression leftExpression, Expression rightExpression) {
    super(leftExpression, rightExpression);
  }

  @Override
  protected ArithmeticBinaryTransformer constructTransformer(
      LayerPointReader leftParentLayerPointReader, LayerPointReader rightParentLayerPointReader) {
    return new ArithmeticDivisionTransformer(
        leftParentLayerPointReader, rightParentLayerPointReader);
  }

  @Override
  protected String operator() {
    return "/";
  }

  public static DivisionExpression deserialize(ByteBuffer buffer) {
    boolean isConstantOperandCache = ReadWriteIOUtils.readBool(buffer);
    DivisionExpression divisionExpression =
        new DivisionExpression(
            ExpressionType.deserialize(buffer), ExpressionType.deserialize(buffer));
    divisionExpression.isConstantOperandCache = isConstantOperandCache;
    return divisionExpression;
  }

  @Override
  public void serialize(ByteBuffer byteBuffer) {
    ExpressionType.Division.serialize(byteBuffer);
    super.serialize(byteBuffer);
  }
}
