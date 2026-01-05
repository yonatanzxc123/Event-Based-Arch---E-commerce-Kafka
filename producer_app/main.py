from fastapi import FastAPI
from producer_app.api.order_api import router as orders_router

app = FastAPI(title="Cart Service (Producer)")


@app.get("/")
async def root():
    return {"message": "Producer is up"}


app.include_router(orders_router)
