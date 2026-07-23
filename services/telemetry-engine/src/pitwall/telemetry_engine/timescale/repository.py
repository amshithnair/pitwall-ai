import asyncpg
import logging
from typing import List, Tuple

logger = logging.getLogger(__name__)

class TimescaleRepository:
    def __init__(self, pool: asyncpg.Pool):
        self.pool = pool
        
    async def insert_telemetry_batch(self, records: List[Tuple]):
        """Efficiently batch-inserts high-frequency telemetry."""
        query = """
        INSERT INTO telemetry (
            time, session_id, driver_id, speed_kph, rpm, gear, 
            throttle_percent, brake_percent, drs_active, x, y, z
        ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12)
        """
        async with self.pool.acquire() as conn:
            await conn.executemany(query, records)
            
    async def insert_lap_analytics(self, record: Tuple):
        """Inserts a single lap analytics record."""
        query = """
        INSERT INTO lap_analytics (
            time, session_id, driver_id, lap_number, lap_time_ms, delta_to_best_ms, 
            is_personal_best, is_session_best, average_speed_kph, max_speed_kph
        ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10)
        """
        async with self.pool.acquire() as conn:
            await conn.execute(query, *record)
