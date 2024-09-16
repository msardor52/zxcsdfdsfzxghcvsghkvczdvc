from fastapi import FastAPI
from database import engine
from routers import products, buyers, basket, auth
import database

app = FastAPI()

database.Base.metadata.create_all(bind=engine)

app.include_router(buyers.router)
app.include_router(products.router)
app.include_router(basket.router)
app.include_router(auth.router)



