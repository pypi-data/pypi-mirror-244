"""Generated implementation of view_materialisation."""

# WARNING DO NOT EDIT
# This code was generated from view-materialisation.mcn

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

from ..attribute import Attribute
from ..cluster import ClusterId, ClusterPropertySetId
from ..commit import CommitId
from ..destination_reference import DestinationReference
from ..feature_store import VersionTarget
from ..label import Label
from ..schedule import Duration, Schedule
from ..table import TableId
from ..user import UserId


@dataclasses.dataclass(frozen=True)
class ViewMaterialisationJobId:
    """Unique identifier of a view materialisation job.
    
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
        """Return the JSON schema for ViewMaterialisationJobId data.
        
        Returns:
            A Python dictionary describing the JSON schema.
        """
        return {
            "type": "integer"
        }
    
    @classmethod
    def from_json(cls, data: dict) -> ViewMaterialisationJobId:
        """Validate and parse JSON data into an instance of ViewMaterialisationJobId.
        
        Args:
            data (dict): JSON data to validate and parse.
        
        Returns:
            An instance of ViewMaterialisationJobId.
        
        Raises:
            ValidationError: When schema validation fails.
            KeyError: When a required field is missing from the JSON.
        """
        try:
            jsonschema.validate(data, cls.json_schema())
            return ViewMaterialisationJobId(int(data))
        except jsonschema.exceptions.ValidationError as ex:
            logging.debug("Invalid JSON data received while parsing ViewMaterialisationJobId", exc_info=ex)
            raise
    
    def to_json(self) -> dict:
        """Serialise this instance as JSON.
        
        Returns:
            Data ready to serialise as JSON.
        """
        return int(self.value)
    
    @classmethod
    def from_json_key(cls, data: str) -> ViewMaterialisationJobId:
        """Parse a JSON string such as a dictionary key."""
        return ViewMaterialisationJobId(int(data))
    
    def to_json_key(self) -> str:
        """Serialise as a JSON string suitable for use as a dictionary key."""
        return str(self.value)


@dataclasses.dataclass(frozen=True)
class ViewMaterialisationJobName:
    """Unique name for a view materialisation job.
    
    Args:
        value (str): A data field.
    """
    
    value: str
    
    def __str__(self) -> str:
        """Return a str of the wrapped value."""
        return str(self.value)
    
    @classmethod
    def json_schema(cls) -> dict:
        """Return the JSON schema for ViewMaterialisationJobName data.
        
        Returns:
            A Python dictionary describing the JSON schema.
        """
        return {
            "type": "string"
        }
    
    @classmethod
    def from_json(cls, data: dict) -> ViewMaterialisationJobName:
        """Validate and parse JSON data into an instance of ViewMaterialisationJobName.
        
        Args:
            data (dict): JSON data to validate and parse.
        
        Returns:
            An instance of ViewMaterialisationJobName.
        
        Raises:
            ValidationError: When schema validation fails.
            KeyError: When a required field is missing from the JSON.
        """
        try:
            jsonschema.validate(data, cls.json_schema())
            return ViewMaterialisationJobName(str(data))
        except jsonschema.exceptions.ValidationError as ex:
            logging.debug("Invalid JSON data received while parsing ViewMaterialisationJobName", exc_info=ex)
            raise
    
    def to_json(self) -> dict:
        """Serialise this instance as JSON.
        
        Returns:
            Data ready to serialise as JSON.
        """
        return str(self.value)
    
    @classmethod
    def from_json_key(cls, data: str) -> ViewMaterialisationJobName:
        """Parse a JSON string such as a dictionary key."""
        return ViewMaterialisationJobName(str(data))
    
    def to_json_key(self) -> str:
        """Serialise as a JSON string suitable for use as a dictionary key."""
        return str(self.value)


@dataclasses.dataclass(frozen=True)
class ViewMaterialisationJobVersionId:
    """Unique identifier for a specific version of a view materialisation job.
    
    Args:
        value (uuid.UUID): A data field.
    """
    
    value: uuid.UUID
    
    def __str__(self) -> str:
        """Return a str of the wrapped value."""
        return str(self.value)
    
    @classmethod
    def json_schema(cls) -> dict:
        """Return the JSON schema for ViewMaterialisationJobVersionId data.
        
        Returns:
            A Python dictionary describing the JSON schema.
        """
        return {
            "type": "string",
            "format": "uuid"
        }
    
    @classmethod
    def from_json(cls, data: dict) -> ViewMaterialisationJobVersionId:
        """Validate and parse JSON data into an instance of ViewMaterialisationJobVersionId.
        
        Args:
            data (dict): JSON data to validate and parse.
        
        Returns:
            An instance of ViewMaterialisationJobVersionId.
        
        Raises:
            ValidationError: When schema validation fails.
            KeyError: When a required field is missing from the JSON.
        """
        try:
            jsonschema.validate(data, cls.json_schema())
            return ViewMaterialisationJobVersionId(uuid.UUID(hex=data))
        except jsonschema.exceptions.ValidationError as ex:
            logging.debug("Invalid JSON data received while parsing ViewMaterialisationJobVersionId", exc_info=ex)
            raise
    
    def to_json(self) -> dict:
        """Serialise this instance as JSON.
        
        Returns:
            Data ready to serialise as JSON.
        """
        return str(self.value)
    
    @classmethod
    def from_json_key(cls, data: str) -> ViewMaterialisationJobVersionId:
        """Parse a JSON string such as a dictionary key."""
        return ViewMaterialisationJobVersionId((lambda s: uuid.UUID(hex=s))(data))
    
    def to_json_key(self) -> str:
        """Serialise as a JSON string suitable for use as a dictionary key."""
        return str(self.value)


@dataclasses.dataclass(frozen=True)
class ViewMaterialisationRunId:
    """Unique identifier of a view materialisation job run.
    
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
        """Return the JSON schema for ViewMaterialisationRunId data.
        
        Returns:
            A Python dictionary describing the JSON schema.
        """
        return {
            "type": "integer"
        }
    
    @classmethod
    def from_json(cls, data: dict) -> ViewMaterialisationRunId:
        """Validate and parse JSON data into an instance of ViewMaterialisationRunId.
        
        Args:
            data (dict): JSON data to validate and parse.
        
        Returns:
            An instance of ViewMaterialisationRunId.
        
        Raises:
            ValidationError: When schema validation fails.
            KeyError: When a required field is missing from the JSON.
        """
        try:
            jsonschema.validate(data, cls.json_schema())
            return ViewMaterialisationRunId(int(data))
        except jsonschema.exceptions.ValidationError as ex:
            logging.debug("Invalid JSON data received while parsing ViewMaterialisationRunId", exc_info=ex)
            raise
    
    def to_json(self) -> dict:
        """Serialise this instance as JSON.
        
        Returns:
            Data ready to serialise as JSON.
        """
        return self.value
    
    @classmethod
    def from_json_key(cls, data: str) -> ViewMaterialisationRunId:
        """Parse a JSON string such as a dictionary key."""
        return ViewMaterialisationRunId(int(data))
    
    def to_json_key(self) -> str:
        """Serialise as a JSON string suitable for use as a dictionary key."""
        return str(self.value)


