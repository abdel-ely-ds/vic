"""
Get Raw data
"""

from dataclasses import replace
from typing import List
import time
from dotenv import dotenv_values
import argparse
from ideas import Idea
import ideas
from login import login
import payload
import thesis
from tqdm import tqdm
from logger_config import get_logger

logger = get_logger(__name__)

creds = dotenv_values(".env")


def build_payload(page_id: int) -> dict:
    page_payload = {k: v for k, v in payload.base.items()}
    page_payload["page"] = str(page_id)
    page_payload["end_page"] = str(page_id)

    return page_payload


def process_page(session, page_id: int) -> List[Idea]:
    page_payload = build_payload(page_id)
    ideas_list = ideas.load(session, page_payload)

    complete_ideas = []
    for idea in tqdm(ideas_list):
        encode_company_name = idea.encode_company_name
        keyid = idea.keyid
        protected_url = (
            f"https://www.valueinvestorsclub.com/idea/{encode_company_name}/{keyid}"
        )
        description = thesis.scrape(session, protected_url)
        complete_ideas.append(
            replace(
                idea,
                add_date=str(idea.add_date),
                market_cap=str(idea.market_cap),
                price=str(idea.price),
                description=description,
            )
        )

        time.sleep(2)

    return complete_ideas


def run(page_id_start: int, page_id_end: int) -> None:
    session = login(creds["username"], creds["password"])

    # logged in
    if session is not None:
        page_id = page_id_start
        while page_id <= page_id_end:
            logger.info(f"Processing page: {page_id}")
            complete_ideas = process_page(session, page_id)
            Idea.save_list_to_file(complete_ideas, f"./data/page_{page_id}")
            page_id += 1
            logger.info(f"Processed page: {page_id}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process pages for ideas.")
    parser.add_argument("page_id_start", type=int, help="Starting page ID.")
    parser.add_argument("page_id_end", type=int, help="Ending page ID.")

    args = parser.parse_args()

    run(args.page_id_start, args.page_id_end)
