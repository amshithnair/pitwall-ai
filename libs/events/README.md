# Protocol Buffers Architecture

This directory (`libs/events/`) contains the Protocol Buffer definitions for the PitWall AI Canonical Event Schema.

## Why Protocol Buffers?
*(See ADR 0002 for full context)*

While JSON is human-readable, PitWall AI requires high-frequency telemetry streaming and strict schema enforcement across multiple microservices (Python, Go, Node.js, frontend).
- **Strong Typing**: Protobuf enforces strict contracts between producers and consumers.
- **Schema Evolution**: Fields can be added or deprecated without breaking older consumers (crucial for replay engine compatibility).
- **Payload Size**: Binary serialization significantly reduces the size of high-frequency telemetry over Redis Streams and WebSockets.

## Directory Structure

We use a versioned package layout:

```text
libs/events/
├── proto/
│   ├── pitwall/
│   │   ├── events/
│   │   │   ├── v1/
│   │   │   │   ├── envelope.proto      # The canonical envelope schema
│   │   │   │   ├── session.proto       # Session state events
│   │   │   │   ├── telemetry.proto     # High frequency data
│   │   │   │   ├── prediction.proto    # Analytics outputs
│   │   │   │   └── enums.proto         # Shared enumerations (Tyres, Flags)
├── python/                             # Auto-generated Python bindings
├── go/                                 # Auto-generated Go bindings
├── ts/                                 # Auto-generated TypeScript bindings
└── Makefile                            # Scripts to run protoc
```

## Schema Versioning

- All proto files reside in a versioned namespace (e.g., `package pitwall.events.v1;`).
- Non-breaking changes (adding optional fields) occur within `v1`.
- Breaking changes (removing fields, changing types) require a new package `v2`.
- The Replay Engine uses the schema version defined in the historical database to deserialize old events correctly.

## Naming Conventions

- **Packages**: `pitwall.<domain>.<version>` (lowercase).
- **Messages**: `PascalCase` (e.g., `LapCompleted`).
- **Fields**: `snake_case` (e.g., `lap_number`).
- **Enums**: `PascalCase` with `UPPER_SNAKE_CASE` values (e.g., `enum TyreCompound { TYRE_COMPOUND_UNKNOWN = 0; TYRE_COMPOUND_SOFT = 1; }`).

## Next Steps
In the next milestone, the actual `.proto` files will be drafted in the `proto/` directory and compilation scripts will be configured.
