"""Generated implementation of destination_creation_request."""

# WARNING DO NOT EDIT
# This code was generated from destination-creation-request.mcn

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

from ..access_control import AccessRule
from ..attribute import Attribute, SensitiveAttribute
from ..credentials_provider_config import CredentialsProviderConfig
from ..destination import (
    DestinationId, DestinationName, DestinationVersionId, ExactTargetSFTPConfig,
    GCSStagingArea
)
from ..file_format import FileFormat
from ..label import Label


@dataclasses.dataclass(frozen=True)
class DestinationCreationRequest(abc.ABC):
    """Requests to create a new output data store.
    
    Args:
        accessRules (typing.List[AccessRule]): A data field.
        attributes (typing.List[Attribute]): A data field.
        description (str): A data field.
        labels (typing.List[Label]): A data field.
        name (DestinationName): A data field.
    """
    
    ADT_TYPE: typing.ClassVar[str] = ""
    adt_type: str = dataclasses.field(init=False, repr=False, default=ADT_TYPE)
    
    accessRules: typing.List[AccessRule]
    attributes: typing.List[Attribute]
    description: str
    labels: typing.List[Label]
    name: DestinationName
    
    @classmethod
    def json_schema(cls) -> DestinationCreationRequest:
        """JSON schema for variant DestinationCreationRequest.
        
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
    def from_json(cls, data: dict) -> DestinationCreationRequest:
        """Validate and parse JSON data into an instance of DestinationCreationRequest.
        
        Args:
            data (dict): JSON data to validate and parse.
        
        Returns:
            An instance of DestinationCreationRequest.
        
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
            logging.debug("Invalid JSON data received while parsing DestinationCreationRequest", exc_info=ex)
            raise
    
    @abc.abstractmethod
    def to_json(self) -> dict:
        """Serialise this instance as JSON.
        
        Returns:
            Data ready to serialise as JSON.
        """
        raise NotImplementedError


@dataclasses.dataclass(frozen=True)
class S3DestinationCreationRequest(DestinationCreationRequest):
    """Create a new output data store on AWS S3.
    
    Args:
        name (DestinationName): A data field.
        description (str): A data field.
        labels (typing.List[Label]): A data field.
        attributes (typing.List[Attribute]): A data field.
        accessRules (typing.List[AccessRule]): A data field.
        bucket (str): A data field.
        path (str): A data field.
        fileFormat (FileFormat): A data field.
    """
    
    ADT_TYPE: typing.ClassVar[str] = "s3"
    adt_type: str = dataclasses.field(init=False, repr=False, default=ADT_TYPE)
    
    name: DestinationName
    description: str
    labels: typing.List[Label]
    attributes: typing.List[Attribute]
    accessRules: typing.List[AccessRule]
    bucket: str
    path: str
    fileFormat: FileFormat
    
    @classmethod
    def json_schema(cls) -> dict:
        """Return the JSON schema for S3DestinationCreationRequest data.
        
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
                "name": DestinationName.json_schema(),
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
                "accessRules": {
                    "type": "array",
                    "item": AccessRule.json_schema()
                },
                "bucket": {
                    "type": "string"
                },
                "path": {
                    "type": "string"
                },
                "fileFormat": FileFormat.json_schema()
            },
            "required": [
                "adt_type",
                "name",
                "description",
                "labels",
                "attributes",
                "accessRules",
                "bucket",
                "path",
                "fileFormat",
            ]
        }
    
    @classmethod
    def from_json(cls, data: dict) -> S3DestinationCreationRequest:
        """Validate and parse JSON data into an instance of S3DestinationCreationRequest.
        
        Args:
            data (dict): JSON data to validate and parse.
        
        Returns:
            An instance of S3DestinationCreationRequest.
        
        Raises:
            ValidationError: When schema validation fails.
            KeyError: When a required field is missing from the JSON.
        """
        try:
            jsonschema.validate(data, cls.json_schema())
            return S3DestinationCreationRequest(
                name=DestinationName.from_json(data["name"]),
                description=str(data["description"]),
                labels=[Label.from_json(v) for v in data["labels"]],
                attributes=[Attribute.from_json(v) for v in data["attributes"]],
                accessRules=[AccessRule.from_json(v) for v in data["accessRules"]],
                bucket=str(data["bucket"]),
                path=str(data["path"]),
                fileFormat=FileFormat.from_json(data["fileFormat"]),
            )
        except jsonschema.exceptions.ValidationError as ex:
            logging.debug(
                "Invalid JSON data received while parsing S3DestinationCreationRequest",
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
            "accessRules": [v.to_json() for v in self.accessRules],
            "bucket": str(self.bucket),
            "path": str(self.path),
            "fileFormat": self.fileFormat.to_json()
        }


@dataclasses.dataclass(frozen=True)
class S3ADestinationCreationRequest(DestinationCreationRequest):
    """Create a new output data store using S3-compatible object storage.
    
    Args:
        name (DestinationName): A data field.
        description (str): A data field.
        labels (typing.List[Label]): A data field.
        attributes (typing.List[Attribute]): A data field.
        accessRules (typing.List[AccessRule]): A data field.
        bucket (str): A data field.
        path (str): A data field.
        fileFormat (FileFormat): A data field.
        endpoint (str): A data field.
        accessKey (str): A data field.
        secretKey (str): A data field.
    """
    
    ADT_TYPE: typing.ClassVar[str] = "s3a"
    adt_type: str = dataclasses.field(init=False, repr=False, default=ADT_TYPE)
    
    name: DestinationName
    description: str
    labels: typing.List[Label]
    attributes: typing.List[Attribute]
    accessRules: typing.List[AccessRule]
    bucket: str
    path: str
    fileFormat: FileFormat
    endpoint: str
    accessKey: str
    secretKey: str
    
    @classmethod
    def json_schema(cls) -> dict:
        """Return the JSON schema for S3ADestinationCreationRequest data.
        
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
                "name": DestinationName.json_schema(),
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
                "accessRules": {
                    "type": "array",
                    "item": AccessRule.json_schema()
                },
                "bucket": {
                    "type": "string"
                },
                "path": {
                    "type": "string"
                },
                "fileFormat": FileFormat.json_schema(),
                "endpoint": {
                    "type": "string"
                },
                "accessKey": {
                    "type": "string"
                },
                "secretKey": {
                    "type": "string"
                }
            },
            "required": [
                "adt_type",
                "name",
                "description",
                "labels",
                "attributes",
                "accessRules",
                "bucket",
                "path",
                "fileFormat",
                "endpoint",
                "accessKey",
                "secretKey",
            ]
        }
    
    @classmethod
    def from_json(cls, data: dict) -> S3ADestinationCreationRequest:
        """Validate and parse JSON data into an instance of S3ADestinationCreationRequest.
        
        Args:
            data (dict): JSON data to validate and parse.
        
        Returns:
            An instance of S3ADestinationCreationRequest.
        
        Raises:
            ValidationError: When schema validation fails.
            KeyError: When a required field is missing from the JSON.
        """
        try:
            jsonschema.validate(data, cls.json_schema())
            return S3ADestinationCreationRequest(
                name=DestinationName.from_json(data["name"]),
                description=str(data["description"]),
                labels=[Label.from_json(v) for v in data["labels"]],
                attributes=[Attribute.from_json(v) for v in data["attributes"]],
                accessRules=[AccessRule.from_json(v) for v in data["accessRules"]],
                bucket=str(data["bucket"]),
                path=str(data["path"]),
                fileFormat=FileFormat.from_json(data["fileFormat"]),
                endpoint=str(data["endpoint"]),
                accessKey=str(data["accessKey"]),
                secretKey=str(data["secretKey"]),
            )
        except jsonschema.exceptions.ValidationError as ex:
            logging.debug(
                "Invalid JSON data received while parsing S3ADestinationCreationRequest",
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
            "accessRules": [v.to_json() for v in self.accessRules],
            "bucket": str(self.bucket),
            "path": str(self.path),
            "fileFormat": self.fileFormat.to_json(),
            "endpoint": str(self.endpoint),
            "accessKey": str(self.accessKey),
            "secretKey": str(self.secretKey)
        }


