import mysql.connector
from time import sleep

class ExampleMySQL:
    def __init__(self):
        self.conn = mysql.connector.connect(user="test", password="test", database="sakila")
        # registering connection
        TimeProfiler().register_connection(self.conn, DBTypes.MYSQL)
        self.cur = self.conn.cursor()
        self.cur.execute("SELECT 0")
        self.cur.fetchall()

    # decorating functions
    @TimeQuery
    @TimeExecution
    def logic(self):
        self.cur.execute('SELECT sleep(2)')
        self.cur.fetchall()
        sleep(1)

if __name__ == '__main__':
    e = ExampleMySQL()
    e.logic()
    e.logic()
    e.logic()
    e.logic()