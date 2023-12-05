import logging
from typing import Any, Type, _GenericAlias, get_args

import parsy
from bs4 import BeautifulSoup, Tag
from pydantic import BaseModel
from pydantic.fields import FieldInfo

from notevault.parse.helper import _parse_value, extract_heading_section_html
from notevault.parse.props_parser import properties_parser, values_parser

log = logging.getLogger(__name__)


def _parse_props_kv(field_name: str, text: str) -> str | int:
    """Parses a key-value pair from a given text string, returning the value associated with the specified field name.
    Or when input is not valid key-value, returns entire text as value for key "field_name".
    This covers sub-sections of heading list items: entire section is value for key "field_name".
    """
    try:
        parsed = properties_parser.parse(text)
    except parsy.ParseError:
        # text is not key-value pair but entire section data
        parsed = [[field_name, text]]
    data = {key: value for key, value in parsed}
    return data.get(field_name)


def _parse_field_name(
    value_tag: Tag, field_name: str, field_info: FieldInfo
) -> Any | None:
    """extract the key-value pair from the tag which matches the field name"""
    field_type = field_info.annotation

    # Extract the actual type from Optional or other generic types
    if isinstance(field_type, _GenericAlias):
        field_type = get_args(field_type)[0]

    is_required = field_info.is_required()
    log.debug(f"{value_tag=}, {field_name=}, {field_type=}, {is_required=}")

    value = _parse_props_kv(field_name, value_tag.text)

    if value is None or value == "":
        if is_required:
            raise ValueError(f"Required field {field_name} is missing.")
        return None

    parsed_value = _parse_value(value, field_type)
    return parsed_value


def do_parse_kv(item: Tag, schema: Type[BaseModel]) -> BaseModel:
    """Parses BeautifulSoup object based on a specified schema, constructing an instance of the schema model.
    Pre-req: input contains tags with kv pairs
    """
    parsed: dict[str, Any] = {}

    for field_name, field_info in schema.model_fields.items():
        log.debug(f"field_name: {field_name}")

        # find the tag with the field name in the soup and extract inner html of corresponding tag
        field_content = item.find(
            string=lambda text: text and field_name in text.lower()
        )
        if field_content:
            # Get the sibling or parent tag that contains the actual field data
            value_tag = (
                field_content.find_next_sibling()
                if isinstance(field_content, Tag)
                else field_content.parent  # gets enclosing tag if field_content is a NavigableString
            )
            assert value_tag.name is not None

            # If the value is a heading, extract the subsection of the heading
            if value_tag.name and value_tag.name.startswith("h"):  # noqa
                value_tag = BeautifulSoup(
                    extract_heading_section_html(value_tag), "html.parser"
                )
            log.debug(f"{value_tag=}, {value_tag.text=}")
            # extract the key-value pair from the tag which matches the field name
            parsed[field_name] = _parse_field_name(value_tag, field_name, field_info)

    log.debug(f"{parsed=}")
    return schema(**parsed)


def do_parse_list(item: Tag, schema: Type[BaseModel]) -> BaseModel:
    """Parses data from a BeautifulSoup object based on a specified schema, constructing an instance of the schema model."""
    parsed: dict[str, Any] = {}
    stripped_string = item.text.strip("\n")
    values = values_parser.parse(stripped_string)
    fields = schema.model_fields.keys()

    for i, field_name in enumerate(fields):  # order matters!!
        log.debug(f"field_name: {field_name}")

        field_info = schema.model_fields[field_name]
        field_type = field_info.annotation
        # Extract the actual type from Optional or other generic types
        if isinstance(field_type, _GenericAlias):
            field_type = get_args(field_type)[0]
        is_required = field_info.is_required()
        log.debug(f"{field_name=}, {field_type=}, {is_required=}")

        value = values[i] if i < len(values) else None
        if value is None or value == "":
            if is_required:
                raise ValueError(f"Required field {field_name} is missing.")
            continue

        parsed[field_name] = _parse_value(value, field_type)

    log.debug(f"{parsed=}")
    return schema(**parsed)