@dataclasses.dataclass(frozen=True)
class JDBCDestinationCreationRequest(DestinationCreationRequest):
    """Create a new output data store using JDBC.
    
    Args:
        name (DestinationName): A data field.
        description (str): A data field.
        labels (typing.List[Label]): A data field.
        attributes (typing.List[Attribute]): A data field.
        accessRules (typing.List[AccessRule]): A data field.
        url (str): A data field.
        schema (str): A data field.
        credentialsProvider (CredentialsProviderConfig): A data field.
    """
    
    ADT_TYPE: typing.ClassVar[str] = "jdbc"
    adt_type: str = dataclasses.field(init=False, repr=False, default=ADT_TYPE)
    
    name: DestinationName
    description: str
    labels: typing.List[Label]
    attributes: typing.List[Attribute]
    accessRules: typing.List[AccessRule]
    url: str
    schema: str
    credentialsProvider: CredentialsProviderConfig
    
    @classmethod
    def json_schema(cls) -> dict:
        """Return the JSON schema for JDBCDestinationCreationRequest data.
        
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
                "name": DestinationName.json_schema(),
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
                "accessRules": {
                    "type": "array",
                    "item": AccessRule.json_schema()
                },
                "url": {
                    "type": "string"
                },
                "schema": {
                    "type": "string"
                },
                "credentialsProvider": CredentialsProviderConfig.json_schema()
            },
            "required": [
                "adt_type",
                "name",
                "description",
                "labels",
                "attributes",
                "accessRules",
                "url",
                "schema",
                "credentialsProvider",
            ]
        }
    
    @classmethod
    def from_json(cls, data: dict) -> JDBCDestinationCreationRequest:
        """Validate and parse JSON data into an instance of JDBCDestinationCreationRequest.
        
        Args:
            data (dict): JSON data to validate and parse.
        
        Returns:
            An instance of JDBCDestinationCreationRequest.
        
        Raises:
            ValidationError: When schema validation fails.
            KeyError: When a required field is missing from the JSON.
        """
        try:
            jsonschema.validate(data, cls.json_schema())
            return JDBCDestinationCreationRequest(
                name=DestinationName.from_json(data["name"]),
                description=str(data["description"]),
                labels=[Label.from_json(v) for v in data["labels"]],
                attributes=[Attribute.from_json(v) for v in data["attributes"]],
                accessRules=[AccessRule.from_json(v) for v in data["accessRules"]],
                url=str(data["url"]),
                schema=str(data["schema"]),
                credentialsProvider=CredentialsProviderConfig.from_json(data["credentialsProvider"]),
            )
        except jsonschema.exceptions.ValidationError as ex:
            logging.debug(
                "Invalid JSON data received while parsing JDBCDestinationCreationRequest",
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
            "accessRules": [v.to_json() for v in self.accessRules],
            "url": str(self.url),
            "schema": str(self.schema),
            "credentialsProvider": self.credentialsProvider.to_json()
        }


@dataclasses.dataclass(frozen=True)
class HiveDestinationCreationRequest(DestinationCreationRequest):
    """Create a new output data store on Hive.
    
    Args:
        name (DestinationName): A data field.
        description (str): A data field.
        labels (typing.List[Label]): A data field.
        attributes (typing.List[Attribute]): A data field.
        accessRules (typing.List[AccessRule]): A data field.
        database (str): A data field.
    """
    
    ADT_TYPE: typing.ClassVar[str] = "hive"
    adt_type: str = dataclasses.field(init=False, repr=False, default=ADT_TYPE)
    
    name: DestinationName
    description: str
    labels: typing.List[Label]
    attributes: typing.List[Attribute]
    accessRules: typing.List[AccessRule]
    database: str
    
    @classmethod
    def json_schema(cls) -> dict:
        """Return the JSON schema for HiveDestinationCreationRequest data.
        
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
                "name": DestinationName.json_schema(),
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
                "accessRules": {
                    "type": "array",
                    "item": AccessRule.json_schema()
                },
                "database": {
                    "type": "string"
                }
            },
            "required": [
                "adt_type",
                "name",
                "description",
                "labels",
                "attributes",
                "accessRules",
                "database",
            ]
        }
    
    @classmethod
    def from_json(cls, data: dict) -> HiveDestinationCreationRequest:
        """Validate and parse JSON data into an instance of HiveDestinationCreationRequest.
        
        Args:
            data (dict): JSON data to validate and parse.
        
        Returns:
            An instance of HiveDestinationCreationRequest.
        
        Raises:
            ValidationError: When schema validation fails.
            KeyError: When a required field is missing from the JSON.
        """
        try:
            jsonschema.validate(data, cls.json_schema())
            return HiveDestinationCreationRequest(
                name=DestinationName.from_json(data["name"]),
                description=str(data["description"]),
                labels=[Label.from_json(v) for v in data["labels"]],
                attributes=[Attribute.from_json(v) for v in data["attributes"]],
                accessRules=[AccessRule.from_json(v) for v in data["accessRules"]],
                database=str(data["database"]),
            )
        except jsonschema.exceptions.ValidationError as ex:
            logging.debug(
                "Invalid JSON data received while parsing HiveDestinationCreationRequest",
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
            "accessRules": [v.to_json() for v in self.accessRules],
            "database": str(self.database)
        }


