from pprint import pprint

import requests


def main():

    print("Latest fucking rassia looses:")

    url = "http://russianwarship.rip/api/v2/statistics/latest"

    resp = requests.get(url=url)

    pprint(resp.json())


if __name__ == "__main__":
    main()
