from bs4 import BeautifulSoup


def scrape(session, protected_url):
    protected_page = session.get(protected_url)

    soup = BeautifulSoup(protected_page.text, "html.parser")

    full_html = str(soup)

    cutoff_point = full_html.find('<div class="tab-pane " id="messages">')
    if cutoff_point != -1:
        truncated_html = full_html[:cutoff_point]
        soup = BeautifulSoup(truncated_html, "html.parser")

    text_content = soup.get_text(separator="\n", strip=True)

    return text_content


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
