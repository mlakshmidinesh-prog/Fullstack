import pymysql

def get_db_connection():
    return pymysql.connect(
        host='localhost',
        user='root',
        password='Dinesh@18102005',
        database='feedback_db',
        cursorclass=pymysql.cursors.DictCursor
    )