@dataclasses.dataclass(frozen=True)
class BigQueryDestinationCreationRequest(DestinationCreationRequest):
    """Create a new output data store on Google BigQuery.
    
    Args:
        name (DestinationName): A data field.
        description (str): A data field.
        labels (typing.List[Label]): A data field.
        attributes (typing.List[Attribute]): A data field.
        accessRules (typing.List[AccessRule]): A data field.
        path (str): A data field.
        stagingArea (GCSStagingArea): A data field.
    """
    
    ADT_TYPE: typing.ClassVar[str] = "bigquery"
    adt_type: str = dataclasses.field(init=False, repr=False, default=ADT_TYPE)
    
    name: DestinationName
    description: str
    labels: typing.List[Label]
    attributes: typing.List[Attribute]
    accessRules: typing.List[AccessRule]
    path: str
    stagingArea: GCSStagingArea
    
    @classmethod
    def json_schema(cls) -> dict:
        """Return the JSON schema for BigQueryDestinationCreationRequest data.
        
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
                "name": DestinationName.json_schema(),
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
                "accessRules": {
                    "type": "array",
                    "item": AccessRule.json_schema()
                },
                "path": {
                    "type": "string"
                },
                "stagingArea": GCSStagingArea.json_schema()
            },
            "required": [
                "adt_type",
                "name",
                "description",
                "labels",
                "attributes",
                "accessRules",
                "path",
                "stagingArea",
            ]
        }
    
    @classmethod
    def from_json(cls, data: dict) -> BigQueryDestinationCreationRequest:
        """Validate and parse JSON data into an instance of BigQueryDestinationCreationRequest.
        
        Args:
            data (dict): JSON data to validate and parse.
        
        Returns:
            An instance of BigQueryDestinationCreationRequest.
        
        Raises:
            ValidationError: When schema validation fails.
            KeyError: When a required field is missing from the JSON.
        """
        try:
            jsonschema.validate(data, cls.json_schema())
            return BigQueryDestinationCreationRequest(
                name=DestinationName.from_json(data["name"]),
                description=str(data["description"]),
                labels=[Label.from_json(v) for v in data["labels"]],
                attributes=[Attribute.from_json(v) for v in data["attributes"]],
                accessRules=[AccessRule.from_json(v) for v in data["accessRules"]],
                path=str(data["path"]),
                stagingArea=GCSStagingArea.from_json(data["stagingArea"]),
            )
        except jsonschema.exceptions.ValidationError as ex:
            logging.debug(
                "Invalid JSON data received while parsing BigQueryDestinationCreationRequest",
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
            "accessRules": [v.to_json() for v in self.accessRules],
            "path": str(self.path),
            "stagingArea": self.stagingArea.to_json()
        }


@dataclasses.dataclass(frozen=True)
class GCSDestinationCreationRequest(DestinationCreationRequest):
    """Create a new output data store on Google Cloud Storage.
    
    Args:
        name (DestinationName): A data field.
        description (str): A data field.
        labels (typing.List[Label]): A data field.
        attributes (typing.List[Attribute]): A data field.
        accessRules (typing.List[AccessRule]): A data field.
        bucket (str): A data field.
        path (str): A data field.
        fileFormat (FileFormat): A data field.
    """
    
    ADT_TYPE: typing.ClassVar[str] = "gcs"
    adt_type: str = dataclasses.field(init=False, repr=False, default=ADT_TYPE)
    
    name: DestinationName
    description: str
    labels: typing.List[Label]
    attributes: typing.List[Attribute]
    accessRules: typing.List[AccessRule]
    bucket: str
    path: str
    fileFormat: FileFormat
    
    @classmethod
    def json_schema(cls) -> dict:
        """Return the JSON schema for GCSDestinationCreationRequest data.
        
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
                "name": DestinationName.json_schema(),
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
                "accessRules": {
                    "type": "array",
                    "item": AccessRule.json_schema()
                },
                "bucket": {
                    "type": "string"
                },
                "path": {
                    "type": "string"
                },
                "fileFormat": FileFormat.json_schema()
            },
            "required": [
                "adt_type",
                "name",
                "description",
                "labels",
                "attributes",
                "accessRules",
                "bucket",
                "path",
                "fileFormat",
            ]
        }
    
    @classmethod
    def from_json(cls, data: dict) -> GCSDestinationCreationRequest:
        """Validate and parse JSON data into an instance of GCSDestinationCreationRequest.
        
        Args:
            data (dict): JSON data to validate and parse.
        
        Returns:
            An instance of GCSDestinationCreationRequest.
        
        Raises:
            ValidationError: When schema validation fails.
            KeyError: When a required field is missing from the JSON.
        """
        try:
            jsonschema.validate(data, cls.json_schema())
            return GCSDestinationCreationRequest(
                name=DestinationName.from_json(data["name"]),
                description=str(data["description"]),
                labels=[Label.from_json(v) for v in data["labels"]],
                attributes=[Attribute.from_json(v) for v in data["attributes"]],
                accessRules=[AccessRule.from_json(v) for v in data["accessRules"]],
                bucket=str(data["bucket"]),
                path=str(data["path"]),
                fileFormat=FileFormat.from_json(data["fileFormat"]),
            )
        except jsonschema.exceptions.ValidationError as ex:
            logging.debug(
                "Invalid JSON data received while parsing GCSDestinationCreationRequest",
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
            "accessRules": [v.to_json() for v in self.accessRules],
            "bucket": str(self.bucket),
            "path": str(self.path),
            "fileFormat": self.fileFormat.to_json()
        }