@dataclasses.dataclass(frozen=True)
class ViewMaterialisationId:
    """Unique identifier of a view materialisation job run.
    
    Args:
        value (uuid.UUID): A data field.
    """
    
    value: uuid.UUID
    
    def __str__(self) -> str:
        """Return a str of the wrapped value."""
        return str(self.value)
    
    @classmethod
    def json_schema(cls) -> dict:
        """Return the JSON schema for ViewMaterialisationId data.
        
        Returns:
            A Python dictionary describing the JSON schema.
        """
        return {
            "type": "string",
            "format": "uuid"
        }
    
    @classmethod
    def from_json(cls, data: dict) -> ViewMaterialisationId:
        """Validate and parse JSON data into an instance of ViewMaterialisationId.
        
        Args:
            data (dict): JSON data to validate and parse.
        
        Returns:
            An instance of ViewMaterialisationId.
        
        Raises:
            ValidationError: When schema validation fails.
            KeyError: When a required field is missing from the JSON.
        """
        try:
            jsonschema.validate(data, cls.json_schema())
            return ViewMaterialisationId(uuid.UUID(hex=data))
        except jsonschema.exceptions.ValidationError as ex:
            logging.debug("Invalid JSON data received while parsing ViewMaterialisationId", exc_info=ex)
            raise
    
    def to_json(self) -> dict:
        """Serialise this instance as JSON.
        
        Returns:
            Data ready to serialise as JSON.
        """
        return str(self.value)
    
    @classmethod
    def from_json_key(cls, data: str) -> ViewMaterialisationId:
        """Parse a JSON string such as a dictionary key."""
        return ViewMaterialisationId((lambda s: uuid.UUID(hex=s))(data))
    
    def to_json_key(self) -> str:
        """Serialise as a JSON string suitable for use as a dictionary key."""
        return str(self.value)


@dataclasses.dataclass(frozen=True)
class ViewMaterialisation:
    """Details particular materialisation.
    
    Args:
        id (ViewMaterialisationId): A data field.
        job (ViewMaterialisationJobId): A data field.
        run (ViewMaterialisationRunId): A data field.
        table (TableId): A data field.
        destination (DestinationReference): A data field.
        commit (CommitId): A data field.
        ops (CommitId): A data field.
        created (datetime.datetime): A data field.
    """
    
    id: ViewMaterialisationId
    job: ViewMaterialisationJobId
    run: ViewMaterialisationRunId
    table: TableId
    destination: DestinationReference
    commit: CommitId
    ops: CommitId
    created: datetime.datetime
    
    @classmethod
    def json_schema(cls) -> dict:
        """Return the JSON schema for ViewMaterialisation data.
        
        Returns:
            A Python dictionary describing the JSON schema.
        """
        return {
            "type": "object",
            "properties": {
                "id": ViewMaterialisationId.json_schema(),
                "job": ViewMaterialisationJobId.json_schema(),
                "run": ViewMaterialisationRunId.json_schema(),
                "table": TableId.json_schema(),
                "destination": DestinationReference.json_schema(),
                "commit": CommitId.json_schema(),
                "ops": CommitId.json_schema(),
                "created": {
                    "type": "string",
                    "format": "date-time"
                }
            },
            "required": [
                "id",
                "job",
                "run",
                "table",
                "destination",
                "commit",
                "ops",
                "created",
            ]
        }
    
    @classmethod
    def from_json(cls, data: dict) -> ViewMaterialisation:
        """Validate and parse JSON data into an instance of ViewMaterialisation.
        
        Args:
            data (dict): JSON data to validate and parse.
        
        Returns:
            An instance of ViewMaterialisation.
        
        Raises:
            ValidationError: When schema validation fails.
            KeyError: When a required field is missing from the JSON.
        """
        try:
            jsonschema.validate(data, cls.json_schema())
            return ViewMaterialisation(
                id=ViewMaterialisationId.from_json(data["id"]),
                job=ViewMaterialisationJobId.from_json(data["job"]),
                run=ViewMaterialisationRunId.from_json(data["run"]),
                table=TableId.from_json(data["table"]),
                destination=DestinationReference.from_json(data["destination"]),
                commit=CommitId.from_json(data["commit"]),
                ops=CommitId.from_json(data["ops"]),
                created=isodate.parse_datetime(data["created"]),
            )
        except jsonschema.exceptions.ValidationError as ex:
            logging.debug(
                "Invalid JSON data received while parsing ViewMaterialisation",
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
            "run": self.run.to_json(),
            "table": self.table.to_json(),
            "destination": self.destination.to_json(),
            "commit": self.commit.to_json(),
            "ops": self.ops.to_json(),
            "created": self.created.strftime('%Y-%m-%dT%H:%M:%S.%f%z')
        }


