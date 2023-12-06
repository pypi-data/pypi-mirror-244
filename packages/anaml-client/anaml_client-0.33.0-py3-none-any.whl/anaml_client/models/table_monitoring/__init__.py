"""Generated implementation of table_monitoring."""

# WARNING DO NOT EDIT
# This code was generated from table-monitoring.mcn

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

from ..cluster import ClusterId, ClusterPropertySetId
from ..job_metrics import ExecutionStatistics
from ..run_error import RunError
from ..run_status import RunStatus
from ..schedule import Schedule, ScheduleState
from ..summary_statistics import SummaryStatistics
from ..table import TableId, TableVersionId
from ..user import UserId


@dataclasses.dataclass(frozen=True)
class TableMonitoringJobId:
    """Unique identifier of a table monitoring job.

    Args:
        value (int): A data field.
    """

    value: int

    def __str__(self) -> str:
        """Return a str of the wrapped value."""
        return str(self.value)

    def __int__(self) -> int:
        """Return an int of the wrapped value."""
        return int(self.value)

    @classmethod
    def json_schema(cls) -> dict:
        """Return the JSON schema for TableMonitoringJobId data.

        Returns:
            A Python dictionary describing the JSON schema.
        """
        return {
            "type": "integer"
        }

    @classmethod
    def from_json(cls, data: dict) -> TableMonitoringJobId:
        """Validate and parse JSON data into an instance of TableMonitoringJobId.

        Args:
            data (dict): JSON data to validate and parse.

        Returns:
            An instance of TableMonitoringJobId.

        Raises:
            ValidationError: When schema validation fails.
            KeyError: When a required field is missing from the JSON.
        """
        try:
            jsonschema.validate(data, cls.json_schema())
            return TableMonitoringJobId(int(data))
        except jsonschema.exceptions.ValidationError as ex:
            logging.debug("Invalid JSON data received while parsing TableMonitoringJobId", exc_info=ex)
            raise

    def to_json(self) -> dict:
        """Serialise this instance as JSON.

        Returns:
            Data ready to serialise as JSON.
        """
        return self.value

    @classmethod
    def from_json_key(cls, data: str) -> TableMonitoringJobId:
        """Parse a JSON string such as a dictionary key."""
        return TableMonitoringJobId(int(data))

    def to_json_key(self) -> str:
        """Serialise as a JSON string suitable for use as a dictionary key."""
        return str(self.value)


@dataclasses.dataclass(frozen=True)
class TableMonitoringJobVersionId:
    """Unique identifier for a specific version of a table monitoring job.

    Args:
        value (uuid.UUID): A data field.
    """

    value: uuid.UUID

    def __str__(self) -> str:
        """Return a str of the wrapped value."""
        return str(self.value)

    @classmethod
    def json_schema(cls) -> dict:
        """Return the JSON schema for TableMonitoringJobVersionId data.

        Returns:
            A Python dictionary describing the JSON schema.
        """
        return {
            "type": "string",
            "format": "uuid"
        }

    @classmethod
    def from_json(cls, data: dict) -> TableMonitoringJobVersionId:
        """Validate and parse JSON data into an instance of TableMonitoringJobVersionId.

        Args:
            data (dict): JSON data to validate and parse.

        Returns:
            An instance of TableMonitoringJobVersionId.

        Raises:
            ValidationError: When schema validation fails.
            KeyError: When a required field is missing from the JSON.
        """
        try:
            jsonschema.validate(data, cls.json_schema())
            return TableMonitoringJobVersionId(uuid.UUID(hex=data))
        except jsonschema.exceptions.ValidationError as ex:
            logging.debug("Invalid JSON data received while parsing TableMonitoringJobVersionId", exc_info=ex)
            raise

    def to_json(self) -> dict:
        """Serialise this instance as JSON.

        Returns:
            Data ready to serialise as JSON.
        """
        return str(self.value)

    @classmethod
    def from_json_key(cls, data: str) -> TableMonitoringJobVersionId:
        """Parse a JSON string such as a dictionary key."""
        return TableMonitoringJobVersionId((lambda s: uuid.UUID(hex=s))(data))

    def to_json_key(self) -> str:
        """Serialise as a JSON string suitable for use as a dictionary key."""
        return str(self.value)


