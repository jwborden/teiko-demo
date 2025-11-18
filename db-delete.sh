# delete/erase the database entirely
DB_DIR="./db/postgres-data"
pg_ctl -D "$DB_DIR" stop
rm -rf "$DB_DIR"
ls /tmp/.s.PGSQL.*
rm -rf /tmp/.s.PGSQL.* # (if needed)
