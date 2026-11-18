from database import get_connection
import mysql.connector


def total_students():
    """Display the total number of registered students."""
    connection = get_connection()
    if connection is None:
        return

    cursor = None
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT COUNT(*) FROM students")
        result = cursor.fetchone()
        print("Total registered students:", result[0])
    except mysql.connector.Error as error:
        print("Could not generate report:", error)
    finally:
        if cursor is not None:
            cursor.close()
        connection.close()


def approved_students():
    """Display the number of approved admissions."""
    connection = get_connection()
    if connection is None:
        return

    cursor = None
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT COUNT(*) FROM students WHERE admission_status = %s", ("Approved",))
        result = cursor.fetchone()
        print("Approved admissions:", result[0])
    except mysql.connector.Error as error:
        print("Could not generate report:", error)
    finally:
        if cursor is not None:
            cursor.close()
        connection.close()


def pending_students():
    """Display the number of pending admissions."""
    connection = get_connection()
    if connection is None:
        return

    cursor = None
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT COUNT(*) FROM students WHERE admission_status = %s", ("Pending",))
        result = cursor.fetchone()
        print("Pending admissions:", result[0])
    except mysql.connector.Error as error:
        print("Could not generate report:", error)
    finally:
        if cursor is not None:
            cursor.close()
        connection.close()


def rejected_students():
    """Display the number of rejected admissions."""
    connection = get_connection()
    if connection is None:
        return

    cursor = None
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT COUNT(*) FROM students WHERE admission_status = %s", ("Rejected",))
        result = cursor.fetchone()
        print("Rejected admissions:", result[0])
    except mysql.connector.Error as error:
        print("Could not generate report:", error)
    finally:
        if cursor is not None:
            cursor.close()
        connection.close()


def course_wise_report():
    """Display student count for each course using GROUP BY."""
    connection = get_connection()
    if connection is None:
        return

    cursor = None
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT course, COUNT(*) FROM students GROUP BY course ORDER BY course")
        records = cursor.fetchall()

        if len(records) == 0:
            print("No course data found.")
            return

        print("\nCourse-wise Report")
        print("Course               Number of Students")
        print("-------------------- -------------------")
        for course, count in records:
            print(str(course).ljust(20), str(count).rjust(19))
    except mysql.connector.Error as error:
        print("Could not generate report:", error)
    finally:
        if cursor is not None:
            cursor.close()
        connection.close()
