from fastapi import FastAPI

from consumer_app.api.order_api import router as order_router
from consumer_app.services.kafka_consumer import start_consumer_in_background

app = FastAPI(title="Order Service (Consumer)")


@app.on_event("startup")
async def startup_event():
    # Start Kafka consumer in a background thread
    start_consumer_in_background()


@app.get("/")
async def root():
    return {"message": "Consumer is up"}


app.include_router(order_router)