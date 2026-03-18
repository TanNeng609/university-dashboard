import sqlite3
from flask import Flask ,jsonify, request
from flask_cors import CORS

app=Flask(__name__)
CORS(app)

def init_db():
    conn=sqlite3.connect("university.db")
    cursor=conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS students(
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   name TEXT NOT NULL ,
                   course TEXT NOT NULL,
                   gpa REAL NOT NULL
                   )
                   
                   ''')
    cursor.execute("SELECT COUNT(*) FROM students")
    if cursor.fetchone()[0]==0:
        cursor.execute("INSERT INTO students(name,course,gpa) VALUES ('TAN WEI NENG','Software Engineering',4.0)")
    conn.commit()
    conn.close()

init_db()

@app.route('/api/students',methods=['GET'])
def get_students():
    conn =sqlite3.connect('university.db')
    
    conn.row_factory=sqlite3.Row
    cursor=conn.cursor()

    cursor.execute("SELECT * FROM students")
    rows= cursor.fetchall()

    student_list=[dict(row)for row in rows]
    return jsonify(student_list)

@app.route('/api/students',methods=['POST'])
def add_student():
    new_student=request.json

    conn=sqlite3.connect("university.db")
    cursor=conn.cursor()

    cursor.execute("INSERT INTO students(name,course,gpa) VALUES (?,?,?)",
                   (new_student['name'],new_student['course'],new_student['gpa']))
    
    conn.commit()

    new_student['id']=cursor.lastrowid
    conn.close()

    print(f"SUCCESS: New student{new_student['name']} added to database!")

    return jsonify({"message":"Student scurely added!","student": new_student})
if __name__=='__main__':
    print("API Server booting up on port 5000....")
    app.run(debug=True,port=5000)