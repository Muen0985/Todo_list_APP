from flask import Flask, jsonify, request
import sqlite3

app=Flask(__name__)

def init_db():
    try:
        conn = sqlite3.connect('todolist.db')
        # conn.cursor(): Creates a cursor object to execute SQL statements
        cursor=conn.cursor() 
        cursor.execute("""
                        CREATE TABLE IF NOT EXISTS todolist (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        title TEXT NOT NULL,
                        completed BOOLEAN NOT NULL DEFAULT 0)
                        """)
        conn.commit()
    except sqlite3.Error as e:
        print(f'Database error {e}')
    finally:
        conn.close()

init_db()

# Read
@app.route("/todos",methods=['GET'])
def get_todos():
    conn=sqlite3.connect('todolist.db')
    cursor=conn.cursor()
    cursor.execute("""SELECT * FROM todolist""")
    data=cursor.fetchall()
    result=[{"id":row[0],"title":row[1],"completed":bool(row[2])} for row in data]
    conn.close()
    return jsonify(result)

# GET 
@app.route("/todos",methods=['POST'])
def add_todos():
    data=request.get_json()
    title=data.get('title')

    conn=sqlite3.connect('todolist.db')
    cursor=conn.cursor()
    cursor.execute("""INSERT INTO todolist (title) VALUES (?)""", (title,))
    conn.commit()
    conn.close()
    return jsonify({"message": "Todo added successfully"}), 200

# Delete
@app.route("/todos/deletetodo/<task_id>",methods=['DELETE'])
def delete_todo(task_id):
    conn=sqlite3.connect('todolist.db')
    cursor=conn.cursor()
    cursor.execute("""DELETE FROM todolist WHERE id = ?""",(int(task_id),))
    conn.commit()
    conn.close()
    return jsonify({"message": "Todo deleted successfully"}), 200

# PUT  
@app.route("/todos/updatetodo/<task_id>",methods=['PUT'])
def update_todo(task_id):
    data=request.get_json()
    title=data.get('title')
    completed=data.get('completed')

    conn=sqlite3.connect('todolist.db')
    cursor=conn.cursor()
    cursor.execute("SELECT * FROM todolist WHERE id = ?", (int(task_id),))
    if cursor.fetchone() is None:
        return jsonify({"message": "Task not found"}), 404
    cursor.execute("""UPDATE todolist SET title=?,completed=? WHERE id =?""",(title,int(completed),int(task_id)))
    conn.commit()
    conn.close()
    return jsonify({"message": "Todo updated successfully"}), 200

@app.route("/todos/clearlist",methods=['DELETE'])
def clear_db():
    conn=sqlite3.connect('todolist.db')
    cursor=conn.cursor()
    cursor.execute("""UPDATE sqlite_sequence SET seq=0 WHERE name='todolist' """)
    cursor.execute("""DELETE FROM todolist""")
    conn.commit()
    conn.close()
    return jsonify({"message": "Todo cleared successfully"}), 200

if __name__=='__main__':
    app.run(debug=True)