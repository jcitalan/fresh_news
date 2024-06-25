from pathlib import Path
from typing import List

from RPA.Excel.Files import Files

from .log import log_decorator
from .news import News


class ParserNews:
    @log_decorator
    def _generate_excel_file(self, data: List[News]):
        """
        Generate an Excel file with the provided news data.

        :param data: List of News objects containing news information.
        """
        header = [
            "title",
            "date",
            "description",
            "picture filename",
            "search phrase count",
            "contains monetary value",
        ]

        excel_data = [header]

        for news in data:
            excel_data.append(
                [
                    news.title,
                    news.date.strftime("%Y-%m-%d"),
                    news.description,
                    news.image_file_name,
                    news.search_phrase_count,
                    str(news.contains_monetary_value),
                ]
            )

        lib = Files()
        output_path = Path("./output/news_data.xlsx")
        output_path.parent.mkdir(parents=True, exist_ok=True)
        lib.create_workbook(str(output_path), fmt="xlsx", sheet_name="News Data")
        lib.append_rows_to_worksheet(excel_data, name="News Data")
        lib.save_workbook()
        self.log.info(f"Excel file created at {output_path}")

    @log_decorator
    def parse(self, data: List[News]):
        """
        Parse the news data and generate an Excel file.

        :param data: List of News objects containing news information.
        """
        self._generate_excel_file(data)
