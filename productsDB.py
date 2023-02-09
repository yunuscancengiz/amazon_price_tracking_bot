import sqlite3

class Product():

    def __init__(self, product_name, product_title, price, product_url, date):
        self.product_name = product_name
        self.product_title = product_title
        self.price = price
        self.product_url = product_url
        self.date = date

    def __str__(self):
        return "Ürün adı: {}\nBaşlık: {}\nFiyat: {}\nÜrün linki: {}\nTarih: {}\n".format(self.product_name, self.product_title, self.price, self.product_url, self.date)

class ProductsDB():

    def __init__(self):
        self.createConnection()
    
    def createConnection(self):
        self.connection = sqlite3.connect("AmazonProducts.db")
        self.cursor = self.connection.cursor()
        query = "CREATE TABLE IF NOT EXISTS Products(İsim TEXT, Başlık TEXT, Fiyat REAL, Link TEXT, Tarih TEXT)"
        self.cursor.execute(query)
        self.connection.commit()

    def disconnect(self):
        self.connection.close()

    def showProducts(self):
        query = "SELECT * FROM Products"
        self.cursor.execute(query)

        my_products = self.cursor.fetchall()

        if(len(my_products) == 0):
            print("Veritabanında hiç ürün yok!")

        else:
            for i in my_products:
                product = Product(i[0], i[1], i[2], i[3], i[4])
                print(product)

    def addProduct(self, product):
        query = "INSERT INTO Products (İsim, Başlık, Fiyat, Link, Tarih) VALUES(?, ?, ?, ?, ?)"
        self.cursor.execute(query, (product.product_name, product.product_title, product.price, product.product_url, product.date))
        self.connection.commit()

    def deleteProduct(self, product):
        query = "DELETE FROM Products WHERE İsim = ?"
        self.cursor.execute(query, (product,))
        self.connection.commit()

    def upgradePrice(self, product, price, date):
        query = "SELECT * FROM Products WHERE Link = ?"
        self.cursor.execute(query, (product,))
        products = self.cursor.fetchall()
        
        #price = products[0][2]
        #price = input("Yeni fiyat: ")
        query2 = "UPDATE Products SET Fiyat = ? WHERE Link = ?"
        self.cursor.execute(query2, (price, product))
        query3 = "UPDATE Products SET Tarih = ? WHERE Link = ?"
        self.cursor.execute(query3, (date, product))
        self.connection.commit()
        
    def showPrice(self, product):
        query = "SELECT Fiyat FROM Products WHERE Link = ?"
        self.cursor.execute(query, (product,))
        the_product = self.cursor.fetchall()

        if(len(the_product) == 0):
            print("Bu ürün veritabanında yok!")
        else:
            price = the_product[0][0]
            return price

    def searchProduct(self, product):
        query = "SELECT * FROM Products WHERE Link = ?"
        self.cursor.execute(query, (product,))
        the_product = self.cursor.fetchall()

        if(len(the_product) == 0):
            return False
        else:
            product = Product(the_product[0][0], the_product[0][1], the_product[0][2], the_product[0][3], the_product[0][4])
            print(product)

    