@dataclasses.dataclass(frozen=True)
class TableMonitoringJobName:
    """Unique name of a table monitoring job.

    Args:
        value (str): A data field.
    """

    value: str

    def __str__(self) -> str:
        """Return a str of the wrapped value."""
        return str(self.value)

    @classmethod
    def json_schema(cls) -> dict:
        """Return the JSON schema for TableMonitoringJobName data.

        Returns:
            A Python dictionary describing the JSON schema.
        """
        return {
            "type": "string"
        }

    @classmethod
    def from_json(cls, data: dict) -> TableMonitoringJobName:
        """Validate and parse JSON data into an instance of TableMonitoringJobName.

        Args:
            data (dict): JSON data to validate and parse.

        Returns:
            An instance of TableMonitoringJobName.

        Raises:
            ValidationError: When schema validation fails.
            KeyError: When a required field is missing from the JSON.
        """
        try:
            jsonschema.validate(data, cls.json_schema())
            return TableMonitoringJobName(str(data))
        except jsonschema.exceptions.ValidationError as ex:
            logging.debug("Invalid JSON data received while parsing TableMonitoringJobName", exc_info=ex)
            raise

    def to_json(self) -> dict:
        """Serialise this instance as JSON.

        Returns:
            Data ready to serialise as JSON.
        """
        return str(self.value)

    @classmethod
    def from_json_key(cls, data: str) -> TableMonitoringJobName:
        """Parse a JSON string such as a dictionary key."""
        return TableMonitoringJobName(str(data))

    def to_json_key(self) -> str:
        """Serialise as a JSON string suitable for use as a dictionary key."""
        return str(self.value)


@dataclasses.dataclass(frozen=True)
class TableMonitoringRunId:
    """Unique identifier of a table monitoring job run.

    Args:
        value (int): A data field.
    """

    value: int

    def __str__(self) -> str:
        """Return a str of the wrapped value."""
        return str(self.value)

    def __int__(self) -> int:
        """Return an int of the wrapped value."""
        return int(self.value)

    @classmethod
    def json_schema(cls) -> dict:
        """Return the JSON schema for TableMonitoringRunId data.

        Returns:
            A Python dictionary describing the JSON schema.
        """
        return {
            "type": "integer"
        }

    @classmethod
    def from_json(cls, data: dict) -> TableMonitoringRunId:
        """Validate and parse JSON data into an instance of TableMonitoringRunId.

        Args:
            data (dict): JSON data to validate and parse.

        Returns:
            An instance of TableMonitoringRunId.

        Raises:
            ValidationError: When schema validation fails.
            KeyError: When a required field is missing from the JSON.
        """
        try:
            jsonschema.validate(data, cls.json_schema())
            return TableMonitoringRunId(int(data))
        except jsonschema.exceptions.ValidationError as ex:
            logging.debug("Invalid JSON data received while parsing TableMonitoringRunId", exc_info=ex)
            raise

    def to_json(self) -> dict:
        """Serialise this instance as JSON.

        Returns:
            Data ready to serialise as JSON.
        """
        return self.value

    @classmethod
    def from_json_key(cls, data: str) -> TableMonitoringRunId:
        """Parse a JSON string such as a dictionary key."""
        return TableMonitoringRunId(int(data))

    def to_json_key(self) -> str:
        """Serialise as a JSON string suitable for use as a dictionary key."""
        return str(self.value)


@dataclasses.dataclass(frozen=True)
class MonitoringResultId:
    """Unique identifier of a table monitoring result.

    Args:
        value (int): A data field.
    """

    value: int

    def __str__(self) -> str:
        """Return a str of the wrapped value."""
        return str(self.value)

    def __int__(self) -> int:
        """Return an int of the wrapped value."""
        return int(self.value)

    @classmethod
    def json_schema(cls) -> dict:
        """Return the JSON schema for MonitoringResultId data.

        Returns:
            A Python dictionary describing the JSON schema.
        """
        return {
            "type": "integer"
        }

    @classmethod
    def from_json(cls, data: dict) -> MonitoringResultId:
        """Validate and parse JSON data into an instance of MonitoringResultId.

        Args:
            data (dict): JSON data to validate and parse.

        Returns:
            An instance of MonitoringResultId.

        Raises:
            ValidationError: When schema validation fails.
            KeyError: When a required field is missing from the JSON.
        """
        try:
            jsonschema.validate(data, cls.json_schema())
            return MonitoringResultId(int(data))
        except jsonschema.exceptions.ValidationError as ex:
            logging.debug("Invalid JSON data received while parsing MonitoringResultId", exc_info=ex)
            raise

    def to_json(self) -> dict:
        """Serialise this instance as JSON.

        Returns:
            Data ready to serialise as JSON.
        """
        return self.value

    @classmethod
    def from_json_key(cls, data: str) -> MonitoringResultId:
        """Parse a JSON string such as a dictionary key."""
        return MonitoringResultId(int(data))

    def to_json_key(self) -> str:
        """Serialise as a JSON string suitable for use as a dictionary key."""
        return str(self.value)


