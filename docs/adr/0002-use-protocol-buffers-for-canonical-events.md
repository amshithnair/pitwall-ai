# 0002. Use Protocol Buffers for Canonical Events

* Status: accepted
* Deciders: Amshith Nair
* Date: 2026-07-21

Technical Story: Milestone 0.5 - Canonical Event Architecture

## Context and Problem Statement

The platform relies on a Canonical Event Schema to normalize data from various external providers. This data must be streamed at high velocity (up to 10Hz per car for telemetry) across Redis Streams to multiple downstream services (written in Python, Go, Node.js, and TypeScript/Browser). We need a serialization format that ensures strict schema adherence, supports backward compatibility for the Replay Engine, and is compact over the wire.

## Decision Drivers

* High-frequency telemetry demands small payload sizes to prevent network and Redis memory bottlenecks.
* Multi-language microservices require a unified, strictly typed schema contract.
* The Replay Engine requires backward compatibility to replay historical races that were recorded under older schema versions.

## Considered Options

* JSON Schema
* Protocol Buffers (Protobuf)
* Apache Avro
* FlatBuffers

## Decision Outcome

Chosen option: "Protocol Buffers", because it offers a mature ecosystem for cross-language generation, strict typing, excellent backward compatibility guarantees out-of-the-box, and a highly compact binary format. While Avro is great for Hadoop/Kafka ecosystems, Protobuf integrates seamlessly with gRPC (if we adopt it later) and has better frontend (protobuf.js / grpc-web) support.

### Positive Consequences

* Strict contracts between services prevent "bad data" crashes downstream.
* Significantly reduced bandwidth and Redis memory usage compared to JSON.
* Auto-generated classes in Python, Go, and TypeScript.

### Negative Consequences

* Binary format makes debugging via `redis-cli` more difficult without a deserialization proxy.
* Slightly higher learning curve for new developers compared to plain JSON.
