from typing import Dict, List, Type

from bs4 import BeautifulSoup
from markdown import markdown
from pydantic import BaseModel

from notevault.parse.helper import extract_heading_section_html
from notevault.parse.section import Section


class MarkdownParser:
    def __init__(self, doc_schema: Dict, generated_schemas: Dict[str, Type[BaseModel]]):
        self.doc_schema = doc_schema
        self.generated_schemas = generated_schemas
        self.parsed_models: list[BaseModel] = []
        self.sections: list[Section] = []

    def parse_markdown(
        self,
        md_text: str,
    ) -> List[BaseModel]:
        """Parses markdown into a list of Pydantic model instances based on the provided document structure and schemas.
        Note:
            The function skips sections where the heading is not found or the model schema is not defined in the generated_schemas.
        """
        soup = BeautifulSoup(markdown(md_text), "html.parser")

        # Loop over every section
        for section_info in self.doc_schema["DocumentStructure"]["Sections"]:
            section_info = section_info["section"]
            heading = section_info["heading"]
            class_name = section_info["type"]
            model = self.doc_schema["Model"][class_name]

            # Find the heading in the markdown
            heading_level = f"h{heading.count('#')}"  # h1
            section_heading = soup.find(
                heading_level, string=heading.strip("# ").strip()
            )

            if section_heading is None:
                print(f"Skipping section {class_name} because no heading was found.")
                continue

            # Get section soup: HTML of the section defined by the heading level
            section_soup = BeautifulSoup(
                extract_heading_section_html(section_heading), "html.parser"
            )

            model_schema = self.generated_schemas.get(class_name)
            if not model_schema:
                print(f"Skipping section {class_name} because no model was found.")
                continue

            section = Section(
                heading=heading,
                model_schema=model_schema,
                is_list=section_info.get("is_list", False),
                list_specifier=section_info.get("list_specifier"),
                heading_field=section_info.get("heading_field"),
                is_kv_list=isinstance(model, dict),
                soup=section_soup,
            )

            parsed_section = section.parse_section()
            self.parsed_models.extend(parsed_section)

        return self.parsed_models