@dataclasses.dataclass(frozen=True)
class TableMonitoringJobCreationRequest:
    """Request to create a new table monitoring job.

    Args:
        name (TableMonitoringJobName): A data field.
        description (str): A data field.
        tables (typing.List[TableId]): A data field.
        schedule (Schedule): A data field.
        cluster (ClusterId): A data field.
        clusterPropertySets (typing.Optional[typing.List[ClusterPropertySetId]]): A data field.
        enabled (bool): A data field.
        principal (typing.Optional[UserId]): A data field.
    """

    name: TableMonitoringJobName
    description: str
    tables: typing.List[TableId]
    schedule: Schedule
    cluster: ClusterId
    clusterPropertySets: typing.Optional[typing.List[ClusterPropertySetId]]
    enabled: bool
    principal: typing.Optional[UserId]

    @classmethod
    def json_schema(cls) -> dict:
        """Return the JSON schema for TableMonitoringJobCreationRequest data.

        Returns:
            A Python dictionary describing the JSON schema.
        """
        return {
            "type": "object",
            "properties": {
                "name": TableMonitoringJobName.json_schema(),
                "description": {
                    "type": "string"
                },
                "tables": {
                    "type": "array",
                    "item": TableId.json_schema()
                },
                "schedule": Schedule.json_schema(),
                "cluster": ClusterId.json_schema(),
                "clusterPropertySets": {
                    "oneOf": [
                        {"type": "null"},
                        {"type": "array", "item": ClusterPropertySetId.json_schema()},
                    ]
                },
                "enabled": {
                    "type": "boolean"
                },
                "principal": {
                    "oneOf": [
                        {"type": "null"},
                        UserId.json_schema(),
                    ]
                }
            },
            "required": [
                "name",
                "description",
                "tables",
                "schedule",
                "cluster",
                "enabled",
            ]
        }

    @classmethod
    def from_json(cls, data: dict) -> TableMonitoringJobCreationRequest:
        """Validate and parse JSON data into an instance of TableMonitoringJobCreationRequest.

        Args:
            data (dict): JSON data to validate and parse.

        Returns:
            An instance of TableMonitoringJobCreationRequest.

        Raises:
            ValidationError: When schema validation fails.
            KeyError: When a required field is missing from the JSON.
        """
        try:
            jsonschema.validate(data, cls.json_schema())
            return TableMonitoringJobCreationRequest(
                name=TableMonitoringJobName.from_json(data["name"]),
                description=str(data["description"]),
                tables=[TableId.from_json(v) for v in data["tables"]],
                schedule=Schedule.from_json(data["schedule"]),
                cluster=ClusterId.from_json(data["cluster"]),
                clusterPropertySets=(
                    lambda v: [ClusterPropertySetId.from_json(v) for v in v] if v is not None else None
                )(
                    data.get("clusterPropertySets", None)
                ),
                enabled=bool(data["enabled"]),
                principal=(
                    lambda v: UserId.from_json(v) if v is not None else None
                )(
                    data.get("principal", None)
                ),
            )
        except jsonschema.exceptions.ValidationError as ex:
            logging.debug(
                "Invalid JSON data received while parsing TableMonitoringJobCreationRequest",
                exc_info=ex
            )
            raise

    def to_json(self) -> dict:
        """Serialise this instance as JSON.

        Returns:
            Data ready to serialise as JSON.
        """
        return {
            "name": self.name.to_json(),
            "description": str(self.description),
            "tables": [v.to_json() for v in self.tables],
            "schedule": self.schedule.to_json(),
            "cluster": self.cluster.to_json(),
            "clusterPropertySets": (lambda v: [v.to_json() for v in v] if v is not None else v)(self.clusterPropertySets),
            "enabled": self.enabled,
            "principal": (lambda v: v.to_json() if v is not None else v)(self.principal)
        }


