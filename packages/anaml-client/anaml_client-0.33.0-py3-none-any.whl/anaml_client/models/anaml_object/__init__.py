"""Generated implementation of anaml_object."""

# WARNING DO NOT EDIT
# This code was generated from anaml-object.mcn

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

from ..entity import EntityId
from ..entity_mapping import EntityMappingId
from ..entity_population import EntityPopulationId
from ..event_store import EventStoreId
from ..feature_id import FeatureId
from ..feature_set import FeatureSetId
from ..feature_store import FeatureStoreId
from ..feature_template import TemplateId
from ..table import TableId
from ..table_caching import TableCachingJobId
from ..table_monitoring import TableMonitoringJobId
from ..view_materialisation import ViewMaterialisationJobId


@dataclasses.dataclass(frozen=True)
class AnamlObject(abc.ABC):
    """References to Anaml 'content' object."""
    
    ADT_TYPE: typing.ClassVar[str] = ""
    adt_type: str = dataclasses.field(init=False, repr=False, default=ADT_TYPE)
    
    @classmethod
    def json_schema(cls) -> AnamlObject:
        """JSON schema for variant AnamlObject.
        
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
    def from_json(cls, data: dict) -> AnamlObject:
        """Validate and parse JSON data into an instance of AnamlObject.
        
        Args:
            data (dict): JSON data to validate and parse.
        
        Returns:
            An instance of AnamlObject.
        
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
            logging.debug("Invalid JSON data received while parsing AnamlObject", exc_info=ex)
            raise
    
    @abc.abstractmethod
    def to_json(self) -> dict:
        """Serialise this instance as JSON.
        
        Returns:
            Data ready to serialise as JSON.
        """
        raise NotImplementedError


@dataclasses.dataclass(frozen=True)
class AnamlEntity(AnamlObject):
    """A reference to an Entity object in Anaml.
    
    Args:
        id (EntityId): A data field.
    """
    
    ADT_TYPE: typing.ClassVar[str] = "anamlentity"
    adt_type: str = dataclasses.field(init=False, repr=False, default=ADT_TYPE)
    
    id: EntityId
    
    @classmethod
    def json_schema(cls) -> dict:
        """Return the JSON schema for AnamlEntity data.
        
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
                "id": EntityId.json_schema()
            },
            "required": [
                "adt_type",
                "id",
            ]
        }
    
    @classmethod
    def from_json(cls, data: dict) -> AnamlEntity:
        """Validate and parse JSON data into an instance of AnamlEntity.
        
        Args:
            data (dict): JSON data to validate and parse.
        
        Returns:
            An instance of AnamlEntity.
        
        Raises:
            ValidationError: When schema validation fails.
            KeyError: When a required field is missing from the JSON.
        """
        try:
            jsonschema.validate(data, cls.json_schema())
            return AnamlEntity(
                id=EntityId.from_json(data["id"]),
            )
        except jsonschema.exceptions.ValidationError as ex:
            logging.debug(
                "Invalid JSON data received while parsing AnamlEntity",
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
            "id": self.id.to_json()
        }


@dataclasses.dataclass(frozen=True)
class AnamlEntityMapping(AnamlObject):
    """A reference to an Entity Mapping object in Anaml.
    
    Args:
        id (EntityMappingId): A data field.
    """
    
    ADT_TYPE: typing.ClassVar[str] = "anamlentitymapping"
    adt_type: str = dataclasses.field(init=False, repr=False, default=ADT_TYPE)
    
    id: EntityMappingId
    
    @classmethod
    def json_schema(cls) -> dict:
        """Return the JSON schema for AnamlEntityMapping data.
        
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
                "id": EntityMappingId.json_schema()
            },
            "required": [
                "adt_type",
                "id",
            ]
        }
    
    @classmethod
    def from_json(cls, data: dict) -> AnamlEntityMapping:
        """Validate and parse JSON data into an instance of AnamlEntityMapping.
        
        Args:
            data (dict): JSON data to validate and parse.
        
        Returns:
            An instance of AnamlEntityMapping.
        
        Raises:
            ValidationError: When schema validation fails.
            KeyError: When a required field is missing from the JSON.
        """
        try:
            jsonschema.validate(data, cls.json_schema())
            return AnamlEntityMapping(
                id=EntityMappingId.from_json(data["id"]),
            )
        except jsonschema.exceptions.ValidationError as ex:
            logging.debug(
                "Invalid JSON data received while parsing AnamlEntityMapping",
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
            "id": self.id.to_json()
        }


