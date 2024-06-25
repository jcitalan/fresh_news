from typing import Any, Dict


class Payload:
    def __init__(self, search_phrase: str, topic: str, months: int) -> None:
        if not isinstance(search_phrase, str):
            raise TypeError("search_phrase must be a string")
        if not isinstance(topic, str):
            raise TypeError("topic must be a string")
        if not isinstance(months, int):
            raise TypeError("months must be a string")

        self.search_phrase = search_phrase
        self.topic = topic
        self.months = months

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Payload":
        return cls(
            search_phrase=data["search_phrase"],
            topic=data["topic"],
            months=data["months"],
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "search_phrase": self.search_phrase,
            "topic": self.topic,
            "months": self.months,
        }
