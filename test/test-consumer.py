from confluent_kafka import Consumer, KafkaError

# Configura la conexión con el clúster Kafka
conf = {
    'bootstrap.servers': 'localhost:9092',  
    'group.id': 'mi-grupo', 
    'auto.offset.reset': 'earliest'  # Lee desde el principio del tema
}

# Crea un consumidor Kafka
consumer = Consumer(conf)

# Suscríbete al tema al que deseas recibir mensajes
topic = 'mi-tema' 
consumer.subscribe([topic])

# Lee mensajes del tema y procesa
while True:
    msg = consumer.poll(1.0)  # Espera 1 segundo para recibir mensajes
    
    if msg is None:
        continue

    if msg.error():
        if msg.error().code() == KafkaError._PARTITION_EOF:
            print(f"Reached end of partition for topic {msg.topic()} [{msg.partition()}]")
        else:
            print(f"Error: {msg.error()}")
    else:
        print(f"Received message: {msg.value().decode('utf-8')}")

# Cierra el consumidor al final
consumer.close()