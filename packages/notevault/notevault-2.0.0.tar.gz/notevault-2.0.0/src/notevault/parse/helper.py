import re
from datetime import date, datetime, time, timedelta
from types import GenericAlias
from typing import Any, _GenericAlias

from bs4 import BeautifulSoup, Tag
from dateutil import parser


def get_top_heading_level(soup: BeautifulSoup) -> int:
    """Get the top heading level of the section soup."""
    heading_levels = [int(h.name[1]) for h in soup.find_all(re.compile("^h[1-6]$"))]
    if len(heading_levels) == 0:
        return 0
    else:
        return sorted(heading_levels)[0]


def extract_heading_section_html(value_tag: Tag) -> str:
    """
    Extracts the HTML as string of a section starting with heading and
    includes all subsequent tags until the next heading of same or higher level.

    Tag Object: represents an HTML or XML tag in the original document.
    For example, in an HTML document, <p>, <div>, <a>, and <li> are all tags that can be represented
    as Tag objects in BeautifulSoup.

    Value Tag: Tag object that contains the specific piece of data you're
    trying to extract. For example, if you're parsing an HTML page to extract the text of a paragraph,
    the Tag object representing the <p> tag with that text would be the "value tag."

    Extracting Data: To extract data from a "value tag," you would typically access its .text attribute
    or use methods like .get_text(). These methods aggregate the text of a tag and all its descendants,
    returning it as a single string.
    """
    heading_level = int(value_tag.name[1:])  # Converts 'h2' to 2, 'h3' to 3, etc.

    # Accumulate elements until the next heading of the same or higher level
    section_content = []
    for sibling in value_tag.next_siblings:
        # If sibling is a Tag and a heading of the same or higher level, break the loop
        if (
            isinstance(sibling, Tag)
            and sibling.name.startswith("h")
            and int(sibling.name[1:]) <= heading_level
        ):
            break
        section_content.append(str(sibling))
    # Join all elements to form the HTML of the section
    section_html = "".join(section_content)
    return section_html


def is_single_unnested_list(soup: Tag) -> bool:
    li_elements = soup.find_all("li", recursive=True)
    return len(li_elements) == 1


def _parse_value(value: str, field_type: type) -> Any:
    """Parses a value from a string, converting it to the specified type."""
    if isinstance(field_type, _GenericAlias) or isinstance(field_type, GenericAlias):
        if "list" in str(field_type).lower():
            return [v.strip() for v in value.split(",")]
    elif isinstance(field_type, type):
        if issubclass(field_type, time):
            return datetime.strptime(value, "%H:%M").time()
        elif issubclass(field_type, datetime):
            return parser.parse(value)
        elif issubclass(field_type, date):
            return parser.parse(value).date()
        elif issubclass(field_type, timedelta):
            hours, minutes = map(int, value.split(":"))
            return timedelta(hours=hours, minutes=minutes)
        elif issubclass(field_type, int):
            return int(value)
        else:
            return str(value)
    else:
        raise ValueError(f"Invalid field type: {field_type}")
