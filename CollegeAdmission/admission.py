from datetime import datetime

from database import get_connection
import mysql.connector


def read_application_id():
    """Read and validate an application ID from the user."""
    try:
        application_id = int(input("Enter Application ID: ").strip())
        if application_id <= 0:
            print("Invalid Application ID. Enter a positive integer.")
            return None
        return application_id
    except ValueError:
        print("Invalid Application ID. Enter a valid integer.")
        return None


def valid_admission_status(status):
    """Check whether admission status is valid."""
    return status in ("Pending", "Approved", "Rejected")


def add_student():
    """Ask for student details and add a new student record."""
    student_name = input("Student Name: ").strip()
    if student_name == "":
        print("Student name cannot be empty.")
        return

    father_name = input("Father Name: ").strip()
    if father_name == "":
        print("Father name cannot be empty.")
        return

    date_of_birth = input("Date of Birth (YYYY-MM-DD): ").strip()
    try:
        datetime.strptime(date_of_birth, "%Y-%m-%d")
    except ValueError:
        print("Invalid date. Please use YYYY-MM-DD format.")
        return

    gender = input("Gender: ").strip()
    if gender == "":
        print("Gender cannot be empty.")
        return

    phone = input("Phone Number: ").strip()
    if phone == "" or not phone.isdigit():
        print("Invalid phone number. Phone number must contain digits only.")
        return

    email = input("Email: ").strip()
    if email == "":
        print("Email cannot be empty.")
        return

    address = input("Address: ").strip()
    if address == "":
        print("Address cannot be empty.")
        return

    course = input("Course: ").strip()
    if course == "":
        print("Course cannot be empty.")
        return

    try:
        percentage = float(input("Percentage: ").strip())
    except ValueError:
        print("Invalid percentage. Enter a number from 0 to 100.")
        return

    if percentage < 0 or percentage > 100:
        print("Invalid percentage. Percentage must be from 0 to 100.")
        return

    connection = get_connection()
    if connection is None:
        return

    cursor = None

    try:
        cursor = connection.cursor()
        query = """
        INSERT INTO students
        (student_name, father_name, date_of_birth, gender, phone, email,
         address, course, percentage, admission_status)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, 'Pending')
        """
        values = (student_name, father_name, date_of_birth, gender, phone,
                  email, address, course, percentage)
        cursor.execute(query, values)
        connection.commit()

        application_id = cursor.lastrowid
        print("\nStudent admission successfully registered!")
        print("Application ID:", application_id)
        print("Student Name:", student_name)
        print("Course:", course)
        print("Admission Status: Pending")
    except mysql.connector.Error as error:
        print("Could not add student:", error)
    finally:
        if cursor is not None:
            cursor.close()
        connection.close()


def view_students():
    """Display all student records."""
    connection = get_connection()
    if connection is None:
        return

    cursor = None

    try:
        cursor = connection.cursor()
        cursor.execute("""
            SELECT application_id, student_name, father_name, date_of_birth,
                   gender, phone, email, address, course, percentage,
                   admission_status
            FROM students
            ORDER BY application_id
        """)
        records = cursor.fetchall()

        if len(records) == 0:
            print("No student records found.")
            return

        print("\nID  Name                 Course       Phone          Status")
        print("--- -------------------- ------------ -------------- ---------")
        for record in records:
            application_id = record[0]
            name = str(record[1])[:20]
            course = str(record[8])[:12]
            phone = str(record[5])
            status = record[10]
            print(application_id, " ", name.ljust(20), " ", course.ljust(12), " ", phone.ljust(14), " ", status)
    except mysql.connector.Error as error:
        print("Could not retrieve students:", error)
    finally:
        if cursor is not None:
            cursor.close()
        connection.close()


def search_student():
    """Search and display complete information for one student."""
    application_id = read_application_id()
    if application_id is None:
        return

    connection = get_connection()
    if connection is None:
        return

    cursor = None

    try:
        cursor = connection.cursor()
        cursor.execute("""
            SELECT application_id, student_name, father_name, date_of_birth,
                   gender, phone, email, address, course, percentage,
                   admission_status
            FROM students
            WHERE application_id = %s
        """, (application_id,))
        record = cursor.fetchone()

        if record is None:
            print("No student found with Application ID:", application_id)
            return

        print("\nComplete Student Information")
        print("Application ID:", record[0])
        print("Student Name:", record[1])
        print("Father Name:", record[2])
        print("Date of Birth:", record[3])
        print("Gender:", record[4])
        print("Phone:", record[5])
        print("Email:", record[6])
        print("Address:", record[7])
        print("Course:", record[8])
        print("Percentage:", record[9])
        print("Admission Status:", record[10])
    except mysql.connector.Error as error:
        print("Could not search for student:", error)
    finally:
        if cursor is not None:
            cursor.close()
        connection.close()


def update_student():
    """Update editable details of an existing student."""
    application_id = read_application_id()
    if application_id is None:
        return

    connection = get_connection()
    if connection is None:
        return

    cursor = None

    try:
        cursor = connection.cursor()
        cursor.execute("SELECT application_id FROM students WHERE application_id = %s", (application_id,))
        record = cursor.fetchone()

        if record is None:
            print("No student found with Application ID:", application_id)
            return

        phone = input("New Phone Number: ").strip()
        if phone == "" or not phone.isdigit():
            print("Invalid phone number. Phone number must contain digits only.")
            return

        email = input("New Email: ").strip()
        if email == "":
            print("Email cannot be empty.")
            return

        address = input("New Address: ").strip()
        if address == "":
            print("Address cannot be empty.")
            return

        course = input("New Course: ").strip()
        if course == "":
            print("Course cannot be empty.")
            return

        status = input("New Admission Status (Pending/Approved/Rejected): ").strip().title()
        if not valid_admission_status(status):
            print("Invalid admission status. Use Pending, Approved or Rejected.")
            return

        cursor.execute("""
            UPDATE students
            SET phone = %s, email = %s, address = %s,
                course = %s, admission_status = %s
            WHERE application_id = %s
        """, (phone, email, address, course, status, application_id))
        connection.commit()

        print("Student details updated successfully.")
    except mysql.connector.Error as error:
        print("Could not update student:", error)
    finally:
        if cursor is not None:
            cursor.close()
        connection.close()


def delete_student():
    """Ask for confirmation and delete a student record."""
    application_id = read_application_id()
    if application_id is None:
        return

    connection = get_connection()
    if connection is None:
        return

    cursor = None

    try:
        cursor = connection.cursor()
        cursor.execute("SELECT student_name FROM students WHERE application_id = %s", (application_id,))
        record = cursor.fetchone()

        if record is None:
            print("No student found with Application ID:", application_id)
            return

        confirm = input("Delete " + record[0] + "? (yes/no): ").strip().lower()
        if confirm != "yes":
            print("Deletion cancelled.")
            return

        cursor.execute("DELETE FROM students WHERE application_id = %s", (application_id,))
        connection.commit()
        print("Student record deleted successfully.")
    except mysql.connector.Error as error:
        print("Could not delete student:", error)
    finally:
        if cursor is not None:
            cursor.close()
        connection.close()
