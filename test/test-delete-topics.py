from confluent_kafka.admin import AdminClient


admin_config = {
    'bootstrap.servers': 'localhost:9092',  
}

topics_to_delete = ['Novedades', 'PopularidadUsuario', 'PopularidadReceta', 'Comentarios']

admin_client = AdminClient(admin_config)

# Elimina los topics
for topic_to_delete in topics_to_delete:
    existing_topics = admin_client.list_topics()
    if topic_to_delete in existing_topics.topics:
        admin_client.delete_topics([topic_to_delete])
        print(f"El topic '{topic_to_delete}' ha sido eliminado con éxito.")
    else:
        print(f"El topic '{topic_to_delete}' no existe y no se puede eliminar.")