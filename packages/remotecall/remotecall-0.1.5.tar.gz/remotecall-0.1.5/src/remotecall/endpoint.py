from __future__ import annotations

import logging
import typing
from inspect import signature, Signature, getdoc, cleandoc, Parameter
from types import MappingProxyType

logger = logging.getLogger(__name__)


class EndpointNotFound(Exception):
    """Raised if endpoint is not found by name."""


class Endpoint:
    def __init__(self, name: str, handler: typing.Callable):
        self.name = name
        self.handler = handler
        self.signature = signature(self.handler)
        self.enabled = True
        self.check_annotations()

    def __str__(self) -> str:
        return f"Endpoint('{self.name}')"

    def __call__(self, *args, **kwargs):
        return self.handler(*args, **kwargs)

    @property
    def doc(self) -> str:
        doc = getdoc(self.handler)
        return cleandoc(doc) if doc else ""

    @property
    def parameters(self) -> MappingProxyType[str, Parameter]:
        return self.signature.parameters

    def get_parameter(self, name: str) -> Parameter:
        return self.parameters[name]

    def check_annotations(self):
        for parameter in self.parameters.values():
            if parameter.annotation is Signature.empty:
                logger.warning(
                    "%s() takes '%s' as an argument but is missing type annotation. "
                    "Server considers the argument as 'str' unless client call provides "
                    "the missing type annotation.",
                    self.name,
                    parameter.name,
                )

    def to_dict(self) -> dict:
        logger.debug("Converting '%s' parameters to dict.", self)

        parameters = [self._parameter_to_dict(p) for p in self.parameters.values()]
        definition = {"name": self.name, "documentation": self.doc, "parameters": parameters}

        if self.signature.return_annotation is not Signature.empty:
            return_annotation = annotation_to_str(self.signature.return_annotation)
        else:
            return_annotation = ""

        definition["return_annotation"] = return_annotation

        return definition

    @classmethod
    def _parameter_to_dict(cls, parameter):
        logger.debug("Converting '%s' parameter to dict.", parameter)

        definition = {
            "name": get_name(parameter),
            "annotation": get_annotation(parameter),
        }

        if parameter.default is not Parameter.empty:
            definition["default"] = get_default(parameter)

        return definition


def is_optional(parameter: Parameter) -> bool:
    """Is parameter optional.

    Returns True if a parameter is optional.

    For example,

        def sample(a: Optional[int] = 1):
            pass
    """
    origin = typing.get_origin(parameter.annotation)
    return origin is typing.Union and type(None) in typing.get_args(parameter.annotation)


def get_name(parameter: Parameter) -> str:
    return parameter.name


def get_annotation(parameter: Parameter) -> str:
    annotation = parameter.annotation

    if annotation is Parameter.empty:
        return type(parameter.default).__name__ if parameter.default else ""

    if is_optional(parameter):
        return str(annotation)

    return annotation_to_str(annotation)


def annotation_to_str(annotation) -> str:
    if isinstance(annotation, str):
        return annotation
    return annotation.__name__


def get_default(parameter: Parameter) -> str:
    return repr(parameter.default)