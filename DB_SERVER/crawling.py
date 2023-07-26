from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.support.ui import Select
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.support.ui import Select
from datetime import datetime, timedelta
import calendar
import datetime
import time
import pandas as pd
from selenium.common.exceptions import NoSuchElementException
import random
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import StaleElementReferenceException
from pytz import timezone
from datetime import datetime, timedelta
import re
from pyvirtualdisplay import Display

class FlightDataGatherer:
    def __init__(self):
        self.arrs = ['NRT', 'HND', 'OSA', 'SPK', 'OKA', 'FUK']
        self.dets = ['ICN','CJJ', 'TAE', 'KWJ', 'PUS']
        self.grades_dict = {'': 'Y','premium': 'P', 'business': 'C', 'first': 'F'}
        self.seoul_tz = timezone('Asia/Seoul')
        self.now = datetime.now(self.seoul_tz).date()
        #self.init_display()
        self.init_driver()


    def init_display(self):
        self.display = Display(visible=0, size=(800, 600))
        self.display.start()

    def init_driver(self):
        self.options = Options()
        self.options.add_argument('--start-maximized')
        #self.options.add_argument('headless')
        self.options.add_experimental_option("detach", True)
        self.options.add_argument("--disable-web-security")
        self.options.add_argument("--disable-site-isolation-trials")
        self.options.add_argument("--disable-blink-features=AutomationControlled")
        self.options.add_argument("user-agent=Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Mobile Safari/537.36")
        self.service = Service(ChromeDriverManager(version="114.0.5735.90").install())
        self.driver = webdriver.Chrome(service=self.service, options=self.options)



    def gather_data(self):
        data = []
        for _ in range(2):
            
            
            for gr in self.grades_dict:
                for arr in self.arrs:
                    print(f"{arr}작업중...")
                    for det in self.dets:
                        for i in range(68, 70):
                            arr_date = self.now + timedelta(days=i)
                            url1 = f"https://flight.naver.com/flights/international/{arr}-{det}-{str(arr_date).replace('-', '')}?adult=1&fareType={self.grades_dict[gr]}"
                            self.driver.get(url1)
                            time.sleep(13)

                            Z = self.driver.find_elements(By.CLASS_NAME, "indivisual_IndivisualItem__3co62.result")
                            for i in range(len(Z)):
                                A = Z[i].text.split("\n")
                                filtered_elements_dir = [element for element in A if element.startswith(('직항', '경유'))]
                                filtered_elements_price = [element for element in A if element.endswith('원~')]
                                if gr == '':
                                    grade = 'economy'
                                else:
                                    grade = gr
                                time_taken = filtered_elements_dir[-1].split(", ")[0]
                                time_dir = filtered_elements_dir[-1].split(", ")[1]
                                data.append([arr, det, arr_date, A[1][:-3], A[2][:-3], time_taken, time_dir,
                                            filtered_elements_price[-1], grade])
                                print([arr, det, arr_date, A[1][:-3], A[2][:-3], time_taken, time_dir,
                                            filtered_elements_price[-1], grade])

                            
            self.swap_airports()
            print(self.arrs,self.dets)
                           

        return data


