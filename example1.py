import psycopg2
from time import sleep

class ExamplePostgres:
    def __init__(self):
        self.conn = psycopg2.connect(database="dvdrental", user="test",
                        password="test", host="127.0.0.1", port="5432")
        # registering connection 
        TimeProfiler().register_connection(self.conn, DBTypes.POSTGRES)
        self.cur = self.conn.cursor()

    # decorating functions
    @TimeQuery
    @TimeExecution
    def logic(self):
        self.cur.execute('SELECT * FROM category')
        sleep(1)

if __name__ == '__main__':
    e = ExamplePostgres()
    e.logic()