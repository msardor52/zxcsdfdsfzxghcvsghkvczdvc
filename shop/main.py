from fastapi import FastAPI

from shop.database import Base, engine
from shop.routers import buyers, products, basket, auth

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(buyers.router)
app.include_router(products.router)
app.include_router(basket.router)
app.include_router(auth.router)


@app.get("/healthy")
def health_check():
    return {"status": "Healthy"}
