#!/bin/bash

# NOTE: Databases typically run on port 5432, but we use 5433 for our isolated environment

DB_DIR="./db/postgres-data"

if [ -d "$DB_DIR" ]; then
    echo "$DB_DIR already exists."
    read -p "Do you want to delete $DB_DIR and start over? (y/n): " answer

    case "$answer" in
        [Nn]* )
            echo "Leaving $DB_DIR as is."
            exit 0
            ;;
        [Yy]* )
            echo "Replacing $DB_DIR..."
            rm -rf "$DB_DIR"
            mkdir -p "$DB_DIR"
            ;;
        * )
            echo "Invalid response. Exiting."
            exit 1
            ;;
    esac
else
    mkdir -p "$DB_DIR"
fi

# Start the database
initdb -D "$DB_DIR" -E UTF8 --locale=C
pg_ctl -D "$DB_DIR" -o "-p 5433" start

# Make a user and a database
psql -h localhost -p 5433 -d postgres -c "CREATE ROLE demo_user LOGIN PASSWORD 'password';"
psql -h localhost -p 5433 -d postgres -c "CREATE DATABASE demo_db OWNER demo_user ENCODING 'UTF8' LC_COLLATE='C' LC_CTYPE='C';"

# Set up the schema
# psql -h localhost -p 5433 -d demo_db -f ./db/init/create_tables.sql

# Seed the data
# psql -h localhost -p 5433 -d demo_db -f ./db/init/seed_data.sql

# NOTE: The database can be managed as follows

# check if the database is running
# pg_ctl -D "$DB_DIR" status

# check that the database is accepting connections
# pg_isready -p 5433

# start the database
# pg_ctl -D "$DB_DIR" -o "-p 5433" start

# stop the database
# pg_ctl -D "$DB_DIR" stop

# delete/erase the database entirely
# pg_ctl -D "$DB_DIR" stop
# rm -rf "$DB_DIR"
# ls /tmp/.s.PGSQL.*
# rm -rf /tmp/.s.PGSQL.* # (if needed)
