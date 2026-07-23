import logging
import threading
import time
from datetime import datetime, timezone
from pitwall.events.redis_broker import RedisEventSubscriber
from pitwall.events.models import PitWallEvent
from pitwall.strategy_engine.state.race_state_manager import RaceStateManager
from pitwall.strategy_engine.evaluator import StrategyEvaluator
from pitwall.strategy_engine.publisher import StrategyPublisher

logger = logging.getLogger(__name__)

class StrategyConsumer:
    """Consumes analytics and race events to run strategy simulations."""
    def __init__(self):
        self.subscriber = RedisEventSubscriber(host="redis", port=6379)
        self.publisher = StrategyPublisher()
        self.state_manager = RaceStateManager()
        self.evaluator = StrategyEvaluator()
        self._running = False
        
    def start(self):
        if not self._running:
            self._running = True
            self.worker_thread = threading.Thread(target=self._consume_loop, daemon=True)
            self.worker_thread.start()
            
    def stop(self):
        self._running = False
        
    def _consume_loop(self):
        logger.info("Starting strategy consumer loop")
        self.subscriber.subscribe("telemetry_group", "strategy_worker")
        
        while self._running:
            try:
                events = self.subscriber.consume(batch_size=1000, timeout_ms=1000)
                for event in events:
                    self._process_event(event)
            except Exception as e:
                logger.error(f"Consumer error: {e}")
                time.sleep(1)
                
    def _process_event(self, event: PitWallEvent):
        if event.event_type.startswith("analytics."):
            self.state_manager.update_from_analytics(event.event_type, event.payload, event.driver_id)
            
            if event.event_type == "analytics.lap":
                best = self.evaluator.evaluate_scenarios(
                    session_id=event.session_id,
                    driver_id=event.driver_id,
                    current_lap=self.state_manager.current_lap,
                    total_laps=60
                )
                
                from pitwall.events.proto.categories_pb2 import StrategySelected
                payload = StrategySelected(scenario_name=best["scenario_name"], reason="Lowest total simulated time")
                strategy_event = PitWallEvent(
                    event_type="strategy.selected",
                    session_id=event.session_id,
                    race_id=event.race_id,
                    source="strategy-engine",
                    payload=payload,
                    timestamp=datetime.now(timezone.utc),
                    driver_id=event.driver_id
                )
                self.publisher.publish(strategy_event)
                
        elif event.event_type == "race.control":
            self.state_manager.update_race_control(event.event_type, event.payload)
