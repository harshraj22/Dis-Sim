from kafka import KafkaConsumer
import json
import os
import base64
import numpy as np

# ------------------------------
os.environ['KAFKA_TOPIC'] = "DATA_MONITOR"

# -----------------------------

def main():
    print("Listening *****************")

    consumer = KafkaConsumer(
        os.getenv("KAFKA_TOPIC"),
        bootstrap_servers=['broker:29092'],
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        group_id='mygroup',
        api_version=(2, 0, 2) # https://stackoverflow.com/a/56449512/10127204
    )

    while True:    
        for msg in consumer:

            payload = json.loads(msg.value)
            # payload["meta_data"]={
            #     "topic":msg.topic,
            #     "partition":msg.partition,
            #     "offset":msg.offset,
            #     "timestamp":msg.timestamp,
            #     "timestamp_type":msg.timestamp_type,
            #     "key":msg.key,
            # }
            img1 = payload['img1']
            img2 = payload['img2']

            img1 = base64.b64decode(img1)
            img2 = base64.b64decode(img2)

            img1 = np.frombuffer(img1, dtype=np.uint8)
            img2 = np.frombuffer(img2, dtype=np.uint8)

            img1_avg = np.mean(img1)
            img2_avg = np.mean(img2)
            print(f'Average Pixel Value of img1: {img1_avg}, Average Pixel Value of img2: {img2_avg}')


print(f'------------------Starting Monitoring----------------')
main()