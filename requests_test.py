from pprint import pprint

import requests


def main():

    print("Latest rassia looses:")

    url = "https://russianwarship.rip/api/v2/statistics/latest"

    resp = requests.get(url=url)
    print(f"response status_code{resp.status_code}")
    pprint(resp.json().get("data").get("increase"))


if __name__ == "__main__":
    main()