@dataclasses.dataclass(frozen=True)
class ViewMaterialisationCreationRequest:
    """Details particular materialisation.
    
    Args:
        job (ViewMaterialisationJobId): A data field.
        run (ViewMaterialisationRunId): A data field.
        table (TableId): A data field.
        destination (DestinationReference): A data field.
        commit (CommitId): A data field.
        ops (CommitId): A data field.
        created (datetime.datetime): A data field.
    """
    
    job: ViewMaterialisationJobId
    run: ViewMaterialisationRunId
    table: TableId
    destination: DestinationReference
    commit: CommitId
    ops: CommitId
    created: datetime.datetime
    
    @classmethod
    def json_schema(cls) -> dict:
        """Return the JSON schema for ViewMaterialisationCreationRequest data.
        
        Returns:
            A Python dictionary describing the JSON schema.
        """
        return {
            "type": "object",
            "properties": {
                "job": ViewMaterialisationJobId.json_schema(),
                "run": ViewMaterialisationRunId.json_schema(),
                "table": TableId.json_schema(),
                "destination": DestinationReference.json_schema(),
                "commit": CommitId.json_schema(),
                "ops": CommitId.json_schema(),
                "created": {
                    "type": "string",
                    "format": "date-time"
                }
            },
            "required": [
                "job",
                "run",
                "table",
                "destination",
                "commit",
                "ops",
                "created",
            ]
        }
    
    @classmethod
    def from_json(cls, data: dict) -> ViewMaterialisationCreationRequest:
        """Validate and parse JSON data into an instance of ViewMaterialisationCreationRequest.
        
        Args:
            data (dict): JSON data to validate and parse.
        
        Returns:
            An instance of ViewMaterialisationCreationRequest.
        
        Raises:
            ValidationError: When schema validation fails.
            KeyError: When a required field is missing from the JSON.
        """
        try:
            jsonschema.validate(data, cls.json_schema())
            return ViewMaterialisationCreationRequest(
                job=ViewMaterialisationJobId.from_json(data["job"]),
                run=ViewMaterialisationRunId.from_json(data["run"]),
                table=TableId.from_json(data["table"]),
                destination=DestinationReference.from_json(data["destination"]),
                commit=CommitId.from_json(data["commit"]),
                ops=CommitId.from_json(data["ops"]),
                created=isodate.parse_datetime(data["created"]),
            )
        except jsonschema.exceptions.ValidationError as ex:
            logging.debug(
                "Invalid JSON data received while parsing ViewMaterialisationCreationRequest",
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
            "run": self.run.to_json(),
            "table": self.table.to_json(),
            "destination": self.destination.to_json(),
            "commit": self.commit.to_json(),
            "ops": self.ops.to_json(),
            "created": self.created.strftime('%Y-%m-%dT%H:%M:%S.%f%z')
        }


@dataclasses.dataclass(frozen=True)
class ViewMaterialisationSpec:
    """Details of the table to be materialised
    
    Args:
        table (TableId): A data field.
        destination (DestinationReference): A data field.
    """
    
    table: TableId
    destination: DestinationReference
    
    @classmethod
    def json_schema(cls) -> dict:
        """Return the JSON schema for ViewMaterialisationSpec data.
        
        Returns:
            A Python dictionary describing the JSON schema.
        """
        return {
            "type": "object",
            "properties": {
                "table": TableId.json_schema(),
                "destination": DestinationReference.json_schema()
            },
            "required": [
                "table",
                "destination",
            ]
        }
    
    @classmethod
    def from_json(cls, data: dict) -> ViewMaterialisationSpec:
        """Validate and parse JSON data into an instance of ViewMaterialisationSpec.
        
        Args:
            data (dict): JSON data to validate and parse.
        
        Returns:
            An instance of ViewMaterialisationSpec.
        
        Raises:
            ValidationError: When schema validation fails.
            KeyError: When a required field is missing from the JSON.
        """
        try:
            jsonschema.validate(data, cls.json_schema())
            return ViewMaterialisationSpec(
                table=TableId.from_json(data["table"]),
                destination=DestinationReference.from_json(data["destination"]),
            )
        except jsonschema.exceptions.ValidationError as ex:
            logging.debug(
                "Invalid JSON data received while parsing ViewMaterialisationSpec",
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
            "destination": self.destination.to_json()
        }


