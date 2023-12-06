"""
Creation and extension of validators, with implementations for existing drafts.
"""
from __future__ import annotations

from collections import deque
from collections.abc import Iterable, Mapping, Sequence
from functools import lru_cache
from operator import methodcaller
from urllib.parse import unquote, urldefrag, urljoin, urlsplit
from urllib.request import urlopen
from warnings import warn
import contextlib
import json
import reprlib
import warnings

from attrs import define, field, fields
from rpds import HashTrieMap
import referencing.exceptions
import referencing.jsonschema

import bsonschema._format
import bsonschema._keywords
import bsonschema._legacy_keywords
import bsonschema._types
import bsonschema._utils
import bsonschema.exceptions

_UNSET = bsonschema._utils.Unset()

_VALIDATORS: dict[str, any] = {}
_META_SCHEMAS = bsonschema._utils.URIDict()

SPECIFICATIONS: referencing.jsonschema.Registry[referencing.jsonschema.Specification[referencing.jsonschema.Schema]] = referencing.jsonschema.Registry(
    {  # type: ignore[reportGeneralTypeIssues]  # :/ internal vs external types
        dialect_id: referencing.jsonschema.Resource.opaque(specification)
        for dialect_id, specification in [
            ("http://json-schema.org/draft-03/schema", referencing.jsonschema.DRAFT3),
        ]
    },
)

draft3string = """
{
	"$schema" : "http://json-schema.org/draft-03/schema#",
	"id" : "http://json-schema.org/draft-03/schema#",
	"type" : "object",
	
	"properties" : {
		"type" : {
			"type" : ["string", "array"],
			"items" : {
				"type" : ["string", {"$ref" : "#"}]
			},
			"uniqueItems" : true,
			"default" : "any"
		},
		
		"properties" : {
			"type" : "object",
			"additionalProperties" : {"$ref" : "#"},
			"default" : {}
		},
		
		"patternProperties" : {
			"type" : "object",
			"additionalProperties" : {"$ref" : "#"},
			"default" : {}
		},
		
		"additionalProperties" : {
			"type" : [{"$ref" : "#"}, "boolean"],
			"default" : {}
		},
		
		"items" : {
			"type" : [{"$ref" : "#"}, "array"],
			"items" : {"$ref" : "#"},
			"default" : {}
		},
		
		"additionalItems" : {
			"type" : [{"$ref" : "#"}, "boolean"],
			"default" : {}
		},
		
		"required" : {
			"type" : "boolean",
			"default" : false
		},
		
		"dependencies" : {
			"type" : "object",
			"additionalProperties" : {
				"type" : ["string", "array", {"$ref" : "#"}],
				"items" : {
					"type" : "string"
				}
			},
			"default" : {}
		},
		
		"minimum" : {
			"type" : "number"
		},
		
		"maximum" : {
			"type" : "number"
		},
		
		"exclusiveMinimum" : {
			"type" : "boolean",
			"default" : false
		},
		
		"exclusiveMaximum" : {
			"type" : "boolean",
			"default" : false
		},
		
		"minItems" : {
			"type" : "integer",
			"minimum" : 0,
			"default" : 0
		},
		
		"maxItems" : {
			"type" : "integer",
			"minimum" : 0
		},
		
		"uniqueItems" : {
			"type" : "boolean",
			"default" : false
		},
		
		"pattern" : {
			"type" : "string",
			"format" : "regex"
		},
		
		"minLength" : {
			"type" : "integer",
			"minimum" : 0,
			"default" : 0
		},
		
		"maxLength" : {
			"type" : "integer"
		},
		
		"enum" : {
			"type" : "array",
			"minItems" : 1,
			"uniqueItems" : true
		},
		
		"default" : {
			"type" : "any"
		},
		
		"title" : {
			"type" : "string"
		},
		
		"description" : {
			"type" : "string"
		},
		
		"format" : {
			"type" : "string"
		},
		
		"divisibleBy" : {
			"type" : "number",
			"minimum" : 0,
			"exclusiveMinimum" : true,
			"default" : 1
		},
		
		"disallow" : {
			"type" : ["string", "array"],
			"items" : {
				"type" : ["string", {"$ref" : "#"}]
			},
			"uniqueItems" : true
		},
		
		"extends" : {
			"type" : [{"$ref" : "#"}, "array"],
			"items" : {"$ref" : "#"},
			"default" : {}
		},
		
		"id" : {
			"type" : "string",
			"format" : "uri"
		},
		
		"$ref" : {
			"type" : "string",
			"format" : "uri"
		},
		
		"$schema" : {
			"type" : "string",
			"format" : "uri"
		}
	},
	
	"dependencies" : {
		"exclusiveMinimum" : "minimum",
		"exclusiveMaximum" : "maximum"
	},
	
	"default" : {}
}"""


