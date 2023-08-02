import undetected_chromedriver as uc 
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

import time
import csv 
 
import csv
from multiprocessing import Process

from datetime import datetime

def read_product_urls(input_file, start_row, end_row):
    products_urls = []
    with open(input_file, 'r') as file:
        reader = csv.reader(file, delimiter=",")

        # Skip rows until the desired start row
        for _ in range(start_row - 1):
            next(reader)

        # Process rows starting from the desired start row
        for row in reader:
            # Process the row here (e.g., print(row))
            products_urls.append(row)
            if (start_row == end_row):
                break
            start_row += 1

        return products_urls

def process(input_file, start_row, end_row):
    driver = uc.Chrome(headless=True)
    prod_urls = read_product_urls(input_file, start_row, end_row)
    for prod in prod_urls:
        driver.get("https://whatismyipaddress.com/")
        time.sleep(10)
        scrape_product(prod, driver)
    driver.quit()

def scrape_product(product_url, driver):
    product = {
        'id': product_url[0].strip(),
        'url': product_url[1].strip(),
        'sold': product_url[2].strip()
    }

    driver.get(product['url'])
    for i in range(0, 10000, 500):
        driver.execute_script(f"window.scrollTo({i}, {i+500});")
        time.sleep(0.2)

    # product name
    try:
        product['name'] = driver.find_element(By.CLASS_NAME, "pdp-product-title").text
    except:
        product['name'] = 'null'

    # prices
    try:
        prices = driver.find_element(By.CLASS_NAME, "pdp-mod-product-price")
        
        # current price
        try:
            product['current_price'] = prices.find_element(By.CLASS_NAME, "pdp-price_type_normal").text
        except:
            product['current_price'] = "0"

        # original price
        try:
            product['original_price'] = prices.find_element(By.CLASS_NAME, "pdp-price_type_deleted").text
        except:
            product['original_price'] = "0"        

        # discount
        try:
            product['discount'] = prices.find_element(By.CLASS_NAME, "pdp-product-price__discount").text
        except:
            product['discount'] = "0"  

    except:
        product['current_price'] = "0"
        product['original_price'] = "0"
        product['discount'] = "0"

    # ratings
    try:
        ratings = driver.find_element(By.CLASS_NAME, "mod-rating")

        # average_rating
        try:
            product['average_rating'] = ratings.find_element(By.CLASS_NAME, "score-average").text
        except:
            product['average_rating'] = "0"

        # rating count
        try:
            product['rating_count'] = ratings.find_element(By.CLASS_NAME, "count").text
        except:
            product['rating_count'] = "0"

        # five_star, four_star, three_star, two_star, one_star
        try:
            percents = ratings.find_elements(By.CLASS_NAME, "percent")
            
            stars = ['five_star', 'four_star', 'three_star', 'two_star', 'one_star']
            star_i = 0
            for p in percents:
                product[stars[star_i]] = p.text
                star_i += 1
        except:
            product['five_star'] = "0"
            product['four_star'] = "0"
            product['three_star'] = "0"
            product['two_star'] = "0"
            product['one_star'] = "0"   


        # seller performance info 
        try:
            seller_info = driver.find_element(By.CLASS_NAME, "pdp-seller-info-pc")

            seller_infos = seller_info.find_elements(By.CLASS_NAME, "seller-info-value")
            infos = ['seller_rating', 'chat_response', 'ship_time_rate']
            infos_i = 0

            for info in seller_infos:
                product[infos[infos_i]] = info.text
                infos_i += 1

        except:
            product['seller_rating'] = "0"
            product['chat_response'] = "0"
            product['ship_time_rate'] = "0"
        
        # specs
        try:
            try:
                view_more = driver.find_element(By.CLASS_NAME, "pdp-view-more-btn")
                actions = ActionChains(driver)
                actions.move_to_element(view_more).perform()
                view_more.click()
                time.sleep(0.2)
                
            except:
                print("no view more button") 

            specs_wrapper = driver.find_element(By.CLASS_NAME, "specification-keys") 

            spec_key_vals = specs_wrapper.find_elements(By.CLASS_NAME, "key-li")
            specs = ""
            for key_val in spec_key_vals:
                key = key_val.find_element(By.CLASS_NAME, "key-title").text.strip()
                val = key_val.find_element(By.CLASS_NAME, "key-value").text.strip()
                specs += key + "\t" + val + "\t\t"
            
            if specs.strip() == "":
                specs = "null"
            product['specs'] = specs
        except:
            product['specs'] = "null"


    except Exception as e:
        print("ERRRRRR")
        print(e)
        print("ERRRRRR")
        product['average_rating'] = "0"
        product['rating_count'] = "0"
        product['five_star'] = "0"
        product['four_star'] = "0"
        product['three_star'] = "0"
        product['two_star'] = "0"
        product['one_star'] = "0"

        if product['name'] == "null":
            product['seller_rating'] = "0"
            product['chat_response'] = "0"
            product['ship_time_rate'] = "0"
            product['specs'] = "null"
    
    print(product)
    with open(r'products_full.csv', 'a', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['id','sold', 'url', 'name', 'current_price', 'original_price', 'discount', 'average_rating', 'rating_count',
                      'five_star', 'four_star', 'three_star', 'two_star', 'one_star', 'seller_rating', 'chat_response', 'ship_time_rate', 'specs']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writerow({'id': product['id'], 
                         'sold': product['sold'],
                         'url': product['url'], 
                         'name': product['name'],
                         'current_price': product['current_price'],
                         'original_price': product['original_price'],
                         'discount': product['discount'],
                         'average_rating': product['average_rating'],
                         'rating_count': product['rating_count'],
                         'five_star': product['five_star'],
                         'four_star': product['four_star'],
                         'three_star': product['three_star'],
                         'two_star': product['two_star'],
                         'one_star': product['one_star'],
                         'seller_rating': product['seller_rating'],
                         'chat_response': product['chat_response'],
                         'ship_time_rate': product['ship_time_rate'],
                         'specs': product['specs'],
                         })
    


if __name__ == "__main__":
    csv_file = "prod_urls.csv"
    for i in range(1350, 1501):
        #Process(target=process, args=(csv_file, i, i)).start()
        process(csv_file, i, i)
    
    #process("prod_urls.csv", 2, 5)


