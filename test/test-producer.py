from confluent_kafka import Producer

# Configura la conexión con el clúster Kafka
conf = {
    'bootstrap.servers': 'localhost:9092',  
}

# Crea un productor Kafka
producer = Producer(conf)

# Define el nombre del tema al que quieres enviar mensajes
topic = 'mi-tema'  

# Envia un mensaje al tema
mensaje = "Hola, Kafka!"
producer.produce(topic=topic, value=mensaje)

# Espera a que todos los mensajes pendientes se entreguen y se confirme su recepción
producer.flush()