@dataclasses.dataclass(frozen=True)
class TableMonitoringJob:
    """Details of a table monitoring job.

    Args:
        id (TableMonitoringJobId): A data field.
        version (TableMonitoringJobVersionId): A data field.
        name (TableMonitoringJobName): A data field.
        description (str): A data field.
        tables (typing.List[TableId]): A data field.
        created (datetime.datetime): A data field.
        schedule (Schedule): A data field.
        cluster (ClusterId): A data field.
        clusterPropertySets (typing.List[ClusterPropertySetId]): A data field.
        enabled (bool): A data field.
        principal (typing.Optional[UserId]): A data field.
    """

    id: TableMonitoringJobId
    version: TableMonitoringJobVersionId
    name: TableMonitoringJobName
    description: str
    tables: typing.List[TableId]
    created: datetime.datetime
    schedule: Schedule
    cluster: ClusterId
    clusterPropertySets: typing.List[ClusterPropertySetId]
    enabled: bool
    principal: typing.Optional[UserId]

    @classmethod
    def json_schema(cls) -> dict:
        """Return the JSON schema for TableMonitoringJob data.

        Returns:
            A Python dictionary describing the JSON schema.
        """
        return {
            "type": "object",
            "properties": {
                "id": TableMonitoringJobId.json_schema(),
                "version": TableMonitoringJobVersionId.json_schema(),
                "name": TableMonitoringJobName.json_schema(),
                "description": {
                    "type": "string"
                },
                "tables": {
                    "type": "array",
                    "item": TableId.json_schema()
                },
                "created": {
                    "type": "string",
                    "format": "date-time"
                },
                "schedule": Schedule.json_schema(),
                "cluster": ClusterId.json_schema(),
                "clusterPropertySets": {
                    "type": "array",
                    "item": ClusterPropertySetId.json_schema()
                },
                "enabled": {
                    "type": "boolean"
                },
                "principal": {
                    "oneOf": [
                        {"type": "null"},
                        UserId.json_schema(),
                    ]
                }
            },
            "required": [
                "id",
                "version",
                "name",
                "description",
                "tables",
                "created",
                "schedule",
                "cluster",
                "clusterPropertySets",
                "enabled",
            ]
        }

    @classmethod
    def from_json(cls, data: dict) -> TableMonitoringJob:
        """Validate and parse JSON data into an instance of TableMonitoringJob.

        Args:
            data (dict): JSON data to validate and parse.

        Returns:
            An instance of TableMonitoringJob.

        Raises:
            ValidationError: When schema validation fails.
            KeyError: When a required field is missing from the JSON.
        """
        try:
            jsonschema.validate(data, cls.json_schema())
            return TableMonitoringJob(
                id=TableMonitoringJobId.from_json(data["id"]),
                version=TableMonitoringJobVersionId.from_json(data["version"]),
                name=TableMonitoringJobName.from_json(data["name"]),
                description=str(data["description"]),
                tables=[TableId.from_json(v) for v in data["tables"]],
                created=isodate.parse_datetime(data["created"]),
                schedule=Schedule.from_json(data["schedule"]),
                cluster=ClusterId.from_json(data["cluster"]),
                clusterPropertySets=[ClusterPropertySetId.from_json(v) for v in data["clusterPropertySets"]],
                enabled=bool(data["enabled"]),
                principal=(
                    lambda v: UserId.from_json(v) if v is not None else None
                )(
                    data.get("principal", None)
                ),
            )
        except jsonschema.exceptions.ValidationError as ex:
            logging.debug(
                "Invalid JSON data received while parsing TableMonitoringJob",
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
            "version": self.version.to_json(),
            "name": self.name.to_json(),
            "description": str(self.description),
            "tables": [v.to_json() for v in self.tables],
            "created": self.created.strftime('%Y-%m-%dT%H:%M:%S.%f%z'),
            "schedule": self.schedule.to_json(),
            "cluster": self.cluster.to_json(),
            "clusterPropertySets": [v.to_json() for v in self.clusterPropertySets],
            "enabled": self.enabled,
            "principal": (lambda v: v.to_json() if v is not None else v)(self.principal)
        }


