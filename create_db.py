"""
Description:
 Creates the people table in the Social Network database
 and populates it with 200 fake people.

Usage:
 python create_db.py
"""

from faker import Faker 
from random import randint
from datetime import datetime
import inspect
import os
import sqlite3


def main():
    global db_path
    db_path = os.path.join(get_script_dir(), 'social_network.db')
    create_people_table()
    populate_people_table()

def create_people_table():
    """Creates the people table in the database"""
    # TODO: Create function body
    # Connect to the database and Initialize the cursor 
    people_db = sqlite3.connect(db_path)
    db_cursor = people_db.cursor()

    # Create the 'people' in the database 
    people_table_query = """
    CREATE TABLE IF NOT EXISTS people
        (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            address TEXT NOT NULL,
            city TEXT NOT NULL,
            province TEXT NOT NULL,
            bio TEXT,
            age INTEGER,
            created_at DATETIME NOT NULL,
            updated_at DATETIME NOT NULL
        );
    """

    # Execute the query to create the table if it doesn't already exist
    db_cursor.execute(people_table_query)
    # Save the changes to the database 
    people_db.commit()
    # Terminate the connection 
    people_db.close()
    return

def populate_people_table():
    """Populates the people table with 200 fake people"""
    fake = Faker("en_CA")
    # Generate 200 fake data names  
    name_list = [fake.name() for _ in range(200)]

    # Generate 200 fake data emails based on the fake names 
    email_list = []
    for name in name_list:
        name = name.split()
        email_list.append(f"{name[0]}.{name[1]}@{fake.free_email_domain()}")

    # Generate 200 fake data street addresses
    address_list = [fake.street_address() for _ in range(200)]

    # Generate 200 fake data city entries 
    city_list = [fake.city() for _ in range(200)]

    # Generate 200 fake data province entries 
    province_list = [fake.administrative_unit() for _ in range(200)]

    # Generate 200 fake data bios 
    bios_list = [fake.sentence(nb_words=10, variable_nb_words=False) for _ in range(200)]

    # Generate 200 fake ages between 1 and 100
    age_list = [randint(1, 100) for _ in range(200)]
    
    # Query to add fake people to the list 
    add_person_query = """
        INSERT INTO people
        (
            name,
            email,
            address,
            city,
            province,
            bio,
            age,
            created_at,
            updated_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);
    """
    # Connect to the database and initialize the cursor
    person_db = sqlite3.connect(db_path)
    db_cursor = person_db.cursor()


    for _ in range(200):
        # Put the person information into a tuple to be inserted into the database
        new_person = (
            name_list[_],
            email_list[_],
            address_list[_],
            city_list[_],
            province_list[_],
            bios_list[_],
            age_list[_],
            datetime.now(),
            datetime.now()
        )
        # Execute the query 
        person_db.execute(add_person_query, new_person)
    
    # Save the changes to the database and terminate the connection
    person_db.commit()
    person_db.close()

    return

def get_script_dir():
    """Determines the path of the directory in which this script resides

    Returns:
        str: Full path of the directory in which this script resides
    """
    script_path = os.path.abspath(inspect.getframeinfo(inspect.currentframe()).filename)
    return os.path.dirname(script_path)

if __name__ == '__main__':
   main()