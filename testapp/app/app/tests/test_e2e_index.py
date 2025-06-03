import time

from django.test import TestCase
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

from .utils import element_has_css_class, make_driver

import os

os.environ["WDM_LOG_LEVEL"] = "0"


class TestBatonIndex(TestCase):
    def setUp(self):
        self.driver = make_driver()
        self.driver.set_window_size(1920, 1080)
        self.driver.implicitly_wait(10)
        self.login()
        time.sleep(2)

    def tearDown(self):
        self.driver.quit()

    def login(self):
        self.driver.get("http://localhost:8000/admin")
        username_field = self.driver.find_element(By.ID, "id_username")
        password_field = self.driver.find_element(By.ID, "id_password")
        button = self.driver.find_element(By.CSS_SELECTOR, "input[type=submit]")

        username_field.send_keys("admin")
        time.sleep(1)
        password_field.send_keys("admin")
        time.sleep(1)
        button.click()

    def test_navbar(self):
        # Wait until baton is ready
        wait = WebDriverWait(self.driver, 10)
        wait.until(element_has_css_class((By.TAG_NAME, "body"), "baton-ready"))

        # site title
        site_name = self.driver.find_element(By.CSS_SELECTOR, "#site-name a")
        self.assertEqual(site_name.get_attribute("innerHTML"), "Baton Test App")

    def test_content(self):
        # Wait until baton is ready
        wait = WebDriverWait(self.driver, 10)
        wait.until(element_has_css_class((By.TAG_NAME, "body"), "baton-ready"))

        time.sleep(1)

        # page title
        page_title = self.driver.find_element(By.CSS_SELECTOR, "#content h1")
        self.assertEqual(page_title.get_attribute("innerHTML"), "Baton administration")
        self.assertEqual(page_title.is_displayed(), True)

        # recent actions
        recent_actions = self.driver.find_element(By.ID, "recent-actions-module")
        self.assertEqual(recent_actions.is_displayed(), True)

        modules = self.driver.find_elements(By.CSS_SELECTOR, "#content-main .module")
        self.assertEqual(len(modules), 3)

    def test_footer(self):
        # Wait until baton is ready
        wait = WebDriverWait(self.driver, 10)
        wait.until(element_has_css_class((By.TAG_NAME, "body"), "baton-ready"))

        links = self.driver.find_elements(By.CSS_SELECTOR, "#footer .col-sm-4 p")
        self.assertEqual(len(links), 3)
        # support
        self.assertEqual(
            links[0].find_element(By.CSS_SELECTOR, "a").get_attribute("href"),
            "mailto:mail@otto.to.it",
        )
        self.assertEqual(links[0].get_attribute("innerText").strip(), "help Support")
        # copyright
        self.assertEqual(
            links[1].get_attribute("innerText").strip(), "copyright © 2024 Otto srl"
        )
        # powered by
        self.assertEqual(
            links[2].get_attribute("innerText").strip(),
            "Baton Test App · Developed by Otto srl",
        )
