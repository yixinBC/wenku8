import unittest
import wenku8_api
import requests


class ApiTestCase(unittest.TestCase):
    def __init__(self, method_name):
        super().__init__(methodName=method_name)
        self.wenku8 = wenku8_api.Wenku8api("wenku8test", "wenku8test", 86400)
        self.user = self.wenku8.get_user()
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
        self.assertEqual(self.user.points, 13)
        self.assertEqual(self.user.avatar_url, "https://www.wenku8.net/images/noavatar.jpg")


if __name__ == '__main__':
    unittest.main()
