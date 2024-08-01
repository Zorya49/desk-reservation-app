from flask import Flask, render_template, request, jsonify
import sqlite3
import os


# Initialize the database
def init_db():
    if not os.path.exists('reservations.db'):
        conn = sqlite3.connect('reservations.db')
        c = conn.cursor()
        c.execute('''
            CREATE TABLE reservations (
                id INTEGER PRIMARY KEY,
                desk_id TEXT NOT NULL,
                name TEXT NOT NULL,
                date TEXT NOT NULL,
                ip_address TEXT NOT NULL
            )
        ''')
        conn.commit()
        conn.close()


app = Flask(__name__)
init_db()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/reserve', methods=['POST'])
def reserve():
    data = request.json  # Parse JSON data
    desk_id = data['desk_id']
    name = data['name']
    date = data['date']
    ip_address = request.remote_addr

    conn = sqlite3.connect('reservations.db')
    c = conn.cursor()
    c.execute('INSERT INTO reservations (desk_id, name, date, ip_address) VALUES (?, ?, ?, ?)',
              (desk_id, name, date, ip_address))
    conn.commit()
    conn.close()

    return jsonify(success=True)


@app.route('/delete_reservation', methods=['POST'])
def delete_reservation():
    data = request.json
    desk_id = data['desk_id']
    date = data['date']
    ip_address = request.remote_addr

    conn = sqlite3.connect('reservations.db')
    c = conn.cursor()
    c.execute('DELETE FROM reservations WHERE desk_id = ? AND date = ? AND ip_address = ?', (desk_id, date, ip_address))
    conn.commit()
    conn.close()

    return jsonify(success=True)


@app.route('/reservations', methods=['GET'])
def reservations():
    date = request.args.get('date')

    conn = sqlite3.connect('reservations.db')
    c = conn.cursor()
    c.execute('SELECT desk_id, name, ip_address FROM reservations WHERE date = ?', (date,))
    reservations = c.fetchall()
    conn.close()
    print(reservations)

    return jsonify(reservations)



if __name__ == '__main__':
    app.run(debug=True)
