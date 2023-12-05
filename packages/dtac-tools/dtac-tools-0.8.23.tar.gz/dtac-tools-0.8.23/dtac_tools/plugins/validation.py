import json

from pydantic import BaseModel, create_model
from typing import Type, get_type_hints, Optional, Union

class Validator(object):
    @classmethod
    def generate_schema(cls, input_class: Type, allow_additional: bool = False) -> str:
        # Retrieve type hints from the input class
        annotations = get_type_hints(input_class)

        fields = {
            name: (cls._extract_type(annotations[name]), cls._extract_default(annotations[name]))
            for name in annotations
        }

        dynamic_model = create_model(
            'DynamicModel',
            **fields,
            __config__=type('Config', (), {'extra': 'allow' if allow_additional else 'forbid', 'arbitrary_types_allowed': True})
        )

        return json.dumps(dynamic_model.schema_json(), indent=2)

    @staticmethod
    def _extract_type(annotation):
        # Extract the actual type from Optional
        if getattr(annotation, '__origin__', None) is Union:
            non_none_args = [arg for arg in annotation.__args__ if arg is not type(None)]
            if len(non_none_args) == 1:
                return non_none_args[0]
        return annotation

    @staticmethod
    def _extract_default(annotation):
        # Return None as default for Optional types
        if getattr(annotation, '__origin__', None) is Union and type(None) in annotation.__args__:
            return None
        return ...