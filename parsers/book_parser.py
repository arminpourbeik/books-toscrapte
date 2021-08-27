import re
import logging

from locators.book_locator import BookLocators


logger = logging.getLogger("scraping.book_parser")


class BookParser:
    """
    Given one of the specific book divs, find out the data about
    the book (name, link, price, rating).
    """

    RATINGS = {
        "One": 1,
        "Two": 2,
        "Three": 3,
        "Four": 4,
        "Five": 5,
    }

    def __init__(self, parent) -> None:
        logger.debug(f"New book parser created from `{parent}`.")
        self.parent = parent

    @property
    def name(self):
        locator = BookLocators.NAME_LOCATOR
        return self.parent.select_one(locator).string

    @property
    def link(self):
        locator = BookLocators.LINK_LOCATOR
        return self.parent.select_one(locator).string

    @property
    def price(self):
        locator = BookLocators.PRICE_LOCATOR
        item_price = self.parent.select_one(locator).string

        pattern = "£([0-9]+\.[0-9]+)"
        matcher = re.search(pattern, item_price)
        return float(matcher.group(1))

    @property
    def rating(self) -> str:
        locator = BookLocators.RATING_LOCATOR
        star_rating = self.parent.select_one(locator)
        classes = star_rating.attrs["class"]
        rating_classes = [c for c in classes if c != "star-rating"]
        return BookParser.RATINGS.get(rating_classes[0])

    def __repr__(self) -> str:
        return f"<Book {self.name}, £{self.price}, rating {self.rating}>"
