import psycopg2
import mysql.connector as mc
from datetime import datetime, timedelta


class Database:
    # Interface used to query a database for query time.  
    def set_timestamp(self):
        self.timestamp = datetime.now()

    def get_query_time(self):
        pass


class PostgresDB(Database):
    # Implementation for PostgreSQL
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
    
    # def _cursor_decorator(self, func):
    #     def inner_wrapper(*args, **kwargs):
    #         cursor = func(*args, **kwargs)
    #         cursor.execute = self._execute_decorator(cursor.execute)
    #         return cursor
    #     return inner_wrapper


    # def _execute_decorator(self, func):
    #     def inner_wrapper(query, vars=None):
    #         func(query+' -- token', vars)
    #     return inner_wrapper

class MysqlDB(Database):
    # Implementation for MySQL
    def __init__(self, uconn):
        uconn.cursor = self._cursor_decorator(uconn.cursor)
        self.pid = uconn.connection_id
        self.db = uconn.database
        self.user = uconn.user
        self.cur = uconn.cursor(buffered=True)
        self.timestamp = datetime.now()

    def get_query_time(self):
        query = f'SELECT query_time FROM mysql.slow_log WHERE user_host LIKE \'{self.user}%\' '
        query += f'AND db = \'{self.db}\' AND thread_id = {self.pid} '
        query += f'AND start_time >= \'{self.timestamp}\''# ORDER BY start_time DESC LIMIT 1'
        query += f'AND CONVERT(sql_text USING utf8) LIKE \'%#token\''
        self.cur.execute(query)
        return [row[0] / timedelta(microseconds=1)/1000 for row in self.cur]

    def _cursor_decorator(self, func):
        def inner_wrapper(*args, **kwargs):
            cursor = func(*args, **kwargs)
            cursor.execute = self._execute_decorator(cursor.execute)
            return cursor
        return inner_wrapper


    def _execute_decorator(self, func):
        def inner_wrapper(operation, params=None, multi=False):
            return func(operation+' #token', params, multi)
        return inner_wrapper