@dataclasses.dataclass(frozen=True)
class ViewMaterialisationJobCreationRequest(abc.ABC):
    """Request to create a new view materialisation job.
    
    Args:
        attributes (typing.List[Attribute]): A data field.
        cluster (ClusterId): A data field.
        clusterPropertySets (typing.Optional[typing.List[ClusterPropertySetId]]): A data field.
        description (str): A data field.
        labels (typing.List[Label]): A data field.
        name (ViewMaterialisationJobName): A data field.
        principal (typing.Optional[UserId]): A data field.
        usageTTL (typing.Optional[Duration]): A data field.
        versionTarget (typing.Optional[VersionTarget]): A data field.
        views (typing.List[ViewMaterialisationSpec]): A data field.
    """
    
    ADT_TYPE: typing.ClassVar[str] = ""
    adt_type: str = dataclasses.field(init=False, repr=False, default=ADT_TYPE)
    
    attributes: typing.List[Attribute]
    cluster: ClusterId
    clusterPropertySets: typing.Optional[typing.List[ClusterPropertySetId]]
    description: str
    labels: typing.List[Label]
    name: ViewMaterialisationJobName
    principal: typing.Optional[UserId]
    usageTTL: typing.Optional[Duration]
    versionTarget: typing.Optional[VersionTarget]
    views: typing.List[ViewMaterialisationSpec]
    
    @classmethod
    def json_schema(cls) -> ViewMaterialisationJobCreationRequest:
        """JSON schema for variant ViewMaterialisationJobCreationRequest.
        
        Returns:
            A Python dictionary describing the JSON schema.
        """
        adt_types = [klass.ADT_TYPE for klass in cls.__subclasses__()]
        return {
            "type": "object",
            "properties": {
                "adt_type": {
                    "type": "string",
                    "enum": adt_types
                }
            },
            "required": [
                "adt_type",
            ]
        }
    
    @classmethod
    def from_json(cls, data: dict) -> ViewMaterialisationJobCreationRequest:
        """Validate and parse JSON data into an instance of ViewMaterialisationJobCreationRequest.
        
        Args:
            data (dict): JSON data to validate and parse.
        
        Returns:
            An instance of ViewMaterialisationJobCreationRequest.
        
        Raises:
            ValidationError: When schema validation fails.
            KeyError: When a required field is missing from the JSON.
        """
        try:
            jsonschema.validate(data, cls.json_schema())
            adt_type = data.get("adt_type", None)
            for klass in cls.__subclasses__():
                if klass.ADT_TYPE == adt_type:
                    return klass.from_json(data)
            raise ValueError("Unknown adt_type: '{ty}'".format(ty=adt_type))
        except jsonschema.exceptions.ValidationError as ex:
            logging.debug("Invalid JSON data received while parsing ViewMaterialisationJobCreationRequest", exc_info=ex)
            raise
    
    @abc.abstractmethod
    def to_json(self) -> dict:
        """Serialise this instance as JSON.
        
        Returns:
            Data ready to serialise as JSON.
        """
        raise NotImplementedError


@dataclasses.dataclass(frozen=True)
class BatchViewMaterialisationJobCreationRequest(ViewMaterialisationJobCreationRequest):
    """A batch view materialisation job creation request.
    
    Args:
        name (ViewMaterialisationJobName): A data field.
        description (str): A data field.
        labels (typing.List[Label]): A data field.
        attributes (typing.List[Attribute]): A data field.
        usageTTL (typing.Optional[Duration]): A data field.
        views (typing.List[ViewMaterialisationSpec]): A data field.
        principal (typing.Optional[UserId]): A data field.
        schedule (Schedule): A data field.
        cluster (ClusterId): A data field.
        clusterPropertySets (typing.Optional[typing.List[ClusterPropertySetId]]): A data field.
        includeMetadata (bool): A data field.
        versionTarget (typing.Optional[VersionTarget]): A data field.
    """
    
    ADT_TYPE: typing.ClassVar[str] = "batch"
    adt_type: str = dataclasses.field(init=False, repr=False, default=ADT_TYPE)
    
    name: ViewMaterialisationJobName
    description: str
    labels: typing.List[Label]
    attributes: typing.List[Attribute]
    usageTTL: typing.Optional[Duration]
    views: typing.List[ViewMaterialisationSpec]
    principal: typing.Optional[UserId]
    schedule: Schedule
    cluster: ClusterId
    clusterPropertySets: typing.Optional[typing.List[ClusterPropertySetId]]
    includeMetadata: bool
    versionTarget: typing.Optional[VersionTarget]
    
    @classmethod
    def json_schema(cls) -> dict:
        """Return the JSON schema for BatchViewMaterialisationJobCreationRequest data.
        
        Returns:
            A Python dictionary describing the JSON schema.
        """
        return {
            "type": "object",
            "properties": {
                "adt_type": {
                    "type": "string",
                    "enum": [cls.ADT_TYPE]
                },
                "name": ViewMaterialisationJobName.json_schema(),
                "description": {
                    "type": "string"
                },
                "labels": {
                    "type": "array",
                    "item": Label.json_schema()
                },
                "attributes": {
                    "type": "array",
                    "item": Attribute.json_schema()
                },
                "usageTTL": {
                    "oneOf": [
                        {"type": "null"},
                        Duration.json_schema(),
                    ]
                },
                "views": {
                    "type": "array",
                    "item": ViewMaterialisationSpec.json_schema()
                },
                "principal": {
                    "oneOf": [
                        {"type": "null"},
                        UserId.json_schema(),
                    ]
                },
                "schedule": Schedule.json_schema(),
                "cluster": ClusterId.json_schema(),
                "clusterPropertySets": {
                    "oneOf": [
                        {"type": "null"},
                        {"type": "array", "item": ClusterPropertySetId.json_schema()},
                    ]
                },
                "includeMetadata": {
                    "type": "boolean"
                },
                "versionTarget": {
                    "oneOf": [
                        {"type": "null"},
                        VersionTarget.json_schema(),
                    ]
                }
            },
            "required": [
                "adt_type",
                "name",
                "description",
                "labels",
                "attributes",
                "views",
                "schedule",
                "cluster",
                "includeMetadata",
            ]
        }
    
    @classmethod
    def from_json(cls, data: dict) -> BatchViewMaterialisationJobCreationRequest:
        """Validate and parse JSON data into an instance of BatchViewMaterialisationJobCreationRequest.
        
        Args:
            data (dict): JSON data to validate and parse.
        
        Returns:
            An instance of BatchViewMaterialisationJobCreationRequest.
        
        Raises:
            ValidationError: When schema validation fails.
            KeyError: When a required field is missing from the JSON.
        """
        try:
            jsonschema.validate(data, cls.json_schema())
            return BatchViewMaterialisationJobCreationRequest(
                name=ViewMaterialisationJobName.from_json(data["name"]),
                description=str(data["description"]),
                labels=[Label.from_json(v) for v in data["labels"]],
                attributes=[Attribute.from_json(v) for v in data["attributes"]],
                usageTTL=(
                    lambda v: Duration.from_json(v) if v is not None else None
                )(
                    data.get("usageTTL", None)
                ),
                views=[ViewMaterialisationSpec.from_json(v) for v in data["views"]],
                principal=(
                    lambda v: UserId.from_json(v) if v is not None else None
                )(
                    data.get("principal", None)
                ),
                schedule=Schedule.from_json(data["schedule"]),
                cluster=ClusterId.from_json(data["cluster"]),
                clusterPropertySets=(
                    lambda v: [ClusterPropertySetId.from_json(v) for v in v] if v is not None else None
                )(
                    data.get("clusterPropertySets", None)
                ),
                includeMetadata=bool(data["includeMetadata"]),
                versionTarget=(
                    lambda v: VersionTarget.from_json(v) if v is not None else None
                )(
                    data.get("versionTarget", None)
                ),
            )
        except jsonschema.exceptions.ValidationError as ex:
            logging.debug(
                "Invalid JSON data received while parsing BatchViewMaterialisationJobCreationRequest",
                exc_info=ex
            )
            raise
    
    def to_json(self) -> dict:
        """Serialise this instance as JSON.
        
        Returns:
            Data ready to serialise as JSON.
        """
        return {
            "adt_type": self.ADT_TYPE,
            "name": self.name.to_json(),
            "description": str(self.description),
            "labels": [v.to_json() for v in self.labels],
            "attributes": [v.to_json() for v in self.attributes],
            "usageTTL": (lambda v: v.to_json() if v is not None else v)(self.usageTTL),
            "views": [v.to_json() for v in self.views],
            "principal": (lambda v: v.to_json() if v is not None else v)(self.principal),
            "schedule": self.schedule.to_json(),
            "cluster": self.cluster.to_json(),
            "clusterPropertySets": (lambda v: [v.to_json() for v in v] if v is not None else v)(self.clusterPropertySets),
            "includeMetadata": self.includeMetadata,
            "versionTarget": (lambda v: v.to_json() if v is not None else v)(self.versionTarget)
        }


