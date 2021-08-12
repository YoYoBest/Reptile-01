from selenium import webdriver
import time


class QCWY:

    def __init__(self, keyword, city, maxpagenum):
        self.keyword = keyword
        self.city = city
        self.maxpagenum = maxpagenum

    def run(self):
        driver = webdriver.Chrome(r'd:\chromedriver\chromedriver.exe')  #chrome服务所在目录
        driver.implicitly_wait(10)

        driver.get('https://www.51job.com/')

        # 输入关键字
        driver.find_element_by_id('kwdselectid').send_keys(self.keyword)

        # 选择城市
        driver.find_element_by_id('work_position_input').click()

        time.sleep(1)

        # 选择城市，点击上方当前已经选中的城市，去掉这些
        selectedCityEles = driver.find_elements_by_css_selector('#work_position_click_multiple_selected>span')

        for one in selectedCityEles:
            one.click()

        # 然后再选择我们要选择的城市
        cityEles = driver.find_elements_by_css_selector('#work_position_click_center_right_list_000000 em')

        target = None
        for cityEle in cityEles:
            # 如果城市名称相同，找到了
            if cityEle.text == self.city:
                target = cityEle
                break

        # 没有找到该名称的城市
        if target is None:
            input(f'{self.city}不在热门城市列表中，请手动点击选中城市后，按回车继续...')
        else:
            target.click()

        # 保存城市选择
        driver.find_element_by_id('work_position_click_bottom_save').click()

        driver.find_element_by_css_selector('div.ush >button').click()

        for pageNo in range(1,self.maxpagenum+1):
            #设置页码
            pageNoInput = driver.find_element_by_id('jump_page')
            pageNoInput.clear()
            pageNoInput.send_keys(str(pageNo))
            driver.find_element_by_css_selector('span.og_but').click()

            #暂停1s
            time.sleep(1)

            self.handleOnePage(driver)

           #是否到了最后一页
            if self.isLastPage(driver):
                break

    #是否到了最后一页
    def isLastPage(self,driver):
        #如果下一页是链接，表示还有下一页
        NextPageButton = driver.find_element_by_css_selector('div.j_page li:last-child')

        driver.implicitly_wait(2)
        hasLink = NextPageButton.find_element_by_tag_name('a')
        driver.implicitly_wait(10)
        if hasLink: #不是最后一页
            return False
        else: #是最后一页
            return True

    #是否到了最后一条

    def handleOnePage(self,driver):

        # 处理每页信息
        jobs = driver.find_elements_by_css_selector('.j_result div[class=e]')

        for job in jobs:
            fields = job.find_elements_by_tag_name('span')
            stringFields = [field.text for field in fields]
            print(stringFields)


QCWY(keyword='软件测试工程师', city='苏州', maxpagenum=1).run()