@dataclasses.dataclass(frozen=True)
class TableMonitoringRunCreationRequest:
    """Request to create a new table monitoring job run.

    Args:
        jobId (TableMonitoringJobId): A data field.
        jobVersionId (TableMonitoringJobVersionId): A data field.
        status (RunStatus): A data field.
        error (typing.Optional[RunError]): A data field.
        scheduleState (typing.Optional[ScheduleState]): A data field.
        executionStatistics (typing.Optional[ExecutionStatistics]): A data field.
        runBy (typing.Optional[UserId]): A data field.
        operationsCommitId (typing.Optional[CommitId]): A data field.
    """

    jobId: TableMonitoringJobId
    jobVersionId: TableMonitoringJobVersionId
    status: RunStatus
    error: typing.Optional[RunError]
    scheduleState: typing.Optional[ScheduleState]
    executionStatistics: typing.Optional[ExecutionStatistics]
    runBy: typing.Optional[UserId]
    operationsCommitId: typing.Optional[CommitId]

    @classmethod
    def json_schema(cls) -> dict:
        """Return the JSON schema for TableMonitoringRunCreationRequest data.

        Returns:
            A Python dictionary describing the JSON schema.
        """
        return {
            "type": "object",
            "properties": {
                "jobId": TableMonitoringJobId.json_schema(),
                "jobVersionId": TableMonitoringJobVersionId.json_schema(),
                "status": RunStatus.json_schema(),
                "error": {
                    "oneOf": [
                        {"type": "null"},
                        RunError.json_schema(),
                    ]
                },
                "scheduleState": {
                    "oneOf": [
                        {"type": "null"},
                        ScheduleState.json_schema(),
                    ]
                },
                "executionStatistics": {
                    "oneOf": [
                        {"type": "null"},
                        ExecutionStatistics.json_schema(),
                    ]
                },
                "runBy": {
                    "oneOf": [
                        {"type": "null"},
                        UserId.json_schema(),
                    ]
                },
                "operationsCommitId": {
                    "oneOf": [
                        {"type": "null"},
                        CommitId.json_schema(),
                    ]
                }
            },
            "required": [
                "jobId",
                "jobVersionId",
                "status",
            ]
        }

    @classmethod
    def from_json(cls, data: dict) -> TableMonitoringRunCreationRequest:
        """Validate and parse JSON data into an instance of TableMonitoringRunCreationRequest.

        Args:
            data (dict): JSON data to validate and parse.

        Returns:
            An instance of TableMonitoringRunCreationRequest.

        Raises:
            ValidationError: When schema validation fails.
            KeyError: When a required field is missing from the JSON.
        """
        try:
            jsonschema.validate(data, cls.json_schema())
            return TableMonitoringRunCreationRequest(
                jobId=TableMonitoringJobId.from_json(data["jobId"]),
                jobVersionId=TableMonitoringJobVersionId.from_json(data["jobVersionId"]),
                status=RunStatus.from_json(data["status"]),
                error=(
                    lambda v: RunError.from_json(v) if v is not None else None
                )(
                    data.get("error", None)
                ),
                scheduleState=(
                    lambda v: ScheduleState.from_json(v) if v is not None else None
                )(
                    data.get("scheduleState", None)
                ),
                executionStatistics=(
                    lambda v: ExecutionStatistics.from_json(v) if v is not None else None
                )(
                    data.get("executionStatistics", None)
                ),
                runBy=(
                    lambda v: UserId.from_json(v) if v is not None else None
                )(
                    data.get("runBy", None)
                ),
                operationsCommitId=(
                    lambda v: CommitId.from_json(v) if v is not None else None
                )(
                    data.get("operationsCommitId", None)
                ),
            )
        except jsonschema.exceptions.ValidationError as ex:
            logging.debug(
                "Invalid JSON data received while parsing TableMonitoringRunCreationRequest",
                exc_info=ex
            )
            raise

    def to_json(self) -> dict:
        """Serialise this instance as JSON.

        Returns:
            Data ready to serialise as JSON.
        """
        return {
            "jobId": self.jobId.to_json(),
            "jobVersionId": self.jobVersionId.to_json(),
            "status": self.status.to_json(),
            "error": (lambda v: v.to_json() if v is not None else v)(self.error),
            "scheduleState": (lambda v: v.to_json() if v is not None else v)(self.scheduleState),
            "executionStatistics": (lambda v: v.to_json() if v is not None else v)(self.executionStatistics),
            "runBy": (lambda v: v.to_json() if v is not None else v)(self.runBy),
            "operationsCommitId": (lambda v: v.to_json() if v is not None else v)(self.operationsCommitId)
        }


