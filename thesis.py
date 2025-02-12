from bs4 import BeautifulSoup
from logger_config import get_logger

logger = get_logger(__name__)


def scrape(session, protected_url):
    protected_page = session.get(protected_url)
    soup = BeautifulSoup(protected_page.text, "html.parser")

    target_div = soup.find("div", id="description")

    if target_div:
        logger.info(f"scrapped successfully the idea: {protected_url}")
        return target_div.get_text(separator="\n", strip=True)
    else:
        logger.info(f"Couldn't find the thesis of the idea: {protected_url}")
        return ""


def clean(thesis: str) -> str:
    # Trimming unnecessary text
    idx = thesis.index("Apply")
    s = len("Apply")
    ret = thesis[idx + s :]
    idx = ret.index("""show\nAll""")
    ret = ret[:idx]

    unwanted_text = [
        "Submit an idea for full membership consideration",
        "and get access to the latest member ideas.",
        "Related Ideas?",
        "Description / Catalyst",
        "Messages",
    ]
    for ut in unwanted_text:
        ret = ret.replace(ut, "")

    idx = ret.index("Description")
    ret = ret[idx:]
    return ret
