from enum import Enum
import databases as db
from functools import update_wrapper
import time
import sys
from functools import partial


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


class TimeProfilerMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class TimeProfiler(metaclass=TimeProfilerMeta):
    def __init__(self):
        self.logs = {}
        self.file = open("log.txt", 'a')

    def register_connection(self, conn, dbtype):
        self.db = DatabaseFactory.create(conn, dbtype)

    def register_time(self, func_name, reg_time, reg_type):
        try:
            self.logs[(func_name, reg_type)].append(reg_time)
        except KeyError:
            self.logs[(func_name, reg_type)] = [reg_time]
        self.file.write(str(func_name)+" " + str(reg_time) + " "+str(reg_type) + "\n")

    def show_logs(self):
        for item in self.logs.items():
            print(item[0])
            for i in item[1]:
                print(i)


class TimeQuery:
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
            for t in times:
                print(f"Query in {self.func.__name__!r} finished in {t} ms")
                self.tprof.register_time(self.func.__name__, t, 'query')
            return value

    def __get__(self, instance, owner):
        return partial(self, instance)


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
        print(f"Finished {self.func.__name__!r} in {run_time:.4f} s")
        self.tprof.register_time(self.func.__name__, str(run_time), 'exec')
        return value

    def __get__(self, instance, owner):
        return partial(self, instance)


if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("Name of the program must be specified!")
    else:
        program = sys.argv[1]
        exec(open(program).read())
        TimeProfiler().show_logs()
