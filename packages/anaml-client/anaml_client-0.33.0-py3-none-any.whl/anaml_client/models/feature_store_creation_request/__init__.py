"""Generated implementation of feature_store_creation_request."""

# WARNING DO NOT EDIT
# This code was generated from feature-store-creation-request.mcn

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
from ..destination_reference import DestinationReference
from ..entity_population import EntityPopulationId
from ..feature_set import FeatureSetId
from ..feature_store import FeatureStoreName, VersionTarget
from ..label import Label
from ..schedule import Schedule
from ..table import TableId
from ..user import UserId


@dataclasses.dataclass(frozen=True)
class FeatureStoreCreationRequest(abc.ABC):
    """Request to create a new feature store.
    
    Args:
        additionalSparkProperties (typing.Optional[typing.Dict[str, str]]): A data field.
        attributes (typing.List[Attribute]): A data field.
        cluster (ClusterId): A data field.
        clusterPropertySets (typing.Optional[typing.List[ClusterPropertySetId]]): A data field.
        description (str): A data field.
        destinations (typing.List[DestinationReference]): A data field.
        enabled (bool): A data field.
        entityPopulation (typing.Optional[EntityPopulationId]): A data field.
        featureSet (FeatureSetId): A data field.
        labels (typing.List[Label]): A data field.
        name (FeatureStoreName): A data field.
        principal (typing.Optional[UserId]): A data field.
        schedule (Schedule): A data field.
        versionTarget (typing.Optional[VersionTarget]): A data field.
    """
    
    ADT_TYPE: typing.ClassVar[str] = ""
    adt_type: str = dataclasses.field(init=False, repr=False, default=ADT_TYPE)
    
    additionalSparkProperties: typing.Optional[typing.Dict[str, str]]
    attributes: typing.List[Attribute]
    cluster: ClusterId
    clusterPropertySets: typing.Optional[typing.List[ClusterPropertySetId]]
    description: str
    destinations: typing.List[DestinationReference]
    enabled: bool
    entityPopulation: typing.Optional[EntityPopulationId]
    featureSet: FeatureSetId
    labels: typing.List[Label]
    name: FeatureStoreName
    principal: typing.Optional[UserId]
    schedule: Schedule
    versionTarget: typing.Optional[VersionTarget]
    
    @classmethod
    def json_schema(cls) -> FeatureStoreCreationRequest:
        """JSON schema for variant FeatureStoreCreationRequest.
        
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
    def from_json(cls, data: dict) -> FeatureStoreCreationRequest:
        """Validate and parse JSON data into an instance of FeatureStoreCreationRequest.
        
        Args:
            data (dict): JSON data to validate and parse.
        
        Returns:
            An instance of FeatureStoreCreationRequest.
        
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
            logging.debug("Invalid JSON data received while parsing FeatureStoreCreationRequest", exc_info=ex)
            raise
    
    @abc.abstractmethod
    def to_json(self) -> dict:
        """Serialise this instance as JSON.
        
        Returns:
            Data ready to serialise as JSON.
        """
        raise NotImplementedError


