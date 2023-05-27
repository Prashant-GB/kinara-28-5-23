from flask import Flask, request, jsonify, render_template
import sqlite3

# Creating name with app
app = Flask(__name__, template_folder='templates')


# Landing Page for  student list
@app.route('/', methods=['GET'])
def get_students():
    # redirecting to landing page
    return render_template('index.html', title='Student Table')


# Server-side Filtering API along with json response
@app.route('/students', methods=['GET'])
def filter_students():
    # Get page number and page size from the query parameters
    draw = int(request.args.get('draw', 1))
    start = int(request.args.get('start', 0))
    length = int(request.args.get('length', 10))

    # Connect to the SQLite database
    conn = sqlite3.connect('students.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # Retrieve and searching student details for the current page
    search = request.args.get('search[value]')
    query = "SELECT * FROM student"
    if search:
        query += " WHERE name LIKE ? LIMIT ?, ?"
        cursor.execute(query, ('%'+search+'%',start, length))
    else:
        query += " LIMIT ?, ?"
        cursor.execute(query,(start, length))

    rows = cursor.fetchall()

    # Get the total number of records in the table
    query = "SELECT COUNT(*) FROM student"
    if search:
        query += " WHERE name LIKE ? LIMIT ?, ?"
        cursor.execute(query, ('%'+search+'%',start, length))
    else:
        query += " LIMIT ?, ?"
        cursor.execute(query,(start, length))

    total_records = cursor.fetchone()[0]

    # Close the database connection
    conn.close()

    # Format the student details in the required JSON format
    students = []
    index=0
    for row in rows:
        index += 1
        students.append({
            "index": index,
            "name": row['name'],
            "total_marks": row['total_marks']
        })

    # Prepare the response for DataTables
    response = {
        "draw": draw,
        "recordsTotal": total_records,
        "recordsFiltered": total_records,
        "data": students,
    }

    return jsonify(response)


if __name__ == '__main__':
    app.run(debug=True)
