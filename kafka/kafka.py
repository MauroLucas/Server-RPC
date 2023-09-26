from confluent_kafka.admin import AdminClient
from confluent_kafka.admin import NewTopic

# Configuración del administrador de Kafka
admin_config = {
    'bootstrap.servers': 'localhost:9092',  # Cambia esto a la dirección y el puerto de tu clúster Kafka
}

# Nombre del topic que deseas verificar
topic_name = 'Novedades'

# Crea un cliente de administración de Kafka
admin_client = AdminClient(admin_config)

# Obtiene los metadatos de los topics existentes
existing_topics = admin_client.list_topics()

# Verifica si el topic ya existe
if topic_name in existing_topics.topics:
    print(f"El topic '{topic_name}' ya existe.")
else:
    # Si el topic no existe, configura y crea el nuevo topic
    new_topic = NewTopic(
        topic_name,
        num_partitions=1,    # Número de particiones
        replication_factor=1  # Factor de replicación
    )

    # Crea el topic
    admin_client.create_topics([new_topic])
    print(f"El topic '{topic_name}' ha sido creado con éxito.")

