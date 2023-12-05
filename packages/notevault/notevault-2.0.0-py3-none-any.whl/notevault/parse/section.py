from dataclasses import dataclass, field
from enum import Enum
from typing import List, Type, Union

from bs4 import BeautifulSoup
from pydantic import BaseModel, ValidationError

from notevault.parse.do_parse import do_parse_kv, do_parse_list
from notevault.parse.helper import extract_heading_section_html, get_top_heading_level


class ListSpecifierEnum(str, Enum):
    HEADING = "heading"
    KV_LIST = "kv_list"
    LIST = "list"


@dataclass
class Section:
    heading: str
    model_schema: Type[BaseModel]
    is_list: bool = False
    list_specifier: Union[str, None] = None
    heading_field: Union[str, None] = None
    is_kv_list: bool = False
    soup: Union[BeautifulSoup, None] = None
    parsed_models: List[BaseModel] = field(default_factory=list)

    def parse_section(self) -> List[BaseModel]:
        """
        Parses a section of HTML soup into a Pydantic model, adding it to a list of parsed models.
        """
        try:
            if self.is_list:
                if self.list_specifier == ListSpecifierEnum.HEADING:
                    sub_heading_level = f"h{get_top_heading_level(self.soup)}"  # h2
                    list_items = self.soup.find_all(sub_heading_level)
                    for list_item in list_items:
                        self.soup = BeautifulSoup(
                            extract_heading_section_html(list_item), "html.parser"
                        )
                        # workaround: inject heading_field as <p> into the heading for parsing as field
                        list_item.string = f"{self.heading_field}: {list_item.string}"
                        list_item.name = "p"
                        list_item = BeautifulSoup(
                            str(list_item) + str(self.soup), "html.parser"
                        )
                        model_instance = do_parse_kv(list_item, self.model_schema)
                        self.parsed_models.append(model_instance)

                elif self.list_specifier == ListSpecifierEnum.KV_LIST:
                    list_items = self.soup.find_all("li")  # TODO: add numbered lists
                    for list_item in list_items:
                        model_instance = do_parse_kv(list_item, self.model_schema)
                        self.parsed_models.append(model_instance)

                elif self.list_specifier == ListSpecifierEnum.LIST:
                    list_items = self.soup.find_all("li")  # TODO: add numbered lists
                    for list_item in list_items:
                        model_instance = do_parse_list(list_item, self.model_schema)
                        self.parsed_models.append(model_instance)

                else:
                    raise ValueError(f"Invalid list_specifier: {self.list_specifier}")

            else:
                model_instance = do_parse_kv(self.soup, self.model_schema)
                self.parsed_models.append(model_instance)

        except ValidationError as e:
            new_exception = RuntimeError(
                f"Data validation error for section {self.model_schema.__class__.__name__}"
            )
            raise new_exception from e

        return self.parsed_models
