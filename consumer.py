
import pika
from settings import *

# setting up RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

# receives the tweet and show it
def receiver(ch, method, properties, body):
    print(" [x] %r:%r" % (method.routing_key, body.decode('utf-8')))


if __name__ == '__main__':
    channel.exchange_declare(exchange=EXCHANGE, exchange_type='topic')
    result = channel.queue_declare('', exclusive=True)
    queue_name = result.method.queue

    print("-------------------------")
    print("\nSelect a topic:\n")
    for index in range(len(TOPICS_LIST)):
        print(f"\t({index}) {TOPICS_LIST[index]}")
    print("\n")

    # get users topic
    topic = input("Topic > ")
    topic = int(topic)

    # chekcs if it is a valid topic
    if topic in [index for index in range(len(TOPICS_LIST))]:
        
        print(f"\nStarts consuming from topic: {topic}\n")
        # starts consuming from the selected topic
        channel.queue_bind(exchange=EXCHANGE, queue=queue_name, routing_key=TOPICS_LIST[topic])
        channel.basic_consume(queue=queue_name, on_message_callback=receiver, auto_ack=True)
        channel.start_consuming()
    else:
        print("Invalid topic")