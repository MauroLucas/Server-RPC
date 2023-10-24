import time
from confluent_kafka import Consumer, KafkaError
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import json

db = psycopg2.connect(
    user="postgres",
    password="root",
    host="localhost",
    port='5432',
    database="chefencasa"
)

cursor = db.cursor()

tiempo = 60


consumer_config = {
        'bootstrap.servers': 'localhost:9092',
        'group.id': 'comentarios-consumer',
        'auto.offset.reset': 'earliest'
    }

consumer = Consumer(consumer_config)
consumer.subscribe(['Comentarios'])

def run_consumer():      


    def handle_message(message):
        print(f"Mensaje recibido en 'Comentarios': {message.value().decode('utf-8')}")
        message_data = json.loads(message.value().decode('utf-8'))

        try:
            usuario = message_data['nombre_usuario']
            titulo_receta = message_data['titulo_receta']
            comentario = message_data['comentario']

            query_user = "SELECT id FROM users WHERE username = '{0}'".format(usuario)
            cursor.execute(query_user)
            result = cursor.fetchone() 
            id_usuario = result[0]
            print("id usuario:" + str(id_usuario))
            query_recipe = "SELECT id FROM recipes WHERE title = '{0}'".format(titulo_receta) 
            cursor.execute(query_recipe)
            result = cursor.fetchone() 
            id_receta = result[0]
            print("id receta:" + str(id_usuario))

            query_insert_comment = "INSERT INTO recipe_comments (id_user,id_recipe,comment) VALUES('{0}','{1}','{2}')".format(id_usuario,id_receta,comentario)
            cursor.execute(query_insert_comment)
            db.commit()
            print("Mensaje insertado en la base de datos.")

        except json.JSONDecodeError as e:
            print(f"Error al decodificar el mensaje JSON: {str(e)}")
        except KeyError as e:
            print(f"Error al acceder a las claves del mensaje JSON: {str(e)}")
        except Exception as e:
            print(f"Error al insertar en la base de datos: {str(e)}")
    
    contador = 0
    while True:
        msg = consumer.poll(1) # Espera 1 segundo por mensaje
        
        if msg is None:
            contador = contador + 1
            if(contador>5):
                break
            continue
            
            
        if msg.error():
            if msg.error().code() == KafkaError._PARTITION_EOF:
                print('Llegamos al final de la partición en Comentarios')
                break  # Salir del bucle cuando llegamos al final de la partición
            else:
                print(f'Error en el consumidor de Comentarios: {msg.error().str()}')
        else:
            handle_message(msg)

if __name__ == "__main__":
    while True:
        print("Persistir Comentarios de la cola de Comentarios")
        run_consumer()
        print("Esperando " + str(tiempo) + " segundos")
        time.sleep(tiempo)
    