def __getattr__(name):
    if name == "ErrorTree":
        warnings.warn(
            "Importing ErrorTree from bsonschema.validators is deprecated. "
            "Instead import it from bsonschema.exceptions.",
            DeprecationWarning,
            stacklevel=2,
        )
        from bsonschema.exceptions import ErrorTree
        return ErrorTree
    elif name == "validators":
        warnings.warn(
            "Accessing bsonschema.validators.validators is deprecated. "
            "Use bsonschema.validators.validator_for with a given schema.",
            DeprecationWarning,
            stacklevel=2,
        )
        return _VALIDATORS
    elif name == "meta_schemas":
        warnings.warn(
            "Accessing bsonschema.validators.meta_schemas is deprecated. "
            "Use bsonschema.validators.validator_for with a given schema.",
            DeprecationWarning,
            stacklevel=2,
        )
        return _META_SCHEMAS
    raise AttributeError(f"module {__name__} has no attribute {name}")


_REMOTE_WARNING_REGISTRY = SPECIFICATIONS


def create(
    validators: (
        Mapping[str, any]
        | Iterable[tuple[str, any]]
    ) = (),
    type_checker: bsonschema._types.TypeChecker = bsonschema._types.draft3_type_checker,
    format_checker: bsonschema._format.FormatChecker = bsonschema._format.draft3_format_checker,
    id_of = referencing.jsonschema.DRAFT3.id_of,
    applicable_validators = methodcaller(
        "items",
    ),
):
    # preemptively don't shadow the `Validator.format_checker` local
    format_checker_arg = format_checker

    specification = (referencing.jsonschema.DRAFT3)

    @define
    class Validator:

        VALIDATORS = dict(validators)  # noqa: RUF012
        META_SCHEMA = referencing.jsonschema.DRAFT3  # noqa: RUF012
        TYPE_CHECKER = type_checker
        FORMAT_CHECKER = format_checker_arg
        ID_OF = staticmethod(id_of)

        _APPLICABLE_VALIDATORS = applicable_validators

        schema: referencing.jsonschema.Schema = field(repr=reprlib.repr)
        _ref_resolver = field(default=None, repr=False, alias="resolver")
        format_checker: bsonschema._format.FormatChecker | None = field(default=None)
        _registry: referencing.jsonschema.SchemaRegistry = field(
            default=_REMOTE_WARNING_REGISTRY,
            kw_only=True,
            repr=False,
        )
        _resolver = field(
            alias="_resolver",
            default=None,
            kw_only=True,
            repr=False,
        )

        def __init_subclass__(cls):
            warnings.warn(
                (
                    "Subclassing validator classes is not intended to "
                    "be part of their public API. A future version "
                    "will make doing so an error, as the behavior of "
                    "subclasses isn't guaranteed to stay the same "
                    "between releases of jsonschema. Instead, prefer "
                    "composition of validators, wrapping them in an object "
                    "owned entirely by the downstream library."
                ),
                DeprecationWarning,
                stacklevel=2,
            )

            def evolve(self, **changes):
                cls = self.__class__
                schema = changes.setdefault("schema", self.schema)
                NewValidator = Validator_

                for field in fields(cls):  # noqa: F402
                    if not field.init:
                        continue
                    attr_name = field.name
                    init_name = field.alias
                    if init_name not in changes:
                        changes[init_name] = getattr(self, attr_name)

                return NewValidator(**changes)

            cls.evolve = evolve

        def __attrs_post_init__(self):
            if self._resolver is None:
                registry = self._registry
                resource = specification.create_resource(self.schema)
                self._resolver = registry.resolver_with_root(resource)

            # REMOVEME: Legacy ref resolution state management.
            push_scope = getattr(self._ref_resolver, "push_scope", None)
            if push_scope is not None:
                id = id_of(self.schema)
                if id is not None:
                    push_scope(id)

        @classmethod
        def check_schema(cls, schema, format_checker=_UNSET):
            Validator = Validator_
            if format_checker is _UNSET:
                format_checker = Validator.FORMAT_CHECKER
            validator = Validator(
                schema=referencing.jsonschema.DRAFT3,
                format_checker=format_checker,
            )
            for error in validator.iter_errors(schema):
                raise bsonschema.exceptions.SchemaError.create_from(error)

        @property
        def resolver(self):
            warnings.warn(
                (
                    f"Accessing {self.__class__.__name__}.resolver is "
                    "deprecated as of v4.18.0, in favor of the "
                    "https://github.com/python-jsonschema/referencing "
                    "library, which provides more compliant referencing "
                    "behavior as well as more flexible APIs for "
                    "customization."
                ),
                DeprecationWarning,
                stacklevel=2,
            )
            return self._ref_resolver

        def evolve(self, **changes):
            schema = changes.setdefault("schema", self.schema)
            NewValidator = Validator_

            for (attr_name, init_name) in evolve_fields:
                if init_name not in changes:
                    changes[init_name] = getattr(self, attr_name)

            return NewValidator(**changes)

        def iter_errors(self, instance, _schema=None):
            if _schema is not None:
                warnings.warn(
                    (
                        "Passing a schema to Validator.iter_errors "
                        "is deprecated and will be removed in a future "
                        "release. Call validator.evolve(schema=new_schema)."
                        "iter_errors(...) instead."
                    ),
                    DeprecationWarning,
                    stacklevel=2,
                )
            else:
                _schema = self.schema

            if _schema is True:
                return
            elif _schema is False:
                yield bsonschema.exceptions.ValidationError(
                    f"False schema does not allow {instance!r}",
                    validator=None,
                    validator_value=None,
                    instance=instance,
                    schema=_schema,
                )
                return

            for k, v in applicable_validators(_schema):
                validator = self.VALIDATORS.get(k)
                if validator is None:
                    continue

                errors = validator(self, v, instance, _schema) or ()
                for error in errors:
                    # set details if not already set by the called fn
                    error._set(
                        validator=k,
                        validator_value=v,
                        instance=instance,
                        schema=_schema,
                        type_checker=self.TYPE_CHECKER,
                    )
                    if k not in {"if", "$ref"}:
                        error.schema_path.appendleft(k)
                    yield error

        def descend(
            self,
            instance,
            schema,
            path=None,
            schema_path=None,
            resolver=None,
        ):
            if schema is True:
                return
            elif schema is False:
                yield bsonschema.exceptions.ValidationError(
                    f"False schema does not allow {instance!r}",
                    validator=None,
                    validator_value=None,
                    instance=instance,
                    schema=schema,
                )
                return

            if self._ref_resolver is not None:
                evolved = self.evolve(schema=schema)
            else:
                if resolver is None:
                    resolver = self._resolver.in_subresource(
                        specification.create_resource(schema),
                    )
                evolved = self.evolve(schema=schema, _resolver=resolver)

            for k, v in applicable_validators(schema):
                validator = evolved.VALIDATORS.get(k)
                if validator is None:
                    continue

                errors = validator(evolved, v, instance, schema) or ()
                for error in errors:
                    # set details if not already set by the called fn
                    error._set(
                        validator=k,
                        validator_value=v,
                        instance=instance,
                        schema=schema,
                        type_checker=evolved.TYPE_CHECKER,
                    )
                    if k not in {"if", "$ref"}:
                        error.schema_path.appendleft(k)
                    if path is not None:
                        error.path.appendleft(path)
                    if schema_path is not None:
                        error.schema_path.appendleft(schema_path)
                    yield error

        def validate(self, *args, **kwargs):
            for error in self.iter_errors(*args, **kwargs):
                raise error

        def is_type(self, instance, type):
            try:
                return self.TYPE_CHECKER.is_type(instance, type)
            except bsonschema.exceptions.UndefinedTypeCheck:
                raise bsonschema.exceptions.UnknownType(type, instance, self.schema)


        def _validate_reference(self, ref, instance):
            if self._ref_resolver is None:
                try:
                    resolved = self._resolver.lookup(ref)
                except referencing.exceptions.Unresolvable as err:
                    raise bsonschema.exceptions._WrappedReferencingError(err)

                return self.descend(
                    instance,
                    resolved.contents,
                    resolver=resolved.resolver,
                )
            else:
                resolve = getattr(self._ref_resolver, "resolve", None)
                if resolve is None:
                    with self._ref_resolver.resolving(ref) as resolved:
                        return self.descend(instance, resolved)
                else:
                    scope, resolved = resolve(ref)
                    self._ref_resolver.push_scope(scope)

                    try:
                        return list(self.descend(instance, resolved))
                    finally:
                        self._ref_resolver.pop_scope()
        
        def is_valid(self, instance, _schema=None):
            if _schema is not None:
                warnings.warn(
                    (
                        "Passing a schema to Validator.is_valid is deprecated "
                        "and will be removed in a future release. Call "
                        "validator.evolve(schema=new_schema).is_valid(...) "
                        "instead."
                    ),
                    DeprecationWarning,
                    stacklevel=2,
                )
                self = self.evolve(schema=_schema)

            error = next(self.iter_errors(instance), None)
            return error is None

    evolve_fields = [
        (field.name, field.alias)
        for field in fields(Validator)
        if field.init
    ]

    return Validator


