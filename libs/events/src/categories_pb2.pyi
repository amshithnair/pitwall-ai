from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class SessionStarted(_message.Message):
    __slots__ = ("session_type", "laps_total")
    SESSION_TYPE_FIELD_NUMBER: _ClassVar[int]
    LAPS_TOTAL_FIELD_NUMBER: _ClassVar[int]
    session_type: str
    laps_total: int
    def __init__(self, session_type: _Optional[str] = ..., laps_total: _Optional[int] = ...) -> None: ...

class SessionEnded(_message.Message):
    __slots__ = ("session_type",)
    SESSION_TYPE_FIELD_NUMBER: _ClassVar[int]
    session_type: str
    def __init__(self, session_type: _Optional[str] = ...) -> None: ...

class LapStarted(_message.Message):
    __slots__ = ("lap_number",)
    LAP_NUMBER_FIELD_NUMBER: _ClassVar[int]
    lap_number: int
    def __init__(self, lap_number: _Optional[int] = ...) -> None: ...

class LapCompleted(_message.Message):
    __slots__ = ("lap_number", "lap_time_ms", "is_personal_best")
    LAP_NUMBER_FIELD_NUMBER: _ClassVar[int]
    LAP_TIME_MS_FIELD_NUMBER: _ClassVar[int]
    IS_PERSONAL_BEST_FIELD_NUMBER: _ClassVar[int]
    lap_number: int
    lap_time_ms: int
    is_personal_best: bool
    def __init__(self, lap_number: _Optional[int] = ..., lap_time_ms: _Optional[int] = ..., is_personal_best: _Optional[bool] = ...) -> None: ...

class SectorCompleted(_message.Message):
    __slots__ = ("sector_number", "sector_time_ms", "is_personal_best")
    SECTOR_NUMBER_FIELD_NUMBER: _ClassVar[int]
    SECTOR_TIME_MS_FIELD_NUMBER: _ClassVar[int]
    IS_PERSONAL_BEST_FIELD_NUMBER: _ClassVar[int]
    sector_number: int
    sector_time_ms: int
    is_personal_best: bool
    def __init__(self, sector_number: _Optional[int] = ..., sector_time_ms: _Optional[int] = ..., is_personal_best: _Optional[bool] = ...) -> None: ...

class PositionChanged(_message.Message):
    __slots__ = ("old_position", "new_position", "overtaken_driver_id")
    OLD_POSITION_FIELD_NUMBER: _ClassVar[int]
    NEW_POSITION_FIELD_NUMBER: _ClassVar[int]
    OVERTAKEN_DRIVER_ID_FIELD_NUMBER: _ClassVar[int]
    old_position: int
    new_position: int
    overtaken_driver_id: str
    def __init__(self, old_position: _Optional[int] = ..., new_position: _Optional[int] = ..., overtaken_driver_id: _Optional[str] = ...) -> None: ...

