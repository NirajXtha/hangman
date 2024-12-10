import mysql.connector
from mysql.connector import Error

def create_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user="root",
            password='1234',
            database='hangman'
        )
        if connection.is_connected():
            print("Successfully connected to the database")
        return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

def create_user(username, password):
    connection = create_connection()
    cursor = connection.cursor()
    query = "INSERT INTO users (username, password) VALUES (%s, %s)"
    cursor.execute(query, (username, password))
    connection.commit()
    cursor.close()
    connection.close()

def verify_user(username, password):
    connection = create_connection()
    cursor = connection.cursor()
    query = "SELECT * FROM users WHERE username = %s AND password = %s"
    cursor.execute(query, (username, password))
    result = cursor.fetchone()
    cursor.close()
    connection.close()
    return result

def get_user(username):
    connection = create_connection()
    cursor = connection.cursor()
    query = "SELECT level, score, life FROM users WHERE username = %s"
    cursor.execute(query, (username))
    result = cursor.fetchone()
    cursor.close()
    connection.close()
    return result

def update_user(username, level):
    connection = create_connection()
    cursor = connection.cursor()
    query = "UPDATE users SET level = %s WHERE username = %s"
    cursor.execute(query, (level,username))
    result = cursor.fetchone()
    cursor.close()
    connection.close()
    return result