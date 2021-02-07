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
        self.uconn = uconn
        self.conn = psycopg2.connect(database=uconn.info.dbname, user=uconn.info.user,
                                     password=uconn.info.password, host=uconn.info.host, port=uconn.info.port)
        self.cur = self.conn.cursor()
        self.timestamp = datetime.now()

    def get_query_time(self):
        self.cur.execute('CREATE TEMP TABLE tmp_log AS SELECT * FROM postgres_log WITH NO DATA')
        self.cur.execute('COPY tmp_log FROM \'C:/Program Files/PostgreSQL/13/data/log/logfile.csv\' DELIMITERS \',\' CSV')
        self.cur.execute('INSERT INTO postgres_log SELECT * FROM tmp_log ON CONFLICT DO NOTHING')
        self.cur.execute('DROP TABLE tmp_log')        
        self.cur.execute(f'SELECT message FROM postgres_log WHERE user_name=\'{self.uconn.info.user}\'')

        return self.cur.fetchall()


class MysqlDB(Database):
    pass
