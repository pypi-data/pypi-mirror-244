from bsonschema.validators import (
    Draft3Validator
)

def __getattr__(name):
    return Draft3Validator

__all__ = [
    "Draft3Validator",
]
