from bs4 import BeautifulSoup
from logger_config import get_logger

logger = get_logger(__name__)


def scrape(session, protected_url):
    protected_page = session.get(protected_url)
    soup = BeautifulSoup(protected_page.text, "html.parser")
    return soup.get_text(separator="\n", strip=True)


def clean(thesis: str) -> str:
    idx1 = thesis.index("Description\n")
    try:
        idx2 = thesis.index("All\n")
    except ValueError:
        idx2 = len(thesis) + 1

    clean_text = thesis[idx1:idx2]
    clean_text = clean_text.replace("<p>", "")
    clean_text = clean_text.replace("</p>", "")

    if clean_text[-5:] == "show\n":
        clean_text = clean_text[:-5]

    try:
        idx3 = clean_text.index("<ul>")
    except ValueError:
        idx3 = len(thesis) + 1

    clean_text = clean_text[:idx3]

    return clean_text
