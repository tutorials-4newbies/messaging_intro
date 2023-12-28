import time

import pika

import sys, os


def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    queue_name = sys.argv[1]
    topic = sys.argv[2]

    # Note we declare on both sides
    channel.exchange_declare(exchange='library', exchange_type='topic')
    queue = channel.queue_declare(queue_name)

    # Note: we need to tell the queue to listen to a specific exchange
    channel.queue_bind(exchange='library', queue=queue.method.queue, routing_key=topic)

    def callback(ch, method, properties, body):
        # ch.ack(delivery_tag=method.delivery_tag)
        print(dir(properties))
        print(f" [x] Received {body.decode()}")

        ch.basic_ack(delivery_tag=method.delivery_tag)

    #
    channel.basic_consume(queue.method.queue, on_message_callback=callback)

    print(f' [*] Waiting for messages registered for topic {topic}. To exit press CTRL+C')
    channel.start_consuming()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