@dataclasses.dataclass(frozen=True)
class StreamingViewMaterialisationJobCreationRequest(ViewMaterialisationJobCreationRequest):
    """A streaming view materialisation job creation request.
    
    Args:
        name (ViewMaterialisationJobName): A data field.
        description (str): A data field.
        labels (typing.List[Label]): A data field.
        attributes (typing.List[Attribute]): A data field.
        usageTTL (typing.Optional[Duration]): A data field.
        views (typing.List[ViewMaterialisationSpec]): A data field.
        principal (typing.Optional[UserId]): A data field.
        cluster (ClusterId): A data field.
        clusterPropertySets (typing.Optional[typing.List[ClusterPropertySetId]]): A data field.
        versionTarget (typing.Optional[VersionTarget]): A data field.
    """
    
    ADT_TYPE: typing.ClassVar[str] = "streaming"
    adt_type: str = dataclasses.field(init=False, repr=False, default=ADT_TYPE)
    
    name: ViewMaterialisationJobName
    description: str
    labels: typing.List[Label]
    attributes: typing.List[Attribute]
    usageTTL: typing.Optional[Duration]
    views: typing.List[ViewMaterialisationSpec]
    principal: typing.Optional[UserId]
    cluster: ClusterId
    clusterPropertySets: typing.Optional[typing.List[ClusterPropertySetId]]
    versionTarget: typing.Optional[VersionTarget]
    
    @classmethod
    def json_schema(cls) -> dict:
        """Return the JSON schema for StreamingViewMaterialisationJobCreationRequest data.
        
        Returns:
            A Python dictionary describing the JSON schema.
        """
        return {
            "type": "object",
            "properties": {
                "adt_type": {
                    "type": "string",
                    "enum": [cls.ADT_TYPE]
                },
                "name": ViewMaterialisationJobName.json_schema(),
                "description": {
                    "type": "string"
                },
                "labels": {
                    "type": "array",
                    "item": Label.json_schema()
                },
                "attributes": {
                    "type": "array",
                    "item": Attribute.json_schema()
                },
                "usageTTL": {
                    "oneOf": [
                        {"type": "null"},
                        Duration.json_schema(),
                    ]
                },
                "views": {
                    "type": "array",
                    "item": ViewMaterialisationSpec.json_schema()
                },
                "principal": {
                    "oneOf": [
                        {"type": "null"},
                        UserId.json_schema(),
                    ]
                },
                "cluster": ClusterId.json_schema(),
                "clusterPropertySets": {
                    "oneOf": [
                        {"type": "null"},
                        {"type": "array", "item": ClusterPropertySetId.json_schema()},
                    ]
                },
                "versionTarget": {
                    "oneOf": [
                        {"type": "null"},
                        VersionTarget.json_schema(),
                    ]
                }
            },
            "required": [
                "adt_type",
                "name",
                "description",
                "labels",
                "attributes",
                "views",
                "cluster",
            ]
        }
    
    @classmethod
    def from_json( cls
                 , data: dict ) -> StreamingViewMaterialisationJobCreationRequest:
        """Validate and parse JSON data into an instance of StreamingViewMaterialisationJobCreationRequest.
        
        Args:
            data (dict): JSON data to validate and parse.
        
        Returns:
            An instance of StreamingViewMaterialisationJobCreationRequest.
        
        Raises:
            ValidationError: When schema validation fails.
            KeyError: When a required field is missing from the JSON.
        """
        try:
            jsonschema.validate(data, cls.json_schema())
            return StreamingViewMaterialisationJobCreationRequest(
                name=ViewMaterialisationJobName.from_json(data["name"]),
                description=str(data["description"]),
                labels=[Label.from_json(v) for v in data["labels"]],
                attributes=[Attribute.from_json(v) for v in data["attributes"]],
                usageTTL=(
                    lambda v: Duration.from_json(v) if v is not None else None
                )(
                    data.get("usageTTL", None)
                ),
                views=[ViewMaterialisationSpec.from_json(v) for v in data["views"]],
                principal=(
                    lambda v: UserId.from_json(v) if v is not None else None
                )(
                    data.get("principal", None)
                ),
                cluster=ClusterId.from_json(data["cluster"]),
                clusterPropertySets=(
                    lambda v: [ClusterPropertySetId.from_json(v) for v in v] if v is not None else None
                )(
                    data.get("clusterPropertySets", None)
                ),
                versionTarget=(
                    lambda v: VersionTarget.from_json(v) if v is not None else None
                )(
                    data.get("versionTarget", None)
                ),
            )
        except jsonschema.exceptions.ValidationError as ex:
            logging.debug(
                "Invalid JSON data received while parsing StreamingViewMaterialisationJobCreationRequest",
                exc_info=ex
            )
            raise
    
    def to_json(self) -> dict:
        """Serialise this instance as JSON.
        
        Returns:
            Data ready to serialise as JSON.
        """
        return {
            "adt_type": self.ADT_TYPE,
            "name": self.name.to_json(),
            "description": str(self.description),
            "labels": [v.to_json() for v in self.labels],
            "attributes": [v.to_json() for v in self.attributes],
            "usageTTL": (lambda v: v.to_json() if v is not None else v)(self.usageTTL),
            "views": [v.to_json() for v in self.views],
            "principal": (lambda v: v.to_json() if v is not None else v)(self.principal),
            "cluster": self.cluster.to_json(),
            "clusterPropertySets": (lambda v: [v.to_json() for v in v] if v is not None else v)(self.clusterPropertySets),
            "versionTarget": (lambda v: v.to_json() if v is not None else v)(self.versionTarget)
        }


