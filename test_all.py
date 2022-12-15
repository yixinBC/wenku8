import unittest
import wenku8_api
import requests


class ApiTestCase(unittest.TestCase):
    def __init__(self, method_name):
        super().__init__(methodName=method_name)
        self.wenku8 = wenku8_api.Wenku8api("wenku8test", "wenku8test", 86400)
        self.user = self.wenku8.get_user()
        self.test_book = self.wenku8.Book("1", self.wenku8.cookies)
        self.cookies = self.wenku8.cookies

    def test_wenku8_login(self):
        self.assertEqual(requests.get("https://www.wenku8.net/index.php",
                                      cookies=self.cookies,
                                      headers=wenku8_api.FAKE_HEADERS).is_redirect, False)  # add assertion here

    def test_user_panel(self):
        self.assertEqual(self.user.id, "1193383")
        self.assertEqual(self.user.name, "wenku8test")
        self.assertEqual(self.user.level, "普通会员")
        self.assertEqual(self.user.honor, "新手上路")
        self.assertEqual(self.user.avatar_url, "https://www.wenku8.net/images/noavatar.jpg")

    def test_book_meta(self):
        self.assertEqual(self.test_book.cover_url, "https://img.wenku8.com/image/0/1/1s.jpg")
        self.assertEqual(self.test_book.author, "野村美月")
        self.assertEqual(self.test_book.name, "文学少女")


if __name__ == '__main__':
    unittest.main()
