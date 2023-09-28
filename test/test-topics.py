from confluent_kafka.admin import AdminClient, NewTopic

# Configura la conexión con el clúster Kafka
conf = {
    'bootstrap.servers': 'localhost:9092',  
}

# Crea un cliente de administración Kafka
admin_client = AdminClient(conf)

# Obtiene la lista de temas existentes
topics = admin_client.list_topics().topics

# Imprime la lista de temas
print("Lista de temas:")
for topic in topics:
    print(topic)

