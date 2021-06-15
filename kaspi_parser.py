from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import bs4
import re
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
# from urllib3 import request
import requests
import time
import os
from seleniumwire import webdriver  as wiredriver
# import xml.etree.ElementTree as ET


class Kaspi_parser(object):
    driver=None
    product_propertyes=['name','price','image','description','category','prices','kaspi_name']
    description_adder='\n<a style="color:red" href="https://kaspi.kz/shop/kaspibutton?masterSKU={product_id}&merchantCode=TeleNova&city=750000000">Купить на kaspi.kz</a>\n'
    user_agent='Mozilla/5.0 (Windows; U; Windows NT 5.01) AppleWebKit/531.41.6 (KHTML, like Gecko) Version/5.0 Safari/531.41.6'
    city_code='750000000'
    _instance = None
    def __new__(class_, *args, **kwargs):
        if not isinstance(class_._instance, class_):
            class_._instance = object.__new__(class_, *args, **kwargs)
            class_._instance._load_driver()
        return class_._instance
    
    def _get_propertyes_methods(self):
        return {
            'kaspi_name':self._parce_name,
            'prices':self._get_product_prices,
            'image':self._parce_image,
            'description':self._parce_description,
            'category':self._parce_category,
        }
    
    def _load_driver(self):
        self.close_driver()
            
        options = Options()
        options.add_argument(f'user-agent={self.user_agent}')
        options.add_argument('--ignore-certificate-errors')
        options.add_argument("--test-type")
        # options.add_argument("--headless")
        options.add_argument("--incognito")
        options.add_argument('--disable-gpu') if os.name == 'nt' else None # Windows workaround
        options.add_argument("--verbose")
        # self.driver = wiredriver.Chrome('./chromedriver',chrome_options=opts)
        self.driver = webdriver.Chrome('./chromedriver',chrome_options=options)
        self.driver.set_page_load_timeout(20)
        # self.driver.implicitly_wait(10)
       
        self.driver.delete_all_cookies()
        
    def close_driver(self):
        try:
            self.driver.close()
        except:
            print('new page')
       
        
    def _parce_image(self,tree,*args):
        try:
            image_url = tree.find(
                "img", {'class': 'item__slider-pic'})['src']
        except:
            image_url = tree.find(
                "img", {'class': 'item__slider-pic'})['data-src']
        return image_url
    
    def _parce_description(self,tree,id):
        description = tree.find(
                                "div", {'class': 'item__description-text'}).text
        description+=self.description_adder.format(product_id=id)
        return description
    
    def _parce_name(self,tree,id):
        name = tree.find(
                                "h1", {'class': 'item__heading'}).text
        
        return name
    
    def _parce_category(self,tree,*args):
        category = tree.findAll("span", {'itemprop': 'name'})[-1].text
        category=category.replace('\n','')
        return category

    def _get_cookies(self):
        selenium_cookies=self.driver.get_cookies()
        requests_cookies={}
        for cookie in selenium_cookies:
            requests_cookies[cookie['name']]=cookie['value']
        return requests_cookies
    
    def _get_product_prices(self,tree,id,*args):
        price_tables=[]
        try:
            table=tree.find('table',{'class':'sellers-table__self'})
            tbody=(table.find('tbody'))
            price_tables=[]
            for product in tbody.findAll('tr'):
                # print(product)
                try:
                    price=product.findAll('td')[3].find('div').text
                    price=re.sub('\D', '', price)
                    # print(price)
                    
                    price_tables.append(int(price))
                except Exception as e:
                    print(e)
                    continue
                # print(price)
        except:
            pass
        return price_tables
        # print(dict_request["data"][0])
        
    def _get_product_id(self,name):
        print('get product id')
        id=None
        while not id:
            driver=self.driver
            # self.driver.get(f"https://google.com")
            try:
                self.driver.get(f"https://kaspi.kz/shop/search/?text={name}")
                WebDriverWait(driver, 20).until(
                                EC.presence_of_element_located((By.CLASS_NAME, 'search-bar__input')))
            except:
                self._load_driver() 
                continue
            try:
                tree = bs4.BeautifulSoup(
                                driver.page_source.encode('utf-8')
                                ,features='lxml')
            except:
                tree = bs4.BeautifulSoup(driver.page_source,features='lxml')
            product=tree.find('div',{'class':"item-card"})
            # print(product,dir(product))
            print('id have found')
            return product['data-product-id']
    
    def _get_product_tree(self,id,*args):
        tree=None
        print('get tree')
        while not tree:
            driver=self.driver
            try:
                self.driver.get(
                                    f"https://kaspi.kz/shop/p/{id}/?c=750000000")
                WebDriverWait(driver,20).until(
                                EC.presence_of_element_located((By.CLASS_NAME, 'item__slider-pic')))
            except:
                self._load_driver()
                continue
            try:
                tree = bs4.BeautifulSoup(
                                self.driver.page_source
                                ,features='lxml')
            except:
                tree = bs4.BeautifulSoup(self.driver.page_source.encode('utf-8'),features='lxml')
            return tree
            
    def parce_product(self,id, **kwargs):
        '''
        kwargs-{'name':'sasha','category:'human'}
        '''
        product_data={key:'' for key in self.product_propertyes}
        if not id:
            id=self._get_product_id(kwargs['name'])
            
        tree=self._get_product_tree(id)
        for property in product_data:
            if kwargs.get(property):
                product_data[property]=kwargs[property]
            else:
                try:
                
                    product_data[property]=self._get_propertyes_methods()[property](tree,id)
                    
                except Exception as e:
                    # print(e)
                    raise Exception(f'have not parce method for {property} property')
        for property in kwargs:
            if  property not in product_data.keys():
                product_data[property]=kwargs[property]
        product_data['kaspi_id']=id
        product_data['id']=id
        return product_data
            
if __name__=='__main__':
    cook=Kaspi_parser().parce_product(id=False,name='airpods',price=20)
    print(cook)
