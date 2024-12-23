import redis
import os

from dotenv import load_dotenv

load_dotenv()

class RedisClient:
    def __init__(self, host='localhost', port=6379, db=0):
        """
        Inicializa el cliente de Redis.
        
        :param host: Dirección del servidor Redis (por defecto: localhost).
        :param port: Puerto del servidor Redis (por defecto: 6379).
        :param db: Base de datos de Redis (por defecto: 0).
        """
        try:
            self.client = redis.StrictRedis(
                host=host,
                port=port,
                db=db,
                decode_responses=True  # Decodifica respuestas a strings (UTF-8)
            )
            # Verifica la conexión
            self.client.ping()
            print(f"Conexión exitosa a Redis en {host}:{port}, DB: {db}")
        except redis.ConnectionError as e:
            print(f"Error al conectar con Redis: {e}")
            raise

    def set(self, key, value, ex=None):
        """
        Guarda un valor en Redis.
        
        :param key: Clave del dato.
        :param value: Valor a almacenar.
        :param ex: Tiempo de expiración en segundos (opcional).
        """
        self.client.set(key, value, ex=ex)

    def get(self, key):
        """
        Obtiene un valor desde Redis.
        
        :param key: Clave del dato.
        :return: Valor asociado a la clave o None si no existe.
        """
        return self.client.get(key)

    def delete(self, key):
        """
        Elimina un valor de Redis.
        
        :param key: Clave del dato a eliminar.
        """
        self.client.delete(key)

    def exists(self, key):
        """
        Verifica si una clave existe en Redis.
        
        :param key: Clave a verificar.
        :return: True si la clave existe, False en caso contrario.
        """
        return self.client.exists(key)

    def increment(self, key, amount=1):
        """
        Incrementa el valor de una clave numérica en Redis.
        
        :param key: Clave del dato.
        :param amount: Cantidad a incrementar (por defecto: 1).
        :return: Nuevo valor después del incremento.
        """
        return self.client.incr(key, amount)

    def keys(self, pattern='*'):
        """
        Lista todas las claves que coinciden con un patrón.
        
        :param pattern: Patrón de búsqueda (por defecto: '*').
        :return: Lista de claves que coinciden.
        """
        return self.client.keys(pattern)

    def flushdb(self):
        """
        Limpia todos los datos de la base de datos actual.
        """
        self.client.flushdb()
        print("Base de datos actual limpiada.")


redis_manager = RedisClient(host=os.getenv("REDIS_HOST"), port=os.getenv("REDIS_PORT"), db=os.getenv("REDIS_DB"))  



if __name__ == "__main__":
    # Conexión al servidor Redis

    # Operaciones básicas
    redis_manager.set("nombre", "Charly", ex=60)  # Guarda un valor con expiración de 60 segundos
    print(redis_manager.get("nombre"))  # Recupera el valor de la clave "nombre"

    redis_manager.increment("contador")  # Incrementa el valor de "contador"
    print(redis_manager.get("contador"))  # Imprime el valor del contador

    print(redis_manager.exists("nombre"))  # Verifica si la clave "nombre" existe

    redis_manager.delete("nombre")  # Elimina la clave "nombre"
    print(redis_manager.get("nombre"))  # Intenta recuperar la clave eliminada (debería ser None)
