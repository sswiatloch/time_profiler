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
todo