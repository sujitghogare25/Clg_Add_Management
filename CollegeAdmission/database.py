import mysql.connector


# Change these settings according to your MySQL installation.
MYSQL_HOST = "localhost"
MYSQL_USER = "root"
MYSQL_PASSWORD = ""
DATABASE_NAME = "college_admission"


def get_connection():
    """Create and return a connection to the college_admission database."""
    try:
        connection = mysql.connector.connect(
            host=MYSQL_HOST,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            database=DATABASE_NAME
        )
        return connection
    except mysql.connector.Error:
        print("Error: Could not connect to MySQL.")
        print("Please check MySQL Server and the settings in database.py.")
        return None


def create_database():
    """Create the college_admission database if it does not exist."""
    connection = None
    cursor = None

    try:
        connection = mysql.connector.connect(
            host=MYSQL_HOST,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD
        )
        cursor = connection.cursor()

        # CREATE DATABASE with IF NOT EXISTS avoids creating the database again.
        cursor.execute("CREATE DATABASE IF NOT EXISTS college_admission")
        connection.commit()
        print("Database is ready.")
    except mysql.connector.Error as error:
        print("Database setup error:", error)
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None:
            connection.close()


def create_students_table():
    """Create the students table if it does not exist."""
    connection = get_connection()
    if connection is None:
        return

    cursor = None

    try:
        cursor = connection.cursor()
        query = """
        CREATE TABLE IF NOT EXISTS students (
            application_id INT PRIMARY KEY AUTO_INCREMENT,
            student_name VARCHAR(100) NOT NULL,
            father_name VARCHAR(100) NOT NULL,
            date_of_birth DATE NOT NULL,
            gender VARCHAR(20) NOT NULL,
            phone VARCHAR(15) NOT NULL,
            email VARCHAR(100) NOT NULL,
            address VARCHAR(255) NOT NULL,
            course VARCHAR(100) NOT NULL,
            percentage FLOAT NOT NULL,
            admission_status VARCHAR(20) DEFAULT 'Pending'
        )
        """
        cursor.execute(query)
        connection.commit()
        print("Students table is ready.")
    except mysql.connector.Error as error:
        print("Table setup error:", error)
    finally:
        if cursor is not None:
            cursor.close()
        connection.close()
