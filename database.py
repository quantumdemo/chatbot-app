import mysql.connector
import os

def get_db_connection():
    """
    Establishes a connection to the MySQL database.
    """
    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "localhost"),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD", ""),
        database=os.getenv("DB_NAME", "chatbot")
    )

def create_tables():
    """
    Creates the necessary tables in the database.
    """
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS conversations (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id VARCHAR(255) NOT NULL,
            message TEXT NOT NULL,
            response TEXT NOT NULL,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    db.commit()
    cursor.close()
    db.close()

def save_interaction(user_id, message, response):
    """
    Saves a user interaction to the database.
    """
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute(
        "INSERT INTO conversations (user_id, message, response) VALUES (%s, %s, %s)",
        (user_id, message, response)
    )
    db.commit()
    cursor.close()
    db.close()
