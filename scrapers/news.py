import re
from dataclasses import dataclass


@dataclass
class News:
    """
    Data class to represent a news item.

    :param search_phrase: The phrase used for searching news.
    :param title: The title of the news.
    :param date: The date of the news.
    :param image_src: The source URL of the news image.
    :param description: The description of the news (optional).
    :param image_file_name: The local file name of the downloaded image (optional).
    """

    search_phrase: str
    title: str
    date: str
    image_src: str
    description: str = ""
    image_file_name: str = ""

    @property
    def search_phrase_count(self) -> int:
        """
        Count the occurrences of the search phrase in the title and description.

        :return: Total count of search phrase occurrences in title and description.
        """
        count_in_title = self.title.lower().count(self.search_phrase.lower())
        count_in_description = self.description.lower().count(
            self.search_phrase.lower()
        )
        return count_in_title + count_in_description

    @property
    def contains_monetary_value(self) -> bool:
        """
        Check if the title or description contains any monetary value.

        :return: True if monetary value is found, otherwise False.
        """
        monetary_patterns = [
            r"\$\d+(\.\d{1,2})?",
            r"\$\d{1,3}(,\d{3})*(\.\d{1,2})?",
            r"\d+\s(dollars|USD)",
        ]
        pattern = "|".join(monetary_patterns)

        if re.search(pattern, self.title) or re.search(pattern, self.description):
            return True
        return False
