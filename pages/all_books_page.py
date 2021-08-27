import re
from typing import List
from bs4 import BeautifulSoup

from locators.books_locators import BooksLocator
from parsers.book_parser import BookParser


class AllBooksPage:
    def __init__(self, page_content) -> None:
        self.soup = BeautifulSoup(page_content, "html.parser")

    @property
    def books(self) -> List[BookParser]:
        return [BookParser(e) for e in self.soup.select(BooksLocator.BOOKS)]

    @property
    def page_count(self) -> int:
        content = self.soup.select_one(BooksLocator.PAGER).string
        pattern = "Page [0-9]+ of ([0-9]+)"
        matcher = re.search(pattern, content)
        pages = int(matcher.group(1))
        return pages
