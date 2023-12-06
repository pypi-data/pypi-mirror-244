"""Generated implementation of view_materialisation_runs."""

# WARNING DO NOT EDIT
# This code was generated from view-materialisation-runs.mcn

from __future__ import annotations

import abc  # noqa: F401
import dataclasses  # noqa: F401
import datetime  # noqa: F401
import enum  # noqa: F401
import isodate  # noqa: F401
import json  # noqa: F401
import jsonschema  # noqa: F401
import logging  # noqa: F401
import typing  # noqa: F401
import uuid  # noqa: F401
try:
    from anaml_client.utils.serialisation import JsonObject  # noqa: F401
except ImportError:
    pass

from ..commit import CommitId
from ..job_metrics import ExtendedExecutionStatistics
from ..run_error import RunError
from ..run_status import RunStatus
from ..schedule import ScheduleState
from ..user import UserId
from ..view_materialisation import (
    ViewMaterialisationJobId, ViewMaterialisationJobVersionId,
    ViewMaterialisationRunId
)


@dataclasses.dataclass(frozen=True)
class ViewMaterialisationRunCreationRequest:
    """Request to create a new table caching job run.
    
    Args:
        job (ViewMaterialisationJobId): A data field.
        jobVersion (ViewMaterialisationJobVersionId): A data field.
        operationsCommit (typing.Optional[CommitId]): A data field.
        commit (typing.Optional[CommitId]): A data field.
        scheduleState (typing.Optional[ScheduleState]): A data field.
        status (RunStatus): A data field.
        runBy (typing.Optional[UserId]): A data field.
        error (typing.Optional[RunError]): A data field.
        statistics (typing.Optional[ExtendedExecutionStatistics]): A data field.
    """
    
    job: ViewMaterialisationJobId
    jobVersion: ViewMaterialisationJobVersionId
    operationsCommit: typing.Optional[CommitId]
    commit: typing.Optional[CommitId]
    scheduleState: typing.Optional[ScheduleState]
    status: RunStatus
    runBy: typing.Optional[UserId]
    error: typing.Optional[RunError]
    statistics: typing.Optional[ExtendedExecutionStatistics]
    
    @classmethod
    def json_schema(cls) -> dict:
        """Return the JSON schema for ViewMaterialisationRunCreationRequest data.
        
        Returns:
            A Python dictionary describing the JSON schema.
        """
        return {
            "type": "object",
            "properties": {
                "job": ViewMaterialisationJobId.json_schema(),
                "jobVersion": ViewMaterialisationJobVersionId.json_schema(),
                "operationsCommit": {
                    "oneOf": [
                        {"type": "null"},
                        CommitId.json_schema(),
                    ]
                },
                "commit": {
                    "oneOf": [
                        {"type": "null"},
                        CommitId.json_schema(),
                    ]
                },
                "scheduleState": {
                    "oneOf": [
                        {"type": "null"},
                        ScheduleState.json_schema(),
                    ]
                },
                "status": RunStatus.json_schema(),
                "runBy": {
                    "oneOf": [
                        {"type": "null"},
                        UserId.json_schema(),
                    ]
                },
                "error": {
                    "oneOf": [
                        {"type": "null"},
                        RunError.json_schema(),
                    ]
                },
                "statistics": {
                    "oneOf": [
                        {"type": "null"},
                        ExtendedExecutionStatistics.json_schema(),
                    ]
                }
            },
            "required": [
                "job",
                "jobVersion",
                "status",
            ]
        }
    
    @classmethod
    def from_json(cls, data: dict) -> ViewMaterialisationRunCreationRequest:
        """Validate and parse JSON data into an instance of ViewMaterialisationRunCreationRequest.
        
        Args:
            data (dict): JSON data to validate and parse.
        
        Returns:
            An instance of ViewMaterialisationRunCreationRequest.
        
        Raises:
            ValidationError: When schema validation fails.
            KeyError: When a required field is missing from the JSON.
        """
        try:
            jsonschema.validate(data, cls.json_schema())
            return ViewMaterialisationRunCreationRequest(
                job=ViewMaterialisationJobId.from_json(data["job"]),
                jobVersion=ViewMaterialisationJobVersionId.from_json(data["jobVersion"]),
                operationsCommit=(
                    lambda v: CommitId.from_json(v) if v is not None else None
                )(
                    data.get("operationsCommit", None)
                ),
                commit=(
                    lambda v: CommitId.from_json(v) if v is not None else None
                )(
                    data.get("commit", None)
                ),
                scheduleState=(
                    lambda v: ScheduleState.from_json(v) if v is not None else None
                )(
                    data.get("scheduleState", None)
                ),
                status=RunStatus.from_json(data["status"]),
                runBy=(
                    lambda v: UserId.from_json(v) if v is not None else None
                )(
                    data.get("runBy", None)
                ),
                error=(
                    lambda v: RunError.from_json(v) if v is not None else None
                )(
                    data.get("error", None)
                ),
                statistics=(
                    lambda v: ExtendedExecutionStatistics.from_json(v) if v is not None else None
                )(
                    data.get("statistics", None)
                ),
            )
        except jsonschema.exceptions.ValidationError as ex:
            logging.debug(
                "Invalid JSON data received while parsing ViewMaterialisationRunCreationRequest",
                exc_info=ex
            )
            raise
    
    def to_json(self) -> dict:
        """Serialise this instance as JSON.
        
        Returns:
            Data ready to serialise as JSON.
        """
        return {
            "job": self.job.to_json(),
            "jobVersion": self.jobVersion.to_json(),
            "operationsCommit": (lambda v: v.to_json() if v is not None else v)(self.operationsCommit),
            "commit": (lambda v: v.to_json() if v is not None else v)(self.commit),
            "scheduleState": (lambda v: v.to_json() if v is not None else v)(self.scheduleState),
            "status": self.status.to_json(),
            "runBy": (lambda v: v.to_json() if v is not None else v)(self.runBy),
            "error": (lambda v: v.to_json() if v is not None else v)(self.error),
            "statistics": (lambda v: v.to_json() if v is not None else v)(self.statistics)
        }