@dataclasses.dataclass(frozen=True)
class TableMonitoringRun:
    """Details of a table monitoring job run.

    Args:
        id (TableMonitoringRunId): A data field.
        jobId (TableMonitoringJobId): A data field.
        jobVersionId (TableMonitoringJobVersionId): A data field.
        created (datetime.datetime): A data field.
        status (RunStatus): A data field.
        error (typing.Optional[RunError]): A data field.
        scheduleState (typing.Optional[ScheduleState]): A data field.
        executionStatistics (typing.Optional[ExecutionStatistics]): A data field.
        runBy (typing.Optional[UserId]): A data field.
        operationsCommitId (typing.Optional[CommitId]): A data field.
    """

    id: TableMonitoringRunId
    jobId: TableMonitoringJobId
    jobVersionId: TableMonitoringJobVersionId
    created: datetime.datetime
    status: RunStatus
    error: typing.Optional[RunError]
    scheduleState: typing.Optional[ScheduleState]
    executionStatistics: typing.Optional[ExecutionStatistics]
    runBy: typing.Optional[UserId]
    operationsCommitId: typing.Optional[CommitId]

    @classmethod
    def json_schema(cls) -> dict:
        """Return the JSON schema for TableMonitoringRun data.

        Returns:
            A Python dictionary describing the JSON schema.
        """
        return {
            "type": "object",
            "properties": {
                "id": TableMonitoringRunId.json_schema(),
                "jobId": TableMonitoringJobId.json_schema(),
                "jobVersionId": TableMonitoringJobVersionId.json_schema(),
                "created": {
                    "type": "string",
                    "format": "date-time"
                },
                "status": RunStatus.json_schema(),
                "error": {
                    "oneOf": [
                        {"type": "null"},
                        RunError.json_schema(),
                    ]
                },
                "scheduleState": {
                    "oneOf": [
                        {"type": "null"},
                        ScheduleState.json_schema(),
                    ]
                },
                "executionStatistics": {
                    "oneOf": [
                        {"type": "null"},
                        ExecutionStatistics.json_schema(),
                    ]
                },
                "runBy": {
                    "oneOf": [
                        {"type": "null"},
                        UserId.json_schema(),
                    ]
                },
                "operationsCommitId": {
                    "oneOf": [
                        {"type": "null"},
                        CommitId.json_schema(),
                    ]
                }
            },
            "required": [
                "id",
                "jobId",
                "jobVersionId",
                "created",
                "status",
            ]
        }

    @classmethod
    def from_json(cls, data: dict) -> TableMonitoringRun:
        """Validate and parse JSON data into an instance of TableMonitoringRun.

        Args:
            data (dict): JSON data to validate and parse.

        Returns:
            An instance of TableMonitoringRun.

        Raises:
            ValidationError: When schema validation fails.
            KeyError: When a required field is missing from the JSON.
        """
        try:
            jsonschema.validate(data, cls.json_schema())
            return TableMonitoringRun(
                id=TableMonitoringRunId.from_json(data["id"]),
                jobId=TableMonitoringJobId.from_json(data["jobId"]),
                jobVersionId=TableMonitoringJobVersionId.from_json(data["jobVersionId"]),
                created=isodate.parse_datetime(data["created"]),
                status=RunStatus.from_json(data["status"]),
                error=(
                    lambda v: RunError.from_json(v) if v is not None else None
                )(
                    data.get("error", None)
                ),
                scheduleState=(
                    lambda v: ScheduleState.from_json(v) if v is not None else None
                )(
                    data.get("scheduleState", None)
                ),
                executionStatistics=(
                    lambda v: ExecutionStatistics.from_json(v) if v is not None else None
                )(
                    data.get("executionStatistics", None)
                ),
                runBy=(
                    lambda v: UserId.from_json(v) if v is not None else None
                )(
                    data.get("runBy", None)
                ),
                operationsCommitId=(
                    lambda v: CommitId.from_json(v) if v is not None else None
                )(
                    data.get("operationsCommitId", None)
                ),
            )
        except jsonschema.exceptions.ValidationError as ex:
            logging.debug(
                "Invalid JSON data received while parsing TableMonitoringRun",
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
            "jobId": self.jobId.to_json(),
            "jobVersionId": self.jobVersionId.to_json(),
            "created": self.created.strftime('%Y-%m-%dT%H:%M:%S.%f%z'),
            "status": self.status.to_json(),
            "error": (lambda v: v.to_json() if v is not None else v)(self.error),
            "scheduleState": (lambda v: v.to_json() if v is not None else v)(self.scheduleState),
            "executionStatistics": (lambda v: v.to_json() if v is not None else v)(self.executionStatistics),
            "runBy": (lambda v: v.to_json() if v is not None else v)(self.runBy),
            "operationsCommitId": (lambda v: v.to_json() if v is not None else v)(self.operationsCommitId)
        }


