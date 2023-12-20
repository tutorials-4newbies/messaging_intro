import time

import pika, sys, os


def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='hello')

    def callback(ch, method, properties, body):
        print(f" [x] Received {body.decode()}")
        sleep_time = body.count(b'.')
        print(f"Sleep seconds: {sleep_time}")
        time.sleep(sleep_time)
        # TODO manual ack ch.ack(delivery_tag=method.delivery_tag)

    channel.basic_consume(queue='hello', on_message_callback=callback, auto_ack=True)
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
