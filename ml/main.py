import streamlit as st
import numpy as np 
import pandas as pd 
import joblib 

cat_encoder = joblib.load("categorical_encoder")
inauth_model = joblib.load("inauth_prod_classifier")

st.title('Counterfeit Mobile Phone Product Classifier')
current_price = st.number_input("Mobile phone price", 0)
discount_price = st.text_input("Discount in percent %", "0%")

# convert discount price to float 
discount_price = float(discount_price.strip('%')) / 100

sold = st.number_input("Number of units sold", 0)

# get stars
five_star = st.number_input("Five star count", 0)
four_star = st.number_input("Four star count", 0)
three_star = st.number_input("Three star count", 0)
two_star = st.number_input("Two star count", 0)
one_star = st.number_input("One star count", 0)
rating_count = (five_star + four_star + three_star + two_star + one_star)

# get average rating
average_rating = (five_star * 5) + (four_star * 4) + (three_star * 3) + (two_star * 2) + (one_star * 1)
if (average_rating == 0):
    average_rating = 0
else:
    average_rating = average_rating / rating_count

# mobile phone brand
brand = st.selectbox('Mobile phone brand', ['Cherry', 'Huawei', 'Hyundai', 'Infinix', 'Lenovo', 'Lg', 'Meizu',
       'Motorola', 'Myphone', 'No Brand', 'Nokia', 'Oneplus', 'Oppo',
       'Others', 'Philips', 'Poco', 'Realme', 'Samsung', 'Tecno',
       'Telego', 'Vivo', 'Xiaomi'])
brand = brand.lower()

# mobile phone warranty 
# ['< 1 month', '>= 1month < 1year', '>= 1year', 'no warranty']
warranty_dict = {
    'Less than a month': '< 1 month',
    'Less than a year': '>= 1month < 1year',
    'One year and up': '>= 1year',
    'No warranty': 'no warranty'
}
warranty = st.selectbox('Mobile phone warranty', ['Less than a month', 'Less than a year',
                                                  'One year and up', 'No warranty'])
warranty = warranty_dict[warranty]

# type of warranty
# ['international warranty', 'lazada return and refund guarantee', 'local warranty', 'no warranty']
warranty_type = st.selectbox('Type of warranty', ['International Warranty', 'Lazada Return And Refund Guarantee',
       'Local Warranty', 'No Warranty'])
warranty_type = warranty_type.lower()

# number of camera 
num_camera = st.selectbox("Number of camera", ['Single', 'Dual', 'Triple', 'Quad',  'Zero', 'Unknown'])
num_camera = num_camera.lower()

# battery capacity 
#['6000 Mah Above', '< 2000 Mah', '>= 2000 Mah < 4000 Mah', '>= 4000 Mah < 6000 Mah', 'Unknown']
battery_dict = {
    "Less than 2000 mAh": '< 2000 Mah',
    "2000 mAh - 3999 mAh": '>= 2000 Mah < 4000 Mah',
    "4000 mAh - 5999 mAh": '>= 4000 Mah < 6000 Mah',
    '6000 mAh and Above': '6000 Mah Above',
    'Unknown': 'Unknown'
}
battery_capacity = st.selectbox('Battery Capacity', ["Less than 2000 mAh", "2000 mAh - 3999 mAh", 
                                                     "4000 mAh - 5999 mAh", '6000 mAh and Above', 'Unknown'])
battery_capacity = battery_dict[battery_capacity].lower()

# RAM 
# ['2gb-4gb', '5gb-8gb', '<2gb', '>8gb', 'unknown']
ram_dict = {
    'Less than 2GB': '<2gb',
    '2GB - 4GB': '2gb-4gb',
    '5GB - 8GB': '5gb-8gb',
    'More than 8GB': '>8gb',
    'Unknown': 'unknown'
}
ram = st.selectbox('Mobile phone memory', ['Less than 2GB', '2GB - 4GB', '5GB - 8GB',
                                           'More than 8GB', 'Unknown'])
ram = ram_dict[ram].lower()

# rom
# ['256gb', '512gb', '64gb-128gb', '<64gb', 'unknown']
rom_dict =  {
    '< 64GB': '<64gb',
    '64GB - 128GB': '64gb-128gb',
    '256GB': '256gb',
    '512GB': '512gb',
    'Unknown': 'unknown'
}
rom = st.selectbox('Mobile phone storage', ['< 64GB', '64GB - 128GB', '256GB', '512GB', 'Unknown'])
rom = rom_dict[rom].lower()

def predict():
    data = pd.Series([current_price, discount_price, sold, average_rating, rating_count, five_star,
                      four_star, three_star, two_star, one_star, brand, warranty, warranty_type, num_camera, battery_capacity, ram, rom])
    output = None 

    data[-7:] = cat_encoder.transform([data[-7:]])[0]

    output = inauth_model.predict([data])[0]

    if output:
        st.error(f"This mobile phone product is likely a counterfeit model.")
    else:
        st.success(f"This mobile phone product is likely authentic.")


trigger = st.button('Check Mobile Phone Authenticity', on_click=predict, type="primary")








