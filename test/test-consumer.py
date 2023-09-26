from confluent_kafka import Consumer, KafkaError

# Configura la conexión con el clúster Kafka
def create_consumer(topic):
    conf = {
        'bootstrap.servers': 'localhost:9092',
        'group.id': 'mi-grupo',
        'auto.offset.reset': 'earliest'  # Lee desde el principio del tema
    }

    # Crea un consumidor Kafka
    consumer = Consumer(conf)

    # Suscríbete al tema al que deseas recibir mensajes
    consumer.subscribe([topic])

    return consumer

def main():
    # Solicita al usuario que ingrese el nombre del topic
    topic = input("Ingresa el nombre del topic: ")

    # Crea el consumidor utilizando el nombre del topic proporcionado por el usuario
    consumer = create_consumer(topic)

    # Lee mensajes del tema y procesa
    try:
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
                # Imprime el valor del mensaje
                print(f"Received message: {msg.value().decode('utf-8')}")

                # Imprime los encabezados del mensaje
                if msg.headers():
                    print("Headers:")
                    for header in msg.headers():
                        print(f"  {header[0]}: {header[1].decode('utf-8')}")

    except KeyboardInterrupt:
        pass
    finally:
        # Cierra el consumidor al final
        consumer.close()

if __name__ == '__main__':
    main()