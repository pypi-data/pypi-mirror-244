import importlib
import logging
import os
import re
from datetime import date, datetime, timedelta
from types import ModuleType
from typing import Any, Optional, Union

from bs4 import Tag
from pydantic import BaseModel
from yaml import safe_load

log = logging.getLogger(__name__)


def serialize_datetime(dt: datetime) -> str:
    """Serializes a datetime object to a string for SQLite storage."""
    return dt.isoformat()


def serialize_timedelta(td: timedelta) -> int:
    """Serializes a timedelta object to an integer (total seconds) for SQLite storage."""
    return int(td.total_seconds())


def deserialize_datetime(dt_str: str) -> datetime:
    """Deserializes a datetime string from SQLite storage to a datetime object."""
    return datetime.fromisoformat(dt_str)


def deserialize_timedelta(seconds: Union[int, float]) -> timedelta:
    """Deserializes an integer or float from SQLite storage to a timedelta object."""
    return timedelta(seconds=seconds)


def slugify_header(text: str) -> str:
    return text.replace(" ", "_").replace("#", "h").lower()


def unslugify_header(slug: str, headings: list) -> str:
    """Convert a slugified header back to its original form."""
    # Create a mapping of slugified headings to their original form
    slug_to_heading = {slugify_header(heading): heading for heading in headings}
    return slug_to_heading[slug]


def load_module_by_name(module_name: str) -> Optional[ModuleType]:
    """Load a module by its string name."""
    try:
        module = importlib.import_module(module_name)
        return module
    except ImportError as e:
        print(f"Module {module_name} cannot be imported: {e}")
        raise


def camel_to_snake(name):
    # This regex will look for the end of an acronym or the start of a new word
    # by checking if a capital letter is followed by a lowercase letter.
    name = re.sub(r"([A-Z]+)([A-Z][a-z])", r"\1_\2", name)
    # Then it will handle the case where a lowercase letter is followed by a capital letter
    # which is the normal camel case situation.
    return re.sub(r"([a-z\d])([A-Z])", r"\1_\2", name).lower()


def load_schema(schema_path: str) -> dict[str, Any]:
    with open(schema_path, "r") as f:
        config = safe_load(f)

    # Assuming 'config' is a dictionary with the keys 'database' and 'template'
    db_path = config["Config"]["database"]
    template_path = config["Config"]["template"]

    # Expand environment variables and user home shortcuts
    config["Config"]["database"] = os.path.expanduser(os.path.expandvars(db_path))
    config["Config"]["template"] = os.path.expanduser(os.path.expandvars(template_path))

    return config


def get_last_working_day(date):
    # Check if the date is a Monday (weekday() returns 0 for Monday)
    if date.weekday() == 0:
        # If it's Monday, the last working day was Friday, so subtract 3 days
        return date - timedelta(days=3)
    else:
        # Otherwise, just subtract one day to get the last working day
        return date - timedelta(days=1)


def calc_duration(parsed_obj: list[BaseModel]) -> tuple[timedelta, timedelta]:
    try:
        general = next(
            (obj for obj in parsed_obj if obj.__class__.__name__ == "General"), None
        )
        if general is not None:
            # Assert that general has the expected attributes
            assert (
                hasattr(general, "start")
                and hasattr(general, "end")
                and hasattr(general, "breaks")
            )
            start = datetime.combine(date.today(), general.start)
            end = datetime.combine(date.today(), general.end)
            duration = end - start - general.breaks
        else:
            duration = timedelta()
        meetings = sum(
            [
                obj.duration
                for obj in parsed_obj
                if obj.__class__.__name__ == "Meeting" and hasattr(obj, "duration")
            ]
        )
        dones = sum(
            [
                obj.duration
                for obj in parsed_obj
                if obj.__class__.__name__ == "Done" and hasattr(obj, "duration")
            ]
        )
        total = timedelta(minutes=(meetings + dones) * 30)
    except Exception as e:
        log.error(e)
        return timedelta(), timedelta()
    return duration, total