class HotelDataGatherer:
    def __init__(self):
        self.options = Options()
        self.options.add_argument('--start-maximized')
        self.options.add_argument('headless')
        self.options.add_experimental_option("detach", True)
        self.options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36")

        self.service = Service(ChromeDriverManager(version="114.0.5735.90").install())
        self.driver = webdriver.Chrome(service=self.service, options=self.options)
        self.seoul_tz = timezone('Asia/Seoul')
        self.now = datetime.now(self.seoul_tz).date()


        self.target_date = 30
        self.place_list = []
        self.area_dict = {
            '3ATokyo': '도쿄',
            '3AOsaka': '오사카',
            '3ASapporo': '삿포로',
            '3AOkinawa_Islands': '오키나와',
            '3AFukuoka': '후쿠오카'
        }
        self.ptype_dict = {
            '0' : '호텔',
            '16%2C28%2C5' : '게스트하우스,캡슐호텔,호스텔',
            '7%2C34%2C11' : '리조트,펜션,료칸'
        }

    def gather_data(self):
        for area in self.area_dict.keys():
            for ptype in self.ptype_dict.keys():
                for i in range(68, 70):
                    arr_date1 = self.now + timedelta(days=i)
                    arr_date2 = arr_date1 + timedelta(days=1)
                    url1 = f"https://hotels.naver.com/list?placeFileName=place%{area}&adultCnt=1&checkIn={arr_date1}&checkOut={arr_date2}&includeTax=false&sortField=popularityKR&sortDirection=descending&propertyTypes={ptype}"
                    self.driver.get(url1)
                    time.sleep(10)
                    s = 0
                    while s < 1:
                        try:
                            data = self.driver.find_elements(By.CLASS_NAME, 'SearchList_HotelItem__aj2GM')
                            for element in data:
                                hname=element.find_element(By.CLASS_NAME,'Detail_title__40_dz').text
                                price = element.find_element(By.CLASS_NAME,'Price_show_price__iQpms').text
                                score = element.find_element(By.CLASS_NAME,'Detail_score__UxnqZ').text
                                star = element.find_element(By.CLASS_NAME,'Detail_grade__y5BmJ').text
                                price = re.sub(r"[^\d]", "", price)
                                self.place_list.append([hname,arr_date1,arr_date2,self.area_dict[area],self.ptype_dict[ptype],score,star,price])
                                print(hname,arr_date1,arr_date2,self.area_dict[area],self.ptype_dict[ptype],score,star,price)
                            time.sleep(3)
                            self.driver.find_element(By.CLASS_NAME,'Pagination_next__OzkO7').click()
                            time.sleep(15)
                            s += 1
                        except NoSuchElementException:
                            break
                    print(len(self.place_list))
        return self.place_list



