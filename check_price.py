import requests
from bs4 import BeautifulSoup
import products
from productsDB import *
import datetime
import emailLoginInfo
import smtplib
import time

today = datetime.date.today()
print(today)

productsdb = ProductsDB()

def sendMail(message):
    sender = "SENDER_EMAIL_HERE"
    receiver = "RECEIVER_EMAIL_HERE"
    email = emailLoginInfo.email
    password = emailLoginInfo.password

    server = smtplib.SMTP("smtp.gmail.com:587")
    server.starttls()
    server.login(email, password)
    server.sendmail(sender, receiver, message)
    server.quit()

    print("\nMAIL GONDERILDI\n")

def check_prices():
    i = 0
    mail_message = ""
    while(i < len(products.product_list)):
        product_url = str(products.product_list[i].values()).split("'")[1]
        product_name = str(products.product_list[i].keys()).split("'")[1]

        headers = {
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.82 Safari/537.36", 
            "X-Amzn-Trace-Id": "Root=1-6209086d-6b68c17b4f73e9d6174b5736"
        }

        r = requests.get(product_url, headers=headers)
        soup = BeautifulSoup(r.content, "lxml")

        title = soup.find("span", attrs={"class":"a-size-large product-title-word-break"}).getText().strip()
        try:
        	price = soup.find("span", attrs={"class":"a-offscreen"}).getText().rstrip(",")
       		new_price = float(price.replace(".", "").replace(",", ".").strip("TL"))
               
        except:
        	price = "Şu an ürün mevcut değil"

        prod = productsdb.searchProduct(product_url)
        if(prod == False):
            new_product = Product(product_name, title, new_price, product_url, today)
            productsdb.addProduct(new_product)
            print("Ürün veritabanına eklendi...")
        else:
            pass

        old_price = productsdb.showPrice(product_url)
        print("Eski fiyat: " + str(old_price))

        if(new_price < old_price):
            print(product_name)
            print(title)
            message = "Fiyat azaldi... Yeni fiyat: " + str(new_price) + " TL" + "\n"
            mail_message += (message + product_url + "\n" + "\n")
            print(message)

            productsdb.upgradePrice(product_url, new_price, today)
            print("Veritabanındaki fiyatı güncellendi...\n")
        elif(new_price > old_price):
            print(product_name)
            print(title)
            message = "Fiyat artti... Yeni fiyat: " + str(new_price) + " TL" + "\n"
            mail_message += (message + product_url + "\n" + "\n")
            print(message)

            productsdb.upgradePrice(product_url, new_price, today)
            print("Veritabanındaki fiyatı güncellendi...\n")
        else:
            message = product_name + "\n" + title + "\n" + "Fiyat değişmedi... Fiyat: " + str(new_price) + " TL" + "\n"
            print(message)

        time.sleep(1.5)

        i += 1

    if(mail_message == ""):
        mail_message = "Fiyati degisen urun yok..."
    print("\n------------------\n" + mail_message)
    sendMail(mail_message)

    
while True:
    check_prices()
    time.sleep(21600)