@dataclasses.dataclass(frozen=True)
class ViewMaterialisationJob(abc.ABC):
    """Definition of a view materialisation job.
    
    Args:
        attributes (typing.List[Attribute]): A data field.
        cluster (ClusterId): A data field.
        clusterPropertySets (typing.List[ClusterPropertySetId]): A data field.
        description (str): A data field.
        id (ViewMaterialisationJobId): A data field.
        labels (typing.List[Label]): A data field.
        name (ViewMaterialisationJobName): A data field.
        principal (typing.Optional[UserId]): A data field.
        usageTTL (typing.Optional[Duration]): A data field.
        version (ViewMaterialisationJobVersionId): A data field.
        versionTarget (typing.Optional[VersionTarget]): A data field.
        views (typing.List[ViewMaterialisationSpec]): A data field.
    """
    
    ADT_TYPE: typing.ClassVar[str] = ""
    adt_type: str = dataclasses.field(init=False, repr=False, default=ADT_TYPE)
    
    attributes: typing.List[Attribute]
    cluster: ClusterId
    clusterPropertySets: typing.List[ClusterPropertySetId]
    description: str
    id: ViewMaterialisationJobId
    labels: typing.List[Label]
    name: ViewMaterialisationJobName
    principal: typing.Optional[UserId]
    usageTTL: typing.Optional[Duration]
    version: ViewMaterialisationJobVersionId
    versionTarget: typing.Optional[VersionTarget]
    views: typing.List[ViewMaterialisationSpec]
    
    @classmethod
    def json_schema(cls) -> ViewMaterialisationJob:
        """JSON schema for variant ViewMaterialisationJob.
        
        Returns:
            A Python dictionary describing the JSON schema.
        """
        adt_types = [klass.ADT_TYPE for klass in cls.__subclasses__()]
        return {
            "type": "object",
            "properties": {
                "adt_type": {
                    "type": "string",
                    "enum": adt_types
                }
            },
            "required": [
                "adt_type",
            ]
        }
    
    @classmethod
    def from_json(cls, data: dict) -> ViewMaterialisationJob:
        """Validate and parse JSON data into an instance of ViewMaterialisationJob.
        
        Args:
            data (dict): JSON data to validate and parse.
        
        Returns:
            An instance of ViewMaterialisationJob.
        
        Raises:
            ValidationError: When schema validation fails.
            KeyError: When a required field is missing from the JSON.
        """
        try:
            jsonschema.validate(data, cls.json_schema())
            adt_type = data.get("adt_type", None)
            for klass in cls.__subclasses__():
                if klass.ADT_TYPE == adt_type:
                    return klass.from_json(data)
            raise ValueError("Unknown adt_type: '{ty}'".format(ty=adt_type))
        except jsonschema.exceptions.ValidationError as ex:
            logging.debug("Invalid JSON data received while parsing ViewMaterialisationJob", exc_info=ex)
            raise
    
    @abc.abstractmethod
    def to_json(self) -> dict:
        """Serialise this instance as JSON.
        
        Returns:
            Data ready to serialise as JSON.
        """
        raise NotImplementedError


