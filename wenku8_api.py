__author__ = "yixinBC"

__doc__ = """
Copyright (C) 2021-  yixinBC
the api for https://www.wenku8.net
"""

import requests
from requests.cookies import RequestsCookieJar
from lxml import etree
from bs4 import BeautifulSoup

FAKE_HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:108.0) Gecko/20100101 Firefox/108.0"}


def _login(username: str, password: str, usecookie: int) -> RequestsCookieJar:
    """
    post to https://www.wenku8.net/login.php ,and get the cookie
    otherwise many api can't use.
    :param: username
    :param: password
    :param: usecookie : its value should be selected in(0, 86400, 2592000, 315360000)
            which corresponds:the returned cookie can save your information for:
            ("this browser process", "one day", "one month", "one year")
    :return: None
    """
    form_data = {
        "username": username,
        "password": password,
        "usecookie": usecookie,
        "action": "login"  # hidden field
    }
    return requests.post("https://www.wenku8.net/login.php",
                         form_data, headers=FAKE_HEADERS).cookies


class Wenku8api:
    """
    wenku8 main class
    """

    class User:
        """
        user class
        """

        def __init__(self, user_id: str, name: str, level: str, honor: str, points: int, avatar_url: str) -> None:
            self.id = user_id
            self.name = name
            self.level = level
            self.honor = honor
            self.points = points
            self.avatar_url = avatar_url

    class Author:
        """
        author class
        """

        def __init__(self, name: str) -> None:
            self.name = name

        @property
        def books(self) -> list:
            """
            get the books of this author
            :return: a list of books
            """
            # TODO: get the books of this author
            pass

    class Book:
        """
        book class
        """

        def __init__(self, book_id: str, user_cookies: RequestsCookieJar) -> None:
            self.book_id = book_id
            self.book_url = f"https://www.wenku8.net/book/{book_id}.htm"
            self.user_cookies = user_cookies
            self.meta_info = BeautifulSoup(
                requests.get(self.book_url, cookies=self.user_cookies, headers=FAKE_HEADERS).content, "lxml")
            self.name = self.meta_info.select("#content > div:nth-child(1) > table:nth-child(1) > tr:nth-child(1) > "
                                              "td:nth-child(1) > table:nth-child(1) > tr:nth-child(1) > td:nth-child("
                                              "1) > span:nth-child(1) > b:nth-child(1)")[0].text
            self.cover_url = self.meta_info.select("#content > div:nth-child(1) > table:nth-child(4) > "
                                                   "tr:nth-child(1) > td:nth-child(1) > img:nth-child(1)")[0]["src"]
            self.author = Wenku8api.Author(
                self.meta_info.select("#content > div:nth-child(1) > table:nth-child(1) > tr:nth-child(2) > "
                                      "td:nth-child(2)")[0].text[5:])

    def __init__(self, username: str, password: str, usecookie: int):
        self.cookies = _login(username, password, usecookie)

    def get_user(self) -> User:
        """
        get user info
        :return: User
        """
        user_info = BeautifulSoup(requests.get("https://www.wenku8.net/userdetail.php",
                                               cookies=self.cookies, headers=FAKE_HEADERS).content, "lxml")
        return self.User(
            user_id=user_info.select("html body div.main div#centerm div#content table.grid tr td.even")[0].text,
            name=user_info.select("html body div.main div#centerm div#content table.grid tr td.even")[3].text,
            level=user_info.select("html body div.main div#centerm div#content table.grid tr td.even")[5].text,
            honor=user_info.select("html body div.main div#centerm div#content table.grid tr td.even")[6].text,
            points=int(user_info.select("html body div.main div#centerm div#content table.grid tr td.even")[15].text),
            avatar_url=user_info.select(".avatar")[0]["src"]
        )

    def get_book(self, book_id) -> Book:
        return self.Book(book_id=book_id, user_cookies=self.cookies)
