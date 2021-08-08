import psycopg2


class DBManager:
    def __init__(self, model):
        self._connection = connection = psycopg2.connect(
            host="localhost",
            database="cafe",
            user="postgres",
            password="1234"
        )
        self._cursor = connection.cursor()
        self.model = model

    def create(self):
        table_name = (self.model.__name__).lower()
        self._cursor.execute(
            f"INSERT INTO {table_name}({' ,'.join(self.model.data.keys())}) "
            f"VAlUES ({' ,'.join(map(str, self.model.data.values()))})")
        self._cursor.close()

    def __del__(self):
        self._connection.close()
