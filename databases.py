import psycopg2
import mysql.connector as mc
from datetime import datetime


class Database:
    def set_timestamp(self):
        self.timestamp = datetime.now()

    def get_query_time(self):
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
        self.cur.execute(
            'CREATE TEMP TABLE tmp_log AS SELECT * FROM postgres_log WITH NO DATA')
        self.cur.execute(
            'COPY tmp_log FROM \'C:/Program Files/PostgreSQL/13/data/log/logfile.csv\' DELIMITERS \',\' CSV')
        self.cur.execute(
            'INSERT INTO postgres_log SELECT * FROM tmp_log ON CONFLICT DO NOTHING')
        self.cur.execute('DROP TABLE tmp_log')
        query = f'SELECT message FROM postgres_log WHERE log_time >=\'{self.timestamp}\' AND '
        query += f'user_name=\'{self.uconn.info.user}\' AND '
        query += f'database_name=\'{self.uconn.info.dbname}\' AND '
        query += f'process_id={self.pid}'
        self.cur.execute(query)

        return [float(row[0].replace('duration: ', '').replace(' ms', '')) for row in self.cur.fetchall() if 'duration: ' in row[0]]


class MysqlDB(Database):
    def __init__(self, uconn):
        self.pid = uconn.connection_id
        self.db = uconn.database
        self.user = uconn.user
        self.cur = uconn.cursor(buffered=True)
        self.timestamp = datetime.now()

    def get_query_time(self):
        query = f'SELECT query_time FROM mysql.slow_log WHERE user_host LIKE \'{self.user}%\' '
        query += f'AND db = \'{self.db}\' AND thread_id = {self.pid} '
        query += f'AND start_time >= \'{self.timestamp}\''
        self.cur.execute(query)
        return [row[0].microseconds/1000 for row in self.cur]
