__author__ = "yixinBC"

__doc__ = """
Copyright (C) 2021-  yixinBC
the api for https://www.wenku8.net
"""

import requests
from requests.cookies import RequestsCookieJar
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
    :return: CookieJar
    """
    form_data = {
        "username": username,
        "password": password,
        "usecookie": usecookie,
        "action": "login"  # hidden field
    }
    return requests.post("https://www.wenku8.net/login.php",
                         form_data, headers=FAKE_HEADERS).cookies


def get_cookies(username: str, password: str, usecookie: int) -> RequestsCookieJar:
    """
    get the cookie
    :param: username
    :param: password
    :param: usecookie : its value should be selected in(0, 86400, 2592000, 315360000)
            which corresponds:the returned cookie can save your information for:
            ("this browser process", "one day", "one month", "one year")
    :return: CookieJar
    """
    return _login(username, password, usecookie)


class ResultList(list):
    """
    the search result
    """

    def __init__(self, *items):
        super().__init__(items)

    def __repr__(self):
        return f"<SearchResult {self.__len__()} items>"

    def __str__(self):
        return f"<SearchResult {self.__len__()} items>"


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

    def __init__(self, cookies: RequestsCookieJar, name: str) -> None:
        self.name = name
        self.cookies = cookies

    @property
    def books(self) -> ResultList:
        """
        get the books of this author
        :return: a list of books
        """
        # TODO: get the books of this author
        return ResultList()


class Book:
    """
    book class
    """

    def __init__(self, cookies: RequestsCookieJar, book_id: str) -> None:
        self.book_id = book_id
        self.book_url = f"https://www.wenku8.net/book/{book_id}.htm"
        self.cookies = cookies
        self.meta_info = BeautifulSoup(
            requests.get(self.book_url, cookies=self.cookies, headers=FAKE_HEADERS).content, "lxml")
        self.name = self.meta_info.select("#content > div:nth-child(1) > table:nth-child(1) > tr:nth-child(1) > "
                                          "td:nth-child(1) > table:nth-child(1) > tr:nth-child(1) > td:nth-child("
                                          "1) > span:nth-child(1) > b:nth-child(1)")[0].text
        self.cover_url = self.meta_info.select("#content > div:nth-child(1) > table:nth-child(4) > "
                                               "tr:nth-child(1) > td:nth-child(1) > img:nth-child(1)")[0]["src"]
        self.author = Author(self.cookies, self.meta_info.select("#content > div:nth-child(1) > table:nth-child(1) > "
                                                                 "tr:nth-child(2) > td:nth-child(2)")[0].text[5:])


def get_user(cookies: RequestsCookieJar) -> User:
    """
        get user info
        :return: User
        """
    user_info = BeautifulSoup(requests.get("https://www.wenku8.net/userdetail.php",
                                           cookies=cookies, headers=FAKE_HEADERS).content, "lxml")
    return User(
        user_id=user_info.select("html body div.main div#centerm div#content table.grid tr td.even")[0].text,
        name=user_info.select("html body div.main div#centerm div#content table.grid tr td.even")[3].text,
        level=user_info.select("html body div.main div#centerm div#content table.grid tr td.even")[5].text,
        honor=user_info.select("html body div.main div#centerm div#content table.grid tr td.even")[6].text,
        points=int(user_info.select("html body div.main div#centerm div#content table.grid tr td.even")[15].text),
        avatar_url=user_info.select(".avatar")[0]["src"]
    )


def get_book(cookies: RequestsCookieJar, book_id: str) -> Book:
    return Book(book_id=book_id, cookies=cookies)
