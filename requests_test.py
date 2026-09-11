from pprint import pprint
import datetime

import requests


def main():

    print(f"Latest rassia looses on date {datetime.date.today()}:")

    url = "https://russianwarship.rip/api/v2/statistics/latest"

    resp = requests.get(url=url)
    print(f"response status_code{resp.status_code}")
    pprint(f"unit losses: {resp.json().get("data").get("increase")}")

    print("end")

if __name__ == "__main__":
    main()
