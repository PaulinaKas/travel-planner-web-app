from selenium import webdriver
import unittest

class NewUser(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Chrome()
        self.browser.implictly_wait(3) # waits 3s for fully loading of website

    def tearDown(self):
        self.browser.quit()

    def test_can_start_weather_app(self):
        self.browser.get('http://127.0.0.1:8000/') # user goes to website's address

        # 1. Checks if website's title is correctly
        self.assertIn('Current weather', self.browser.title)
        self.fail('End of test')

if __name__ == '__main__':
    unittest.main()
