import json

from pydantic import BaseModel, create_model
from typing import Type, get_type_hints, Optional, Union

class Validator(object):
    @classmethod
    def generate_schema(cls, model_class: Type[BaseModel], allow_additional: bool = False) -> str:
        # Modify the Config of the model class to handle 'extra' behavior
        class DynamicConfig:
            extra = 'allow' if allow_additional else 'ignore'

        # Create a subclass of the model with the dynamic configuration
        dynamic_model = type('DynamicModel', (model_class,), {'Config': DynamicConfig})

        # Generate the JSON schema and serialize it to a JSON string
        return json.dumps(dynamic_model.schema_json(), indent=2)