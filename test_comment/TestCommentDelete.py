import time

from selenium import webdriver
import unittest

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys

from keywords.on_admin_ui_page import click_a_dashboard_button
from keywords.wait_until_is_visible import wait_until_home_page_is_visible, wait_until_comments_page_is_visible, \
    wait_until_delete_warning_dialog, wait_until_edit_comment_page_is_visible, wait_until_admin_ui_page_is_visible, \
    wait_until_posts_page_is_visible, wait_until_element_visible_by_xpath

# on posts_page -> admin_ui_page
from test_post.TestPostCreate import click_create_submit_button, sign_in_as_admin, go_to_posts_page_from_admin_ui_page, \
    create_a_post, sign_out, go_back_to_home_page_from_sign_in_page


def go_to_comments_page_from_admin_ui_page(self):
    click_a_dashboard_button(self, 'Posts', 'Comments')
    wait_until_posts_page_is_visible(self)


def click_create_comment_button(self):
    self.driver.find_element_by_xpath('//*[contains(text(), "Create ")]').click()


def input_comment_author(self, comment_author):
    self.driver.find_element_by_xpath(
        '//*[contains(@class, "css-1wrt3l9") and @for="author"]//*[@class = "Select-arrow"]').click()
    time.sleep(2)  # todo: wait
    self.driver.find_element_by_xpath(
        '//*[contains(@class, "css-1wrt3l9") and @for="author"]//*[contains(@aria-activedescendant, "react-select")]') \
        .send_keys(comment_author)
    time.sleep(2)  # todo: wait
    self.driver.find_element_by_xpath(
        '//*[contains(@class, "css-1wrt3l9") and @for="author"]//*[contains(@aria-activedescendant, "react-select")]') \
        .send_keys(Keys.ENTER)


def input_comment_post(self, post_name):
    self.driver.find_element_by_xpath(
        '//*[contains(@class, "css-1wrt3l9") and @for="post"]//*[@class = "Select-arrow"]').click()
    time.sleep(2)  # todo: wait
    self.driver.find_element_by_xpath(
        '//*[contains(@class, "css-1wrt3l9") and @for="post"]//*[contains(@aria-activedescendant, "react-select")]') \
        .send_keys(post_name)
    time.sleep(2)  # todo: wait
    self.driver.find_element_by_xpath(
        '//*[contains(@class, "css-1wrt3l9") and @for="post"]//*[contains(@aria-activedescendant, "react-select")]') \
        .send_keys(Keys.ENTER)


#########################################################################################
def wait_until_create_a_new_comment_dialog_is_visible(self):
    wait_until_element_visible_by_xpath(self, '//*[@class="css-s2cbvv"]')


def create_a_comment(self, comment_author, post_name):
    click_create_comment_button(self)
    wait_until_create_a_new_comment_dialog_is_visible(self)
    input_comment_author(self, comment_author)
    input_comment_post(self, post_name)
    click_create_submit_button(self)
    wait_until_edit_comment_page_is_visible(self)


def go_back_to_comments_page(self):
    self.driver.find_element_by_link_text('Comments').click()
    wait_until_comments_page_is_visible(self)


def verify_comments_page_have_comment(self, comment_id):
    self.assertTrue(self.driver.find_element_by_xpath(
        '//*[contains(@href, "/keystone/post-comments/' + comment_id + '")]') is not None)
    self.assertTrue(self.driver.find_element_by_link_text('Demo User') is not None)


def go_to_admin_ui_page_from_comments_page(self):
    self.driver.find_element_by_xpath('//*[@href="/keystone"]').click()
    wait_until_admin_ui_page_is_visible(self)


def click_cancel_button(self):
    self.driver.find_element_by_xpath('//*[contains(text(), "Cancel") and @data-button-type="cancel"]').click()


def delete_a_comment(self, comment_id):
    self.driver.find_element_by_xpath('//*[@href="/keystone/post-comments/' + comment_id + '"]').click()
    wait_until_edit_comment_page_is_visible(self)
    self.driver.find_element_by_xpath('//*[contains(@data-button, "delete")]').click()
    wait_until_delete_warning_dialog(self)
    self.driver.find_element_by_xpath(
        '//*[contains(@data-button-type, "confirm") and contains(text(), "Delete")]').click()
    wait_until_comments_page_is_visible(self)


