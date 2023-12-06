"""Generated implementation of commit."""

# WARNING DO NOT EDIT
# This code was generated from commit.mcn

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

from ..user import UserId


@dataclasses.dataclass(frozen=True)
class CommitId:
    """Unique identifier of a commit.
    
    Args:
        value (uuid.UUID): A data field.
    """
    
    value: uuid.UUID
    
    def __str__(self) -> str:
        """Return a str of the wrapped value."""
        return str(self.value)
    
    @classmethod
    def json_schema(cls) -> dict:
        """Return the JSON schema for CommitId data.
        
        Returns:
            A Python dictionary describing the JSON schema.
        """
        return {
            "type": "string",
            "format": "uuid"
        }
    
    @classmethod
    def from_json(cls, data: dict) -> CommitId:
        """Validate and parse JSON data into an instance of CommitId.
        
        Args:
            data (dict): JSON data to validate and parse.
        
        Returns:
            An instance of CommitId.
        
        Raises:
            ValidationError: When schema validation fails.
            KeyError: When a required field is missing from the JSON.
        """
        try:
            jsonschema.validate(data, cls.json_schema())
            return CommitId(uuid.UUID(hex=data))
        except jsonschema.exceptions.ValidationError as ex:
            logging.debug("Invalid JSON data received while parsing CommitId", exc_info=ex)
            raise
    
    def to_json(self) -> dict:
        """Serialise this instance as JSON.
        
        Returns:
            Data ready to serialise as JSON.
        """
        return str(self.value)
    
    @classmethod
    def from_json_key(cls, data: str) -> CommitId:
        """Parse a JSON string such as a dictionary key."""
        return CommitId((lambda s: uuid.UUID(hex=s))(data))
    
    def to_json_key(self) -> str:
        """Serialise as a JSON string suitable for use as a dictionary key."""
        return str(self.value)


@dataclasses.dataclass(frozen=True)
class Commit:
    """Metadata of a commit.
    
    Args:
        id (CommitId): A data field.
        parents (typing.List[CommitId]): A data field.
        createdAt (datetime.datetime): A data field.
        author (UserId): A data field.
        description (typing.Optional[str]): A data field.
    """
    
    id: CommitId
    parents: typing.List[CommitId]
    createdAt: datetime.datetime
    author: UserId
    description: typing.Optional[str]
    
    @classmethod
    def json_schema(cls) -> dict:
        """Return the JSON schema for Commit data.
        
        Returns:
            A Python dictionary describing the JSON schema.
        """
        return {
            "type": "object",
            "properties": {
                "id": CommitId.json_schema(),
                "parents": {
                    "type": "array",
                    "item": CommitId.json_schema()
                },
                "createdAt": {
                    "type": "string",
                    "format": "date-time"
                },
                "author": UserId.json_schema(),
                "description": {
                    "oneOf": [
                        {"type": "null"},
                        {"type": "string"},
                    ]
                }
            },
            "required": [
                "id",
                "parents",
                "createdAt",
                "author",
            ]
        }
    
    @classmethod
    def from_json(cls, data: dict) -> Commit:
        """Validate and parse JSON data into an instance of Commit.
        
        Args:
            data (dict): JSON data to validate and parse.
        
        Returns:
            An instance of Commit.
        
        Raises:
            ValidationError: When schema validation fails.
            KeyError: When a required field is missing from the JSON.
        """
        try:
            jsonschema.validate(data, cls.json_schema())
            return Commit(
                id=CommitId.from_json(data["id"]),
                parents=[CommitId.from_json(v) for v in data["parents"]],
                createdAt=isodate.parse_datetime(data["createdAt"]),
                author=UserId.from_json(data["author"]),
                description=(
                    lambda v: str(v) if v is not None else None
                )(
                    data.get("description", None)
                ),
            )
        except jsonschema.exceptions.ValidationError as ex:
            logging.debug(
                "Invalid JSON data received while parsing Commit",
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
            "parents": [v.to_json() for v in self.parents],
            "createdAt": self.createdAt.strftime('%Y-%m-%dT%H:%M:%S.%f%z'),
            "author": self.author.to_json(),
            "description": (lambda v: str(v) if v is not None else v)(self.description)
        }


@dataclasses.dataclass(frozen=True)
class CommitWithName:
    """Metadata of a commit.
    
    Args:
        id (CommitId): A data field.
        parents (typing.List[CommitId]): A data field.
        createdAt (datetime.datetime): A data field.
        author (UserId): A data field.
        description (typing.Optional[str]): A data field.
        name (typing.Optional[str]): A data field.
    """
    
    id: CommitId
    parents: typing.List[CommitId]
    createdAt: datetime.datetime
    author: UserId
    description: typing.Optional[str]
    name: typing.Optional[str]
    
    @classmethod
    def json_schema(cls) -> dict:
        """Return the JSON schema for CommitWithName data.
        
        Returns:
            A Python dictionary describing the JSON schema.
        """
        return {
            "type": "object",
            "properties": {
                "id": CommitId.json_schema(),
                "parents": {
                    "type": "array",
                    "item": CommitId.json_schema()
                },
                "createdAt": {
                    "type": "string",
                    "format": "date-time"
                },
                "author": UserId.json_schema(),
                "description": {
                    "oneOf": [
                        {"type": "null"},
                        {"type": "string"},
                    ]
                },
                "name": {
                    "oneOf": [
                        {"type": "null"},
                        {"type": "string"},
                    ]
                }
            },
            "required": [
                "id",
                "parents",
                "createdAt",
                "author",
            ]
        }
    
    @classmethod
    def from_json(cls, data: dict) -> CommitWithName:
        """Validate and parse JSON data into an instance of CommitWithName.
        
        Args:
            data (dict): JSON data to validate and parse.
        
        Returns:
            An instance of CommitWithName.
        
        Raises:
            ValidationError: When schema validation fails.
            KeyError: When a required field is missing from the JSON.
        """
        try:
            jsonschema.validate(data, cls.json_schema())
            return CommitWithName(
                id=CommitId.from_json(data["id"]),
                parents=[CommitId.from_json(v) for v in data["parents"]],
                createdAt=isodate.parse_datetime(data["createdAt"]),
                author=UserId.from_json(data["author"]),
                description=(
                    lambda v: str(v) if v is not None else None
                )(
                    data.get("description", None)
                ),
                name=(lambda v: str(v) if v is not None else None)(data.get("name", None)),
            )
        except jsonschema.exceptions.ValidationError as ex:
            logging.debug(
                "Invalid JSON data received while parsing CommitWithName",
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
            "parents": [v.to_json() for v in self.parents],
            "createdAt": self.createdAt.strftime('%Y-%m-%dT%H:%M:%S.%f%z'),
            "author": self.author.to_json(),
            "description": (lambda v: str(v) if v is not None else v)(self.description),
            "name": (lambda v: str(v) if v is not None else v)(self.name)
        }