@dataclasses.dataclass(frozen=True)
class AnamlEntityPopulation(AnamlObject):
    """A reference to an Entity Population object in Anaml.
    
    Args:
        id (EntityPopulationId): A data field.
    """
    
    ADT_TYPE: typing.ClassVar[str] = "anamlentitypopulation"
    adt_type: str = dataclasses.field(init=False, repr=False, default=ADT_TYPE)
    
    id: EntityPopulationId
    
    @classmethod
    def json_schema(cls) -> dict:
        """Return the JSON schema for AnamlEntityPopulation data.
        
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
                "id": EntityPopulationId.json_schema()
            },
            "required": [
                "adt_type",
                "id",
            ]
        }
    
    @classmethod
    def from_json(cls, data: dict) -> AnamlEntityPopulation:
        """Validate and parse JSON data into an instance of AnamlEntityPopulation.
        
        Args:
            data (dict): JSON data to validate and parse.
        
        Returns:
            An instance of AnamlEntityPopulation.
        
        Raises:
            ValidationError: When schema validation fails.
            KeyError: When a required field is missing from the JSON.
        """
        try:
            jsonschema.validate(data, cls.json_schema())
            return AnamlEntityPopulation(
                id=EntityPopulationId.from_json(data["id"]),
            )
        except jsonschema.exceptions.ValidationError as ex:
            logging.debug(
                "Invalid JSON data received while parsing AnamlEntityPopulation",
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
            "id": self.id.to_json()
        }


@dataclasses.dataclass(frozen=True)
class AnamlEventStore(AnamlObject):
    """A reference to an Event Store object in Anaml.
    
    Args:
        id (EventStoreId): A data field.
    """
    
    ADT_TYPE: typing.ClassVar[str] = "anamleventstore"
    adt_type: str = dataclasses.field(init=False, repr=False, default=ADT_TYPE)
    
    id: EventStoreId
    
    @classmethod
    def json_schema(cls) -> dict:
        """Return the JSON schema for AnamlEventStore data.
        
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
                "id": EventStoreId.json_schema()
            },
            "required": [
                "adt_type",
                "id",
            ]
        }
    
    @classmethod
    def from_json(cls, data: dict) -> AnamlEventStore:
        """Validate and parse JSON data into an instance of AnamlEventStore.
        
        Args:
            data (dict): JSON data to validate and parse.
        
        Returns:
            An instance of AnamlEventStore.
        
        Raises:
            ValidationError: When schema validation fails.
            KeyError: When a required field is missing from the JSON.
        """
        try:
            jsonschema.validate(data, cls.json_schema())
            return AnamlEventStore(
                id=EventStoreId.from_json(data["id"]),
            )
        except jsonschema.exceptions.ValidationError as ex:
            logging.debug(
                "Invalid JSON data received while parsing AnamlEventStore",
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
            "id": self.id.to_json()
        }


