import requests
from bs4 import BeautifulSoup


def login(username, password):

    session = requests.Session()
    login_url = "https://www.valueinvestorsclub.com/login"

    response = session.get(login_url)
    soup = BeautifulSoup(response.text, "html.parser")

    csrf_token = soup.find("input", {"name": "_token"})["value"]
    payload = {
        "_token": csrf_token,
        "login[login_name]": username,
        "login[password]": password,
        "login[remember_me]": "on",
        "commit": "Login",
    }
    return session.post(login_url, data=payload)
