
#### This program scrapes naukri.com's page and gives our result as a 
#### list of all the job_profiles which are currently present there. 

import undetected_chromedriver as uc 
from selenium.webdriver.common.by import By

import time
import csv 



try:
    browser = uc.Chrome()
    pages_n = 120

    # scrape n number of pages
    for i in range(pages_n):
        # get webpage
        url = f"https://www.lazada.com.ph/shop-mobiles/?page={i+1}&spm=a2o4l.home.cate_1.1.7a9cca18AlV8HZ"
        browser.get(url)
        time.sleep(3)

        product_examples = []

        # get products
        products = browser.find_elements(By.CSS_SELECTOR, "div[data-qa-locator='product-item']")
        for product in products:
            product_url = product.find_element(By.TAG_NAME, "a")
            
            # get product id and url, and number of items sold
            id = product.get_attribute('data-item-id')
            
            # get number of product sold 
            num_sold = "0"
            try:
                num_sold = product.find_element(By.CLASS_NAME, "_1cEkb").text
            except:
                num_sold = "0"    

            href = product_url.get_attribute('href')

            product_examples.append({"id": id, "url":href, "sold": num_sold})
        
        # append product_id and url of each page to product_urls.csv
        with open(r'prod_urls.csv', 'a', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['id','url', 'sold']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            for product in product_examples:
                writer.writerow({'id': product['id'], 'url': product['url'], 'sold': product['sold']})

    browser.quit()
    print("Done!")
except Exception as e:
    print("an exception occurred:", e)
