import asyncpg
import logging

logger = logging.getLogger(__name__)

async def setup_schema(conn: asyncpg.Connection):
    """Initializes TimescaleDB hypertables for telemetry and analytics."""
    # 1. Telemetry hypertable
    await conn.execute("""
        CREATE TABLE IF NOT EXISTS telemetry (
            time TIMESTAMPTZ NOT NULL,
            session_id TEXT NOT NULL,
            driver_id TEXT NOT NULL,
            speed_kph INT,
            rpm INT,
            gear INT,
            throttle_percent INT,
            brake_percent INT,
            drs_active BOOLEAN,
            x FLOAT,
            y FLOAT,
            z FLOAT
        );
    """)
    await conn.execute("SELECT create_hypertable('telemetry', 'time', if_not_exists => TRUE);")
    
    # 2. Lap Analytics hypertable
    await conn.execute("""
        CREATE TABLE IF NOT EXISTS lap_analytics (
            time TIMESTAMPTZ NOT NULL,
            session_id TEXT NOT NULL,
            driver_id TEXT NOT NULL,
            lap_number INT,
            lap_time_ms INT,
            delta_to_best_ms INT,
            is_personal_best BOOLEAN,
            is_session_best BOOLEAN,
            average_speed_kph INT,
            max_speed_kph INT
        );
    """)
    await conn.execute("SELECT create_hypertable('lap_analytics', 'time', if_not_exists => TRUE);")
    
    # 3. Driver Analytics hypertable
    await conn.execute("""
        CREATE TABLE IF NOT EXISTS driver_analytics (
            time TIMESTAMPTZ NOT NULL,
            session_id TEXT NOT NULL,
            driver_id TEXT NOT NULL,
            gap_to_leader_ms INT,
            gap_to_ahead_ms INT,
            gap_to_behind_ms INT,
            consistency_score FLOAT,
            average_lap_time_ms INT,
            position_changes INT
        );
    """)
    await conn.execute("SELECT create_hypertable('driver_analytics', 'time', if_not_exists => TRUE);")
    logger.info("TimescaleDB schema initialized.")
