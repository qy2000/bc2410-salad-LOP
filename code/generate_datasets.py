"""
Generate Demand Dataset using Kaggle Data

Using Kaggle Store Item Demand Dataset, we replaced the item ID with SaladStop's ingredient names to generate a simulated demand dataset
Kaggle Data: https://www.kaggle.com/competitions/demand-forecasting-kernels-only/data?select=train.csv
"""

'''
Import libraries
'''
import pandas as pd

'''
Import dataset from kaggle
'''
df = pd.read_csv("../data/train.csv")

'''
Clean dataset appropriately
'''
df = df[df["store"] == 1]
df = df.drop(columns=["store"])
newf = df.pivot(index='date', columns='item')
df = df.set_index('date')
newf.columns = newf.columns.droplevel(0)
df15 = newf.iloc[:, 10:25]
df22 =  newf.iloc[:, 16:38]
df = pd.concat([newf, df15, df22], axis=1)

'''
Set dataset columns to the list of ingredients offered by Salad Stop
'''
df.columns = list(pd.read_csv("../data/menu.csv").Ingredient)[:-1]

'''
Restructure final dataset
'''
temp = df["Red & White Cabbage"]
df["Red & White Cabbage"] = df["Tomato Wrap"]
df["Tomato Wrap"] = df["Baby Spinach"]
df["Spinach Wrap"] = df["Olive Oil"]

'''
Export final dataset for ingredient demand over a period of time
'''
df.to_csv("../data/demand_kaggle.csv")



"""
Generate Purchase likelihood based on number of items on menu Dataset using Faker python library and weighted randomness
"""

'''
Import libraries
'''
import random
from faker import Faker
import numpy as np
SEED = 0
Faker.seed(SEED)
np.random.seed(SEED)
random.seed(SEED)

'''
Use python's Faker libary to artificially generate fake data.
'''
fake = Faker()

'''
Fake Restaurant Names obtained from https://businessnamegenerator.com/restaurants-business-name-generator-ideas/
'''
restaurant_names = ["Bistro Bazaar","Bistro Captain","Bistroporium","Cuisine Street","Cuisine Wave","Deli Divine","Deli Feast","Eatery Hotspot","Eateryworks","Feast Lounge","Feast Palace","Grub Chef","Grub lord","Kitchen Sensation","Kitchen Takeout","Menu Feed","Menu Gusto","Munchies","Munch Grill","Munchtastic","Island Grill","Flavoroso","Green Curry","El Pirata Porch","Sweet Escape","Salty Squid","Bangalore Spices","Pancake World","Veganic Corner","Masala","Grassfed Grill","Greenanic Smoothies","Freddy’s Stove","Grandma’s Sweets","Spicella Spanish Kitchen","Xin Chao Vietnamese Restaurant","Paterro's Kitchen","Mediterra Seafood","Street Deli","Whispering Bamboo"]

'''
Randomly populate number of menu items for each of the restaurant
'''
restaurant_number_of_items = [random.randint(1, 40) for _ in range(len(restaurant_names))]

'''
Weighted function which returns whether there was a purchase based on the number of items on the menu.
'''
def random_there_was_a_purchase_generator(num_of_items_on_menu):
    if 1 <= num_of_items_on_menu <= 3:
        return np.random.choice([0, 1], 1, p=[0.95, 0.05])[0]
    
    if 4 <= num_of_items_on_menu <= 5:
        return np.random.choice([0, 1], 1, p=[0.9, 0.1])[0]
    
    elif 6 <= num_of_items_on_menu <= 8:
        return np.random.choice([0, 1], 1, p=[0.05, 0.95])[0]
    
    elif 9 <= num_of_items_on_menu <= 11:
        return np.random.choice([0, 1], 1, p=[0.05, 0.95])[0]
    
    elif 12 <= num_of_items_on_menu <= 14:
        return np.random.choice([0, 1], 1, p=[0.9, 0.1])[0]
    
    elif 15 <= num_of_items_on_menu <= 17:
        return np.random.choice([0, 1], 1, p=[0.9, 0.1])[0]
    
    elif 18 <= num_of_items_on_menu <= 20:
        return np.random.choice([0, 1], 1, p=[0.9, 0.1])[0]
    
    elif 21 <= num_of_items_on_menu <= 25:
        return np.random.choice([0, 1], 1, p=[0.95, 0.05])[0]
    
    elif 26 <= num_of_items_on_menu <= 30:
        return np.random.choice([0, 1], 1, p=[0.95, 0.05])[0]
    
    elif 31 <= num_of_items_on_menu <= 40:
        return np.random.choice([0, 1], 1, p=[0.9995, 0.0005])[0]
    else:
        return np.random.choice([0, 1], 1, p=[0.9995, 0.0005])[0]

'''
Creating a fake dataset based on our faked data and variables
'''
def generate_fake_dataset():

    res_name = restaurant_names[random.randint(0, 39)]
    res_num_items = restaurant_number_of_items[restaurant_names.index(res_name)]
    is_purchase = random_there_was_a_purchase_generator(res_num_items)
    
    return {
        "UUID": "ID-{}".format(fake.credit_card_number()[1:10]),
        "Name": fake.name(),
        "Restaurant Visited": res_name,
        "Number of items on menu": res_num_items,
        "Purchase": is_purchase
    }

'''
Export final dataset
'''
df = pd.DataFrame([generate_fake_dataset() for _ in range(1000)])
df.to_csv('../data/faked_purchase_dataset.csv') 