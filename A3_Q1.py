import sys
import psycopg2
from psycopg2 import sql, OperationalError

def connect_db():
    try:
        conn = psycopg2.connect("dbname=postgres user=siddharthnatamai password=postgres")
        return conn
    except OperationalError as e:
        print(f"An error occurred: {e}")
        return None

def getAllStudents(conn):
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM students")
        rows = cur.fetchall()
        for row in rows:
            print(row)

def addStudent(conn, first_name, last_name, email, enrollment_date):
    with conn.cursor() as cur:
        cur.execute("INSERT INTO students (first_name, last_name, email, enrollment_date) VALUES (%s, %s, %s, %s)", (first_name, last_name, email, enrollment_date))
        conn.commit()

def updateStudentEmail(conn, student_id, new_email):
    with conn.cursor() as cur:
        cur.execute("UPDATE students SET email = %s WHERE student_id = %s", (new_email, student_id))
        conn.commit()

def deleteStudent(conn, student_id):
    with conn.cursor() as cur:
        cur.execute("DELETE FROM students WHERE student_id = %s", (student_id,))
        conn.commit()

def print_usage():
    print("Usage:")
    print("  python A3_Q1.py getAllStudents")
    print("  python A3_Q1.py addStudent <first_name> <last_name> <email> <enrollment_date>")
    print("  python A3_Q1.py updateStudentEmail <student_id> <new_email>")
    print("  python A3_Q1.py deleteStudent <student_id>")
    print("\nExamples:")
    print("  python A3_Q1.py getAllStudents")
    print("  python A3_Q1.py addStudent John Doe john.doe@example.com 2023-09-01")
    print("  python A3_Q1.py updateStudentEmail 1 john.new@example.com")
    print("  python A3_Q1.py deleteStudent 2")

def main(args):
    conn = connect_db()
    if conn is None:
        return

    try:
        if args[0] == "getAllStudents":
            getAllStudents(conn)
        elif args[0] == "addStudent" and len(args) == 5:
            addStudent(conn, args[1], args[2], args[3], args[4])
        elif args[0] == "updateStudentEmail" and len(args) == 3:
            updateStudentEmail(conn, int(args[1]), args[2])
        elif args[0] == "deleteStudent" and len(args) == 2:
            deleteStudent(conn, int(args[1]))
        else:
            print_usage()
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(sys.argv[1:])
    else:
        print_usage()