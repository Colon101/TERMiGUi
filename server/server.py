from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)
http_port = 80
app_port = 3000

conn = sqlite3.connect('leaderboard.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS scores (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        score INTEGER
    )
''')

conn.commit()
cursor.close()
conn.close()

@app.route('/', methods=['POST'])
def handle_post():
    req_data = request.get_json()
    username = req_data.get('username')
    score = req_data.get('score')

    if not username:
        return 'Username is required.', 400

    if score is None:
        return 'Score is required.', 400

    conn = sqlite3.connect('leaderboard.db')
    cursor = conn.cursor()

    cursor.execute('SELECT score FROM scores WHERE username = ?', (username,))
    row = cursor.fetchone()

    if row:
        if int(score) > int(row[0]):
            cursor.execute('UPDATE scores SET score = ? WHERE username = ?', (score, username))
            conn.commit()
    else:
        cursor.execute('INSERT INTO scores (username, score) VALUES (?, ?)', (username, score))
        conn.commit()

    cursor.close()
    conn.close()

    return '', 200


@app.route('/')
def handle_get():
    conn = sqlite3.connect('leaderboard.db')
    cursor = conn.cursor()

    cursor.execute('SELECT username, score FROM scores ORDER BY score DESC')
    rows = cursor.fetchall()

    leaderboard = ''.join(
        f'<tr><td>{index + 1}</td><td>{row[0]}</td><td>{row[1]}</td></tr>'
        for index, row in enumerate(rows)
    )

    html = f'''
        <!DOCTYPE html>
        <html>
          <head>
            <title>Leaderboard</title>
            <style>
              body {{
                background-color: #222;
                color: #fff;
                font-size: 24px;
                font-family: Arial, sans-serif;
                margin: 0;
                padding: 20px;
              }}

              h1 {{
                font-size: 36px;
                text-align: center;
              }}

              p {{
                text-align: center;
                margin-bottom: 20px;
              }}

              a {{
                color: #fff;
                text-decoration: none;
              }}

              table {{
                border-collapse: collapse;
                width: 100%;
                margin-top: 20px;
              }}

              th,
              td {{
                border: 1px solid #fff;
                padding: 8px;
                text-align: left;
                font-size: 20px;
              }}

              th {{
                background-color: #555;
                color: #fff;
                font-weight: bold;
              }}

              td {{
                background-color: #222;
              }}
            </style>
          </head>
          <body>
            <h1>Leaderboard</h1>
            <p><a href="https://github.com/Colon101/TERMiGUi" target="_blank">Check out my program</a></p>
            <table>
              <tr>
                <th>Rank</th>
                <th>Username</th>
                <th>Score</th>
              </tr>
              {leaderboard}
            </table>
          </body>
        </html>
    '''

    cursor.close()
    conn.close()

    return html

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=app_port, debug=True)
