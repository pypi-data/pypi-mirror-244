import json

from pydantic import BaseModel, create_model
from typing import Type, get_type_hints, Optional

class Validator(object):
    @classmethod
    def generate_schema(cls, input_class: Type, allow_additional: bool = False) -> str:
        # Retrieve type hints from the input class
        annotations = get_type_hints(input_class)

        # Create a Pydantic model dynamically with proper handling of Optional fields
        fields = {
            name: (annotations[name], None) if annotations[name] == Optional[annotations[name].__args__[0]] else (annotations[name], ...)
            for name in annotations
        }

        dynamic_model = create_model(
            'DynamicModel',
            **fields,
            __config__=type('Config', (), {'extra': 'allow' if allow_additional else 'forbid'})
        )

        # Generate the JSON schema and serialize it to a JSON string
        schema = dynamic_model.model_json_schema()
        return json.dumps(schema, indent=2)