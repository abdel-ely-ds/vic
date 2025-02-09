from dataclasses import replace
from typing import List
import time
from dotenv import dotenv_values

from idea import Idea
import ideas
from login import login
import payload
import thesis

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
    for idea in ideas_list:
        encode_company_name = idea["encode_company_name"]
        keyid = idea["keyid"]
        protected_url = (
            f"https://www.valueinvestorsclub.com/idea/{encode_company_name}/{keyid}"
        )
        description = thesis.scrape(session, protected_url)
        complete_ideas.append(replace(idea, description=description))

        time.sleep(5)

    return complete_ideas


def main(page_id_start: int, page_id_end: int) -> None:
    session = login(creds["username"], creds["password"])

    # logged in
    if session is not None:
        page_id = page_id_start
        while page_id <= page_id_end:
            print(f"Processing page: {page_id}")
            complete_ideas = process_page(session, page_id)
            Idea.save_list_to_file(complete_ideas, f"./data/page_{page_id}")
            page_id += 1


if __name__ == "__main__":
    main()
