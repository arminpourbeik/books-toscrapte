import re
import logging
from typing import List
from bs4 import BeautifulSoup

from locators.books_locators import BooksLocator
from parsers.book_parser import BookParser

# Child logger of `scrapping` logger
logger = logging.getLogger("scraping.all_books_page")


class AllBooksPage:
    def __init__(self, page_content) -> None:
        logger.debug("Parsing page content with BeautifulSoup HTML parser.")
        self.soup = BeautifulSoup(page_content, "html.parser")

    @property
    def books(self) -> List[BookParser]:
        logging.debug(f"Finding all books in the page.")
        return [BookParser(e) for e in self.soup.select(BooksLocator.BOOKS)]

    @property
    def page_count(self) -> int:
        logger.debug("Finding all number of pages available.")
        content = self.soup.select_one(BooksLocator.PAGER).string
        logger.info(f"Found the number of pages available. `{content}`.")
        pattern = "Page [0-9]+ of ([0-9]+)"
        matcher = re.search(pattern, content)
        pages = int(matcher.group(1))
        return pages
