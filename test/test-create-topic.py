from kafka import KafkaAdminClient
from kafka.admin import NewTopic

# Configura la conexión con el clúster Kafka
admin_client = KafkaAdminClient(bootstrap_servers='localhost:9092')

# Define el nombre del nuevo topic que deseas crear
topic_name = 'mi-tema'  

# Define las configuraciones para el nuevo topic 
new_topic = NewTopic(
    name=topic_name,
    num_partitions=1,  # Número de particiones
    replication_factor=1  # Factor de replicación
)

# Crea el nuevo topic
admin_client.create_topics([new_topic])

print(f"El topic '{topic_name}' ha sido creado con éxito.")