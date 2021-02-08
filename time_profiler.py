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

class TimeProfilerMeta(type):
    
    instances={}

    def __call__(cls,*args,**kwargs):
        if cls not in cls.instances:
            instance = super().__call__(*args,**kwargs)
            instance.database=DatabaseFactory.create()
            cls.instances[cls]=instance
        return cls.instances[cls]

class TimeProfiler(metaclass=TimeProfilerMeta):

    def register_connection(self,type, conn):
        return DatabaseFactory.create(conn,type)

    def reqister_time(self, func_name, time, type):
        pass
    
    def show_logs():
        pass

class TimeQuerry:
    def __init__(self, func):
        self.func=func
        self.num=0
        
        
    def __call__(self, *args, **kwargs):
        self.num+=1
        self.prof=TimeProfiler()
        

class TimeExecution:
    def __init__(self, func):
        self.func=func
        self.num=0
        

    def __call__(self, *args, **kwargs):
        self.num+=1
        self.prof=TimeProfiler()
