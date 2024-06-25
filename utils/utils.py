import datetime
import re


def get_month_range(number_of_months: int) -> datetime.datetime:
    """Get the start date of a range of months before the current date.

    Args:
    - number_of_months (int): Number of months.

    Returns:
    - datetime.datetime: Start date of the range.
    """
    today = datetime.datetime.now()
    if number_of_months < 2:
        end_date = today.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    else:
        end_date = today - datetime.timedelta(days=30 * (number_of_months - 1))
        end_date = end_date.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    return end_date


def count_phrases(search_phrase: str, title: str, description: str) -> int:
    """Count the occurrences of a search phrase in the title and description.

    Args:
    - search_phrase (str): Search phrase.
    - title (str): Title string.
    - description (str): Description string.

    Returns:
    - int: Total count of occurrences of the search phrase in the title and description.
    """
    title_count = title.lower().count(search_phrase.lower())
    description_count = description.lower().count(search_phrase.lower())
    return title_count + description_count


def contains_money(title: str, description: str) -> bool:
    """Check if either the title or description contains a monetary value.

    Args:
    - title (str): Title string.
    - description (str): Description string.

    Returns:
    - bool: True if either the title or description contains a monetary value, False otherwise.
    """
    money_pattern = re.compile(
        r"""
        (\$\d{1,3}(,\d{3})*(\.\d{2})?)|  # $11.1 or $111,111.11
        (\d+(\.\d{1,2})?\s*dollars?)|    # dollars
        (\d+(\.\d{1,2})?\s*USD)          # USD
        """,
        re.VERBOSE | re.IGNORECASE,
    )

    return bool(money_pattern.search(title)) or bool(money_pattern.search(description))
