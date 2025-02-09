def load_ideas(session, payload):
    ideas_url = "https://www.valueinvestorsclub.com/ideas/loadideas"
    ideas_response = session.post(ideas_url, data=payload)
    return ideas_response.json()["result"]
