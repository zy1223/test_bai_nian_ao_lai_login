import allure
import pytest

from base.get_data import GetData
from base.unite_page import UnitePage
from base.get_driver import get_driver
# 导入超时异常
from selenium.common.exceptions import TimeoutException


def login_data():
    login_data_info = GetData().get_yaml_data('login_test_data_2.yml')
    suc_data_list = []
    dis_data_list = []
    for i in login_data_info:
        if login_data_info.get(i).get('toast'):
            dis_data_list.append((i, login_data_info.get(i).get('username'), login_data_info.get(i).get('password'),
                                  login_data_info.get(i).get('toast'), login_data_info.get(i).get('exp_data')))
        else:
            suc_data_list.append((i, login_data_info.get(i).get('username'), login_data_info.get(i).get('password'),
                                  login_data_info.get(i).get('exp_data')))
    return {'suc': suc_data_list, 'dis': dis_data_list}


class TestLogin(object):
    def setup_class(self):
        # 初始化driver
        self.driver = get_driver('com.yunmall.lc', 'com.yunmall.ymctoc.ui.activity.MainActivity')
        # 实例化统一入口类
        self.unite_page = UnitePage(self.driver)

    def teardown_class(self):
        # 退出driver
        self.driver.quit()

    @pytest.fixture(autouse=True)
    def go_to_login(self):
        """跳转到登录页面,每次用例执行都要依赖一次"""
        # 点击我
        self.unite_page.home_page().click_me_btn()
        # 点击已有账号去登录
        self.unite_page.choice_login().click_exists_account_login()
    def person_logout(self):
        """个人中心执行退出操作"""
        # 1、点击设置
        self.unite_page.person_page().click_setting_btn()
        # 2、退出
        self.unite_page.setting_page().logout()


    @pytest.mark.parametrize('case_num, username, pwd, exp_data', login_data().get('suc'))
    @allure.step('登录正向测试-预期成功')
    def test_suc_login(self, case_num, username, pwd, exp_data):
        """
        预期成功
        :param case_num: 用例编号
        :param username: 用户名
        :param pwd: 密码
        :param exp_data: 预期结果
        :return:
        """
        # 登录
        self.unite_page.login_page().login(username, pwd)
        try:
            # 获取我的收藏
            shopping_cart_text_info = self.unite_page.person_page().get_text_my_shopping_cart()
            try:
                # 断言我的收藏是否在个人中心页面
                assert exp_data == shopping_cart_text_info
            except AssertionError:
                # 断言失败，“我的收藏”不在个人中心
                # 截图
                self.unite_page.login_page().screen()
                # 断言失败，防止捕获断言异常，没有断言，那么测试方法默认断言通过
                assert False
            finally:
                # 退出
                self.person_logout()
        except TimeoutException:
            #  超时异常 定位不到“我的收藏”这个元素
            #  截图
            self.unite_page.login_page().screen()
            try:
                # 判断登录按钮是否在此页面
                assert self.unite_page.login_page().if_login_btn()
                # 关闭登登录页面
                self.unite_page.login_page().close_login_page()
            except AssertionError:
                # 退出操作
                self.person_logout()
            # 断言失败，防止捕获断言异常，没有断言，那么测试方法默认断言通过
            assert False

    @pytest.mark.parametrize('case_num, username, pwd,toast, exp_data', login_data().get('dis'))
    @allure.step('登录逆向测试-预期失败')
    def test_fail_login(self, case_num, username, pwd, toast, exp_data):
        """
        预期失败
        :param case_num: 用例编号
        :param username: 用户名
        :param pwd: 密码
        :param toast:消息拼接语句
        :param exp_data: 预期结果
        :return:
        """
        # 登录
        self.unite_page.login_page().login(username, pwd)
        try:
            # 定位到toast消息
            toast_info_text = self.unite_page.login_page().get_toast(toast)
            try:
                # 断言预期结果是否在获取的toast文本信息中
                assert exp_data == toast_info_text
            except AssertionError:
                # 截图
                self.unite_page.login_page().screen()
                # 断言失败，防止捕获断言异常，没有断言，那么测试方法默认断言通过
                assert False
        except TimeoutException:
            # 定位不到toast
            # 截图
            self.unite_page.login_page().screen()
            # 断言失败，防止捕获断言异常，没有断言，那么测试方法默认断言通过
            assert False
        finally:
            try:
                # 断言登录按钮
                assert self.unite_page.login_page().if_login_btn()
                # 关闭登录页面
                self.unite_page.login_page().close_login_page()
            except AssertionError:
                # 截图
                self.unite_page.login_page().screen()
                # 退出个人中心
                self.person_logout()
                # 断言失败，防止捕获断言异常，没有断言，那么测试方法默认断言通过
                assert False
