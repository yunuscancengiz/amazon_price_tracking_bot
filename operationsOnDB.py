from productsDB import *
import datetime

productsdb = ProductsDB()
today = datetime.date.today()
print("""
**********************************
Veritabanı İşlemleri
----------------------------
1) Ürünleri göster
2) Ürün ekle
3) Ürün sil
4) Fiyatı güncelle
5) Fiyatı göster
6) Ürün ara

q) ÇIKIŞ
**********************************
""")

while True:
    operation = input("İşlem seç: ")

    if(operation == "q"):
        print("Program kapatılıyor...")
        break

    elif(operation == "1"):
        productsdb.showProducts()

    elif(operation == "2"):
        product_name = input("Ürün Adı: ")
        product_title = input("Başlık: ")
        price = input("Fiyat: ")
        product_url = input("Link: ")
        date = today

        new_product = Product(product_name, product_title, price, product_url, date)
        productsdb.addProduct(new_product)
        print("Ürün eklendi...")

    elif(operation == "3"):
        product_name = input("Ürün adı: ")
        check_decision = input("Ürünü silmek istediğine emin misin?(y/n): ")
        if(check_decision == "y"):
            productsdb.deleteProduct(product_name)
            print("Ürün silindi...")
        elif(check_decision == "n"):
            print("Ürün silinmedi...")
        else:
            print("Geçersiz giriş yapıldı lütfen sadece y veya n giriniz...")

    elif(operation == "4"):
        try:
            product_url = input("Link: ")
            new_price = input("Yeni fiyat: ")
            productsdb.upgradePrice(product_url, new_price, today)
            print("Fiyat güncellendi...")
        except:
            print("Ürün veritabanında bulunamadı...")

    elif(operation == "5"):
        product_url = input("Link: ")
        price = productsdb.showPrice(product_url)
        print(price)
    
    elif(operation == "6"):
        product_url = input("Link: ")
        prod = productsdb.searchProduct(product_url)
        print(prod)

    else:
        print("Geçersiz işlem...")