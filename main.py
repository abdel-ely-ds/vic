from dotenv import dotenv_values

from login import login

creds = dotenv_values(".env")


def main(page_id_start: int, page_id_end: int) -> None:
    session = login(creds["username"], creds["password"])

    # logged in
    if session is not None:
        return session


if __name__ == "__main__":
    main()
