import re
from functools import partial

import genson

Builder = genson.SchemaBuilder


def create_schema(**kwargs):
    return Builder(**kwargs)


class SchemaNode:
    SCHEMA_ATTRIBUTES = (
        "$schema",
        "type",
        "title",
        "required",
        "properties",
        "patternProperties",
        "items",
    )
    SCHEMA_REQUIRED_ATTRIBUTES = (
        "$schema",
        "type",
        "title",
        "required",
        "properties",
    )
    OTHER_ATTRIBUTES = ("patternProperties", "items")

    def __init__(self, **kwargs):
        self._attributes = {}
        self.set_attributes(**kwargs)
        self._register()

    def _set_attr(self, key, value):
        self.set_attributes(**{key: value})

    def _register(self):
        def set_field(key, value):
            self.set_attributes(**{key: value})

        for attr in self.SCHEMA_ATTRIBUTES:
            name = re.sub(r"^[\s,$]+", "", attr)
            name = re.sub(r"[\s,$]+$", "", name)
            self.__dict__.update({f"set_{name}": partial(set_field, name)})

    def validate_attributes(self, **kwargs):
        # required_attrs = set(self.SCHEMA_REQUIRED_ATTRIBUTES) - set(kwargs.keys())
        # if required_attrs:
        #     raise AttributeError(f"Attribute(s) {required_attrs} is(are) required")
        pass

    def set_attributes(self, **kwargs):
        self.validate_attributes(**kwargs)
        for key, value in kwargs.items():
            if key in self.OTHER_ATTRIBUTES and value:
                self._attributes[key] = value
            if key in self.SCHEMA_ATTRIBUTES:
                self._attributes[key] = value

    def to_node(self):
        return self._attributes

    # TODO value validation
