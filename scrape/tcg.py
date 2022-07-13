import requests, posixpath, json

API_URL = "https://mpapi.tcgplayer.com/v2/"
SEARCH_API_URL = posixpath.join(API_URL, "search/request")

class CardSearchResult:
    """
    Contains information about a card from a TCGPlayer search result.
    """

    def __init__(self, result: dict) -> None:
        self.name = result["productUrlName"]
        self.marketPrice = result.get("marketPrice", None)
        self.setName = result["setName"]

    def __str__(self) -> str:
        return f"{self.name} ({self.setName}) - {self.price_str()}"

    def __repr__(self) -> str:
        return self.__str__()

    def price_str(self) -> str:
        price = self.marketPrice
        return "No Price" if price is None else f"${price}"


def search(name: str, size: int = 24) -> list[CardSearchResult]:
    """Searches for a card from TCGPlayer and returns the results.

    Args:
        name (str): Name of the card to search for
        size (int, optional): Number of cards to retrieve. Defaults to 24.

    Raises:
        Exception: When the request fails.

    Returns:
        list[CardSearchResult]: All parsed card search results.
    """

    params = {
        "q": name,
        "isList": False
    }

    headers = {
        "Content-Type": "application/json",
    }

    payload = {
        "algorithm": "",
        "context": {
            "cart": {},
            "shippingCountry": "US",
        },
        "filters": {
            "match": {},
            "range": {},
            "term": {
                "productLineName": [
                    "magic"
                ]
            }
        },
        "from": 0,
        "listingSearch": {
            "context": {
                "cart": {}
            },
            "filters": {
                "term": {},
                "range": {
                    "quantity": {
                        "gte": 1
                    }
                },
                "exclude": {
                    "channelExclusion": 0
                }
            }
        },
        "size": size,
        "sort": {}
    }

    payload_json = json.dumps(payload)

    r = requests.post(SEARCH_API_URL, headers=headers, params=params, data=payload_json)

    if r.status_code == 200:
        j = r.json()
        cards = []
        for result in j["results"][0]["results"]:
            cards.append(CardSearchResult(result))

        return cards

    raise Exception(f"Failed to fetch card data ({r.status_code}): {r.text}")