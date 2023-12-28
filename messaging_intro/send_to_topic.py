import sys

import pika

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()
channel.exchange_declare(exchange='library', exchange_type='topic')

body = sys.argv[1] or "Hello World!"
routing_key = sys.argv[2]
print(f"sending to {routing_key}")

channel.basic_publish(exchange='library',
                      routing_key=routing_key,
                      body=body.encode('utf-8'))
print(f" [x] Sent '{body}'")
connection.close()