@dataclasses.dataclass(frozen=True)
class OnlineFeatureStoreDestinationCreationRequest(DestinationCreationRequest):
    """Create a new output data store using the online feature store.
    
    Args:
        name (DestinationName): A data field.
        description (str): A data field.
        labels (typing.List[Label]): A data field.
        attributes (typing.List[Attribute]): A data field.
        accessRules (typing.List[AccessRule]): A data field.
        url (str): A data field.
        schema (str): A data field.
        credentialsProvider (CredentialsProviderConfig): A data field.
    """
    
    ADT_TYPE: typing.ClassVar[str] = "onlinefeaturestore"
    adt_type: str = dataclasses.field(init=False, repr=False, default=ADT_TYPE)
    
    name: DestinationName
    description: str
    labels: typing.List[Label]
    attributes: typing.List[Attribute]
    accessRules: typing.List[AccessRule]
    url: str
    schema: str
    credentialsProvider: CredentialsProviderConfig
    
    @classmethod
    def json_schema(cls) -> dict:
        """Return the JSON schema for OnlineFeatureStoreDestinationCreationRequest data.
        
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
                "name": DestinationName.json_schema(),
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
                "accessRules": {
                    "type": "array",
                    "item": AccessRule.json_schema()
                },
                "url": {
                    "type": "string"
                },
                "schema": {
                    "type": "string"
                },
                "credentialsProvider": CredentialsProviderConfig.json_schema()
            },
            "required": [
                "adt_type",
                "name",
                "description",
                "labels",
                "attributes",
                "accessRules",
                "url",
                "schema",
                "credentialsProvider",
            ]
        }
    
    @classmethod
    def from_json(cls, data: dict) -> OnlineFeatureStoreDestinationCreationRequest:
        """Validate and parse JSON data into an instance of OnlineFeatureStoreDestinationCreationRequest.
        
        Args:
            data (dict): JSON data to validate and parse.
        
        Returns:
            An instance of OnlineFeatureStoreDestinationCreationRequest.
        
        Raises:
            ValidationError: When schema validation fails.
            KeyError: When a required field is missing from the JSON.
        """
        try:
            jsonschema.validate(data, cls.json_schema())
            return OnlineFeatureStoreDestinationCreationRequest(
                name=DestinationName.from_json(data["name"]),
                description=str(data["description"]),
                labels=[Label.from_json(v) for v in data["labels"]],
                attributes=[Attribute.from_json(v) for v in data["attributes"]],
                accessRules=[AccessRule.from_json(v) for v in data["accessRules"]],
                url=str(data["url"]),
                schema=str(data["schema"]),
                credentialsProvider=CredentialsProviderConfig.from_json(data["credentialsProvider"]),
            )
        except jsonschema.exceptions.ValidationError as ex:
            logging.debug(
                "Invalid JSON data received while parsing OnlineFeatureStoreDestinationCreationRequest",
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
            "accessRules": [v.to_json() for v in self.accessRules],
            "url": str(self.url),
            "schema": str(self.schema),
            "credentialsProvider": self.credentialsProvider.to_json()
        }


@dataclasses.dataclass(frozen=True)
class LocalDestinationCreationRequest(DestinationCreationRequest):
    """Create a new output data store on the local filesystem.
    
    Args:
        name (DestinationName): A data field.
        description (str): A data field.
        labels (typing.List[Label]): A data field.
        attributes (typing.List[Attribute]): A data field.
        accessRules (typing.List[AccessRule]): A data field.
        path (str): A data field.
        fileFormat (FileFormat): A data field.
    """
    
    ADT_TYPE: typing.ClassVar[str] = "local"
    adt_type: str = dataclasses.field(init=False, repr=False, default=ADT_TYPE)
    
    name: DestinationName
    description: str
    labels: typing.List[Label]
    attributes: typing.List[Attribute]
    accessRules: typing.List[AccessRule]
    path: str
    fileFormat: FileFormat
    
    @classmethod
    def json_schema(cls) -> dict:
        """Return the JSON schema for LocalDestinationCreationRequest data.
        
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
                "name": DestinationName.json_schema(),
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
                "accessRules": {
                    "type": "array",
                    "item": AccessRule.json_schema()
                },
                "path": {
                    "type": "string"
                },
                "fileFormat": FileFormat.json_schema()
            },
            "required": [
                "adt_type",
                "name",
                "description",
                "labels",
                "attributes",
                "accessRules",
                "path",
                "fileFormat",
            ]
        }
    
    @classmethod
    def from_json(cls, data: dict) -> LocalDestinationCreationRequest:
        """Validate and parse JSON data into an instance of LocalDestinationCreationRequest.
        
        Args:
            data (dict): JSON data to validate and parse.
        
        Returns:
            An instance of LocalDestinationCreationRequest.
        
        Raises:
            ValidationError: When schema validation fails.
            KeyError: When a required field is missing from the JSON.
        """
        try:
            jsonschema.validate(data, cls.json_schema())
            return LocalDestinationCreationRequest(
                name=DestinationName.from_json(data["name"]),
                description=str(data["description"]),
                labels=[Label.from_json(v) for v in data["labels"]],
                attributes=[Attribute.from_json(v) for v in data["attributes"]],
                accessRules=[AccessRule.from_json(v) for v in data["accessRules"]],
                path=str(data["path"]),
                fileFormat=FileFormat.from_json(data["fileFormat"]),
            )
        except jsonschema.exceptions.ValidationError as ex:
            logging.debug(
                "Invalid JSON data received while parsing LocalDestinationCreationRequest",
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
            "accessRules": [v.to_json() for v in self.accessRules],
            "path": str(self.path),
            "fileFormat": self.fileFormat.to_json()
        }


