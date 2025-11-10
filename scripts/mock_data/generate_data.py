import random
import faker
from db import get_db_connection

def generate_brazil_coordinates():
    lat = random.uniform(-33.75, 5.27)     # Latitude Brasil
    lon = random.uniform(-73.98, -34.79)   # Longitude Brasil
    return round(lat, 6), round(lon, 6)

def insert_stores(quantity):
    fake = faker.Faker("pt_BR")
    conn = get_db_connection()
    cursor = conn.cursor()

    for _ in range(quantity):
        store_name = f"Ice Cream Store {fake.city()}"
        address = fake.street_address()
        city = fake.city()
        state = fake.estado_sigla()
        zipcode = fake.postcode()

        lat, lon = generate_brazil_coordinates()

        cursor.execute("""
            INSERT INTO "store" 
            (storename, addressline, city, state, zipcode, latitude, longitude, createdat)
            VALUES (%s, %s, %s, %s, %s, %s, %s, NOW());
        """, (store_name, address, city, state, zipcode, lat, lon))

    conn.commit()
    cursor.close()
    conn.close()
    
    
def insert_sellers():
    fake = faker.Faker("pt_BR")
    conn = get_db_connection()
    cursor = conn.cursor()

    # Buscar IDs das lojas existentes
    cursor.execute('SELECT "storeid" FROM "store";')
    stores = [row[0] for row in cursor.fetchall()]

    for store_id in stores:
        for _ in range(5):   # 5 vendedores por loja

            first_name = fake.first_name()
            last_name = fake.last_name()
            birth_date = fake.date_of_birth(minimum_age=18, maximum_age=60)
            employee_code = f"EMP{fake.random_int(10000,99999)}"
            phone = fake.phone_number()
            document = fake.cpf()

            cursor.execute("""
                INSERT INTO "seller" 
                (firstname, lastname, birthdate, employeecode, phonenumber, documentnumber, storeid, createdat)
                VALUES (%s, %s, %s, %s, %s, %s, %s, NOW());
            """, (first_name, last_name, birth_date, employee_code, phone, document, store_id))

    conn.commit()
    cursor.close()
    conn.close()

if __name__ == "__main__":
    insert_stores(1000)
    insert_sellers()