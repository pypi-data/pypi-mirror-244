# This file was auto-generated by Fern from our API Definition.

from __future__ import annotations

import typing

import typing_extensions

from .observation_create_event import ObservationCreateEvent
from .observation_update_event import ObservationUpdateEvent
from .score_event import ScoreEvent
from .trace_event import TraceEvent


class IngestionEvent_TraceCreate(TraceEvent):
    type: typing_extensions.Literal["trace-create"]

    class Config:
        frozen = True
        smart_union = True
        allow_population_by_field_name = True


class IngestionEvent_ScoreCreate(ScoreEvent):
    type: typing_extensions.Literal["score-create"]

    class Config:
        frozen = True
        smart_union = True
        allow_population_by_field_name = True


class IngestionEvent_ObservationCreate(ObservationCreateEvent):
    type: typing_extensions.Literal["observation-create"]

    class Config:
        frozen = True
        smart_union = True
        allow_population_by_field_name = True


class IngestionEvent_ObservationUpdate(ObservationUpdateEvent):
    type: typing_extensions.Literal["observation-update"]

    class Config:
        frozen = True
        smart_union = True
        allow_population_by_field_name = True


IngestionEvent = typing.Union[
    IngestionEvent_TraceCreate,
    IngestionEvent_ScoreCreate,
    IngestionEvent_ObservationCreate,
    IngestionEvent_ObservationUpdate,
]
