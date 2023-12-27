import time

import pika, sys, os


def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    # Note we declare on both sides
    channel.exchange_declare(exchange='events', exchange_type='fanout')
    queue = channel.queue_declare(queue='', exclusive=True, durable=False)
    queue_name = queue.method.queue  # the name is automatically given
    # Note: we need to tell the queue to listen to a specific exchange
    channel.queue_bind(exchange='events', queue=queue_name)

    def callback(ch, method, properties, body):
        # ch.ack(delivery_tag=method.delivery_tag)

        print(f" [x] Received {body.decode()}")
        sleep_time = body.count(b'.')
        print(f"Sleep seconds: {sleep_time}")
        time.sleep(sleep_time)
        ch.basic_ack(delivery_tag=method.delivery_tag)

    #
    channel.basic_consume(queue_name, on_message_callback=callback)
    # TODO: remove auto ack and implement manual ack
    print(' [*] Waiting for messages. To exit press CTRL+C')
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
