"""
An implementation of JSON Schema for Python.

The main functionality is provided by the validator classes for each of the
supported JSON Schema versions.

Most commonly, `jsonschema.validators.validate` is the quickest way to simply
validate a given instance under a schema, and will create a validator
for you.
"""
import warnings

from bsonschema._format import FormatChecker
from bsonschema._types import TypeChecker
from bsonschema.exceptions import SchemaError, ValidationError
from bsonschema.validators import (
    Draft3Validator
)

def __getattr__(name):
    return Draft3Validator

__all__ = [
    "Draft3Validator",
]
