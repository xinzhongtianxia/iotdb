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
package org.apache.iotdb.db.mpp.buffer;

import com.google.common.util.concurrent.ListenableFuture;

import java.nio.ByteBuffer;

public interface SinkHandle {

  /** Get a future that will be completed when the buffer is not full. */
  ListenableFuture<Void> isFull();

  /**
   * Sends a tsBlock to an unpartitioned buffer. If no-more-tsBlocks has been set, the send tsBlock
   * call is ignored. This can happen with limit queries.
   */
  void send(ByteBuffer tsBlock);

  /**
   * Sends a tsBlock to a specific partition. If no-more-tsBlocks has been set, the send tsBlock
   * call is ignored. This can happen with limit queries.
   */
  void send(int partition, ByteBuffer tsBlock);

  /**
   * Notify SinkHandle that no more tsBlocks will be sent. Any future calls to send a tsBlock are
   * ignored.
   */
  void setNoMoreTsBlocks();

  /** close the sink handle, discarding all tsBlocks which may still in memory buffer. */
  void close();

  /**
   * Abort the sink handle, discarding all tsBlocks which may still in memory buffer, but blocking
   * readers. It is expected that readers will be unblocked when the failed query is cleaned up.
   */
  void abort();
}