@dataclasses.dataclass(frozen=True)
class MonitoringResultCreationRequest:
    """Request to record monitoring results from a monitoring run.
    
    Args:
        table (TableId): A data field.
        tableVersion (TableVersionId): A data field.
        job (TableMonitoringJobId): A data field.
        run (TableMonitoringRunId): A data field.
        partition (str): A data field.
        count (int): A data field.
        columnStatistics (typing.List[SummaryStatistics]): A data field.
    """

    table: TableId
    tableVersion: TableVersionId
    job: TableMonitoringJobId
    run: TableMonitoringRunId
    partition: str
    count: int
    columnStatistics: typing.List[SummaryStatistics]

    @classmethod
    def json_schema(cls) -> dict:
        """Return the JSON schema for MonitoringResultCreationRequest data.
        
        Returns:
            A Python dictionary describing the JSON schema.
        """
        return {
            "type": "object",
            "properties": {
                "table": TableId.json_schema(),
                "tableVersion": TableVersionId.json_schema(),
                "job": TableMonitoringJobId.json_schema(),
                "run": TableMonitoringRunId.json_schema(),
                "partition": {
                    "type": "string"
                },
                "count": {
                    "type": "integer"
                },
                "columnStatistics": {
                    "type": "array",
                    "item": SummaryStatistics.json_schema()
                }
            },
            "required": [
                "table",
                "tableVersion",
                "job",
                "run",
                "partition",
                "count",
                "columnStatistics",
            ]
        }

    @classmethod
    def from_json(cls, data: dict) -> MonitoringResultCreationRequest:
        """Validate and parse JSON data into an instance of MonitoringResultCreationRequest.
        
        Args:
            data (dict): JSON data to validate and parse.
        
        Returns:
            An instance of MonitoringResultCreationRequest.
        
        Raises:
            ValidationError: When schema validation fails.
            KeyError: When a required field is missing from the JSON.
        """
        try:
            jsonschema.validate(data, cls.json_schema())
            return MonitoringResultCreationRequest(
                table=TableId.from_json(data["table"]),
                tableVersion=TableVersionId.from_json(data["tableVersion"]),
                job=TableMonitoringJobId.from_json(data["job"]),
                run=TableMonitoringRunId.from_json(data["run"]),
                partition=str(data["partition"]),
                count=int(data["count"]),
                columnStatistics=[SummaryStatistics.from_json(v) for v in data["columnStatistics"]],
            )
        except jsonschema.exceptions.ValidationError as ex:
            logging.debug(
                "Invalid JSON data received while parsing MonitoringResultCreationRequest",
                exc_info=ex
            )
            raise

    def to_json(self) -> dict:
        """Serialise this instance as JSON.
        
        Returns:
            Data ready to serialise as JSON.
        """
        return {
            "table": self.table.to_json(),
            "tableVersion": self.tableVersion.to_json(),
            "job": self.job.to_json(),
            "run": self.run.to_json(),
            "partition": str(self.partition),
            "count": self.count,
            "columnStatistics": [v.to_json() for v in self.columnStatistics]
        }


@dataclasses.dataclass(frozen=True)
class MonitoringResultPartial:
    """Partial details of a monitoring result.
    
    This class omits the large fields containing detailed monitoring data to
    reduce the amount of data transferred from the server.
    
    Args:
        id (MonitoringResultId): A data field.
        table (TableId): A data field.
        tableVersion (TableVersionId): A data field.
        job (TableMonitoringJobId): A data field.
        run (TableMonitoringRunId): A data field.
        partition (str): A data field.
        count (int): A data field.
    """

    id: MonitoringResultId
    table: TableId
    tableVersion: TableVersionId
    job: TableMonitoringJobId
    run: TableMonitoringRunId
    partition: str
    count: int

    @classmethod
    def json_schema(cls) -> dict:
        """Return the JSON schema for MonitoringResultPartial data.
        
        Returns:
            A Python dictionary describing the JSON schema.
        """
        return {
            "type": "object",
            "properties": {
                "id": MonitoringResultId.json_schema(),
                "table": TableId.json_schema(),
                "tableVersion": TableVersionId.json_schema(),
                "job": TableMonitoringJobId.json_schema(),
                "run": TableMonitoringRunId.json_schema(),
                "partition": {
                    "type": "string"
                },
                "count": {
                    "type": "integer"
                }
            },
            "required": [
                "id",
                "table",
                "tableVersion",
                "job",
                "run",
                "partition",
                "count",
            ]
        }

    @classmethod
    def from_json(cls, data: dict) -> MonitoringResultPartial:
        """Validate and parse JSON data into an instance of MonitoringResultPartial.
        
        Args:
            data (dict): JSON data to validate and parse.
        
        Returns:
            An instance of MonitoringResultPartial.
        
        Raises:
            ValidationError: When schema validation fails.
            KeyError: When a required field is missing from the JSON.
        """
        try:
            jsonschema.validate(data, cls.json_schema())
            return MonitoringResultPartial(
                id=MonitoringResultId.from_json(data["id"]),
                table=TableId.from_json(data["table"]),
                tableVersion=TableVersionId.from_json(data["tableVersion"]),
                job=TableMonitoringJobId.from_json(data["job"]),
                run=TableMonitoringRunId.from_json(data["run"]),
                partition=str(data["partition"]),
                count=int(data["count"]),
            )
        except jsonschema.exceptions.ValidationError as ex:
            logging.debug(
                "Invalid JSON data received while parsing MonitoringResultPartial",
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
            "table": self.table.to_json(),
            "tableVersion": self.tableVersion.to_json(),
            "job": self.job.to_json(),
            "run": self.run.to_json(),
            "partition": str(self.partition),
            "count": self.count
        }


