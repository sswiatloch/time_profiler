from enum import Enum
import databases as db


class DBTypes(Enum):
    POSTGRES = 1
    MYSQL = 2


class DatabaseFactory:
    @staticmethod
    def create(conn, dbtype):
        if dbtype == DBTypes.POSTGRES:
            return db.PostgresDB(conn)
        elif dbtype == DBTypes.MYSQL:
            return db.MysqlDB(conn)


class TimeProfiler:
    def get_instance(self):
        pass

    def register_connection(self):
        pass

    def reqister_time(self, func_name, time, dbtype):
        pass


class TimeQuerry:
    def __init__(self, func):
        pass

    def __call__(self, *args, **kwargs):
        pass


class TimeExecution:
    def __init__(self, func):
        pass

    def __call__(self, *args, **kwargs):
        pass
