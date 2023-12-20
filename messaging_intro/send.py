import pika

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='hello')
print("Please input your message")
body = input("")
channel.basic_publish(exchange='', routing_key='hello', body=body)
print(f" [x] Sent '{body}'")
connection.close()