@dataclasses.dataclass(frozen=True)
class BatchViewMaterialisationJob(ViewMaterialisationJob):
    """A batch view materialisation job.
    
    Args:
        id (ViewMaterialisationJobId): A data field.
        name (ViewMaterialisationJobName): A data field.
        description (str): A data field.
        labels (typing.List[Label]): A data field.
        attributes (typing.List[Attribute]): A data field.
        usageTTL (typing.Optional[Duration]): A data field.
        views (typing.List[ViewMaterialisationSpec]): A data field.
        principal (typing.Optional[UserId]): A data field.
        schedule (Schedule): A data field.
        cluster (ClusterId): A data field.
        clusterPropertySets (typing.List[ClusterPropertySetId]): A data field.
        includeMetadata (bool): A data field.
        versionTarget (typing.Optional[VersionTarget]): A data field.
        version (ViewMaterialisationJobVersionId): A data field.
    """
    
    ADT_TYPE: typing.ClassVar[str] = "batch"
    adt_type: str = dataclasses.field(init=False, repr=False, default=ADT_TYPE)
    
    id: ViewMaterialisationJobId
    name: ViewMaterialisationJobName
    description: str
    labels: typing.List[Label]
    attributes: typing.List[Attribute]
    usageTTL: typing.Optional[Duration]
    views: typing.List[ViewMaterialisationSpec]
    principal: typing.Optional[UserId]
    schedule: Schedule
    cluster: ClusterId
    clusterPropertySets: typing.List[ClusterPropertySetId]
    includeMetadata: bool
    versionTarget: typing.Optional[VersionTarget]
    version: ViewMaterialisationJobVersionId
    
    @classmethod
    def json_schema(cls) -> dict:
        """Return the JSON schema for BatchViewMaterialisationJob data.
        
        Returns:
            A Python dictionary describing the JSON schema.
        """
        return {
            "type": "object",
            "properties": {
                "adt_type": {
                    "type": "string",
                    "enum": [cls.ADT_TYPE]
                },
                "id": ViewMaterialisationJobId.json_schema(),
                "name": ViewMaterialisationJobName.json_schema(),
                "description": {
                    "type": "string"
                },
                "labels": {
                    "type": "array",
                    "item": Label.json_schema()
                },
                "attributes": {
                    "type": "array",
                    "item": Attribute.json_schema()
                },
                "usageTTL": {
                    "oneOf": [
                        {"type": "null"},
                        Duration.json_schema(),
                    ]
                },
                "views": {
                    "type": "array",
                    "item": ViewMaterialisationSpec.json_schema()
                },
                "principal": {
                    "oneOf": [
                        {"type": "null"},
                        UserId.json_schema(),
                    ]
                },
                "schedule": Schedule.json_schema(),
                "cluster": ClusterId.json_schema(),
                "clusterPropertySets": {
                    "type": "array",
                    "item": ClusterPropertySetId.json_schema()
                },
                "includeMetadata": {
                    "type": "boolean"
                },
                "versionTarget": {
                    "oneOf": [
                        {"type": "null"},
                        VersionTarget.json_schema(),
                    ]
                },
                "version": ViewMaterialisationJobVersionId.json_schema()
            },
            "required": [
                "adt_type",
                "id",
                "name",
                "description",
                "labels",
                "attributes",
                "views",
                "schedule",
                "cluster",
                "clusterPropertySets",
                "includeMetadata",
                "version",
            ]
        }
    
    @classmethod
    def from_json(cls, data: dict) -> BatchViewMaterialisationJob:
        """Validate and parse JSON data into an instance of BatchViewMaterialisationJob.
        
        Args:
            data (dict): JSON data to validate and parse.
        
        Returns:
            An instance of BatchViewMaterialisationJob.
        
        Raises:
            ValidationError: When schema validation fails.
            KeyError: When a required field is missing from the JSON.
        """
        try:
            jsonschema.validate(data, cls.json_schema())
            return BatchViewMaterialisationJob(
                id=ViewMaterialisationJobId.from_json(data["id"]),
                name=ViewMaterialisationJobName.from_json(data["name"]),
                description=str(data["description"]),
                labels=[Label.from_json(v) for v in data["labels"]],
                attributes=[Attribute.from_json(v) for v in data["attributes"]],
                usageTTL=(
                    lambda v: Duration.from_json(v) if v is not None else None
                )(
                    data.get("usageTTL", None)
                ),
                views=[ViewMaterialisationSpec.from_json(v) for v in data["views"]],
                principal=(
                    lambda v: UserId.from_json(v) if v is not None else None
                )(
                    data.get("principal", None)
                ),
                schedule=Schedule.from_json(data["schedule"]),
                cluster=ClusterId.from_json(data["cluster"]),
                clusterPropertySets=[ClusterPropertySetId.from_json(v) for v in data["clusterPropertySets"]],
                includeMetadata=bool(data["includeMetadata"]),
                versionTarget=(
                    lambda v: VersionTarget.from_json(v) if v is not None else None
                )(
                    data.get("versionTarget", None)
                ),
                version=ViewMaterialisationJobVersionId.from_json(data["version"]),
            )
        except jsonschema.exceptions.ValidationError as ex:
            logging.debug(
                "Invalid JSON data received while parsing BatchViewMaterialisationJob",
                exc_info=ex
            )
            raise
    
    def to_json(self) -> dict:
        """Serialise this instance as JSON.
        
        Returns:
            Data ready to serialise as JSON.
        """
        return {
            "adt_type": self.ADT_TYPE,
            "id": self.id.to_json(),
            "name": self.name.to_json(),
            "description": str(self.description),
            "labels": [v.to_json() for v in self.labels],
            "attributes": [v.to_json() for v in self.attributes],
            "usageTTL": (lambda v: v.to_json() if v is not None else v)(self.usageTTL),
            "views": [v.to_json() for v in self.views],
            "principal": (lambda v: v.to_json() if v is not None else v)(self.principal),
            "schedule": self.schedule.to_json(),
            "cluster": self.cluster.to_json(),
            "clusterPropertySets": [v.to_json() for v in self.clusterPropertySets],
            "includeMetadata": self.includeMetadata,
            "versionTarget": (lambda v: v.to_json() if v is not None else v)(self.versionTarget),
            "version": self.version.to_json()
        }


