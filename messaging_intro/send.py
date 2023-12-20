import sys

import pika

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='hello')
body = ' '.join(sys.argv[1:]) or "Hello World!"

channel.basic_publish(exchange='', routing_key='hello', body=body)
print(f" [x] Sent '{body}'")
connection.close()
