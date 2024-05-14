from datetime import datetime, UTC

from fastapi import status, Depends, APIRouter, UploadFile
from motor.motor_asyncio import AsyncIOMotorDatabase
import pika

from src import models, oauth2
from src.schemas.videos import VideoCreate, VideoStatus
from src.config import settings
from src.database.mongo import get_mongo_db, get_or_create_collection
from src.message_queue import channel as rabbit_channel


router = APIRouter(prefix="/videos", tags=["Videos"])


@router.post("", status_code=status.HTTP_201_CREATED, response_model=VideoStatus)
async def upload_video(
    upload_file: UploadFile,
    current_user: models.User = Depends(oauth2.get_current_user),
    mongo_db: AsyncIOMotorDatabase = Depends(get_mongo_db),
):
    global settings
    # insert video into MongoDB
    collection = await get_or_create_collection(
        mongo_db, settings.mongo_videos_collection
    )
    video_content = await upload_file.read()
    await upload_file.close()
    video = VideoCreate(
        user_id=current_user.id,
        video_name=upload_file.filename,
        video_content=video_content,
        created_at=datetime.now(UTC),
    )
    result = await collection.insert_one(video.model_dump())

    # insert video ID into RabbitMQ queue
    queue_message = dict(user_id=current_user.id, video_id=str(result.inserted_id))
    rabbit_channel.queue_declare(queue=settings.rabbit_videos_queue, durable=True)
    rabbit_channel.basic_publish(
        exchange="",
        routing_key=settings.rabbit_videos_queue,
        body=queue_message,
        properties=pika.BasicProperties(delivery_mode=pika.DeliveryMode.Persistent),
    )
    return queue_message