@dataclasses.dataclass(frozen=True)
class StreamingViewMaterialisationJob(ViewMaterialisationJob):
    """A streaming view materialisation job.
    
    Args:
        id (ViewMaterialisationJobId): A data field.
        name (ViewMaterialisationJobName): A data field.
        description (str): A data field.
        labels (typing.List[Label]): A data field.
        attributes (typing.List[Attribute]): A data field.
        usageTTL (typing.Optional[Duration]): A data field.
        views (typing.List[ViewMaterialisationSpec]): A data field.
        principal (typing.Optional[UserId]): A data field.
        cluster (ClusterId): A data field.
        clusterPropertySets (typing.List[ClusterPropertySetId]): A data field.
        versionTarget (typing.Optional[VersionTarget]): A data field.
        version (ViewMaterialisationJobVersionId): A data field.
    """
    
    ADT_TYPE: typing.ClassVar[str] = "streaming"
    adt_type: str = dataclasses.field(init=False, repr=False, default=ADT_TYPE)
    
    id: ViewMaterialisationJobId
    name: ViewMaterialisationJobName
    description: str
    labels: typing.List[Label]
    attributes: typing.List[Attribute]
    usageTTL: typing.Optional[Duration]
    views: typing.List[ViewMaterialisationSpec]
    principal: typing.Optional[UserId]
    cluster: ClusterId
    clusterPropertySets: typing.List[ClusterPropertySetId]
    versionTarget: typing.Optional[VersionTarget]
    version: ViewMaterialisationJobVersionId
    
    @classmethod
    def json_schema(cls) -> dict:
        """Return the JSON schema for StreamingViewMaterialisationJob data.
        
        Returns:
            A Python dictionary describing the JSON schema.
        """
        return {
            "type": "object",
            "properties": {
                "adt_type": {
                    "type": "string",
                    "enum": [cls.ADT_TYPE]
                },
                "id": ViewMaterialisationJobId.json_schema(),
                "name": ViewMaterialisationJobName.json_schema(),
                "description": {
                    "type": "string"
                },
                "labels": {
                    "type": "array",
                    "item": Label.json_schema()
                },
                "attributes": {
                    "type": "array",
                    "item": Attribute.json_schema()
                },
                "usageTTL": {
                    "oneOf": [
                        {"type": "null"},
                        Duration.json_schema(),
                    ]
                },
                "views": {
                    "type": "array",
                    "item": ViewMaterialisationSpec.json_schema()
                },
                "principal": {
                    "oneOf": [
                        {"type": "null"},
                        UserId.json_schema(),
                    ]
                },
                "cluster": ClusterId.json_schema(),
                "clusterPropertySets": {
                    "type": "array",
                    "item": ClusterPropertySetId.json_schema()
                },
                "versionTarget": {
                    "oneOf": [
                        {"type": "null"},
                        VersionTarget.json_schema(),
                    ]
                },
                "version": ViewMaterialisationJobVersionId.json_schema()
            },
            "required": [
                "adt_type",
                "id",
                "name",
                "description",
                "labels",
                "attributes",
                "views",
                "cluster",
                "clusterPropertySets",
                "version",
            ]
        }
    
    @classmethod
    def from_json(cls, data: dict) -> StreamingViewMaterialisationJob:
        """Validate and parse JSON data into an instance of StreamingViewMaterialisationJob.
        
        Args:
            data (dict): JSON data to validate and parse.
        
        Returns:
            An instance of StreamingViewMaterialisationJob.
        
        Raises:
            ValidationError: When schema validation fails.
            KeyError: When a required field is missing from the JSON.
        """
        try:
            jsonschema.validate(data, cls.json_schema())
            return StreamingViewMaterialisationJob(
                id=ViewMaterialisationJobId.from_json(data["id"]),
                name=ViewMaterialisationJobName.from_json(data["name"]),
                description=str(data["description"]),
                labels=[Label.from_json(v) for v in data["labels"]],
                attributes=[Attribute.from_json(v) for v in data["attributes"]],
                usageTTL=(
                    lambda v: Duration.from_json(v) if v is not None else None
                )(
                    data.get("usageTTL", None)
                ),
                views=[ViewMaterialisationSpec.from_json(v) for v in data["views"]],
                principal=(
                    lambda v: UserId.from_json(v) if v is not None else None
                )(
                    data.get("principal", None)
                ),
                cluster=ClusterId.from_json(data["cluster"]),
                clusterPropertySets=[ClusterPropertySetId.from_json(v) for v in data["clusterPropertySets"]],
                versionTarget=(
                    lambda v: VersionTarget.from_json(v) if v is not None else None
                )(
                    data.get("versionTarget", None)
                ),
                version=ViewMaterialisationJobVersionId.from_json(data["version"]),
            )
        except jsonschema.exceptions.ValidationError as ex:
            logging.debug(
                "Invalid JSON data received while parsing StreamingViewMaterialisationJob",
                exc_info=ex
            )
            raise
    
    def to_json(self) -> dict:
        """Serialise this instance as JSON.
        
        Returns:
            Data ready to serialise as JSON.
        """
        return {
            "adt_type": self.ADT_TYPE,
            "id": self.id.to_json(),
            "name": self.name.to_json(),
            "description": str(self.description),
            "labels": [v.to_json() for v in self.labels],
            "attributes": [v.to_json() for v in self.attributes],
            "usageTTL": (lambda v: v.to_json() if v is not None else v)(self.usageTTL),
            "views": [v.to_json() for v in self.views],
            "principal": (lambda v: v.to_json() if v is not None else v)(self.principal),
            "cluster": self.cluster.to_json(),
            "clusterPropertySets": [v.to_json() for v in self.clusterPropertySets],
            "versionTarget": (lambda v: v.to_json() if v is not None else v)(self.versionTarget),
            "version": self.version.to_json()
        }
