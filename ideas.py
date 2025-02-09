from typing import Dict, Optional, List
import json
from dataclasses import dataclass
from datetime import datetime


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
    def save_list_to_file(ideas: List["Idea"], filename: str):
        with open(filename, "w") as file:
            json.dump([idea.__dict__ for idea in ideas], file, default=str)

    @staticmethod
    def load_list_from_file(filename: str) -> List["Idea"]:
        with open(filename, "r") as file:
            data = json.load(file)

            # to be fixed
            return [
                Idea(
                    **{
                        **idea,
                        "add_date": datetime.strptime(
                            idea["add_date"], "%Y-%m-%d %H:%M:%S"
                        ),
                    }
                )
                for idea in data
            ]


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