@dataclasses.dataclass(frozen=True)
class AnamlEventStoreBatch(AnamlObject):
    """A reference to an Event Store Batch object in Anaml.
    
    Args:
        id (EventStoreId): A data field.
    """
    
    ADT_TYPE: typing.ClassVar[str] = "anamleventstorebatch"
    adt_type: str = dataclasses.field(init=False, repr=False, default=ADT_TYPE)
    
    id: EventStoreId
    
    @classmethod
    def json_schema(cls) -> dict:
        """Return the JSON schema for AnamlEventStoreBatch data.
        
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
                "id": EventStoreId.json_schema()
            },
            "required": [
                "adt_type",
                "id",
            ]
        }
    
    @classmethod
    def from_json(cls, data: dict) -> AnamlEventStoreBatch:
        """Validate and parse JSON data into an instance of AnamlEventStoreBatch.
        
        Args:
            data (dict): JSON data to validate and parse.
        
        Returns:
            An instance of AnamlEventStoreBatch.
        
        Raises:
            ValidationError: When schema validation fails.
            KeyError: When a required field is missing from the JSON.
        """
        try:
            jsonschema.validate(data, cls.json_schema())
            return AnamlEventStoreBatch(
                id=EventStoreId.from_json(data["id"]),
            )
        except jsonschema.exceptions.ValidationError as ex:
            logging.debug(
                "Invalid JSON data received while parsing AnamlEventStoreBatch",
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
            "id": self.id.to_json()
        }


@dataclasses.dataclass(frozen=True)
class AnamlFeature(AnamlObject):
    """A reference to an Feature object in Anaml.
    
    Args:
        id (FeatureId): A data field.
    """
    
    ADT_TYPE: typing.ClassVar[str] = "anamlfeature"
    adt_type: str = dataclasses.field(init=False, repr=False, default=ADT_TYPE)
    
    id: FeatureId
    
    @classmethod
    def json_schema(cls) -> dict:
        """Return the JSON schema for AnamlFeature data.
        
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
                "id": FeatureId.json_schema()
            },
            "required": [
                "adt_type",
                "id",
            ]
        }
    
    @classmethod
    def from_json(cls, data: dict) -> AnamlFeature:
        """Validate and parse JSON data into an instance of AnamlFeature.
        
        Args:
            data (dict): JSON data to validate and parse.
        
        Returns:
            An instance of AnamlFeature.
        
        Raises:
            ValidationError: When schema validation fails.
            KeyError: When a required field is missing from the JSON.
        """
        try:
            jsonschema.validate(data, cls.json_schema())
            return AnamlFeature(
                id=FeatureId.from_json(data["id"]),
            )
        except jsonschema.exceptions.ValidationError as ex:
            logging.debug(
                "Invalid JSON data received while parsing AnamlFeature",
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
            "id": self.id.to_json()
        }


@dataclasses.dataclass(frozen=True)
class AnamlFeatureTemplate(AnamlObject):
    """A reference to an Feature Template object in Anaml.
    
    Args:
        id (TemplateId): A data field.
    """
    
    ADT_TYPE: typing.ClassVar[str] = "anamlfeaturetemplate"
    adt_type: str = dataclasses.field(init=False, repr=False, default=ADT_TYPE)
    
    id: TemplateId
    
    @classmethod
    def json_schema(cls) -> dict:
        """Return the JSON schema for AnamlFeatureTemplate data.
        
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
                "id": TemplateId.json_schema()
            },
            "required": [
                "adt_type",
                "id",
            ]
        }
    
    @classmethod
    def from_json(cls, data: dict) -> AnamlFeatureTemplate:
        """Validate and parse JSON data into an instance of AnamlFeatureTemplate.
        
        Args:
            data (dict): JSON data to validate and parse.
        
        Returns:
            An instance of AnamlFeatureTemplate.
        
        Raises:
            ValidationError: When schema validation fails.
            KeyError: When a required field is missing from the JSON.
        """
        try:
            jsonschema.validate(data, cls.json_schema())
            return AnamlFeatureTemplate(
                id=TemplateId.from_json(data["id"]),
            )
        except jsonschema.exceptions.ValidationError as ex:
            logging.debug(
                "Invalid JSON data received while parsing AnamlFeatureTemplate",
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
            "id": self.id.to_json()
        }


@dataclasses.dataclass(frozen=True)
class AnamlFeatureSet(AnamlObject):
    """A reference to an Feature Set object in Anaml.
    
    Args:
        id (FeatureSetId): A data field.
    """
    
    ADT_TYPE: typing.ClassVar[str] = "anamlfeatureset"
    adt_type: str = dataclasses.field(init=False, repr=False, default=ADT_TYPE)
    
    id: FeatureSetId
    
    @classmethod
    def json_schema(cls) -> dict:
        """Return the JSON schema for AnamlFeatureSet data.
        
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
                "id": FeatureSetId.json_schema()
            },
            "required": [
                "adt_type",
                "id",
            ]
        }
    
    @classmethod
    def from_json(cls, data: dict) -> AnamlFeatureSet:
        """Validate and parse JSON data into an instance of AnamlFeatureSet.
        
        Args:
            data (dict): JSON data to validate and parse.
        
        Returns:
            An instance of AnamlFeatureSet.
        
        Raises:
            ValidationError: When schema validation fails.
            KeyError: When a required field is missing from the JSON.
        """
        try:
            jsonschema.validate(data, cls.json_schema())
            return AnamlFeatureSet(
                id=FeatureSetId.from_json(data["id"]),
            )
        except jsonschema.exceptions.ValidationError as ex:
            logging.debug(
                "Invalid JSON data received while parsing AnamlFeatureSet",
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
            "id": self.id.to_json()
        }


