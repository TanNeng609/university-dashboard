import requests
from bs4 import BeautifulSoup
import time

URL="https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"


while True:
    print("sending our robot to the website")
    response= requests.get(URL)


    if response.status_code==200:
        print("Successfully Connected!\n")

        soup= BeautifulSoup(response.text,"html.parser")

        title=soup.find("h1").text

        price=soup.find("p",class_="price_color").text

        print(f"Product: {title}")
        print(f"Current Price: {price}")

        price=price[2:]
        clean_price= float(price)

        if clean_price<55.00:
            print("\n Alert:The price has dropped!!!!!")
        else:
            print("Price is still too high")

        print("Going to sleep check again tmr")
        time.sleep(5)
        

    else:
        print(f"Failed to connect.Error Code:{response.status_code}")