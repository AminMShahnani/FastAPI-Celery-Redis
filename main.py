import time
import os
import logging

from fastapi import FastAPI
from celery import shared_task, Celery

from config import settings

if not os.path.exists('logs'):
    os.makedirs('logs')

logging.basicConfig(filename='logs/app.log', level=logging.INFO, format='%(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


app = FastAPI()

celery = Celery(
    __name__,
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND
)

@celery.task
def send_push_notification(device_token: str):
    logger.info("starting background task")

    time.sleep(10)  # simulates slow network call to firebase/sns
    
    # with open("notification.log", mode="a") as notification_log:
    #     response = f"Successfully sent push notification to: {device_token}\n"
    #     notification_log.write(response)

    try:
        a=11/0 #critical part that may fail, and its analysis is important
        logger.info(f"notification sent {device_token}")
    except Exception as e:
        logger.error(f"exception while division {e}")


@app.get("/push/{device_token}")
async def notify(device_token: str):
    logger.info("sending notification in background")
    send_push_notification.delay(device_token)
    return {"message": "Notification sent"}