class CarRentalDataGatherer:
    def __init__(self):
        self.options = Options()
        self.options.add_argument('--start-maximized')
        self.options.add_argument('headless')
        self.options.add_experimental_option("detach", True)
        self.options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)")
        self.service = Service(ChromeDriverManager(version="114.0.5735.90").install())
        self.driver = webdriver.Chrome(service=self.service, options=self.options)
        self.seoul_tz = timezone('Asia/Seoul')
        self.now = datetime.now(self.seoul_tz).date()
        self.df_list = []
        self.locations =[
        {
            "name": "FUKUOKA",
            "sls": "OS209",
            "ssac": "FUKUOKA",
            "latitude": "33.5903189",
            "longitude": "130.4467091",
            "lid": "31",
            "locName": "후쿠오카%20공항(FUK)"
        },
        {
            "name": "FUKUOKA",
            "sls": "OS209",
            "ssac": "FUKUOKA",
            "latitude": "33.8390098",
            "longitude": "131.0333225",
            "lid": "350",
            "locName": "기타큐슈%20공항(KKJ)"
        },
        {
            "name": "OKINAWA",
            "sls": "OS208",
            "ssac": "OKINAWA",
            "latitude": "26.2064033",
            "longitude": "127.6465422",
            "lid": "30",
            "locName": "나하%20공항(OKA)"
        },
        {
            "name": "TOKYO",
            "sls": "OS210",
            "ssac": "TOKYO",
            "latitude": "35.771991",
            "longitude": "140.3928501",
            "lid": "32",
            "locName": "나리타%20국제공항(NRT)"
        },
        {
            "name": "TOKYO",
            "sls": "OS210",
            "ssac": "TOKYO",
            "latitude": "35.5493975",
            "longitude": "139.7798386",
            "lid": "33",
            "locName": "도쿄%20하네다%20국제공항(HND)"
        },
        {
            "name": "OSAKA",
            "sls": "OS211",
            "ssac": "OSAKA",
            "latitude": "34.4320024",
            "longitude": "135.2303939",
            "lid": "35",
            "locName": "간사이%20국제공항(KIX)"
        },
        {
            "name": "SAPPORO",
            "sls": "OS212",
            "ssac": "SAPPORO",
            "latitude": "42.7821883",
            "longitude": "141.6890474",
            "lid": "29",
            "locName": "신치토세%20공항(CTS)"
        },
    ]

    def gather_data(self):
        for location in self.locations:
            for i in range(68, 70):
                arr_date1 = self.now + timedelta(days=i)
                arr_date2 = arr_date1 + timedelta(days=1)
                n = 1
                url1 = f"https://carmore.kr/home/carlist.html?rt=1&mt=1&ssat=2&msat=1&msac={location['name']}&srsd={arr_date1}%2010:00:00&sred={arr_date2}%2010:00:00&isOverSeas=true&isOverseasReturnSelectMode=false&isOneway=false&pet=0&fishing=0&army=0&foreigner=0&sls={location['sls']}&ssac={location['ssac']}&latitude={location['latitude']}&longitude={location['longitude']}&lid={location['lid']}&locName={location['locName']}&age=30&nationalCode=JP&v=230720_3&rentStartDate={arr_date1}%2010:00:00&rentEndDate={arr_date2}%2010:00:00&areaCode={location['name']}&returnAreaCode=&returnLocName=&rlid=&rsls=&delivery[delivery]=1&delivery[ssat]=1&delivery[ssac]={location['name']}&delivery[rt]=1&delivery[srsd]={arr_date1}%2010:00:00&delivery[sred]={arr_date2}%2010:00:00&delivery[startAddress][areaCode]={location['name']}&delivery[startAddress][shortAddress]={location['locName']}&delivery[startAddress][lat]={location['latitude']}&delivery[startAddress][longt]={location['longitude']}&delivery[endAddress][areaCode]=&delivery[endAddress][shortAddress]=&delivery[endAddress][lat]=&delivery[endAddress][longt]=&rssac="
                self.driver.get(url1)
                time.sleep(5)

                # 스크롤을 맨 아래로 내림
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(3)
                
                try:
                    more_button = self.driver.find_element(By.CLASS_NAME, 'js-btn-carlist-more-load')
                    self.driver.execute_script("arguments[0].click();", more_button)
                except NoSuchElementException:
                    pass

                time.sleep(3)
                # 스크롤을 맨 아래로 내림
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(15)
                
            while True:
                try:
                    data = self.driver.find_element(By.XPATH, f'//*[@id="vsl_item_car_list_short_{n}"]')
                    try:
                        car_name = data.find_element(By.CLASS_NAME, 'js-vsl-txt-car-model').text
                        print(car_name)
                    except NoSuchElementException:
                        print("Element not found during car_name fetching")

                    try:
                        company = data.find_element(By.CLASS_NAME, 'js-vsl-txt-company-name').text
                        print(company)
                    except NoSuchElementException:
                        print("Element not found during company fetching")

                    try:
                        fuel = data.find_element(By.CLASS_NAME, 'js-vsl-price-info-only-top').text
                        print(fuel)
                    except NoSuchElementException:
                        print("Element not found during fuel fetching")

                    try:
                        grade = data.find_element(By.CLASS_NAME, 'js-vsl-badge-car-type').text
                        print(grade)
                    except NoSuchElementException:
                        print("Element not found during grade fetching")

                    try:
                        people = data.find_element(By.CLASS_NAME, 'js-car-info-txt-passenger').text
                        print(people)
                    except NoSuchElementException:
                        print("Element not found during people fetching")

                    try:
                        gear = data.find_element(By.CLASS_NAME, 'js-car-info-txt-transmission').text
                        print(gear)
                    except NoSuchElementException:
                        print("Element not found during gear fetching")

                    try:
                        insurance = data.find_element(By.CLASS_NAME, 'js-txt-car-additional-info').text
                        print(insurance)
                    except NoSuchElementException:
                        print("Element not found during insurance fetching")

                    try:
                        rental_price = data.find_element(By.CLASS_NAME, 'js-vsl-txt-car-price-range').text
                        print(rental_price)
                    except NoSuchElementException:
                        print("Element not found during rental_price fetching")

                    data_dict = {'Region': location['name'], 'Area': location['locName'], 'Car_Name': car_name, 'Company': company, 'Start_Date': arr_date1, 'End_Date': arr_date2, 'Fuel': fuel, 'Grade': grade, 'People': people, 'Gear': gear, 'insurance': insurance, 'Rental_Price': rental_price}
                    self.df_list.append(data_dict)
                    print(self.df_list)

                    print(f"현재 처리된 요소 번호: {n}")
                    n += 1

                except NoSuchElementException:
                    print(f"No element with id vsl_item_car_list_short_{n}, moving to the next date...")
                    break

        return self.df_list