@dataclasses.dataclass(frozen=True)
class AnamlFeatureStore(AnamlObject):
    """A reference to an Feature Store object in Anaml.
    
    Args:
        id (FeatureStoreId): A data field.
    """
    
    ADT_TYPE: typing.ClassVar[str] = "anamlfeaturestore"
    adt_type: str = dataclasses.field(init=False, repr=False, default=ADT_TYPE)
    
    id: FeatureStoreId
    
    @classmethod
    def json_schema(cls) -> dict:
        """Return the JSON schema for AnamlFeatureStore data.
        
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
                "id": FeatureStoreId.json_schema()
            },
            "required": [
                "adt_type",
                "id",
            ]
        }
    
    @classmethod
    def from_json(cls, data: dict) -> AnamlFeatureStore:
        """Validate and parse JSON data into an instance of AnamlFeatureStore.
        
        Args:
            data (dict): JSON data to validate and parse.
        
        Returns:
            An instance of AnamlFeatureStore.
        
        Raises:
            ValidationError: When schema validation fails.
            KeyError: When a required field is missing from the JSON.
        """
        try:
            jsonschema.validate(data, cls.json_schema())
            return AnamlFeatureStore(
                id=FeatureStoreId.from_json(data["id"]),
            )
        except jsonschema.exceptions.ValidationError as ex:
            logging.debug(
                "Invalid JSON data received while parsing AnamlFeatureStore",
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
            "id": self.id.to_json()
        }


@dataclasses.dataclass(frozen=True)
class AnamlTable(AnamlObject):
    """A reference to an Table object in Anaml.
    
    Args:
        id (TableId): A data field.
    """
    
    ADT_TYPE: typing.ClassVar[str] = "anamltable"
    adt_type: str = dataclasses.field(init=False, repr=False, default=ADT_TYPE)
    
    id: TableId
    
    @classmethod
    def json_schema(cls) -> dict:
        """Return the JSON schema for AnamlTable data.
        
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
                "id": TableId.json_schema()
            },
            "required": [
                "adt_type",
                "id",
            ]
        }
    
    @classmethod
    def from_json(cls, data: dict) -> AnamlTable:
        """Validate and parse JSON data into an instance of AnamlTable.
        
        Args:
            data (dict): JSON data to validate and parse.
        
        Returns:
            An instance of AnamlTable.
        
        Raises:
            ValidationError: When schema validation fails.
            KeyError: When a required field is missing from the JSON.
        """
        try:
            jsonschema.validate(data, cls.json_schema())
            return AnamlTable(
                id=TableId.from_json(data["id"]),
            )
        except jsonschema.exceptions.ValidationError as ex:
            logging.debug(
                "Invalid JSON data received while parsing AnamlTable",
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
            "id": self.id.to_json()
        }


