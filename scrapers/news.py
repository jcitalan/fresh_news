import re
from dataclasses import dataclass


@dataclass
class News:
    search_phrase: str
    title: str
    date: str
    image_src: str
    description: str = ""
    image_file_name: str = ""

    @property
    def search_phrase_count(self) -> int:
        count_in_title = self.title.lower().count(self.search_phrase.lower())
        count_in_description = self.description.lower().count(
            self.search_phrase.lower()
        )

        return count_in_title + count_in_description

    @property
    def contains_monetary_value(self) -> bool:
        monetary_patterns = [
            r"\$\d+(\.\d{1,2})?",
            r"\$\d{1,3}(,\d{3})*(\.\d{1,2})?",
            r"\d+\s(dollars|USD)",
        ]
        pattern = "|".join(monetary_patterns)

        if re.search(pattern, self.title) or re.search(pattern, self.description):
            return True

        return False
