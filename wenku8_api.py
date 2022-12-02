__author__ = "yixinBC"

__doc__ = """
Copyright (C) 2021-  yixinBC
the api for https://www.wenku8.net
"""

import requests
from requests.cookies import RequestsCookieJar
from lxml import etree

FAKE_HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0"}


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
        def __init__(self, user_id: str, name: str, level: str, honor: str, points: int, avatar_url: str) -> None:
            print(user_id, name, level, honor, points, avatar_url)
            self.id = user_id
            self.name = name
            self.level = level
            self.honor = honor
            self.points = points
            self.avatar_url = avatar_url

    class Book:
        def __init__(self, book_id: str, user_cookies: RequestsCookieJar) -> None:
            self.book_id = book_id
            self.book_url = f"https://www.wenku8.net/book/{book_id}.htm"
            self.user_cookies = user_cookies
            self.meta_info = etree.HTML(
                requests.get(self.book_url, cookies=self.user_cookies, headers=FAKE_HEADERS).text)
            self.cover_url = self.meta_info.xpath(
                '//*[@id="content"]/div[1]/table[2]/tbody/tr/td[1]/img/attribute::src')
            self.author = self.meta_info.xpath('//*[@id="content"]/div[1]/table[1]/tbody/tr[2]/td[2]/text()')

    def __init__(self, username: str, password: str, usecookie: int):
        self.cookies = _login(username, password, usecookie)

    def get_user(self) -> User:
        """
        get user info
        :return: User
        """
        user_info = etree.HTML(
            requests.get("https://www.wenku8.net/userdetail.php", cookies=self.cookies, headers=FAKE_HEADERS).text)
        return self.User(
            user_id=user_info.xpath('//*[@id="content"]/table/tbody/tr[1]/td[2]/text()'),
            name=user_info.xpath('//*[@id="content"]/table/tbody/tr[3]/td[2]/text()'),
            level=user_info.xpath('//*[@id="content"]/table/tbody/tr[5]/td[2]/text()'),
            honor=user_info.xpath('//*[@id="content"]/table/tbody/tr[6]/td[2]/text()'),
            points=int(user_info.xpath('//*[@id="content"]/table/tbody/tr[16]/td[2]/text()')),
            avatar_url=user_info.xpath('//*[@id="content"]/table/tbody/tr[1]/td[3]/img/attribute::src')
        )

    def get_book(self, book_id) -> Book:
        return self.Book(book_id=book_id, user_cookies=self.cookies)
