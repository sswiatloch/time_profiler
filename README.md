# time_profiler
Biblioteka do mierzenia wydajności czasowej aplikacji.

# Przygotowanie bazy PostgreSQL
Aby zapewnić poprawne działanie biblioteki, należy odpowienio przygotować bazę danych. Poniższe komendy należy wykonywać jako superuser. {user} należy zamienić na nazwę użytkownika wykorzystywaną w swojej aplikacji do połączenia z bazą danych.

```
ALTER SYSTEM SET log_min_duration_statement = 0;
ALTER SYSTEM  SET log_statement = 'all';
ALTER SYSTEM SET logging_collector = on;
ALTER SYSTEM  SET log_directory = 'log';
ALTER SYSTEM  SET  log_destination = 'csvlog';
ALTER SYSTEM  SET  log_filename = 'logfile.log';
ALTER SYSTEM SET log_truncate_on_rotation = on;
SELECT pg_reload_conf();
CREATE TABLE postgres_log
(
  log_time timestamp(3) with time zone,
  user_name text,
  database_name text,
  process_id integer,
  connection_from text,
  session_id text,
  session_line_num bigint,
  command_tag text,
  session_start_time timestamp with time zone,
  virtual_transaction_id text,
  transaction_id bigint,
  error_severity text,
  sql_state_code text,
  message text,
  detail text,
  hint text,
  internal_query text,
  internal_query_pos integer,
  context text,
  query text,
  query_pos integer,
  location text,
  application_name text,
  backend_type text,
  PRIMARY KEY (session_id, session_line_num)
);
GRANT pg_read_server_files TO {user};
GRANT ALL PRIVILEGES ON postgres_log TO {user};
```

# Przygotowanie bazy MySQL
W wierszu poleceń MySQL wykonaj:
```
SET GLOBAL general_log = 'ON';
SET GLOBAL slow_query_log = 'ON';
SET GLOBAL long_query_time = 0;
SET GLOBAL log_output = 'TABLE';
GRANT SELECT ON mysql.slow_log TO '{user}'@'localhost';
```

# Sposób użycia
Bibliotekę można używać na dwa sposoby:
1. jako skrypt
2. przez bezpośrednie imporotwanie modułu

# Używanie skryptu
Na początku należy udekorować wybrane funkcje dekoratorami @TimeQuery lub @ TimeExecution. Jeżeli jest używany TimeQuery, neleży również zarejestrować połączenie do bazy danych. W przypadku stosowania obu dekratorów na raz, dla lepszych wyników zaleca się używanie @TimeQuery przed @TimeExecution.
```
# rejestrowanie połączenia dla PostgreSQL
conn = psycopg2.connect(...)
TimeProfiler().register_connection(conn, tp.DBTypes.POSTGRES)
```
```
# rejestrowanie połączenia dla MySQL
conn = mysql.connector.connect(...)
TimeProfiler().register_connection(conn, DBTypes.MYSQL, password='...')
```
```
# dekorowanie funkcji
@TimeQuery
@TimeExecution
def foo(a):
    return a+1
```

Aby uruchomić program, należy wywołać:
```
python -m time_profiler example.py
```
W terminalu ukazywać się będą normalne wyniki programu oraz logi time_profiler. Na koniec zostanie wyświetlone podsumowanie.

# Bezpośrdenie importowanie biblioteki
Można również zaimportować time_profiler bezpośrednio do programu.
```
import time_profiler as tp

@tp.TimeExecution
def foo(a):
    return a+1
```
Przy tym użyciu można normalnie wywołać program, jednak nie będzie wyświetlone podsumowanie.