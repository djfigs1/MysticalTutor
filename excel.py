from scrape.tcg import search
import sys

card_names = sys.argv[1].split(";")
for name in card_names:
    # check for empty string
    if len(name) > 0:
        try:
            cards = search(name)
            if len(cards) > 0:
                line = cards[0].price_str()
            else:
                line = "No Results"
        except Exception as e:
            line = "Err: " + str(e)

        print(line)