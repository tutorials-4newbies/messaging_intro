import sys

import pika

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()
channel.exchange_declare(exchange='events', exchange_type='fanout')

body = ' '.join(sys.argv[1:]) or "Hello World!"

channel.basic_publish(exchange='events',
                      routing_key='',
                      body=body.encode('utf-8'))
print(f" [x] Sent '{body}'")
connection.close()
