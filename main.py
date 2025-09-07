from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import os
import json

with open("parameters.json", "r") as f:
    params = json.load(f)

output_dir = "orders"
os.makedirs(output_dir, exist_ok=True)

orders = params["ordersurl"]

options = webdriver.ChromeOptions()
options.binary_location = params["bin-location"]

userdatadir = os.path.expandvars(params["user-data-dir"])
options.add_argument(f"user-data-dir={userdatadir}")

profiledir = params["profile-dir"]
options.add_argument(f"profile-directory={profiledir}")

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

for url in orders:
    driver.get(url)
    time.sleep(5)
    html = driver.page_source
    orderid = url.split("/")[-1]
    filepath = os.path.join(output_dir, f"order_{orderid}.html")

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(html)

        print(f"✅ Order {orderid} saved in {filepath}")

driver.quit()