@dataclasses.dataclass(frozen=True)
class HDFSDestinationCreationRequest(DestinationCreationRequest):
    """Create a new output data store on HDFS.
    
    Args:
        name (DestinationName): A data field.
        description (str): A data field.
        labels (typing.List[Label]): A data field.
        attributes (typing.List[Attribute]): A data field.
        accessRules (typing.List[AccessRule]): A data field.
        path (str): A data field.
        fileFormat (FileFormat): A data field.
    """
    
    ADT_TYPE: typing.ClassVar[str] = "hdfs"
    adt_type: str = dataclasses.field(init=False, repr=False, default=ADT_TYPE)
    
    name: DestinationName
    description: str
    labels: typing.List[Label]
    attributes: typing.List[Attribute]
    accessRules: typing.List[AccessRule]
    path: str
    fileFormat: FileFormat
    
    @classmethod
    def json_schema(cls) -> dict:
        """Return the JSON schema for HDFSDestinationCreationRequest data.
        
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
                "name": DestinationName.json_schema(),
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
                "accessRules": {
                    "type": "array",
                    "item": AccessRule.json_schema()
                },
                "path": {
                    "type": "string"
                },
                "fileFormat": FileFormat.json_schema()
            },
            "required": [
                "adt_type",
                "name",
                "description",
                "labels",
                "attributes",
                "accessRules",
                "path",
                "fileFormat",
            ]
        }
    
    @classmethod
    def from_json(cls, data: dict) -> HDFSDestinationCreationRequest:
        """Validate and parse JSON data into an instance of HDFSDestinationCreationRequest.
        
        Args:
            data (dict): JSON data to validate and parse.
        
        Returns:
            An instance of HDFSDestinationCreationRequest.
        
        Raises:
            ValidationError: When schema validation fails.
            KeyError: When a required field is missing from the JSON.
        """
        try:
            jsonschema.validate(data, cls.json_schema())
            return HDFSDestinationCreationRequest(
                name=DestinationName.from_json(data["name"]),
                description=str(data["description"]),
                labels=[Label.from_json(v) for v in data["labels"]],
                attributes=[Attribute.from_json(v) for v in data["attributes"]],
                accessRules=[AccessRule.from_json(v) for v in data["accessRules"]],
                path=str(data["path"]),
                fileFormat=FileFormat.from_json(data["fileFormat"]),
            )
        except jsonschema.exceptions.ValidationError as ex:
            logging.debug(
                "Invalid JSON data received while parsing HDFSDestinationCreationRequest",
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
            "accessRules": [v.to_json() for v in self.accessRules],
            "path": str(self.path),
            "fileFormat": self.fileFormat.to_json()
        }


@dataclasses.dataclass(frozen=True)
class KafkaDestinationCreationRequest(DestinationCreationRequest):
    """Create a new output data store on Kafka.
    
    Args:
        name (DestinationName): A data field.
        description (str): A data field.
        labels (typing.List[Label]): A data field.
        attributes (typing.List[Attribute]): A data field.
        accessRules (typing.List[AccessRule]): A data field.
        bootstrapServers (str): A data field.
        schemaRegistryUrl (str): A data field.
        kafkaPropertiesProviders (typing.List[SensitiveAttribute]): A data field.
    """
    
    ADT_TYPE: typing.ClassVar[str] = "kafka"
    adt_type: str = dataclasses.field(init=False, repr=False, default=ADT_TYPE)
    
    name: DestinationName
    description: str
    labels: typing.List[Label]
    attributes: typing.List[Attribute]
    accessRules: typing.List[AccessRule]
    bootstrapServers: str
    schemaRegistryUrl: str
    kafkaPropertiesProviders: typing.List[SensitiveAttribute]
    
    @classmethod
    def json_schema(cls) -> dict:
        """Return the JSON schema for KafkaDestinationCreationRequest data.
        
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
                "name": DestinationName.json_schema(),
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
                "accessRules": {
                    "type": "array",
                    "item": AccessRule.json_schema()
                },
                "bootstrapServers": {
                    "type": "string"
                },
                "schemaRegistryUrl": {
                    "type": "string"
                },
                "kafkaPropertiesProviders": {
                    "type": "array",
                    "item": SensitiveAttribute.json_schema()
                }
            },
            "required": [
                "adt_type",
                "name",
                "description",
                "labels",
                "attributes",
                "accessRules",
                "bootstrapServers",
                "schemaRegistryUrl",
                "kafkaPropertiesProviders",
            ]
        }
    
    @classmethod
    def from_json(cls, data: dict) -> KafkaDestinationCreationRequest:
        """Validate and parse JSON data into an instance of KafkaDestinationCreationRequest.
        
        Args:
            data (dict): JSON data to validate and parse.
        
        Returns:
            An instance of KafkaDestinationCreationRequest.
        
        Raises:
            ValidationError: When schema validation fails.
            KeyError: When a required field is missing from the JSON.
        """
        try:
            jsonschema.validate(data, cls.json_schema())
            return KafkaDestinationCreationRequest(
                name=DestinationName.from_json(data["name"]),
                description=str(data["description"]),
                labels=[Label.from_json(v) for v in data["labels"]],
                attributes=[Attribute.from_json(v) for v in data["attributes"]],
                accessRules=[AccessRule.from_json(v) for v in data["accessRules"]],
                bootstrapServers=str(data["bootstrapServers"]),
                schemaRegistryUrl=str(data["schemaRegistryUrl"]),
                kafkaPropertiesProviders=[SensitiveAttribute.from_json(v) for v in data["kafkaPropertiesProviders"]],
            )
        except jsonschema.exceptions.ValidationError as ex:
            logging.debug(
                "Invalid JSON data received while parsing KafkaDestinationCreationRequest",
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
            "accessRules": [v.to_json() for v in self.accessRules],
            "bootstrapServers": str(self.bootstrapServers),
            "schemaRegistryUrl": str(self.schemaRegistryUrl),
            "kafkaPropertiesProviders": [v.to_json() for v in self.kafkaPropertiesProviders]
        }