class PitEntry(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class PitStop(_message.Message):
    __slots__ = ("stationary_duration_ms",)
    STATIONARY_DURATION_MS_FIELD_NUMBER: _ClassVar[int]
    stationary_duration_ms: int
    def __init__(self, stationary_duration_ms: _Optional[int] = ...) -> None: ...

class PitExit(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class TyreChanged(_message.Message):
    __slots__ = ("compound", "is_new", "stint_number")
    COMPOUND_FIELD_NUMBER: _ClassVar[int]
    IS_NEW_FIELD_NUMBER: _ClassVar[int]
    STINT_NUMBER_FIELD_NUMBER: _ClassVar[int]
    compound: str
    is_new: bool
    stint_number: int
    def __init__(self, compound: _Optional[str] = ..., is_new: _Optional[bool] = ..., stint_number: _Optional[int] = ...) -> None: ...

class TyreDegradation(_message.Message):
    __slots__ = ("degradation_percentage", "estimated_laps_remaining")
    DEGRADATION_PERCENTAGE_FIELD_NUMBER: _ClassVar[int]
    ESTIMATED_LAPS_REMAINING_FIELD_NUMBER: _ClassVar[int]
    degradation_percentage: float
    estimated_laps_remaining: int
    def __init__(self, degradation_percentage: _Optional[float] = ..., estimated_laps_remaining: _Optional[int] = ...) -> None: ...

class TelemetryPoint(_message.Message):
    __slots__ = ("speed_kph", "throttle_percent", "brake_percent", "gear", "rpm", "drs_active", "x", "y", "z")
    SPEED_KPH_FIELD_NUMBER: _ClassVar[int]
    THROTTLE_PERCENT_FIELD_NUMBER: _ClassVar[int]
    BRAKE_PERCENT_FIELD_NUMBER: _ClassVar[int]
    GEAR_FIELD_NUMBER: _ClassVar[int]
    RPM_FIELD_NUMBER: _ClassVar[int]
    DRS_ACTIVE_FIELD_NUMBER: _ClassVar[int]
    X_FIELD_NUMBER: _ClassVar[int]
    Y_FIELD_NUMBER: _ClassVar[int]
    Z_FIELD_NUMBER: _ClassVar[int]
    speed_kph: int
    throttle_percent: int
    brake_percent: int
    gear: int
    rpm: int
    drs_active: bool
    x: float
    y: float
    z: float
    def __init__(self, speed_kph: _Optional[int] = ..., throttle_percent: _Optional[int] = ..., brake_percent: _Optional[int] = ..., gear: _Optional[int] = ..., rpm: _Optional[int] = ..., drs_active: _Optional[bool] = ..., x: _Optional[float] = ..., y: _Optional[float] = ..., z: _Optional[float] = ...) -> None: ...

class WeatherUpdated(_message.Message):
    __slots__ = ("air_temp_c", "track_temp_c", "humidity_percent", "rain_probability", "wind_speed_mps")
    AIR_TEMP_C_FIELD_NUMBER: _ClassVar[int]
    TRACK_TEMP_C_FIELD_NUMBER: _ClassVar[int]
    HUMIDITY_PERCENT_FIELD_NUMBER: _ClassVar[int]
    RAIN_PROBABILITY_FIELD_NUMBER: _ClassVar[int]
    WIND_SPEED_MPS_FIELD_NUMBER: _ClassVar[int]
    air_temp_c: float
    track_temp_c: float
    humidity_percent: float
    rain_probability: float
    wind_speed_mps: float
    def __init__(self, air_temp_c: _Optional[float] = ..., track_temp_c: _Optional[float] = ..., humidity_percent: _Optional[float] = ..., rain_probability: _Optional[float] = ..., wind_speed_mps: _Optional[float] = ...) -> None: ...

class RaceControlFlag(_message.Message):
    __slots__ = ("flag_type", "reason")
    FLAG_TYPE_FIELD_NUMBER: _ClassVar[int]
    REASON_FIELD_NUMBER: _ClassVar[int]
    flag_type: str
    reason: str
    def __init__(self, flag_type: _Optional[str] = ..., reason: _Optional[str] = ...) -> None: ...

class PredictionGenerated(_message.Message):
    __slots__ = ("prediction_type", "payload_json", "confidence")
    PREDICTION_TYPE_FIELD_NUMBER: _ClassVar[int]
    PAYLOAD_JSON_FIELD_NUMBER: _ClassVar[int]
    CONFIDENCE_FIELD_NUMBER: _ClassVar[int]
    prediction_type: str
    payload_json: str
    confidence: float
    def __init__(self, prediction_type: _Optional[str] = ..., payload_json: _Optional[str] = ..., confidence: _Optional[float] = ...) -> None: ...

class StrategyGenerated(_message.Message):
    __slots__ = ("strategy_type", "payload_json")
    STRATEGY_TYPE_FIELD_NUMBER: _ClassVar[int]
    PAYLOAD_JSON_FIELD_NUMBER: _ClassVar[int]
    strategy_type: str
    payload_json: str
    def __init__(self, strategy_type: _Optional[str] = ..., payload_json: _Optional[str] = ...) -> None: ...

class InsightGenerated(_message.Message):
    __slots__ = ("insight_text", "category", "confidence")
    INSIGHT_TEXT_FIELD_NUMBER: _ClassVar[int]
    CATEGORY_FIELD_NUMBER: _ClassVar[int]
    CONFIDENCE_FIELD_NUMBER: _ClassVar[int]
    insight_text: str
    category: str
    confidence: float
    def __init__(self, insight_text: _Optional[str] = ..., category: _Optional[str] = ..., confidence: _Optional[float] = ...) -> None: ...

class LapAnalytics(_message.Message):
    __slots__ = ("lap_number", "lap_time_ms", "delta_to_best_ms", "is_personal_best", "is_session_best", "average_speed_kph", "max_speed_kph")
    LAP_NUMBER_FIELD_NUMBER: _ClassVar[int]
    LAP_TIME_MS_FIELD_NUMBER: _ClassVar[int]
    DELTA_TO_BEST_MS_FIELD_NUMBER: _ClassVar[int]
    IS_PERSONAL_BEST_FIELD_NUMBER: _ClassVar[int]
    IS_SESSION_BEST_FIELD_NUMBER: _ClassVar[int]
    AVERAGE_SPEED_KPH_FIELD_NUMBER: _ClassVar[int]
    MAX_SPEED_KPH_FIELD_NUMBER: _ClassVar[int]
    lap_number: int
    lap_time_ms: int
    delta_to_best_ms: int
    is_personal_best: bool
    is_session_best: bool
    average_speed_kph: int
    max_speed_kph: int
    def __init__(self, lap_number: _Optional[int] = ..., lap_time_ms: _Optional[int] = ..., delta_to_best_ms: _Optional[int] = ..., is_personal_best: _Optional[bool] = ..., is_session_best: _Optional[bool] = ..., average_speed_kph: _Optional[int] = ..., max_speed_kph: _Optional[int] = ...) -> None: ...

class SectorAnalytics(_message.Message):
    __slots__ = ("sector_number", "sector_time_ms", "delta_to_best_ms", "is_personal_best", "is_session_best")
    SECTOR_NUMBER_FIELD_NUMBER: _ClassVar[int]
    SECTOR_TIME_MS_FIELD_NUMBER: _ClassVar[int]
    DELTA_TO_BEST_MS_FIELD_NUMBER: _ClassVar[int]
    IS_PERSONAL_BEST_FIELD_NUMBER: _ClassVar[int]
    IS_SESSION_BEST_FIELD_NUMBER: _ClassVar[int]
    sector_number: int
    sector_time_ms: int
    delta_to_best_ms: int
    is_personal_best: bool
    is_session_best: bool
    def __init__(self, sector_number: _Optional[int] = ..., sector_time_ms: _Optional[int] = ..., delta_to_best_ms: _Optional[int] = ..., is_personal_best: _Optional[bool] = ..., is_session_best: _Optional[bool] = ...) -> None: ...

class DriverAnalytics(_message.Message):
    __slots__ = ("gap_to_leader_ms", "gap_to_ahead_ms", "gap_to_behind_ms", "consistency_score", "average_lap_time_ms", "position_changes")
    GAP_TO_LEADER_MS_FIELD_NUMBER: _ClassVar[int]
    GAP_TO_AHEAD_MS_FIELD_NUMBER: _ClassVar[int]
    GAP_TO_BEHIND_MS_FIELD_NUMBER: _ClassVar[int]
    CONSISTENCY_SCORE_FIELD_NUMBER: _ClassVar[int]
    AVERAGE_LAP_TIME_MS_FIELD_NUMBER: _ClassVar[int]
    POSITION_CHANGES_FIELD_NUMBER: _ClassVar[int]
    gap_to_leader_ms: int
    gap_to_ahead_ms: int
    gap_to_behind_ms: int
    consistency_score: float
    average_lap_time_ms: int
    position_changes: int
    def __init__(self, gap_to_leader_ms: _Optional[int] = ..., gap_to_ahead_ms: _Optional[int] = ..., gap_to_behind_ms: _Optional[int] = ..., consistency_score: _Optional[float] = ..., average_lap_time_ms: _Optional[int] = ..., position_changes: _Optional[int] = ...) -> None: ...

class TyreAnalytics(_message.Message):
    __slots__ = ("tyre_age_laps", "stint_length", "estimated_degradation")
    TYRE_AGE_LAPS_FIELD_NUMBER: _ClassVar[int]
    STINT_LENGTH_FIELD_NUMBER: _ClassVar[int]
    ESTIMATED_DEGRADATION_FIELD_NUMBER: _ClassVar[int]
    tyre_age_laps: int
    stint_length: int
    estimated_degradation: float
    def __init__(self, tyre_age_laps: _Optional[int] = ..., stint_length: _Optional[int] = ..., estimated_degradation: _Optional[float] = ...) -> None: ...

class PitWindowCalculated(_message.Message):
    __slots__ = ("optimal_pit_lap", "pit_loss_ms", "earliest_safe_lap", "latest_safe_lap")
    OPTIMAL_PIT_LAP_FIELD_NUMBER: _ClassVar[int]
    PIT_LOSS_MS_FIELD_NUMBER: _ClassVar[int]
    EARLIEST_SAFE_LAP_FIELD_NUMBER: _ClassVar[int]
    LATEST_SAFE_LAP_FIELD_NUMBER: _ClassVar[int]
    optimal_pit_lap: int
    pit_loss_ms: int
    earliest_safe_lap: int
    latest_safe_lap: int
    def __init__(self, optimal_pit_lap: _Optional[int] = ..., pit_loss_ms: _Optional[int] = ..., earliest_safe_lap: _Optional[int] = ..., latest_safe_lap: _Optional[int] = ...) -> None: ...

class StrategyScenarioGenerated(_message.Message):
    __slots__ = ("scenario_name", "total_race_time_ms", "estimated_finish_position", "risk_score")
    SCENARIO_NAME_FIELD_NUMBER: _ClassVar[int]
    TOTAL_RACE_TIME_MS_FIELD_NUMBER: _ClassVar[int]
    ESTIMATED_FINISH_POSITION_FIELD_NUMBER: _ClassVar[int]
    RISK_SCORE_FIELD_NUMBER: _ClassVar[int]
    scenario_name: str
    total_race_time_ms: int
    estimated_finish_position: int
    risk_score: float
    def __init__(self, scenario_name: _Optional[str] = ..., total_race_time_ms: _Optional[int] = ..., estimated_finish_position: _Optional[int] = ..., risk_score: _Optional[float] = ...) -> None: ...

class TrafficAnalysisGenerated(_message.Message):
    __slots__ = ("estimated_rejoin_position", "ahead_driver_id", "behind_driver_id", "clear_air_probability")
    ESTIMATED_REJOIN_POSITION_FIELD_NUMBER: _ClassVar[int]
    AHEAD_DRIVER_ID_FIELD_NUMBER: _ClassVar[int]
    BEHIND_DRIVER_ID_FIELD_NUMBER: _ClassVar[int]
    CLEAR_AIR_PROBABILITY_FIELD_NUMBER: _ClassVar[int]
    estimated_rejoin_position: int
    ahead_driver_id: str
    behind_driver_id: str
    clear_air_probability: int
    def __init__(self, estimated_rejoin_position: _Optional[int] = ..., ahead_driver_id: _Optional[str] = ..., behind_driver_id: _Optional[str] = ..., clear_air_probability: _Optional[int] = ...) -> None: ...

class StrategySelected(_message.Message):
    __slots__ = ("scenario_name", "reason")
    SCENARIO_NAME_FIELD_NUMBER: _ClassVar[int]
    REASON_FIELD_NUMBER: _ClassVar[int]
    scenario_name: str
    reason: str
    def __init__(self, scenario_name: _Optional[str] = ..., reason: _Optional[str] = ...) -> None: ...

class SystemHealth(_message.Message):
    __slots__ = ("service_name", "status")
    SERVICE_NAME_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    service_name: str
    status: str
    def __init__(self, service_name: _Optional[str] = ..., status: _Optional[str] = ...) -> None: ...

class ReplayStateChanged(_message.Message):
    __slots__ = ("replay_id", "state", "speed_multiplier")
    REPLAY_ID_FIELD_NUMBER: _ClassVar[int]
    STATE_FIELD_NUMBER: _ClassVar[int]
    SPEED_MULTIPLIER_FIELD_NUMBER: _ClassVar[int]
    replay_id: str
    state: str
    speed_multiplier: float
    def __init__(self, replay_id: _Optional[str] = ..., state: _Optional[str] = ..., speed_multiplier: _Optional[float] = ...) -> None: ...
