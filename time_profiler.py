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
        self.file = open("log.txt", 'w')

    def register_connection(self, conn, dbtype):
        self.db = DatabaseFactory.create(conn, dbtype)

    def register_time(self, func_name, reg_time, reg_type):
        try:
            self.logs[func_name].append((reg_time, reg_type))
        except KeyError:
            self.logs[(func_name)] = [(reg_time, reg_type)]
        self.file.write(str(func_name)+" " + str(reg_time) + " "+str(reg_type) + "\n")

    def show_logs(self):
        for item in self.logs.items():
            print(f'Summary of function: {item[0]}')
            execs = [x[0] for x in item[1] if x[1]=='exec']
            queries = [x[0] for x in item[1] if x[1]=='query']
            if len(execs) > 0:
                print(f'Number of exeutions: {len(execs)}\nAverage execution time: {sum(execs)/len(execs):.4f} s')
            if len(queries) > 0:
                print(f'Number of queries: {len(queries)}\nAverage query time: {sum(queries)/len(queries):.4f} ms')


class TimeQuery:
    def __init__(self, func):
        update_wrapper(self, func)
        self.func = func
        self.tprof = TimeProfiler()

    def __call__(self, *args, **kwargs):
        if self.tprof.db is None:
            print("[tprof] There is no connection registered! Queries will not be timed")
            return self.func(*args, **kwargs)
        else:
            self.tprof.db.set_timestamp()
            value = self.func(*args, **kwargs)
            times = self.tprof.db.get_query_time()
            for t in times:
                print(f"[tprof] Query in {self.func.__name__!r} finished in {t} ms")
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
        print(f"[tprof] Function {self.func.__name__!r} finished in {run_time:.4f} s")
        self.tprof.register_time(self.func.__name__, run_time, 'exec')
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