def extend(
    validator,
    validators=(),
    type_checker=None,
    format_checker=None,
):
    all_validators = dict(validator.VALIDATORS)
    all_validators.update(validators)

    if type_checker is None:
        type_checker = validator.TYPE_CHECKER
    if format_checker is None:
        format_checker = validator.FORMAT_CHECKER
    return create(
        validators=all_validators,
        type_checker=type_checker,
        format_checker=format_checker,
        id_of=validator.ID_OF,
        applicable_validators=validator._APPLICABLE_VALIDATORS,
    )


Validator_ = create(
    validators={
        "$ref": bsonschema._keywords.ref,
        "additionalItems": bsonschema._legacy_keywords.additionalItems,
        "additionalProperties": bsonschema._keywords.additionalProperties,
        "dependencies": bsonschema._legacy_keywords.dependencies_draft3,
        "disallow": bsonschema._legacy_keywords.disallow_draft3,
        "divisibleBy": bsonschema._keywords.multipleOf,
        "enum": bsonschema._keywords.enum,
        "extends": bsonschema._legacy_keywords.extends_draft3,
        "format": bsonschema._keywords.format,
        "items": bsonschema._legacy_keywords.items_draft3_draft4,
        "maxItems": bsonschema._keywords.maxItems,
        "maxLength": bsonschema._keywords.maxLength,
        "maximum": bsonschema._legacy_keywords.maximum_draft3_draft4,
        "minItems": bsonschema._keywords.minItems,
        "minLength": bsonschema._keywords.minLength,
        "minimum": bsonschema._legacy_keywords.minimum_draft3_draft4,
        "pattern": bsonschema._keywords.pattern,
        "patternProperties": bsonschema._keywords.patternProperties,
        "properties": bsonschema._legacy_keywords.properties_draft3,
        "type": bsonschema._legacy_keywords.type_draft3,
        "uniqueItems": bsonschema._keywords.uniqueItems,
    },
    type_checker=bsonschema._types.draft3_type_checker,
    format_checker=bsonschema._format.draft3_format_checker,
    id_of=referencing.jsonschema.DRAFT3.id_of,
    applicable_validators=bsonschema._legacy_keywords.ignore_ref_siblings,
)

_SUBSCHEMAS_KEYWORDS = ("$id", "id", "$anchor", "$dynamicAnchor")

def validate(instance, schema, cls=None, *args, **kwargs):  # noqa: D417
    cls.check_schema(schema)
    validator = cls(schema, *args, **kwargs)
    error = bsonschema.exceptions.best_match(validator.iter_errors(instance))
    if error is not None:
        raise error

