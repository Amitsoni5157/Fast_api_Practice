from fastapi import FastAPI
from models import Product

app = FastAPI()

@app.get("/")
def greet():
    return "Wellcom to Telusko Trac"

products =[
    Product(id=1, name="Mobile Phone", description="Samsung galaxy S 23 mobile", price=100, quantity=10),
    Product(id=2, name="Laptop", description="here is very good laptop", price=1000, quantity=5),
    Product(id=3, name="Speaker", description="it is 5 star jbl speaker", price=500, quantity=7),
    Product(id=4, name="Mouse", description="here it is mouse bluetooth mouse", price=10, quantity=20),
    Product(id=5, name="charger", description="it is fast laptop charger", price=200, quantity=13)
]

@app.get("/products")
def get_all_products():
    return products

@app.get("/product/{id}")
def get_product_by_id(id: int):
    for product in products:
        if product.id == id:
            return product

    return "product not found"

@app.post("/product")
def add_product(product: Product):
    products.append(product)
    return product

@app.put("/product")
def update_product(id: int, product: Product):
    for i in range(len(products)):
        if products[i].id == id:
            products[i] = product
            return "Product Added successfully"

    return "No product found"

@app.delete("/product")
def delete_product(id: int):
    for i in range(len(products)):
        if products[i].id == id:
            del products[i]
            return "Product Deleted"
            
    return "Product not found"