@dataclasses.dataclass(frozen=True)
class BatchFeatureStoreCreationRequest(FeatureStoreCreationRequest):
    """A batch feature store.
    
    Args:
        name (FeatureStoreName): A data field.
        description (str): A data field.
        labels (typing.List[Label]): A data field.
        attributes (typing.List[Attribute]): A data field.
        featureSet (FeatureSetId): A data field.
        enabled (bool): A data field.
        destinations (typing.List[DestinationReference]): A data field.
        cluster (ClusterId): A data field.
        clusterPropertySets (typing.Optional[typing.List[ClusterPropertySetId]]): A data field.
        entityPopulation (typing.Optional[EntityPopulationId]): A data field.
        principal (typing.Optional[UserId]): A data field.
        schedule (Schedule): A data field.
        startDate (typing.Optional[datetime.date]): A data field.
        endDate (typing.Optional[datetime.date]): A data field.
        runDateOffset (typing.Optional[int]): A data field.
        includeMetadata (typing.Optional[bool]): A data field.
        additionalSparkProperties (typing.Optional[typing.Dict[str, str]]): A data field.
        versionTarget (typing.Optional[VersionTarget]): A data field.
    """
    
    ADT_TYPE: typing.ClassVar[str] = "batch"
    adt_type: str = dataclasses.field(init=False, repr=False, default=ADT_TYPE)
    
    name: FeatureStoreName
    description: str
    labels: typing.List[Label]
    attributes: typing.List[Attribute]
    featureSet: FeatureSetId
    enabled: bool
    destinations: typing.List[DestinationReference]
    cluster: ClusterId
    clusterPropertySets: typing.Optional[typing.List[ClusterPropertySetId]]
    entityPopulation: typing.Optional[EntityPopulationId]
    principal: typing.Optional[UserId]
    schedule: Schedule
    startDate: typing.Optional[datetime.date]
    endDate: typing.Optional[datetime.date]
    runDateOffset: typing.Optional[int]
    includeMetadata: typing.Optional[bool]
    additionalSparkProperties: typing.Optional[typing.Dict[str, str]]
    versionTarget: typing.Optional[VersionTarget]
    
    @classmethod
    def json_schema(cls) -> dict:
        """Return the JSON schema for BatchFeatureStoreCreationRequest data.
        
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
                "name": FeatureStoreName.json_schema(),
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
                "featureSet": FeatureSetId.json_schema(),
                "enabled": {
                    "type": "boolean"
                },
                "destinations": {
                    "type": "array",
                    "item": DestinationReference.json_schema()
                },
                "cluster": ClusterId.json_schema(),
                "clusterPropertySets": {
                    "oneOf": [
                        {"type": "null"},
                        {"type": "array", "item": ClusterPropertySetId.json_schema()},
                    ]
                },
                "entityPopulation": {
                    "oneOf": [
                        {"type": "null"},
                        EntityPopulationId.json_schema(),
                    ]
                },
                "principal": {
                    "oneOf": [
                        {"type": "null"},
                        UserId.json_schema(),
                    ]
                },
                "schedule": Schedule.json_schema(),
                "startDate": {
                    "oneOf": [
                        {"type": "null"},
                        {"type": "string", "format": "date"},
                    ]
                },
                "endDate": {
                    "oneOf": [
                        {"type": "null"},
                        {"type": "string", "format": "date"},
                    ]
                },
                "runDateOffset": {
                    "oneOf": [
                        {"type": "null"},
                        {"type": "integer"},
                    ]
                },
                "includeMetadata": {
                    "oneOf": [
                        {"type": "null"},
                        {"type": "boolean"},
                    ]
                },
                "additionalSparkProperties": {
                    "oneOf": [
                        {"type": "null"},
                        {"type": "object", "additionalProperties": {"type": "string"}},
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
                "featureSet",
                "enabled",
                "destinations",
                "cluster",
                "schedule",
            ]
        }
    
    @classmethod
    def from_json(cls, data: dict) -> BatchFeatureStoreCreationRequest:
        """Validate and parse JSON data into an instance of BatchFeatureStoreCreationRequest.
        
        Args:
            data (dict): JSON data to validate and parse.
        
        Returns:
            An instance of BatchFeatureStoreCreationRequest.
        
        Raises:
            ValidationError: When schema validation fails.
            KeyError: When a required field is missing from the JSON.
        """
        try:
            jsonschema.validate(data, cls.json_schema())
            return BatchFeatureStoreCreationRequest(
                name=FeatureStoreName.from_json(data["name"]),
                description=str(data["description"]),
                labels=[Label.from_json(v) for v in data["labels"]],
                attributes=[Attribute.from_json(v) for v in data["attributes"]],
                featureSet=FeatureSetId.from_json(data["featureSet"]),
                enabled=bool(data["enabled"]),
                destinations=[DestinationReference.from_json(v) for v in data["destinations"]],
                cluster=ClusterId.from_json(data["cluster"]),
                clusterPropertySets=(
                    lambda v: [ClusterPropertySetId.from_json(v) for v in v] if v is not None else None
                )(
                    data.get("clusterPropertySets", None)
                ),
                entityPopulation=(
                    lambda v: EntityPopulationId.from_json(v) if v is not None else None
                )(
                    data.get("entityPopulation", None)
                ),
                principal=(
                    lambda v: UserId.from_json(v) if v is not None else None
                )(
                    data.get("principal", None)
                ),
                schedule=Schedule.from_json(data["schedule"]),
                startDate=(
                    lambda v: datetime.date.fromisoformat(v) if v is not None else None
                )(
                    data.get("startDate", None)
                ),
                endDate=(
                    lambda v: datetime.date.fromisoformat(v) if v is not None else None
                )(
                    data.get("endDate", None)
                ),
                runDateOffset=(
                    lambda v: int(v) if v is not None else None
                )(
                    data.get("runDateOffset", None)
                ),
                includeMetadata=(
                    lambda v: bool(v) if v is not None else None
                )(
                    data.get("includeMetadata", None)
                ),
                additionalSparkProperties=(
                    lambda v: {str(k): str(v) for k, v in v.items()} if v is not None else None
                )(
                    data.get("additionalSparkProperties", None)
                ),
                versionTarget=(
                    lambda v: VersionTarget.from_json(v) if v is not None else None
                )(
                    data.get("versionTarget", None)
                ),
            )
        except jsonschema.exceptions.ValidationError as ex:
            logging.debug(
                "Invalid JSON data received while parsing BatchFeatureStoreCreationRequest",
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
            "featureSet": self.featureSet.to_json(),
            "enabled": self.enabled,
            "destinations": [v.to_json() for v in self.destinations],
            "cluster": self.cluster.to_json(),
            "clusterPropertySets": (lambda v: [v.to_json() for v in v] if v is not None else v)(self.clusterPropertySets),
            "entityPopulation": (lambda v: v.to_json() if v is not None else v)(self.entityPopulation),
            "principal": (lambda v: v.to_json() if v is not None else v)(self.principal),
            "schedule": self.schedule.to_json(),
            "startDate": (lambda v: v.isoformat() if v is not None else v)(self.startDate),
            "endDate": (lambda v: v.isoformat() if v is not None else v)(self.endDate),
            "runDateOffset": (lambda v: int(v) if v is not None else v)(self.runDateOffset),
            "includeMetadata": (lambda v: v if v is not None else v)(self.includeMetadata),
            "additionalSparkProperties": (lambda v: {str(k): str(v) for k, v in v.items()} if v is not None else v)(self.additionalSparkProperties),
            "versionTarget": (lambda v: v.to_json() if v is not None else v)(self.versionTarget)
        }


@dataclasses.dataclass(frozen=True)
class StreamingFeatureStoreCreationRequest(FeatureStoreCreationRequest):
    """A streaming feature store.
    
    Args:
        name (FeatureStoreName): A data field.
        description (str): A data field.
        labels (typing.List[Label]): A data field.
        attributes (typing.List[Attribute]): A data field.
        featureSet (FeatureSetId): A data field.
        enabled (bool): A data field.
        destinations (typing.List[DestinationReference]): A data field.
        cluster (ClusterId): A data field.
        clusterPropertySets (typing.Optional[typing.List[ClusterPropertySetId]]): A data field.
        entityPopulation (typing.Optional[EntityPopulationId]): A data field.
        principal (typing.Optional[UserId]): A data field.
        schedule (Schedule): A data field.
        table (TableId): A data field.
        additionalSparkProperties (typing.Optional[typing.Dict[str, str]]): A data field.
        versionTarget (typing.Optional[VersionTarget]): A data field.
    """
    
    ADT_TYPE: typing.ClassVar[str] = "streaming"
    adt_type: str = dataclasses.field(init=False, repr=False, default=ADT_TYPE)
    
    name: FeatureStoreName
    description: str
    labels: typing.List[Label]
    attributes: typing.List[Attribute]
    featureSet: FeatureSetId
    enabled: bool
    destinations: typing.List[DestinationReference]
    cluster: ClusterId
    clusterPropertySets: typing.Optional[typing.List[ClusterPropertySetId]]
    entityPopulation: typing.Optional[EntityPopulationId]
    principal: typing.Optional[UserId]
    schedule: Schedule
    table: TableId
    additionalSparkProperties: typing.Optional[typing.Dict[str, str]]
    versionTarget: typing.Optional[VersionTarget]
    
    @classmethod
    def json_schema(cls) -> dict:
        """Return the JSON schema for StreamingFeatureStoreCreationRequest data.
        
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
                "name": FeatureStoreName.json_schema(),
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
                "featureSet": FeatureSetId.json_schema(),
                "enabled": {
                    "type": "boolean"
                },
                "destinations": {
                    "type": "array",
                    "item": DestinationReference.json_schema()
                },
                "cluster": ClusterId.json_schema(),
                "clusterPropertySets": {
                    "oneOf": [
                        {"type": "null"},
                        {"type": "array", "item": ClusterPropertySetId.json_schema()},
                    ]
                },
                "entityPopulation": {
                    "oneOf": [
                        {"type": "null"},
                        EntityPopulationId.json_schema(),
                    ]
                },
                "principal": {
                    "oneOf": [
                        {"type": "null"},
                        UserId.json_schema(),
                    ]
                },
                "schedule": Schedule.json_schema(),
                "table": TableId.json_schema(),
                "additionalSparkProperties": {
                    "oneOf": [
                        {"type": "null"},
                        {"type": "object", "additionalProperties": {"type": "string"}},
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
                "featureSet",
                "enabled",
                "destinations",
                "cluster",
                "schedule",
                "table",
            ]
        }
    
    @classmethod
    def from_json(cls, data: dict) -> StreamingFeatureStoreCreationRequest:
        """Validate and parse JSON data into an instance of StreamingFeatureStoreCreationRequest.
        
        Args:
            data (dict): JSON data to validate and parse.
        
        Returns:
            An instance of StreamingFeatureStoreCreationRequest.
        
        Raises:
            ValidationError: When schema validation fails.
            KeyError: When a required field is missing from the JSON.
        """
        try:
            jsonschema.validate(data, cls.json_schema())
            return StreamingFeatureStoreCreationRequest(
                name=FeatureStoreName.from_json(data["name"]),
                description=str(data["description"]),
                labels=[Label.from_json(v) for v in data["labels"]],
                attributes=[Attribute.from_json(v) for v in data["attributes"]],
                featureSet=FeatureSetId.from_json(data["featureSet"]),
                enabled=bool(data["enabled"]),
                destinations=[DestinationReference.from_json(v) for v in data["destinations"]],
                cluster=ClusterId.from_json(data["cluster"]),
                clusterPropertySets=(
                    lambda v: [ClusterPropertySetId.from_json(v) for v in v] if v is not None else None
                )(
                    data.get("clusterPropertySets", None)
                ),
                entityPopulation=(
                    lambda v: EntityPopulationId.from_json(v) if v is not None else None
                )(
                    data.get("entityPopulation", None)
                ),
                principal=(
                    lambda v: UserId.from_json(v) if v is not None else None
                )(
                    data.get("principal", None)
                ),
                schedule=Schedule.from_json(data["schedule"]),
                table=TableId.from_json(data["table"]),
                additionalSparkProperties=(
                    lambda v: {str(k): str(v) for k, v in v.items()} if v is not None else None
                )(
                    data.get("additionalSparkProperties", None)
                ),
                versionTarget=(
                    lambda v: VersionTarget.from_json(v) if v is not None else None
                )(
                    data.get("versionTarget", None)
                ),
            )
        except jsonschema.exceptions.ValidationError as ex:
            logging.debug(
                "Invalid JSON data received while parsing StreamingFeatureStoreCreationRequest",
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
            "featureSet": self.featureSet.to_json(),
            "enabled": self.enabled,
            "destinations": [v.to_json() for v in self.destinations],
            "cluster": self.cluster.to_json(),
            "clusterPropertySets": (lambda v: [v.to_json() for v in v] if v is not None else v)(self.clusterPropertySets),
            "entityPopulation": (lambda v: v.to_json() if v is not None else v)(self.entityPopulation),
            "principal": (lambda v: v.to_json() if v is not None else v)(self.principal),
            "schedule": self.schedule.to_json(),
            "table": self.table.to_json(),
            "additionalSparkProperties": (lambda v: {str(k): str(v) for k, v in v.items()} if v is not None else v)(self.additionalSparkProperties),
            "versionTarget": (lambda v: v.to_json() if v is not None else v)(self.versionTarget)
        }
