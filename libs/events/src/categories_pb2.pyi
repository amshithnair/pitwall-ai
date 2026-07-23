from typing import ClassVar as _ClassVar

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message

DESCRIPTOR: _descriptor.FileDescriptor

class SessionStarted(_message.Message):
    __slots__ = ("session_type", "laps_total")
    SESSION_TYPE_FIELD_NUMBER: _ClassVar[int]
    LAPS_TOTAL_FIELD_NUMBER: _ClassVar[int]
    session_type: str
    laps_total: int
    def __init__(self, session_type: str | None = ..., laps_total: int | None = ...) -> None: ...

class SessionEnded(_message.Message):
    __slots__ = ("session_type",)
    SESSION_TYPE_FIELD_NUMBER: _ClassVar[int]
    session_type: str
    def __init__(self, session_type: str | None = ...) -> None: ...

class LapStarted(_message.Message):
    __slots__ = ("lap_number",)
    LAP_NUMBER_FIELD_NUMBER: _ClassVar[int]
    lap_number: int
    def __init__(self, lap_number: int | None = ...) -> None: ...

class LapCompleted(_message.Message):
    __slots__ = ("lap_number", "lap_time_ms", "is_personal_best")
    LAP_NUMBER_FIELD_NUMBER: _ClassVar[int]
    LAP_TIME_MS_FIELD_NUMBER: _ClassVar[int]
    IS_PERSONAL_BEST_FIELD_NUMBER: _ClassVar[int]
    lap_number: int
    lap_time_ms: int
    is_personal_best: bool
    def __init__(
        self,
        lap_number: int | None = ...,
        lap_time_ms: int | None = ...,
        is_personal_best: bool | None = ...,
    ) -> None: ...

class SectorCompleted(_message.Message):
    __slots__ = ("sector_number", "sector_time_ms", "is_personal_best")
    SECTOR_NUMBER_FIELD_NUMBER: _ClassVar[int]
    SECTOR_TIME_MS_FIELD_NUMBER: _ClassVar[int]
    IS_PERSONAL_BEST_FIELD_NUMBER: _ClassVar[int]
    sector_number: int
    sector_time_ms: int
    is_personal_best: bool
    def __init__(
        self,
        sector_number: int | None = ...,
        sector_time_ms: int | None = ...,
        is_personal_best: bool | None = ...,
    ) -> None: ...

class PositionChanged(_message.Message):
    __slots__ = ("old_position", "new_position", "overtaken_driver_id")
    OLD_POSITION_FIELD_NUMBER: _ClassVar[int]
    NEW_POSITION_FIELD_NUMBER: _ClassVar[int]
    OVERTAKEN_DRIVER_ID_FIELD_NUMBER: _ClassVar[int]
    old_position: int
    new_position: int
    overtaken_driver_id: str
    def __init__(
        self,
        old_position: int | None = ...,
        new_position: int | None = ...,
        overtaken_driver_id: str | None = ...,
    ) -> None: ...

class PitEntry(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class PitStop(_message.Message):
    __slots__ = ("stationary_duration_ms",)
    STATIONARY_DURATION_MS_FIELD_NUMBER: _ClassVar[int]
    stationary_duration_ms: int
    def __init__(self, stationary_duration_ms: int | None = ...) -> None: ...

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
    def __init__(
        self, compound: str | None = ..., is_new: bool | None = ..., stint_number: int | None = ...
    ) -> None: ...

class TyreDegradation(_message.Message):
    __slots__ = ("degradation_percentage", "estimated_laps_remaining")
    DEGRADATION_PERCENTAGE_FIELD_NUMBER: _ClassVar[int]
    ESTIMATED_LAPS_REMAINING_FIELD_NUMBER: _ClassVar[int]
    degradation_percentage: float
    estimated_laps_remaining: int
    def __init__(
        self, degradation_percentage: float | None = ..., estimated_laps_remaining: int | None = ...
    ) -> None: ...

class TelemetryPoint(_message.Message):
    __slots__ = (
        "speed_kph",
        "throttle_percent",
        "brake_percent",
        "gear",
        "rpm",
        "drs_active",
        "x",
        "y",
        "z",
    )
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
    def __init__(
        self,
        speed_kph: int | None = ...,
        throttle_percent: int | None = ...,
        brake_percent: int | None = ...,
        gear: int | None = ...,
        rpm: int | None = ...,
        drs_active: bool | None = ...,
        x: float | None = ...,
        y: float | None = ...,
        z: float | None = ...,
    ) -> None: ...

class WeatherUpdated(_message.Message):
    __slots__ = (
        "air_temp_c",
        "track_temp_c",
        "humidity_percent",
        "rain_probability",
        "wind_speed_mps",
    )
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
    def __init__(
        self,
        air_temp_c: float | None = ...,
        track_temp_c: float | None = ...,
        humidity_percent: float | None = ...,
        rain_probability: float | None = ...,
        wind_speed_mps: float | None = ...,
    ) -> None: ...

class RaceControlFlag(_message.Message):
    __slots__ = ("flag_type", "reason")
    FLAG_TYPE_FIELD_NUMBER: _ClassVar[int]
    REASON_FIELD_NUMBER: _ClassVar[int]
    flag_type: str
    reason: str
    def __init__(self, flag_type: str | None = ..., reason: str | None = ...) -> None: ...

class PredictionGenerated(_message.Message):
    __slots__ = ("prediction_type", "payload_json", "confidence")
    PREDICTION_TYPE_FIELD_NUMBER: _ClassVar[int]
    PAYLOAD_JSON_FIELD_NUMBER: _ClassVar[int]
    CONFIDENCE_FIELD_NUMBER: _ClassVar[int]
    prediction_type: str
    payload_json: str
    confidence: float
    def __init__(
        self,
        prediction_type: str | None = ...,
        payload_json: str | None = ...,
        confidence: float | None = ...,
    ) -> None: ...

class StrategyGenerated(_message.Message):
    __slots__ = ("strategy_type", "payload_json")
    STRATEGY_TYPE_FIELD_NUMBER: _ClassVar[int]
    PAYLOAD_JSON_FIELD_NUMBER: _ClassVar[int]
    strategy_type: str
    payload_json: str
    def __init__(self, strategy_type: str | None = ..., payload_json: str | None = ...) -> None: ...

class InsightGenerated(_message.Message):
    __slots__ = ("insight_text", "category", "confidence")
    INSIGHT_TEXT_FIELD_NUMBER: _ClassVar[int]
    CATEGORY_FIELD_NUMBER: _ClassVar[int]
    CONFIDENCE_FIELD_NUMBER: _ClassVar[int]
    insight_text: str
    category: str
    confidence: float
    def __init__(
        self,
        insight_text: str | None = ...,
        category: str | None = ...,
        confidence: float | None = ...,
    ) -> None: ...

class SystemHealth(_message.Message):
    __slots__ = ("service_name", "status")
    SERVICE_NAME_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    service_name: str
    status: str
    def __init__(self, service_name: str | None = ..., status: str | None = ...) -> None: ...

class ReplayStateChanged(_message.Message):
    __slots__ = ("replay_id", "state", "speed_multiplier")
    REPLAY_ID_FIELD_NUMBER: _ClassVar[int]
    STATE_FIELD_NUMBER: _ClassVar[int]
    SPEED_MULTIPLIER_FIELD_NUMBER: _ClassVar[int]
    replay_id: str
    state: str
    speed_multiplier: float
    def __init__(
        self,
        replay_id: str | None = ...,
        state: str | None = ...,
        speed_multiplier: float | None = ...,
    ) -> None: ...
