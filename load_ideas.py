from typing import Dict, List
from idea import Idea


def parse_ideas(data: Dict[str, List[Dict]]) -> List[Idea]:
    ideas = []
    for date, ideas_list in data.items():
        for idea_data in ideas_list:
            ideas.append(Idea(**idea_data))
    return ideas


def load_ideas(session, payload) -> List[Idea]:
    ideas_url = "https://www.valueinvestorsclub.com/ideas/loadideas"
    ideas_response = session.post(ideas_url, data=payload)
    results = ideas_response.json()["result"]
    return parse_ideas(results)
