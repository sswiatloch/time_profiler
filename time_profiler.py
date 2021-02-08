from enum import Enum
import databases as db
from functools import update_wrapper
import time


class DBTypes(Enum):
    POSTGRES = 1
    MYSQL = 2


class DatabaseFactory:
    @staticmethod
    def create(conn, dbtype, password=''):
        if dbtype == DBTypes.POSTGRES:
            return db.PostgresDB(conn)
        elif dbtype == DBTypes.MYSQL:
            return db.MysqlDB(conn, password)


class TimeProfilerMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class TimeProfiler(metaclass=TimeProfilerMeta):
    def __init__(self):
        self.logs = []

    def register_connection(self, conn, dbtype, password=''):
        self.db = DatabaseFactory.create(conn, dbtype, password='')

    def register_time(self, func_name, time, reg_type):
        self.logs.append((func_name, time, reg_type))

    def show_logs(self):
        for log in self.logs:
            print(log)


class TimeQuerry:
    def __init__(self, func):
        update_wrapper(self, func)
        self.func = func
        self.tprof = TimeProfiler()

    def __call__(self, *args, **kwargs):
        if self.tprof.db is None:
            print("There is no connection registered! Failed to time query/queries")
            return self.func(*args, **kwargs)
        else:
            self.tprof.db.set_timestamp()
            value = self.func(*args, **kwargs)
            times = self.tprof.db.get_query_time()
            for time in times:
                print(f"Query in {self.func.__name__!r} finished in {time}")
            return value


class TimeExecution:
    def __init__(self, func):
        update_wrapper(self, func)
        self.func = func
        self.tprof = TimeProfiler()

    def __call__(self, *args, **kwargs):
        start_time = time.perf_counter()
        value = self.func(*args, **kwargs)
        end_time = time.perf_counter()
        run_time = end_time - start_time
        print(f"Finished {self.func.__name__!r} in {run_time:.4f} secs")
        return value


if __name__ == "__main__":
    print("yay!")
