# External Data Sources

PitWall AI relies on external data sources for race information. Because external APIs can change, deprecate, or enforce rate limits, the architecture strictly abstracts these providers. No internal service is aware of which provider is currently active.

## 1. Live Timing & Telemetry

### Primary: FastF1 Live Timing
- **Capabilities**: Unofficial signalR stream for live timing, car data (telemetry), position data, track status, weather, and session status.
- **Limitations**: Reverse-engineered. Not officially supported. The schema changes occasionally without warning.
- **Rate Limits**: None explicitly defined, but connections are monitored by F1.
- **Licensing**: Personal/Educational use only. Not for commercial redistribution.
- **Failure Handling**: If the stream disconnects, the Provider Adapter must attempt to reconnect with backoff.
- **Replacement Strategy**: Multiviewer API ecosystem or direct OpenF1 integration if it becomes available.

## 2. Historical Race Metadata

### Primary: Jolpica (Ergast API Successor)
- **Capabilities**: Historical race results, driver standings, constructor standings, circuit info, schedule data back to 1950.
- **Limitations**: Data is usually updated a few hours after a session ends. Not suitable for live data.
- **Rate Limits**: 4 requests per second, 200 requests per hour per IP.
- **Licensing**: MIT / Open Source.
- **Failure Handling**: Data is pulled once during a backfill. Retries on 429 Too Many Requests.
- **Replacement Strategy**: FastF1 historical data parsing or a custom scraped dataset.

## 3. Historical Telemetry

### Primary: FastF1 (Python Library)
- **Capabilities**: Downloads granular telemetry (speed, throttle, brake, RPM) for historical sessions.
- **Limitations**: High storage requirement. Downloads can be slow. Data is cached locally.
- **Rate Limits**: Subject to the upstream F1 data servers.
- **Licensing**: MIT (Library), Data subject to F1 terms.
- **Failure Handling**: If a download fails, the Historical Loader marks the session as incomplete and retries later.

## 4. Weather

### Primary: OpenWeather API
- **Capabilities**: Current weather, minute-by-minute precipitation forecasts.
- **Limitations**: Accuracy varies by circuit location. Does not provide track temperature.
- **Rate Limits**: 1,000 API calls per day (Free tier).
- **Licensing**: Commercial plans available.
- **Failure Handling**: If unavailable, the platform degrades gracefully by omitting weather impact from prediction models.

### Secondary: FastF1 Weather Data
- **Capabilities**: Provides track temperature and air temperature from the official F1 feed.
- **Limitations**: Only available during active sessions.

## 5. Static Metadata

### Track and Team Metadata
- **Capabilities**: Circuit layouts, corner lists, team principals, tyre compound allocations per weekend.
- **Source**: Curated internal JSON/CSV files.
- **Limitations**: Requires manual updates at the start of every season.

## Provider Abstraction Contract

Every live provider must implement this conceptual interface in the `Provider Adapter`:

```python
class TimingProvider:
    async def connect(self) -> None:
        """Establish connection to the external source."""
        pass

    async def stream_events(self) -> AsyncIterator[RawEvent]:
        """Yield raw events as they arrive from the source."""
        pass
        
    async def disconnect(self) -> None:
        """Cleanly close the connection."""
        pass
```

The `Normalizer` takes `RawEvent` and produces a Canonical Event. If FastF1 changes its payload, only the FastF1 Provider Adapter and Normalizer require updates. The rest of PitWall AI is unaffected.
