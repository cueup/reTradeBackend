import psycopg2
import os

# -------------------------
# DB CONNECTION
# -------------------------

def get_db():
    return psycopg2.connect(dbname="market_data_db",
    user="postgres",
    password="uLKjNalzwsmblGQ6",
    host="srv-captain--timescaledb",
    port="6543")