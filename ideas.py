from typing import Dict, Optional, List
import json
from dataclasses import dataclass, asdict
from datetime import datetime
import pandas as pd


@dataclass
class Idea:
    add_date: datetime
    alt_display_type: Optional[str]
    by_user: str
    company_name: str
    deleted_by_user_id: Optional[int]
    description: str
    display_name: str
    encode_company_name: str
    format_date: str
    id: int
    idea_status: int
    is_long: int
    is_weekly_winner: int
    keyid: str
    market_cap: float
    num_new_msgs: int
    price: float
    rating: str
    rating_num_user_votes: int
    symbol: str
    total_return: Optional[float]
    user_id: int
    user_status: int

    def __post_init__(self):
        self.add_date = datetime.strptime(self.add_date, "%Y-%m-%d %H:%M:%S")
        self.market_cap = float(self.market_cap.replace(",", ""))
        self.price = float(self.price)

    @staticmethod
    def save_list_to_file(ideas, filename):
        data_to_save = []
        for idea in ideas:
            idea_dict = idea.__dict__
            idea_dict["price"] = str(idea_dict["price"])
            idea_dict["market_cap"] = str(idea_dict["market_cap"])
            idea_dict["add_date"] = str(idea_dict["add_date"])
            data_to_save.append(idea_dict)

        with open(filename, "w") as file:
            json.dump(data_to_save, file, default=str)

    @staticmethod
    def load_list_from_file(filename: str) -> List["Idea"]:
        with open(filename, "r") as file:
            data = json.load(file)

        return [Idea(**d) for d in data]

    @classmethod
    def to_dataframe(cls, ideas: List["Idea"]) -> pd.DataFrame:
        idea_dicts = [asdict(idea) for idea in ideas]
        return pd.DataFrame(idea_dicts)


def parse_ideas(data: Dict[str, List[Dict]]) -> List[Idea]:
    ideas = []
    for date, ideas_list in data.items():
        for idea_data in ideas_list:
            ideas.append(Idea(**idea_data))
    return ideas


def load(session, payload) -> List[Idea]:
    ideas_url = "https://www.valueinvestorsclub.com/ideas/loadideas"
    ideas_response = session.post(ideas_url, data=payload)
    results = ideas_response.json()["result"]
    return parse_ideas(results)
