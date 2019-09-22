import allure

from base.Base import Base
from page.page_elements import PageElements


class PersonPage(Base):
    """个人中心页面"""

    def __init__(self, driver):
        Base.__init__(self, driver)

    @allure.step('个人中心==点击设置')
    def click_setting_btn(self):
        """点击设置"""
        self.click_element(PageElements.person_setting_btn_id)

    @allure.step('个人中心页面==定位我的收藏')
    def get_text_my_shopping_cart(self):
        """返回我的收藏文本信息"""
        # 我的收藏
        my_cart_info = self.get_element(PageElements.person_my_shopping_cart_id).text
        allure.attach('结果：', '%s' % my_cart_info)
        return my_cart_info
