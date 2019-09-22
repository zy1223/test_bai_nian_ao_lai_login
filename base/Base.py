import os
import time

import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait


class Base(object):
    def __init__(self, driver):
        self.driver = driver

    def get_element(self, loc, timeout=10, poll_frequency=1.0):
        """
        定位单个元素
        :param loc: 元组（By.ID,属性值），（By.CLASS_NAME,属性值），（By.XPATH,属性值）
        :param timeout: 超时时间10
        :param poll_frequency: 间隔时长1.0
        :return:定位对象
        """
        return WebDriverWait(self.driver, timeout, poll_frequency).until(lambda x: x.find_element(*loc))

    def get_elements(self, loc, timeout=10, poll_frequency=1.0):
        """
        定位一组元素
        :param loc: 元组（By.ID,属性值），（By.CLASS_NAME,属性值），（By.XPATH,属性值）
        :param timeout: 超时时间10
        :param poll_frequency: 间隔时长1.0
        :return:定位对象列表
        """
        return WebDriverWait(self.driver, timeout, poll_frequency).until(lambda x: x.find_elements(*loc))

    def click_element(self, loc):
        """
        点击方法
        :param loc: 元组（By.ID,属性值），（By.CLASS_NAME,属性值），（By.XPATH,属性值）
        :return:
        """
        self.get_element(loc).click()

    def send_element(self, loc, text):
        """
        输入方法
        :param loc:
        :param text: 元组（By.ID,属性值），（By.CLASS_NAME,属性值），（By.XPATH,属性值）
        :return:
        """
        self.get_element(loc).clear()
        self.get_element(loc).send_keys(text)

    @allure.step('滑动屏幕操作')
    def swipe_screen(self, tag=1):
        time.sleep(2)
        """
        滑动屏幕，默认向上滑动屏幕
        :param tag:1向上，2向下，3向左，4向右
        :return:
        """
        size = self.driver.get_window_size()  # 获取屏幕尺寸大小
        width = size.get('width')  # 获取屏幕宽
        height = size.get('height')  # 获取屏幕高
        if tag == 1:
            allure.attach('滑动方向：','向上滑动')
            # 向上滑动 宽0.5，高0.8->高0.3
            self.driver.swipe(width * 0.5, height * 0.8, width * 0.5, height * 0.3)
        elif tag == 2:
            allure.attach('滑动方向：','向下滑动')
            # 向下滑动 宽0.5，高0.3->高0.8
            self.driver.swipe(width * 0.5, height * 0.3, width * 0.5, height * 0.8)
        elif tag == 3:
            allure.attach('滑动方向：','向左滑动')
            # 向左滑动 高0.5，宽0.8->宽0.3
            self.driver.swipe(width * 0.8, height * 0.5, width * 0.3, height * 0.5)
        elif tag == 4:
            allure.attach('滑动方向：','向右滑动')
            # 向右滑动 高0.5，宽0.3->宽0.8
            self.driver.swipe(width * 0.3, height * 0.5, width * 0.8, height * 0.5)

    @allure.step('登录页面==获取toast消息')
    def get_toast(self, mess):
        """
        获取toast消息
        :param mess: 要获取的toast消息中的部分文本内容
        :return:
        """
        message = (By.XPATH, '//*[contains(@text,"%s")]' % mess)
        toast_mes_text = self.get_element(message, timeout=3, poll_frequency=0.3).text
        allure.attach('结果：', '%s' % toast_mes_text)
        return toast_mes_text

    @allure.step('截图操作')
    def screen(self, name='截图'):
        """截图添加到报告中"""
        # 图片的名字
        image_name = "." + os.sep + 'img' + os.sep + "%d.png" % int(time.time())
        # 截图
        self.driver.get_screenshot_as_file(image_name)
        # 将截图添加到报告中
        with open(image_name, 'rb') as f:
            allure.attach('截图', f.read(), allure.attach_type.PNG)
        allure.attach('截图名称：', '%s' % name)
        assert True
