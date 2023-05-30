from celery import Celery
import base64
import os
from fastapi import Depends, FastAPI
from pydantic import BaseModel
import logging
import mysql.connector

celery_feedback = Celery(
    'result_feedback',
    backend='redis://redis:6379/1',
    broker='redis://redis:6379/1'
)


celery_similarity = Celery(
    'result_similarity',
    backend='redis://redis:6379/0',
    broker='redis://redis:6379/0'
)

# Create a logger instance
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


@celery_feedback.task()
def feedback(task_id: str, response: bool):
    """Saves the user feedback to the database."""
    logger.info(f'Feedback recieved for task_id: {task_id} with response: {response}')

    # ToDo: Save the feedback to the database
    # step 1: Get the images from the redis backend of similarity celery using the task id
    similarity_images = celery_similarity.AsyncResult(task_id).kwargs
    # celery_similarity.backend.get(task_id)

    logger.info(f'Similarity Images: {similarity_images.keys()} having type: {type(similarity_images["img1"])} and length: {len(similarity_images["img1"])}')
    # step 2: connect to the database
    database = mysql.connector.connect(
        host ="feedback_db",
        user ="root",
        passwd ="mypassword",
        database = 'DB',
        port = 3306
    )

    cursor_object = database.cursor()
    # step 3: save the feedback to the database
    # For now, we are saving a part of image1 and image2 to the database. Later they can be saved to a file system and the path can be saved to the database.
    query = f"""INSERT INTO feedback (task_id, response, img1, img2) VALUES ('{task_id}', {response}, '{similarity_images["img1"][:200]}', '{similarity_images["img2"][:200]}')"""

    cursor_object.execute(query)
    database.commit()
    cursor_object.close()
    database.close()

    return True