@dataclasses.dataclass(frozen=True)
class AnamlTableCaching(AnamlObject):
    """A reference to an Table Caching object in Anaml.
    
    Args:
        id (TableCachingJobId): A data field.
    """
    
    ADT_TYPE: typing.ClassVar[str] = "anamltablecaching"
    adt_type: str = dataclasses.field(init=False, repr=False, default=ADT_TYPE)
    
    id: TableCachingJobId
    
    @classmethod
    def json_schema(cls) -> dict:
        """Return the JSON schema for AnamlTableCaching data.
        
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
                "id": TableCachingJobId.json_schema()
            },
            "required": [
                "adt_type",
                "id",
            ]
        }
    
    @classmethod
    def from_json(cls, data: dict) -> AnamlTableCaching:
        """Validate and parse JSON data into an instance of AnamlTableCaching.
        
        Args:
            data (dict): JSON data to validate and parse.
        
        Returns:
            An instance of AnamlTableCaching.
        
        Raises:
            ValidationError: When schema validation fails.
            KeyError: When a required field is missing from the JSON.
        """
        try:
            jsonschema.validate(data, cls.json_schema())
            return AnamlTableCaching(
                id=TableCachingJobId.from_json(data["id"]),
            )
        except jsonschema.exceptions.ValidationError as ex:
            logging.debug(
                "Invalid JSON data received while parsing AnamlTableCaching",
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
            "id": self.id.to_json()
        }


@dataclasses.dataclass(frozen=True)
class AnamlTableMonitoring(AnamlObject):
    """A reference to an Table Monitoring object in Anaml.
    
    Args:
        id (TableMonitoringJobId): A data field.
    """
    
    ADT_TYPE: typing.ClassVar[str] = "anamltablemonitoring"
    adt_type: str = dataclasses.field(init=False, repr=False, default=ADT_TYPE)
    
    id: TableMonitoringJobId
    
    @classmethod
    def json_schema(cls) -> dict:
        """Return the JSON schema for AnamlTableMonitoring data.
        
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
                "id": TableMonitoringJobId.json_schema()
            },
            "required": [
                "adt_type",
                "id",
            ]
        }
    
    @classmethod
    def from_json(cls, data: dict) -> AnamlTableMonitoring:
        """Validate and parse JSON data into an instance of AnamlTableMonitoring.
        
        Args:
            data (dict): JSON data to validate and parse.
        
        Returns:
            An instance of AnamlTableMonitoring.
        
        Raises:
            ValidationError: When schema validation fails.
            KeyError: When a required field is missing from the JSON.
        """
        try:
            jsonschema.validate(data, cls.json_schema())
            return AnamlTableMonitoring(
                id=TableMonitoringJobId.from_json(data["id"]),
            )
        except jsonschema.exceptions.ValidationError as ex:
            logging.debug(
                "Invalid JSON data received while parsing AnamlTableMonitoring",
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
            "id": self.id.to_json()
        }


@dataclasses.dataclass(frozen=True)
class AnamlViewMaterialisation(AnamlObject):
    """A reference to an View Materialisation object in Anaml.
    
    Args:
        id (ViewMaterialisationJobId): A data field.
    """
    
    ADT_TYPE: typing.ClassVar[str] = "anamlviewmaterialisation"
    adt_type: str = dataclasses.field(init=False, repr=False, default=ADT_TYPE)
    
    id: ViewMaterialisationJobId
    
    @classmethod
    def json_schema(cls) -> dict:
        """Return the JSON schema for AnamlViewMaterialisation data.
        
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
                "id": ViewMaterialisationJobId.json_schema()
            },
            "required": [
                "adt_type",
                "id",
            ]
        }
    
    @classmethod
    def from_json(cls, data: dict) -> AnamlViewMaterialisation:
        """Validate and parse JSON data into an instance of AnamlViewMaterialisation.
        
        Args:
            data (dict): JSON data to validate and parse.
        
        Returns:
            An instance of AnamlViewMaterialisation.
        
        Raises:
            ValidationError: When schema validation fails.
            KeyError: When a required field is missing from the JSON.
        """
        try:
            jsonschema.validate(data, cls.json_schema())
            return AnamlViewMaterialisation(
                id=ViewMaterialisationJobId.from_json(data["id"]),
            )
        except jsonschema.exceptions.ValidationError as ex:
            logging.debug(
                "Invalid JSON data received while parsing AnamlViewMaterialisation",
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
            "id": self.id.to_json()
        }