@dataclasses.dataclass(frozen=True)
class ViewMaterialisationRunUpdateRequest:
    """Request to update a table caching job run.
    
    Args:
        status (RunStatus): A data field.
        error (typing.Optional[RunError]): A data field.
        statistics (typing.Optional[ExtendedExecutionStatistics]): A data field.
    """
    
    status: RunStatus
    error: typing.Optional[RunError]
    statistics: typing.Optional[ExtendedExecutionStatistics]
    
    @classmethod
    def json_schema(cls) -> dict:
        """Return the JSON schema for ViewMaterialisationRunUpdateRequest data.
        
        Returns:
            A Python dictionary describing the JSON schema.
        """
        return {
            "type": "object",
            "properties": {
                "status": RunStatus.json_schema(),
                "error": {
                    "oneOf": [
                        {"type": "null"},
                        RunError.json_schema(),
                    ]
                },
                "statistics": {
                    "oneOf": [
                        {"type": "null"},
                        ExtendedExecutionStatistics.json_schema(),
                    ]
                }
            },
            "required": [
                "status",
            ]
        }
    
    @classmethod
    def from_json(cls, data: dict) -> ViewMaterialisationRunUpdateRequest:
        """Validate and parse JSON data into an instance of ViewMaterialisationRunUpdateRequest.
        
        Args:
            data (dict): JSON data to validate and parse.
        
        Returns:
            An instance of ViewMaterialisationRunUpdateRequest.
        
        Raises:
            ValidationError: When schema validation fails.
            KeyError: When a required field is missing from the JSON.
        """
        try:
            jsonschema.validate(data, cls.json_schema())
            return ViewMaterialisationRunUpdateRequest(
                status=RunStatus.from_json(data["status"]),
                error=(
                    lambda v: RunError.from_json(v) if v is not None else None
                )(
                    data.get("error", None)
                ),
                statistics=(
                    lambda v: ExtendedExecutionStatistics.from_json(v) if v is not None else None
                )(
                    data.get("statistics", None)
                ),
            )
        except jsonschema.exceptions.ValidationError as ex:
            logging.debug(
                "Invalid JSON data received while parsing ViewMaterialisationRunUpdateRequest",
                exc_info=ex
            )
            raise
    
    def to_json(self) -> dict:
        """Serialise this instance as JSON.
        
        Returns:
            Data ready to serialise as JSON.
        """
        return {
            "status": self.status.to_json(),
            "error": (lambda v: v.to_json() if v is not None else v)(self.error),
            "statistics": (lambda v: v.to_json() if v is not None else v)(self.statistics)
        }


