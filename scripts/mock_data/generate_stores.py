import random
import faker
import pyodbc

import os
from dotenv import load_dotenv
load_dotenv()

conn_str = (
    "DRIVER={ODBC Driver 17 for SQL Server};"
    f"SERVER={os.getenv('MAIN_SERVER')};"
    f"DATABASE={os.getenv('SQL_NAME')};"
    f"UID={os.getenv('SQL_USER')};"
    f"PWD={os.getenv('SQL_PASS')};"
)

def generate_brazil_coordinates():
    lat = random.uniform(-33.75, 5.27)     # Latitude Brasil
    lon = random.uniform(-73.98, -34.79)   # Longitude Brasil
    return round(lat, 6), round(lon, 6)

def insert_stores(quantity):
    fake = faker.Faker("pt_BR")
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()

    for _ in range(quantity):
        store_name = f"Ice Cream Store {fake.city()}"
        address = fake.street_address()
        city = fake.city()
        state = fake.estado_sigla()
        zipcode = fake.postcode()

        lat, lon = generate_brazil_coordinates()

        cursor.execute(
            """
            INSERT INTO Store (StoreName, AddressLine, City, State, ZipCode, Latitude, Longitude)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            store_name, address, city, state, zipcode, lat, lon
        )

    conn.commit()
    cursor.close()
    conn.close()

insert_stores(100)
