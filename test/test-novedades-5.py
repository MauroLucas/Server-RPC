from confluent_kafka import Consumer, KafkaError
import time
import datetime
import json

# Obtiene la marca de tiempo actual en milisegundos
timestamp_ms = int(time.time() * 1000)

# Concatena el timestamp al group.id
group_id = f'novedades-consumer-{timestamp_ms}'

consumer_config = {
    'bootstrap.servers': 'localhost:9092',
    'group.id': group_id,
    'auto.offset.reset': 'earliest'
}

consumer = Consumer(consumer_config)
consumer.subscribe(['Novedades'])

# Lista para almacenar datos JSON
data_list = []

try:
    contador = 0
    while True:
        msg = consumer.poll(1.0)  # Espera 1 segundo por mensajes nuevos

        if msg is None:
            if(contador > 4):
                break
            contador = contador + 1
            continue
        if msg.error():
            if msg.error().code() == KafkaError._PARTITION_EOF:
                print('Llegamos al final de la partición en Novedades')
            else:
                print(f'Error en el consumidor de Novedades: {msg.error().str()}')
        else:
            # Procesa el mensaje aquí
            mensaje = json.loads(msg.value().decode("utf-8"))
            print(f'Mensaje recibido en Novedades: {mensaje}')
            
            # Obtiene el valor del encabezado "timestamp"
            headers = msg.headers()
            timestamp = None
            for header in headers:
                if header[0] == "timestamp":
                    timestamp = header[1].decode("utf-8")
                    break
            
            if timestamp is not None:
                # Crea un diccionario JSON con los datos
                data = {
                    "Usuario": mensaje["Usuario"],
                    "title": mensaje["title"],
                    "URL Foto": mensaje["URL Foto"],
                    "timestamp": timestamp
                }
                
                # Agrega el diccionario a la lista
                data_list.append(data)
                
                # Ordena la lista por timestamp de mayor a menor
                data_list = sorted(data_list, key=lambda x: x["timestamp"], reverse=True)
                
                # Limita la lista a los 5 datos más recientes
                data_list = data_list[:5]

except KeyboardInterrupt:
    pass

finally:
    consumer.close()

# Imprime la lista de datos JSON
print(json.dumps(data_list, indent=4))