@dataclasses.dataclass(frozen=True)
class ViewMaterialisationRun:
    """Details of a table caching job run.
    
    Args:
        id (ViewMaterialisationRunId): A data field.
        job (ViewMaterialisationJobId): A data field.
        jobVersion (ViewMaterialisationJobVersionId): A data field.
        operationsCommit (typing.Optional[CommitId]): A data field.
        commit (typing.Optional[CommitId]): A data field.
        scheduleState (typing.Optional[ScheduleState]): A data field.
        status (RunStatus): A data field.
        runBy (typing.Optional[UserId]): A data field.
        error (typing.Optional[RunError]): A data field.
        statistics (typing.Optional[ExtendedExecutionStatistics]): A data field.
        created (datetime.datetime): A data field.
    """
    
    id: ViewMaterialisationRunId
    job: ViewMaterialisationJobId
    jobVersion: ViewMaterialisationJobVersionId
    operationsCommit: typing.Optional[CommitId]
    commit: typing.Optional[CommitId]
    scheduleState: typing.Optional[ScheduleState]
    status: RunStatus
    runBy: typing.Optional[UserId]
    error: typing.Optional[RunError]
    statistics: typing.Optional[ExtendedExecutionStatistics]
    created: datetime.datetime
    
    @classmethod
    def json_schema(cls) -> dict:
        """Return the JSON schema for ViewMaterialisationRun data.
        
        Returns:
            A Python dictionary describing the JSON schema.
        """
        return {
            "type": "object",
            "properties": {
                "id": ViewMaterialisationRunId.json_schema(),
                "job": ViewMaterialisationJobId.json_schema(),
                "jobVersion": ViewMaterialisationJobVersionId.json_schema(),
                "operationsCommit": {
                    "oneOf": [
                        {"type": "null"},
                        CommitId.json_schema(),
                    ]
                },
                "commit": {
                    "oneOf": [
                        {"type": "null"},
                        CommitId.json_schema(),
                    ]
                },
                "scheduleState": {
                    "oneOf": [
                        {"type": "null"},
                        ScheduleState.json_schema(),
                    ]
                },
                "status": RunStatus.json_schema(),
                "runBy": {
                    "oneOf": [
                        {"type": "null"},
                        UserId.json_schema(),
                    ]
                },
                "error": {
                    "oneOf": [
                        {"type": "null"},
                        RunError.json_schema(),
                    ]
                },
                "statistics": {
                    "oneOf": [
                        {"type": "null"},
                        ExtendedExecutionStatistics.json_schema(),
                    ]
                },
                "created": {
                    "type": "string",
                    "format": "date-time"
                }
            },
            "required": [
                "id",
                "job",
                "jobVersion",
                "status",
                "created",
            ]
        }
    
    @classmethod
    def from_json(cls, data: dict) -> ViewMaterialisationRun:
        """Validate and parse JSON data into an instance of ViewMaterialisationRun.
        
        Args:
            data (dict): JSON data to validate and parse.
        
        Returns:
            An instance of ViewMaterialisationRun.
        
        Raises:
            ValidationError: When schema validation fails.
            KeyError: When a required field is missing from the JSON.
        """
        try:
            jsonschema.validate(data, cls.json_schema())
            return ViewMaterialisationRun(
                id=ViewMaterialisationRunId.from_json(data["id"]),
                job=ViewMaterialisationJobId.from_json(data["job"]),
                jobVersion=ViewMaterialisationJobVersionId.from_json(data["jobVersion"]),
                operationsCommit=(
                    lambda v: CommitId.from_json(v) if v is not None else None
                )(
                    data.get("operationsCommit", None)
                ),
                commit=(
                    lambda v: CommitId.from_json(v) if v is not None else None
                )(
                    data.get("commit", None)
                ),
                scheduleState=(
                    lambda v: ScheduleState.from_json(v) if v is not None else None
                )(
                    data.get("scheduleState", None)
                ),
                status=RunStatus.from_json(data["status"]),
                runBy=(
                    lambda v: UserId.from_json(v) if v is not None else None
                )(
                    data.get("runBy", None)
                ),
                error=(
                    lambda v: RunError.from_json(v) if v is not None else None
                )(
                    data.get("error", None)
                ),
                statistics=(
                    lambda v: ExtendedExecutionStatistics.from_json(v) if v is not None else None
                )(
                    data.get("statistics", None)
                ),
                created=isodate.parse_datetime(data["created"]),
            )
        except jsonschema.exceptions.ValidationError as ex:
            logging.debug(
                "Invalid JSON data received while parsing ViewMaterialisationRun",
                exc_info=ex
            )
            raise
    
    def to_json(self) -> dict:
        """Serialise this instance as JSON.
        
        Returns:
            Data ready to serialise as JSON.
        """
        return {
            "id": self.id.to_json(),
            "job": self.job.to_json(),
            "jobVersion": self.jobVersion.to_json(),
            "operationsCommit": (lambda v: v.to_json() if v is not None else v)(self.operationsCommit),
            "commit": (lambda v: v.to_json() if v is not None else v)(self.commit),
            "scheduleState": (lambda v: v.to_json() if v is not None else v)(self.scheduleState),
            "status": self.status.to_json(),
            "runBy": (lambda v: v.to_json() if v is not None else v)(self.runBy),
            "error": (lambda v: v.to_json() if v is not None else v)(self.error),
            "statistics": (lambda v: v.to_json() if v is not None else v)(self.statistics),
            "created": self.created.strftime('%Y-%m-%dT%H:%M:%S.%f%z')
        }
