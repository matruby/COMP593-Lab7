"""
Description:
 Prints the name and age of all people in the Social Network database
 who are age 50 or older, and saves the information to a CSV file.

Usage:
 python old_people.py
"""
import inspect 
import os
import pandas as pd 
import sqlite3

def main():
    global db_path
    script_dir = get_script_dir()
    db_path = os.path.join(script_dir, 'social_network.db')

    # Get the names and ages of all old people
    old_people_list = get_old_people()

    # Print the names and ages of all old people
    print_name_and_age(old_people_list)

    # Save the names and ages of all old people to a CSV file
    old_people_csv = os.path.join(script_dir, 'old_people.csv')
    save_name_and_age_to_csv(old_people_list, old_people_csv)

def get_old_people():
    """Queries the Social Network database for all people who are at least 50 years old.

    Returns:
        list: (name, age) of old people 
    """
    # Connect to the database and initialize the cursor 
    people_db = sqlite3.connect(db_path)
    db_cursor = people_db.cursor()

    # Query for people who are at least 50 years old
    fifty_or_older = "SELECT name, age FROM people WHERE age >= 50"

    # Get the results of the query and store them in a variable
    query_result = db_cursor.execute(fifty_or_older)
    fifty_and_older = query_result.fetchall()

    # Terminate the connection to the database 
    people_db.close()

    # Return the list of people who are at least 50 years old 
    return fifty_and_older

def print_name_and_age(name_and_age_list):
    """Prints name and age of all people in provided list

    Args:
        name_and_age_list (list): (name, age) of people
    """
    for value in name_and_age_list:
        print(f"{value[0]} is {value[1]} years old.")

    return None 

def save_name_and_age_to_csv(name_and_age_list, csv_path):
    """Saves name and age of all people in provided list

    Args:
        name_and_age_list (list): (name, age) of people
        csv_path (str): Path of CSV file
    """
    # Get the path of the current directory 
    current_dir = get_script_dir()

    # Create the dataframe and pass in name and age data
    old_people_df = pd.DataFrame(name_and_age_list, columns=['name', 'age'])

    # Save the dataframe to a csv 
    old_people_df.to_csv(csv_path, index=False)

    return None 

def get_script_dir():
    """Determines the path of the directory in which this script resides

    Returns:
        str: Full path of the directory in which this script resides
    """
    script_path = os.path.abspath(inspect.getframeinfo(inspect.currentframe()).filename)
    return os.path.dirname(script_path)

if __name__ == '__main__':
   main()