@dataclasses.dataclass(frozen=True)
class SnowflakeDestinationCreationRequest(DestinationCreationRequest):
    """Create a new output data store on Snowflake.
    
    Args:
        name (DestinationName): A data field.
        description (str): A data field.
        labels (typing.List[Label]): A data field.
        attributes (typing.List[Attribute]): A data field.
        accessRules (typing.List[AccessRule]): A data field.
        url (str): A data field.
        warehouse (str): A data field.
        database (str): A data field.
        schema (str): A data field.
        credentialsProvider (CredentialsProviderConfig): A data field.
    """
    
    ADT_TYPE: typing.ClassVar[str] = "snowflake"
    adt_type: str = dataclasses.field(init=False, repr=False, default=ADT_TYPE)
    
    name: DestinationName
    description: str
    labels: typing.List[Label]
    attributes: typing.List[Attribute]
    accessRules: typing.List[AccessRule]
    url: str
    warehouse: str
    database: str
    schema: str
    credentialsProvider: CredentialsProviderConfig
    
    @classmethod
    def json_schema(cls) -> dict:
        """Return the JSON schema for SnowflakeDestinationCreationRequest data.
        
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
                "name": DestinationName.json_schema(),
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
                "accessRules": {
                    "type": "array",
                    "item": AccessRule.json_schema()
                },
                "url": {
                    "type": "string"
                },
                "warehouse": {
                    "type": "string"
                },
                "database": {
                    "type": "string"
                },
                "schema": {
                    "type": "string"
                },
                "credentialsProvider": CredentialsProviderConfig.json_schema()
            },
            "required": [
                "adt_type",
                "name",
                "description",
                "labels",
                "attributes",
                "accessRules",
                "url",
                "warehouse",
                "database",
                "schema",
                "credentialsProvider",
            ]
        }
    
    @classmethod
    def from_json(cls, data: dict) -> SnowflakeDestinationCreationRequest:
        """Validate and parse JSON data into an instance of SnowflakeDestinationCreationRequest.
        
        Args:
            data (dict): JSON data to validate and parse.
        
        Returns:
            An instance of SnowflakeDestinationCreationRequest.
        
        Raises:
            ValidationError: When schema validation fails.
            KeyError: When a required field is missing from the JSON.
        """
        try:
            jsonschema.validate(data, cls.json_schema())
            return SnowflakeDestinationCreationRequest(
                name=DestinationName.from_json(data["name"]),
                description=str(data["description"]),
                labels=[Label.from_json(v) for v in data["labels"]],
                attributes=[Attribute.from_json(v) for v in data["attributes"]],
                accessRules=[AccessRule.from_json(v) for v in data["accessRules"]],
                url=str(data["url"]),
                warehouse=str(data["warehouse"]),
                database=str(data["database"]),
                schema=str(data["schema"]),
                credentialsProvider=CredentialsProviderConfig.from_json(data["credentialsProvider"]),
            )
        except jsonschema.exceptions.ValidationError as ex:
            logging.debug(
                "Invalid JSON data received while parsing SnowflakeDestinationCreationRequest",
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
            "accessRules": [v.to_json() for v in self.accessRules],
            "url": str(self.url),
            "warehouse": str(self.warehouse),
            "database": str(self.database),
            "schema": str(self.schema),
            "credentialsProvider": self.credentialsProvider.to_json()
        }


@dataclasses.dataclass(frozen=True)
class BigtableDestinationCreationRequest(DestinationCreationRequest):
    """Create a new online data destination in Google Bigtable.
    
    Args:
        name (DestinationName): A data field.
        description (str): A data field.
        labels (typing.List[Label]): A data field.
        attributes (typing.List[Attribute]): A data field.
        accessRules (typing.List[AccessRule]): A data field.
        project (str): A data field.
        instance (str): A data field.
    """
    
    ADT_TYPE: typing.ClassVar[str] = "bigtable"
    adt_type: str = dataclasses.field(init=False, repr=False, default=ADT_TYPE)
    
    name: DestinationName
    description: str
    labels: typing.List[Label]
    attributes: typing.List[Attribute]
    accessRules: typing.List[AccessRule]
    project: str
    instance: str
    
    @classmethod
    def json_schema(cls) -> dict:
        """Return the JSON schema for BigtableDestinationCreationRequest data.
        
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
                "name": DestinationName.json_schema(),
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
                "accessRules": {
                    "type": "array",
                    "item": AccessRule.json_schema()
                },
                "project": {
                    "type": "string"
                },
                "instance": {
                    "type": "string"
                }
            },
            "required": [
                "adt_type",
                "name",
                "description",
                "labels",
                "attributes",
                "accessRules",
                "project",
                "instance",
            ]
        }
    
    @classmethod
    def from_json(cls, data: dict) -> BigtableDestinationCreationRequest:
        """Validate and parse JSON data into an instance of BigtableDestinationCreationRequest.
        
        Args:
            data (dict): JSON data to validate and parse.
        
        Returns:
            An instance of BigtableDestinationCreationRequest.
        
        Raises:
            ValidationError: When schema validation fails.
            KeyError: When a required field is missing from the JSON.
        """
        try:
            jsonschema.validate(data, cls.json_schema())
            return BigtableDestinationCreationRequest(
                name=DestinationName.from_json(data["name"]),
                description=str(data["description"]),
                labels=[Label.from_json(v) for v in data["labels"]],
                attributes=[Attribute.from_json(v) for v in data["attributes"]],
                accessRules=[AccessRule.from_json(v) for v in data["accessRules"]],
                project=str(data["project"]),
                instance=str(data["instance"]),
            )
        except jsonschema.exceptions.ValidationError as ex:
            logging.debug(
                "Invalid JSON data received while parsing BigtableDestinationCreationRequest",
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
            "accessRules": [v.to_json() for v in self.accessRules],
            "project": str(self.project),
            "instance": str(self.instance)
        }


