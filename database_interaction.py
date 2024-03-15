import psycopg2
from psycopg2 import Error
import datetime

# Connect to PostgreSQL database
def connect():
    try:
        connection = psycopg2.connect(
            user="postgres",
            password="reshma2501",
            host="localhost",
            port="2003",
            database="student_database"
        )
        return connection
    except (Exception, Error) as error:
        print("Error while connecting to PostgreSQL", error)

# Function to retrieve all students
def getAllStudents():
    try:
        connection = connect()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM students")
        students = cursor.fetchall()
        for student in students:
            print(student)
    except (Exception, Error) as error:
        print("Error while fetching data from PostgreSQL", error)
    finally:
        if connection:
            cursor.close()
            connection.close()

# Function to add a new student
def addStudent(first_name, last_name, email, enrollment_date):
    try:
        connection = connect()
        cursor = connection.cursor()
        # Convert enrollment_date string to date object
        enrollment_date = datetime.datetime.strptime(enrollment_date, "%Y-%m-%d").date()
        cursor.execute("INSERT INTO students (first_name, last_name, email, enrollment_date) VALUES (%s, %s, %s, %s)", (first_name, last_name, email, enrollment_date))
        connection.commit()
        print("Student added successfully")
    except psycopg2.IntegrityError as integrity_error:
        # Handle duplicate email error silently
        if "duplicate key value violates unique constraint" not in str(integrity_error):
            print("Error while adding student to PostgreSQL", integrity_error)
    except (Exception, Error) as error:
        print("Error while adding student to PostgreSQL", error)
    finally:
        if connection:
            cursor.close()
            connection.close()

# Function to update student email
def updateStudentEmail(student_id, new_email):
    try:
        connection = connect()
        cursor = connection.cursor()
        cursor.execute("UPDATE students SET email = %s WHERE student_id = %s", (new_email, student_id))
        connection.commit()
        print("Email updated successfully")
    except (Exception, Error) as error:
        print("Error while updating student email in PostgreSQL", error)
    finally:
        if connection:
            cursor.close()
            connection.close()

# Function to delete a student
def deleteStudent(student_id):
    try:
        connection = connect()
        cursor = connection.cursor()
        cursor.execute("DELETE FROM students WHERE student_id = %s", (student_id,))
        connection.commit()
        print("Student deleted successfully")
    except (Exception, Error) as error:
        print("Error while deleting student from PostgreSQL", error)
    finally:
        if connection:
            cursor.close()
            connection.close()

 # Example usage
if __name__ == "__main__":
    getAllStudents()
    addStudent("Alice", "Wonderland", "alice@example.com", "2024-03-15")  #Adding Alice
    getAllStudents()    
    updateStudentEmail(4, "alice.updated@example.com")
    getAllStudents()
    deleteStudent(3)  # Deleting student 3, which is Jim.
    getAllStudents()
