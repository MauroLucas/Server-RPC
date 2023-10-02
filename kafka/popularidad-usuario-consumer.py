import time
from confluent_kafka import Consumer, KafkaError
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import json
tiempo = 60 #segundos


db = psycopg2.connect(
    user="postgres",
    password="root",
    host="localhost",
    port='5432',
    database="chefencasa"
)

cursor = db.cursor()

consumer_config = {
        'bootstrap.servers': 'localhost:9092',
        'group.id': 'popularidad-user-consumer',
        'auto.offset.reset': 'earliest'
    }

consumer = Consumer(consumer_config)
consumer.subscribe(['PopularidadUsuario'])

def run_consumer():
  

    def handle_message(message):
        print(f"Mensaje recibido en 'PopularidadUsuario': {message.value().decode('utf-8')}")
        message_data = json.loads(message.value().decode('utf-8'))
        try:
            nombreUsuario = message_data['nombreUsuario']
            Puntaje = message_data['Puntaje']   
            print("id receta " + str(nombreUsuario))
            print("puntaje " + str(Puntaje))         
            
            query_user_id = "SELECT u.id FROM users as u WHERE u.username = '{0}'".format(nombreUsuario)
            cursor.execute(query_user_id)
            id_user = cursor.fetchone()[0]

            query_insert = "INSERT INTO user_popularity (id_user,popularity) VALUES('{0}','{1}')".format(id_user,Puntaje)
            cursor.execute(query_insert)
            db.commit()
            print("Mensaje insertado en la base de datos.")
            #Actualizo la receta
            print("Actualizar popularidad usuario")
            query_update_user = "UPDATE users set popularity = (SELECT SUM(popularity) FROM user_popularity WHERE id_user = '{0}') WHERE id = '{1}'".format(id_user,id_user)
            cursor.execute(query_update_user)
            db.commit()
        except json.JSONDecodeError as e:
            print(f"Error al decodificar el mensaje JSON: {str(e)}")
        except KeyError as e:
            print(f"Error al acceder a las claves del mensaje JSON: {str(e)}")
        except Exception as e:
            print(f"Error al insertar en la base de datos: {str(e)}")



    contador = 0
    while True:
        msg = consumer.poll(1) #segundos
        if msg is None:
            if(contador>5):
                print("Se procesaron todos los datos")
                break
            contador = contador + 1
            continue
        if msg.error():
            if msg.error().code() == KafkaError._PARTITION_EOF:
                print('Llegamos al final de la partición en PopularidadReceta')
            else:
                print(f'Error en el consumidor de PopularidadReceta: {msg.error().str()}')
        else:
            handle_message(msg)

if __name__ == "__main__":
    while True:
        print("Persistir datos de popularidad")
        run_consumer()
        print("Esperando " + str(tiempo) + " segundos")
        time.sleep(tiempo)