@dataclasses.dataclass(frozen=True)
class ExactTargetDestinationCreationRequest(DestinationCreationRequest):
    """Create a new SalesForce Marketing cloud destination.
    
    Args:
        id (DestinationId): A data field.
        name (DestinationName): A data field.
        description (str): A data field.
        labels (typing.List[Label]): A data field.
        attributes (typing.List[Attribute]): A data field.
        accessRules (typing.List[AccessRule]): A data field.
        credentialsProvider (CredentialsProviderConfig): A data field.
        authEndpoint (str): A data field.
        restEndpoint (str): A data field.
        soapEndpoint (str): A data field.
        sftpSettingsConfig (typing.Optional[ExactTargetSFTPConfig]): A data field.
        version (DestinationVersionId): A data field.
    """
    
    ADT_TYPE: typing.ClassVar[str] = "exacttarget"
    adt_type: str = dataclasses.field(init=False, repr=False, default=ADT_TYPE)
    
    id: DestinationId
    name: DestinationName
    description: str
    labels: typing.List[Label]
    attributes: typing.List[Attribute]
    accessRules: typing.List[AccessRule]
    credentialsProvider: CredentialsProviderConfig
    authEndpoint: str
    restEndpoint: str
    soapEndpoint: str
    sftpSettingsConfig: typing.Optional[ExactTargetSFTPConfig]
    version: DestinationVersionId
    
    @classmethod
    def json_schema(cls) -> dict:
        """Return the JSON schema for ExactTargetDestinationCreationRequest data.
        
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
                "id": DestinationId.json_schema(),
                "name": DestinationName.json_schema(),
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
                "accessRules": {
                    "type": "array",
                    "item": AccessRule.json_schema()
                },
                "credentialsProvider": CredentialsProviderConfig.json_schema(),
                "authEndpoint": {
                    "type": "string"
                },
                "restEndpoint": {
                    "type": "string"
                },
                "soapEndpoint": {
                    "type": "string"
                },
                "sftpSettingsConfig": {
                    "oneOf": [
                        {"type": "null"},
                        ExactTargetSFTPConfig.json_schema(),
                    ]
                },
                "version": DestinationVersionId.json_schema()
            },
            "required": [
                "adt_type",
                "id",
                "name",
                "description",
                "labels",
                "attributes",
                "accessRules",
                "credentialsProvider",
                "authEndpoint",
                "restEndpoint",
                "soapEndpoint",
                "version",
            ]
        }
    
    @classmethod
    def from_json(cls, data: dict) -> ExactTargetDestinationCreationRequest:
        """Validate and parse JSON data into an instance of ExactTargetDestinationCreationRequest.
        
        Args:
            data (dict): JSON data to validate and parse.
        
        Returns:
            An instance of ExactTargetDestinationCreationRequest.
        
        Raises:
            ValidationError: When schema validation fails.
            KeyError: When a required field is missing from the JSON.
        """
        try:
            jsonschema.validate(data, cls.json_schema())
            return ExactTargetDestinationCreationRequest(
                id=DestinationId.from_json(data["id"]),
                name=DestinationName.from_json(data["name"]),
                description=str(data["description"]),
                labels=[Label.from_json(v) for v in data["labels"]],
                attributes=[Attribute.from_json(v) for v in data["attributes"]],
                accessRules=[AccessRule.from_json(v) for v in data["accessRules"]],
                credentialsProvider=CredentialsProviderConfig.from_json(data["credentialsProvider"]),
                authEndpoint=str(data["authEndpoint"]),
                restEndpoint=str(data["restEndpoint"]),
                soapEndpoint=str(data["soapEndpoint"]),
                sftpSettingsConfig=(
                    lambda v: ExactTargetSFTPConfig.from_json(v) if v is not None else None
                )(
                    data.get("sftpSettingsConfig", None)
                ),
                version=DestinationVersionId.from_json(data["version"]),
            )
        except jsonschema.exceptions.ValidationError as ex:
            logging.debug(
                "Invalid JSON data received while parsing ExactTargetDestinationCreationRequest",
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
            "accessRules": [v.to_json() for v in self.accessRules],
            "credentialsProvider": self.credentialsProvider.to_json(),
            "authEndpoint": str(self.authEndpoint),
            "restEndpoint": str(self.restEndpoint),
            "soapEndpoint": str(self.soapEndpoint),
            "sftpSettingsConfig": (lambda v: v.to_json() if v is not None else v)(self.sftpSettingsConfig),
            "version": self.version.to_json()
        }
