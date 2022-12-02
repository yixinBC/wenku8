import unittest
import wenku8_api
import requests


class MyTestCase(unittest.TestCase):
    def test_wenku8_login(self):
        self.assertEqual(requests.get("https://www.wenku8.net/index.php",
                                      cookies=wenku8_api._login("wenku8test", "wenku8test", 86400),
                                      headers=wenku8_api.FAKE_HEADERS).is_redirect, False)  # add assertion here


if __name__ == '__main__':
    unittest.main()
