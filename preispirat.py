import time
import datetime

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import presence_of_element_located
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

from scraper import Scraper
from datastructures import ProductCompany


class Preispirat(Scraper):
    def __init__(self):
        Scraper.__init__(self)
        self.driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + 't')
        self.driver.get('https://www.preispirat.ch/')
        self.login()

    def login(self):
        self.wait.until(presence_of_element_located((By.LINK_TEXT, 'Deal einsenden')))
        self.driver.find_element_by_link_text('Deal einsenden').click()
        #self.driver.find_element_by_class_name('wpsm-button red medium addsomebtn mobileinmenu ml10 act-rehub-login-popup').click()
        self.wait.until(presence_of_element_located((By.NAME, 'rehub_user_login')))
        for element in self.driver.find_elements_by_name('rehub_user_login'):
            try:
                element.send_keys('pricedrop')
                break
            except:
                pass

        for element in self.driver.find_elements_by_name('rehub_user_pass'):
            try:
                element.send_keys('5qe3viJeLwpnN3E')
                break
            except:
                pass

        for element in self.driver.find_elements_by_tag_name('button'):
            try:
                element.click()
                break
            except:
                pass

        self.wait.until(presence_of_element_located((By.LINK_TEXT, 'Deal einsenden')))

    def uploadProduct(self, product):
        toppreis = self.get_toppreis(product)
        self.enter_info(toppreis)
        self.driver.find_element_by_name('Deal einsenden').click()

    def get_toppreis(self, product):
        print(f'https://www.toppreise.ch/produktsuche?q={product.product.manufacturer_id}')
        user_input = None
        while(True):
            try:
                user_input = list(map(str, input(f'Price: {self.get_latest_price(product).price}\nEnter only lowest price or second lowest price if showed price is cheaper, then also with preispirat url:').split()))
                if len(user_input) > 2:
                    print("Failed, retry", len(user_input), user_input)
            except Exception as e:
                print(f'Failed parsing values {e}')
                continue
            break
        if len(user_input) == 1:
            return

        return Toppreis(user_input[1], self.get_latest_price(product), user_input[0], product)

    def enter_info(self, toppreis):
        if type(toppreis) != Toppreis:
            print("wrong format")
            return
        self.driver.get('https://www.preispirat.ch/dealeinsenden/')
        self.driver.find_element_by_id('wpfepp-form-1-title-field').send_keys(f'{toppreis.product.product.name} bei {toppreis.product.company.name}')
        description = f'{toppreis.product.product.name} ist derzeit bei {toppreis.product.company.name} für nur CHF {toppreis.topprice} erhältlich. Zweitbester Preis ist laut Toppreise.ch CHF {toppreis.secondprice}: {toppreis.url}'
        self.driver.find_element_by_id('wpfepp-form-1-content-field-html').click()
        self.driver.find_element_by_id('wpfepp-form-1-content-field').send_keys(description)
        self.driver.find_element_by_id('wpfepp-form-1-rehub_offer_product_url-field').send_keys(toppreis.product.url)
        self.driver.find_element_by_id('wpfepp-form-1-rehub_offer_product_price-field').send_keys(str(toppreis.topprice))
        self.driver.find_element_by_id('wpfepp-form-1-rehub_offer_product_price_old-field').send_keys(str(toppreis.secondprice))
        self.driver.find_element_by_id('wpfepp-form-1-rehub_offer_coupon_date-field').send_keys(str(datetime.date.today() + datetime.timedelta(days=2)))
        self.driver.find_elements_by_class_name('select2-search__field')[0].send_keys("Elektronik & Unterhaltung ")
        self.driver.find_elements_by_class_name('select2-search__field')[0].send_keys(Keys.ENTER)
        self.driver.find_elements_by_class_name('select2-search__field')[1].send_keys(toppreis.product.company.name)
        self.driver.find_elements_by_class_name('select2-search__field')[1].send_keys(Keys.ENTER)
        while len(self.driver.find_elements_by_xpath('./div[contains(@class, "cls")]')) < 1:
            time.sleep(2)


class Toppreis:
    def __init__(self, url, topprice, secondprice, product):
        self.url = url
        self.topprice = float(topprice.price)
        self.secondprice = float(secondprice)
        self.product = product
