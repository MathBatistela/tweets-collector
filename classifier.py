
import pika
from settings import *
import logging

# logger config
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s]: %(message)s",
)

# setting up RabbitMQ config
connection = pika.BlockingConnection(pika.ConnectionParameters(host=HOST))
channel = connection.channel()

# receives the data from queue 
def receiver(ch, method, properties, body):
    text = body.decode('utf-8')

    # classify the tweet by topics keyword and send it to the topic queue
    for topic in TOPICS_LIST:
        if topic in text.lower():
            logging.info(f"Sendind to topic: [{topic}]")
            channel.basic_publish(exchange=EXCHANGE, routing_key=topic, body=body)

if __name__ == '__main__':

    # setting up the queue
    channel.queue_declare(queue=QUEUE)
    channel.basic_consume(queue=QUEUE, on_message_callback=receiver, auto_ack=True)
    channel.exchange_declare(exchange=EXCHANGE, exchange_type='topic')

    # starts consuming from queue
    logging.info(f"Waiting for messages on queue: {QUEUE}")
    channel.start_consuming()