@dataclasses.dataclass(frozen=True)
class MonitoringResult:
    """Detailed monitoring results from a table monitoring run.
    
    Instances of this class contain the full results from a table monitoring
    job run. As such, they can be very large. Unless you need to use the
    statistical results computed during the monitoring run, you should use
    MonitoringResultPartial instead.
    
    Args:
        id (MonitoringResultId): A data field.
        table (TableId): A data field.
        tableVersion (TableVersionId): A data field.
        job (TableMonitoringJobId): A data field.
        run (TableMonitoringRunId): A data field.
        partition (str): A data field.
        count (int): A data field.
        columnStatistics (typing.List[SummaryStatistics]): A data field.
    """

    id: MonitoringResultId
    table: TableId
    tableVersion: TableVersionId
    job: TableMonitoringJobId
    run: TableMonitoringRunId
    partition: str
    count: int
    columnStatistics: typing.List[SummaryStatistics]

    @classmethod
    def json_schema(cls) -> dict:
        """Return the JSON schema for MonitoringResult data.
        
        Returns:
            A Python dictionary describing the JSON schema.
        """
        return {
            "type": "object",
            "properties": {
                "id": MonitoringResultId.json_schema(),
                "table": TableId.json_schema(),
                "tableVersion": TableVersionId.json_schema(),
                "job": TableMonitoringJobId.json_schema(),
                "run": TableMonitoringRunId.json_schema(),
                "partition": {
                    "type": "string"
                },
                "count": {
                    "type": "integer"
                },
                "columnStatistics": {
                    "type": "array",
                    "item": SummaryStatistics.json_schema()
                }
            },
            "required": [
                "id",
                "table",
                "tableVersion",
                "job",
                "run",
                "partition",
                "count",
                "columnStatistics",
            ]
        }

    @classmethod
    def from_json(cls, data: dict) -> MonitoringResult:
        """Validate and parse JSON data into an instance of MonitoringResult.
        
        Args:
            data (dict): JSON data to validate and parse.
        
        Returns:
            An instance of MonitoringResult.
        
        Raises:
            ValidationError: When schema validation fails.
            KeyError: When a required field is missing from the JSON.
        """
        try:
            jsonschema.validate(data, cls.json_schema())
            return MonitoringResult(
                id=MonitoringResultId.from_json(data["id"]),
                table=TableId.from_json(data["table"]),
                tableVersion=TableVersionId.from_json(data["tableVersion"]),
                job=TableMonitoringJobId.from_json(data["job"]),
                run=TableMonitoringRunId.from_json(data["run"]),
                partition=str(data["partition"]),
                count=int(data["count"]),
                columnStatistics=[SummaryStatistics.from_json(v) for v in data["columnStatistics"]],
            )
        except jsonschema.exceptions.ValidationError as ex:
            logging.debug(
                "Invalid JSON data received while parsing MonitoringResult",
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
            "table": self.table.to_json(),
            "tableVersion": self.tableVersion.to_json(),
            "job": self.job.to_json(),
            "run": self.run.to_json(),
            "partition": str(self.partition),
            "count": self.count,
            "columnStatistics": [v.to_json() for v in self.columnStatistics]
        }
