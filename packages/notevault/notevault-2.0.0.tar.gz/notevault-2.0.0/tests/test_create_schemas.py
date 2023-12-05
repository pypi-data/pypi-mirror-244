# Mock YAML Specification
from datetime import time, timedelta
from typing import List, Optional, Type

import pytest
from pydantic import BaseModel, ValidationError

from notevault.create_schemas import generate_models_from_yaml


@pytest.fixture
def sample_yaml_spec():
    return {
        "General": {
            "start": {"type": "time", "nullable": True},
            "end": {"type": "time", "nullable": True},
            "breaks": {"type": "timedelta", "nullable": True},
            "timestamp": {"type": "datetime", "nullable": True},
            "date": {"type": "date", "nullable": True},
        },
        "Meeting": {
            "name": {"type": "string"},
            "start": {"type": "time"},
            "duration": {"type": "timedelta", "nullable": True},
            "minutes": {"type": "string", "nullable": True},
            "participants": {"type": "array", "nullable": True},
        },
    }


def test_correct_class_generation(sample_yaml_spec):
    generated_classes = generate_models_from_yaml(sample_yaml_spec)
    assert "General" in generated_classes
    assert "Meeting" in generated_classes


def test_field_type_mapping(sample_yaml_spec):
    generated_classes = generate_models_from_yaml(sample_yaml_spec)
    assert (
        str(generated_classes["General"].model_fields["start"].annotation)
        == "typing.Optional[datetime.time]"
    )
    assert (
        str(generated_classes["Meeting"].model_fields["name"].annotation)
        == "<class 'str'>"
    )


def test_nullable_fields(sample_yaml_spec):
    generated_classes = generate_models_from_yaml(sample_yaml_spec)
    assert generated_classes["General"].model_fields["start"].is_required() is False
    assert generated_classes["Meeting"].model_fields["name"].is_required()


def test_non_nullable_fields(sample_yaml_spec):
    generated_classes = generate_models_from_yaml(sample_yaml_spec)
    with pytest.raises(ValidationError):
        generated_classes["Meeting"](**{"name": None})  # Name is a non-nullable field


def test_model_from_list():
    model_spec = {
        "todos": [
            {"field": {"name": "todo", "nullable": False, "type": "string"}},
            {"field": {"name": "status", "nullable": True, "type": "int"}},
        ]
    }
    generated_classes = generate_models_from_yaml(model_spec)

    class TodoItem(BaseModel):
        todo: str
        status: Optional[int] = None

    assert compare_fields(generated_classes.get("todos"), TodoItem)


def test_model_from_dict():
    model_spec = {
        "Meeting": {
            "name": {"type": "string"},
            "start": {"type": "time"},
            "duration": {"type": "timedelta", "nullable": True},
            "minutes": {"type": "string", "nullable": True},
            "participants": {"type": "array", "nullable": True},
        }
    }
    meeting = generate_models_from_yaml(model_spec).get("Meeting")

    class Meeting(BaseModel):
        name: str
        start: time
        duration: Optional[timedelta] = None
        minutes: Optional[str] = None
        participants: Optional[List[str]] = None

    assert compare_fields(meeting, Meeting)


def compare_fields(model1: Type[BaseModel], model2: Type[BaseModel]):
    if model1.model_fields.keys() != model2.model_fields.keys():
        return False

    for field_name, field in model1.model_fields.items():
        other_field = model2.model_fields[field_name]

        # Compare specific attributes of the fields
        if field.annotation != other_field.annotation:
            return False
        if field.is_required() != other_field.is_required():
            return False

    return True
