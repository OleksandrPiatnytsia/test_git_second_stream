from pprint import pprint
import datetime

import requests


def main():

    print(f"Latest russia looses on date {datetime.date.today()}:")

    url = "https://russianwarshdip.rip/api/v2/statistics/latest"

    resp = requests.get(url=url)

    print(f"response status_code{resp.status_code}")
    pprint(resp.json().get("data"))

if __name__ == "__main__":
    main()
