import psycopg2
from time import sleep
from random import randrange

class ExamplePostgres:
    def __init__(self):
        self.conn = psycopg2.connect(database="dvdrental", user="test",
                        password="test", host="127.0.0.1", port="5432")
        # registering connection 
        TimeProfiler().register_connection(self.conn, DBTypes.POSTGRES)
        self.cur = self.conn.cursor()
        self.cur.execute("SELECT 0")

    # decorating functions
    @TimeQuery
    @TimeExecution
    def query_function(self):
        self.cur.execute('SELECT * FROM category')
        self.cur.execute('SELECT pg_sleep(2)')
        sleep(1)

    @TimeExecution
    def foo(self):
        sleep(1/randrange(1,10))

    

if __name__ == '__main__':
    e = ExamplePostgres()
    e.query_function()

    for _ in range(5):
        e.foo()