#############################################################################

class TestPostCreate(unittest.TestCase):
    driver = None

    @classmethod
    def setUpClass(cls) -> None:
        cls.driver = webdriver.Chrome('../chromedriver.exe')

    def setUp(self) -> None:
        self.driver.get('http://127.0.0.1:3000/')
        self.driver.maximize_window()
        wait_until_home_page_is_visible(self)
        sign_in_as_admin(self)

    def test_delete_comment_with_ISP_input1(self):
        # setup
        go_to_posts_page_from_admin_ui_page(self)
        post_name = 'post_name'
        create_a_post(self, post_name)
        go_to_admin_ui_page_from_comments_page(self)
        go_to_comments_page_from_admin_ui_page(self)
        comment_author = 'Demo User'
        create_a_comment(self, comment_author, post_name)
        self.driver.back()  # todo: back?
        time.sleep(2)
        # delete comment
        comment_id = self.driver.find_element_by_xpath('//*[contains(@href, "/keystone/post-comments/")]').text
        delete_a_comment(self, comment_id)
        with self.assertRaises(NoSuchElementException):
            self.driver.find_element_by_link_text(comment_id)
        print('test_delete_comment ok')

    def test_delete_comment_with_ISP_input2(self):
        # setup
        go_to_posts_page_from_admin_ui_page(self)
        post_name = 'post_name'
        create_a_post(self, post_name)
        go_to_admin_ui_page_from_comments_page(self)
        go_to_comments_page_from_admin_ui_page(self)
        comment_author = 'Demo User'
        create_a_comment(self, comment_author, post_name)
        self.driver.back()  # todo: back?
        time.sleep(1)
        # delete comment
        comment_id = self.driver.find_element_by_xpath('//*[contains(@href, "/keystone/post-comments/")]').text
        delete_a_comment(self, comment_id)
        with self.assertRaises(NoSuchElementException):
            self.driver.find_element_by_link_text(comment_id)
        print('test_delete_comment ok')

    def test_delete_comment_with_ISP_input3(self):
        # setup
        go_to_posts_page_from_admin_ui_page(self)
        post_name = 'post_name_post_name_post_name_post_name_post_name_post_name_post_name_post_name_post_name_post_name_post_name'
        create_a_post(self, post_name)
        go_to_admin_ui_page_from_comments_page(self)
        go_to_comments_page_from_admin_ui_page(self)
        comment_author = 'Demo User'
        create_a_comment(self, comment_author, post_name)
        self.driver.back()  # todo: back?

        # delete comment
        time.sleep(1)
        comment_id = self.driver.find_element_by_xpath('//*[contains(@href, "/keystone/post-comments/")]').text
        delete_a_comment(self, comment_id)
        with self.assertRaises(NoSuchElementException):
            self.driver.find_element_by_link_text(comment_id)
        print('test_delete_comment ok')

    def test_delete_comment_with_cancel(self):
        # setup
        go_to_posts_page_from_admin_ui_page(self)
        post_name = 'post_name_post_name_post_name_post_name_post_name_post_name_post_name_post_name_post_name_post_name_post_name'
        create_a_post(self, post_name)
        go_to_admin_ui_page_from_comments_page(self)
        go_to_comments_page_from_admin_ui_page(self)
        comment_author = 'Demo User'
        create_a_comment(self, comment_author, post_name)
        self.driver.back()  # todo: back?

        # delete comment
        time.sleep(1)
        comment_id = self.driver.find_element_by_xpath('//*[contains(@href, "/keystone/post-comments/")]').text
        time.sleep(1)
        self.driver.find_element_by_xpath('//*[@href="/keystone/post-comments/' + comment_id + '"]').click()
        wait_until_edit_comment_page_is_visible(self)
        self.driver.find_element_by_xpath('//*[contains(@data-button, "delete")]').click()
        wait_until_delete_warning_dialog(self)
        click_cancel_button(self)
        self.driver.back()
        time.sleep(1)
        verify_comments_page_have_comment(self, comment_id)

    def tearDown(self) -> None:
        # todo: delete all post?
        sign_out(self)
        go_back_to_home_page_from_sign_in_page(self)

    @classmethod
    def tearDownClass(cls) -> None:
        cls.driver.close()
        cls.driver.quit()
