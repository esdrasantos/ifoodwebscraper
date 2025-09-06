from bs4 import BeautifulSoup
from typing import List
from typing import Iterable
from dataclasses import asdict
import os
import re
import pandas as pd
from order_data import Order
from order_data import Item

class OrderParser:

    @staticmethod
    def fetch_orders(paths: Iterable[str]) -> List[Order]:

        orders = []

        for path in paths:

            items = []

            with open(path, "r", encoding="utf-8") as f:
                soup = BeautifulSoup(f, "html.parser")

                restaurant = soup.select_one("h2.order-details-header__title").get_text(strip=True)
                total = soup.select_one("p.order-details-value span:nth-of-type(2)").get_text(strip=True)
                id = soup.select_one("p.order-details-footer-info span:nth-of-type(2)").get_text(strip=True)

                for li in soup.select("li.order-details-item"):

                    qty_name = li.select_one("div.order-details-item__infos span:nth-of-type(1)").get_text(strip=True)
                    price = li.select_one("div.order-details-item__infos span:nth-of-type(2)").get_text(strip=True)
                    obs_tag = li.select_one("div.order-details-cart__observation")
                    obs = obs_tag.get_text(strip=True) if obs_tag else None

                    match = re.match(r'(\d+)x\s+(.+)', qty_name)
                    qty = 1
                    name = qty_name

                    if match:
                        qty = int(match.group(1))
                        name = match.group(2)

                    item = Item(name=name, price=price, quantity=qty, obs=obs)
                    items.append(item)
            
            order = Order(id=id, restaurant=restaurant, total=total, items=items)
            orders.append(order)
        
        return orders

folder = r'orders'
files = [f'{folder}/{f}' for f in os.listdir(folder)]
orders = OrderParser.fetch_orders(paths=files)
orders_dict = [asdict(order) for order in orders]

df = pd.json_normalize(
    orders_dict,
    record_path='items',
    meta=['id', 'restaurant', 'total'],
    errors='ignore'
)
df.sort_values(by='id', inplace=True)
df = df[['id','restaurant','name','price','quantity','obs','total']]
         
df.to_csv('marketorders.csv', index=False, encoding='utf-8-sig')