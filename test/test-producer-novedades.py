from confluent_kafka import Producer
import datetime

# Configuración del productor
producer_config = {
    'bootstrap.servers': 'localhost:9092',  # Cambia esto a la dirección y el puerto de tu clúster Kafka
    'client.id': 'python-producer'
}

# Nombre del topic al que deseas enviar mensajes
topic_name = 'Novedades'

# Datos simulados de una receta
usuario = 'usuario123'
titulo_receta = 'Receta de prueba'
url_foto = 'https://ejemplo.com/foto.jpg'

# Obtén la fecha y hora actual
fecha_hora_actual = datetime.datetime.now()

# Crea un productor Kafka
producer = Producer(producer_config)

# Agrega la marca de tiempo como un encabezado
headers = [('timestamp', str(fecha_hora_actual))]

# Formatea los datos en un mensaje
mensaje_receta = f'Usuario: {usuario}, Título: {titulo_receta}, URL Foto: {url_foto}'

# Envia el mensaje al topic "Novedades" con los encabezados
producer.produce(topic=topic_name, value=mensaje_receta, headers=headers)

# Espera a que todos los mensajes se envíen 
producer.flush()
