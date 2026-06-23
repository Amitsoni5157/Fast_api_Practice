from fastapi import Depends, FastAPI
from models import Product
import database_models
from database import session, engine
from database_models import Base
from sqlalchemy.orm import Session
app = FastAPI()

# database_models.metadata.create_all(bind=engine)
Base.metadata.create_all(bind=engine)


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

def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()

def init_db():
    db = session()

    count = db.query(database_models.Product).count

    if count == 0:
        for product in products:
            db.add(database_models.Product(**product.model_dump()))

    db.commit()

init_db()

@app.get("/products")
def get_all_products(db: Session = Depends(get_db)):

    db_products = db.query(database_models.Product).all()

    return db_products

@app.get("/product/{id}")
def get_product_by_id(id: int, db: Session = Depends(get_db)):
    db_product = db.query(database_models.Product).filter(database_models.Product.id == id).first()
    if db_product:
            return db_product
    return "product not found"

@app.post("/product")
def add_product(product: Product, db: Session = Depends(get_db)):
        db.add(database_models.Product(**product.model_dump()))
        db.commit()
        return product

@app.put("/product")
def update_product(id: int, product: Product, db: Session = Depends(get_db)):
     db_product = db.query(database_models.Product).filter(database_models.Product.id == id).first()   
     if db_product:
            db_product.name = product.name
            db_product.description = product.description
            db_product.price = product.price
            db_product.quantity = product.quantity
            db.commit()
            return "Product updated"
     else:
        return "No product found"

@app.delete("/product")
def delete_product(id: int):
    for i in range(len(products)):
        if products[i].id == id:
            del products[i]
            return "Product Deleted"

    return "Product not found"
