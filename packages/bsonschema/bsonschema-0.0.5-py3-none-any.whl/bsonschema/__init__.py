"""
An implementation of JSON Schema for Python.

The main functionality is provided by the validator classes for each of the
supported JSON Schema versions.

Most commonly, `bsonschema.validators.validate` is the quickest way to simply
validate a given instance under a schema, and will create a validator
for you.
"""
import warnings

from bsonschema._format import FormatChecker
from bsonschema._types import TypeChecker
from bsonschema.exceptions import SchemaError, ValidationError
from bsonschema.validators import Draft3Validator


def __getattr__(name):
    if name == "__version__":
        warnings.warn(
            "Accessing bsonschema.__version__ is deprecated and will be "
            "removed in a future release. Use importlib.metadata directly "
            "to query for bsonschema's version.",
            DeprecationWarning,
            stacklevel=2,
        )

        from importlib import metadata
        return metadata.version("bsonschema")
    elif name == "RefResolver":
        from bsonschema.validators import _RefResolver
        warnings.warn(
            _RefResolver._DEPRECATION_MESSAGE,
            DeprecationWarning,
            stacklevel=2,
        )
        return _RefResolver
    elif name == "ErrorTree":
        warnings.warn(
            "Importing ErrorTree directly from the bsonschema package "
            "is deprecated and will become an ImportError. Import it from "
            "bsonschema.exceptions instead.",
            DeprecationWarning,
            stacklevel=2,
        )
        from bsonschema.exceptions import ErrorTree
        return ErrorTree
    elif name == "FormatError":
        warnings.warn(
            "Importing FormatError directly from the bsonschema package "
            "is deprecated and will become an ImportError. Import it from "
            "bsonschema.exceptions instead.",
            DeprecationWarning,
            stacklevel=2,
        )
        from bsonschema.exceptions import FormatError
        return FormatError
    elif name == "Validator":
        warnings.warn(
            "Importing Validator directly from the bsonschema package "
            "is deprecated and will become an ImportError. Import it from "
            "bsonschema.protocols instead.",
            DeprecationWarning,
            stacklevel=2,
        )
        from bsonschema.protocols import Validator
        return Validator
    elif name == "RefResolutionError":
        from bsonschema.exceptions import _RefResolutionError
        warnings.warn(
            _RefResolutionError._DEPRECATION_MESSAGE,
            DeprecationWarning,
            stacklevel=2,
        )
        return _RefResolutionError

    format_checkers = {
        "draft3_format_checker": Draft3Validator,
    }
    ValidatorForFormat = format_checkers.get(name)
    if ValidatorForFormat is not None:
        warnings.warn(
            f"Accessing bsonschema.{name} is deprecated and will be "
            "removed in a future release. Instead, use the FORMAT_CHECKER "
            "attribute on the corresponding Validator.",
            DeprecationWarning,
            stacklevel=2,
        )
        return ValidatorForFormat.FORMAT_CHECKER

    raise AttributeError(f"module {__name__} has no attribute {name}")


__all__ = [
    "Draft3Validator"
]
