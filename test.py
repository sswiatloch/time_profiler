import time_profiler as tp
import psycopg2
import mysql.connector as mc
import time

# This isn't the final example program!
# Database is populated with data from:
# https://www.postgresqltutorial.com/postgresql-sample-database/
# conn = psycopg2.connect(database="dvdrental", user="test",
#                         password="test", host="127.0.0.1", port="5432")
# tp.TimeProfiler().register_connection(conn, tp.DBTypes.POSTGRES)
# cur = conn.cursor()

# https://dev.mysql.com/doc/employee/en/
conn = mc.connect(user="test", password="test", database="sakila")
tp.TimeProfiler().register_connection(conn, tp.DBTypes.MYSQL, password='test')
cur = conn.cursor()


@tp.TimeQuerry
@tp.TimeExecution
def foo():
    cur.execute("SELECT * FROM category")
    rows = cur.fetchall()
    for row in rows:
        print(row)
    return 1


foo()
tp.TimeProfiler().show_logs()
