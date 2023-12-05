import json

from pydantic import BaseModel, create_model
from typing import Type, get_type_hints, Optional, Union

class Validator(object):
    @classmethod
    def generate_schema(cls, input_class: Type, allow_additional: bool = False) -> str:
        # Retrieve type hints from the input class
        annotations = get_type_hints(input_class)

        fields = {
            name: (cls._extract_type(annotations[name]), ...)
            for name in annotations
        }

        dynamic_model = create_model(
            'DynamicModel',
            **fields,
            __config__=type('Config', (), {'extra': 'allow' if allow_additional else 'forbid'})
        )

        return json.dumps(dynamic_model.schema_json(), indent=2)

    @staticmethod
    def _extract_type(annotation):
        # Check if the annotation is Optional
        if getattr(annotation, '__origin__', None) is Union:
            optional_types = [arg for arg in annotation.__args__ if arg is not type(None)]
            if len(optional_types) == 1:
                return (optional_types[0], None)
        return (annotation, ...)