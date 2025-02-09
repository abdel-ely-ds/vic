from dataclasses import dataclass
from datetime import datetime
from typing import Optional


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
