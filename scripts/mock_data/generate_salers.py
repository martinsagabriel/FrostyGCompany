import faker
import random
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

def insert_sellers():
    fake = faker.Faker("pt_BR")
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()

    # Buscar IDs das lojas existentes
    cursor.execute("SELECT StoreId FROM Store")
    stores = [row[0] for row in cursor.fetchall()]

    for store_id in stores:
        for _ in range(5):   # 5 vendedores por loja

            first_name = fake.first_name()
            last_name = fake.last_name()
            birth_date = fake.date_of_birth(minimum_age=18, maximum_age=60)
            employee_code = f"EMP{fake.random_int(10000,99999)}"
            phone = fake.phone_number()
            document = fake.cpf()

            cursor.execute(
                """
                INSERT INTO Seller (FirstName, LastName, BirthDate, EmployeeCode, 
                                    PhoneNumber, DocumentNumber, StoreId)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                first_name, last_name, birth_date, employee_code,
                phone, document, store_id
            )

    conn.commit()
    cursor.close()
    conn.close()


insert_sellers()
