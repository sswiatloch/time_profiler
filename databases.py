import psycopg2
from datetime import datetime


class Database:
    def set_timestamp(self):
        self.timestamp = datetime.now()

    def get_query_time(self):
        pass


class DatabaseFactory:
    def create(self, conn, type):
        pass


class PostgresDB(Database):
    def __init__(self, uconn):
        self.pid = uconn.get_backend_pid()
        params = uconn.info.dsn_parameterts
        self.conn = psycopg2.connect(database=uconn.info.dbname, user=uconn.info.user,
                                     password=uconn.info.password, host=uconn.info.host, port=uconn.info.port)
        self.timestamp = datetime.now()

    def get_query_time(self):
        return None


class MysqlDB(Database):
    pass
