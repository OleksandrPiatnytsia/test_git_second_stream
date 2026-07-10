from pprint import pprint

import requests


def main():

    resp = requests.get(url="https://russianwarship.rip/api/v2/statistics?offset=0&limit=50&date_from=2022-02-24&date_to=2022-03-01")

    pprint(resp.json())


if __name__ == "__main__":
    main()
