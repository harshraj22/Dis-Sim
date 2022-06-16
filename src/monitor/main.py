from kafka import KafkaConsumer
import json
import os
import sys

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

    for msg in consumer:

        payload = json.loads(msg.value)
        payload["meta_data"]={
            "topic":msg.topic,
            "partition":msg.partition,
            "offset":msg.offset,
            "timestamp":msg.timestamp,
            "timestamp_type":msg.timestamp_type,
            "key":msg.key,
        }
        print(payload, end="\n")



if __name__ == "__main__":
    main()