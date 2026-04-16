import mysql.connector


def get_connection():

    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Dinesh@18102005",   
        database="university_db"
    )

    return conn