from database import create_database, create_students_table
from admission import (add_student, view_students, search_student,
                       update_student, delete_student)
from reports import (total_students, approved_students, pending_students,
                     rejected_students, course_wise_report)


def show_main_menu():
    print("\nCOLLEGE ADMISSION MANAGEMENT SYSTEM")
    print("1. Add New Student")
    print("2. View All Students")
    print("3. Search Student")
    print("4. Update Student")
    print("5. Delete Student")
    print("6. Admission Reports")
    print("7. Exit")


def show_reports_menu():
    while True:
        print("\nADMISSION REPORTS")
        print("1. Total Students")
        print("2. Approved Students")
        print("3. Pending Students")
        print("4. Rejected Students")
        print("5. Course-wise Report")
        print("6. Back to Main Menu")

        choice = input("Enter report choice: ").strip()

        if choice == "1":
            total_students()
        elif choice == "2":
            approved_students()
        elif choice == "3":
            pending_students()
        elif choice == "4":
            rejected_students()
        elif choice == "5":
            course_wise_report()
        elif choice == "6":
            break
        else:
            print("Invalid choice. Please enter a number from 1 to 6.")


def main():
    create_database()
    create_students_table()

    while True:
        show_main_menu()
        choice = input("Enter your choice: ").strip()

        if choice == "1":
            add_student()
        elif choice == "2":
            view_students()
        elif choice == "3":
            search_student()
        elif choice == "4":
            update_student()
        elif choice == "5":
            delete_student()
        elif choice == "6":
            show_reports_menu()
        elif choice == "7":
            print("Thank you. Exiting the program.")
            break
        else:
            print("Invalid choice. Please enter a number from 1 to 7.")


if __name__ == "__main__":
    main()
