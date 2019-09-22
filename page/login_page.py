import time

import allure

from base.Base import Base
from page.page_elements import PageElements
from selenium.common.exceptions import TimeoutException


class LoginPage(Base):
    """登录页面"""

    def __init__(self, driver):
        Base.__init__(self, driver)

    @allure.step('登录页面==执行登录操作')
    def login(self, username, password):
        time.sleep(3)
        """
        登录
        :param username: 账号
        :param password: 密码
        :return:
        """
        self.send_element(PageElements.login_username_id, username)  # 输入账号
        time.sleep(2)
        self.send_element(PageElements.login_password_id, password)  # 输入密码
        self.click_element(PageElements.login_login_btn_id)  # 点击登录
        allure.attach('登录信息', '账号：%s, 密码：%s' % (username, password))

    @allure.step('获取登录按钮的文本信息')
    def get_login_btn_text(self):
        """返回登录按钮的文本信息"""
        return self.get_element(PageElements.login_login_btn_id).text

    @allure.step('关闭登录页面')
    def close_login_page(self):
        """关闭登录页面"""
        self.click_element(PageElements.login_close_login_page_btn_id)

    @allure.step('登录页面==判断登录按钮是否在此页面')
    def if_login_btn(self):
        """判断登录按钮是否在登录页面"""
        try:
            # 定位到登录按钮，返回true
            self.get_element(PageElements.login_login_btn_id)
            allure.attach('结果：', '登录按钮存在')
            return True
        except TimeoutException:
            # 定位不到返回false
            allure.attach('结果：', '没有登录按钮')
            return False
