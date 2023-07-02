from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)
http_port = 80
app_port = 80

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
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <style>
              body {{
                background-color: #222;
                color: #fff;
                font-family: Arial, sans-serif;
                margin: 0;
                padding: 20px;
              }}

              h1 {{
                font-size: 36px;
                text-align: center;
                margin-bottom: 30px;
              }}

              p {{
                text-align: center;
                margin-bottom: 30px;
              }}

              /* Add the button-30 styles below */
              .button-30 {{
                align-items: center;
                appearance: none;
                background-color: #FCFCFD;
                border-radius: 4px;
                border-width: 0;
                box-shadow: rgba(45, 35, 66, 0.4) 0 2px 4px,rgba(45, 35, 66, 0.3) 0 7px 13px -3px,#D6D6E7 0 -3px 0 inset;
                box-sizing: border-box;
                color: #36395A;
                cursor: pointer;
                display: inline-flex;
                font-family: "JetBrains Mono",monospace;
                height: 48px;
                justify-content: center;
                line-height: 1;
                list-style: none;
                overflow: hidden;
                padding-left: 16px;
                padding-right: 16px;
                position: relative;
                text-align: left;
                text-decoration: none;
                transition: box-shadow .15s,transform .15s;
                user-select: none;
                -webkit-user-select: none;
                touch-action: manipulation;
                white-space: nowrap;
                will-change: box-shadow,transform;
                font-size: 18px;
              }}

              .button-30:focus {{
                box-shadow: #D6D6E7 0 0 0 1.5px inset, rgba(45, 35, 66, 0.4) 0 2px 4px, rgba(45, 35, 66, 0.3) 0 7px 13px -3px, #D6D6E7 0 -3px 0 inset;
              }}

              .button-30:hover {{
                box-shadow: rgba(45, 35, 66, 0.4) 0 4px 8px, rgba(45, 35, 66, 0.3) 0 7px 13px -3px, #D6D6E7 0 -3px 0 inset;
                transform: translateY(-2px);
              }}

              .button-30:active {{
                box-shadow: #D6D6E7 0 3px 7px inset;
                transform: translateY(2px);
              }}
              /* End of button-30 styles */

              table {{
                border-collapse: collapse;
                width: 100%;
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

              @media screen and (max-width: 600px) {{
                h1 {{
                  font-size: 28px;
                }}

                table {{
                  font-size: 18px;
                }}
              }}
            </style>
          </head>
          <body>
            <h1>Leaderboard</h1>
            <p><a href="https://github.com/Colon101/TERMiGUi" target="_blank" class="button button-30">Check out my program</a></p>
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
