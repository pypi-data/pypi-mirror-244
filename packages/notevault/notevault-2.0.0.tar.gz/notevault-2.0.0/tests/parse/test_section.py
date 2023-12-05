import pytest
from bs4 import BeautifulSoup
from pydantic import BaseModel

from notevault.parse.section import ListSpecifierEnum, Section


class MockModel(BaseModel):
    name: str


def test_parse_section_with_heading():
    soup_heading = BeautifulSoup("<h1>Test Heading</h1>", "html.parser")
    section = Section(
        heading="Test Heading",
        model_schema=MockModel,
        is_list=True,
        list_specifier=ListSpecifierEnum.HEADING,
        heading_field="name",
        soup=soup_heading,
    )
    result = section.parse_section()
    assert len(result) == 1
    assert result[0].name == "Test Heading"


def test_parse_section_with_kv_list():
    soup_kv_list = BeautifulSoup("<ul><li>name: Test Value</li></ul>", "html.parser")

    section = Section(
        heading="Test KV List",
        model_schema=MockModel,
        is_list=True,
        list_specifier=ListSpecifierEnum.KV_LIST,
        soup=soup_kv_list,
    )
    result = section.parse_section()

    assert len(result) == 1
    assert (
        result[0].name == "Test Value"
    )  # Validate that 'name' field is correctly parsed


def test_parse_section_with_list():
    # Define the test HTML structure for a simple list
    sample_html_list = "<ul><li>Test Item 1</li><li>Test Item 2</li></ul>"
    soup_list = BeautifulSoup(sample_html_list, "html.parser")

    # Create a Section instance with the appropriate list_specifier
    section = Section(
        heading="Test List",
        model_schema=MockModel,
        is_list=True,
        list_specifier=ListSpecifierEnum.LIST,
        soup=soup_list,
    )

    # Call the parse_section method
    result = section.parse_section()

    # Assertions to validate the parsed data
    assert len(result) == 2  # There are two items in the list
    assert result[0].name == "Test Item 1"  # Validate the first item
    assert result[1].name == "Test Item 2"  # Validate the second item


def test_parse_section_invalid_specifier():
    section = Section(
        heading="Test Heading",
        model_schema=MockModel,
        is_list=True,
        list_specifier="invalid_specifier",
        soup=BeautifulSoup("<p>Test</p>", "html.parser"),
    )
    with pytest.raises(ValueError):
        section.parse_section()


# Additional tests can be written to cover more scenarios, edge cases, and error handling
