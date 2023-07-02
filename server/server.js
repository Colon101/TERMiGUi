const express = require('express');
const app = express();
const port = 80;

const sqlite3 = require('sqlite3').verbose();
const db = new sqlite3.Database('leaderboard.db');

db.run(`
    CREATE TABLE IF NOT EXISTS scores (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        score INTEGER
    )
`);

app.use(express.json());

app.post('/', (req, res) => {
    const { username, score } = req.body;

    if (!username) {
        return res.status(400).send('Username is required.');
    }

    if (score === undefined) {
        return res.status(400).send('Score is required.');
    }

    db.serialize(() => {
        db.get('SELECT score FROM scores WHERE username = ?', [username], (err, row) => {
            if (err) {
                return res.status(500).send('Internal Server Error.');
            }

            if (row) {
                if (score > row.score) {
                    db.run('UPDATE scores SET score = ? WHERE username = ?', [score, username], (err) => {
                        if (err) {
                            return res.status(500).send('Internal Server Error.');
                        }
                        res.sendStatus(200);
                    });
                } else {
                    res.sendStatus(200);
                }
            } else {
                db.run('INSERT INTO scores (username, score) VALUES (?, ?)', [username, score], (err) => {
                    if (err) {
                        return res.status(500).send('Internal Server Error.');
                    }
                    res.sendStatus(200);
                });
            }
        });
    });
});

app.get('/', (req, res) => {
    db.all('SELECT username, score FROM scores ORDER BY score DESC', (err, rows) => {
        if (err) {
            return res.status(500).send('Internal Server Error.');
        }

        const leaderboard = rows
            .map((row, index) => `<tr><td>${index + 1}</td><td>${row.username}</td><td>${row.score}</td></tr>`)
            .join('');

        const html = `
            <!DOCTYPE html>
            <html>
              <head>
                <title>Leaderboard</title>
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <style>
                  body {
                    background-color: #222;
                    color: #fff;
                    font-family: Arial, sans-serif;
                    margin: 0;
                    padding: 20px;
                  }
                  
                  h1 {
                    font-size: 36px;
                    text-align: center;
                    margin-bottom: 30px;
                  }
                  
                  p {
                    text-align: center;
                    margin-bottom: 30px;
                  }
                  
                  /* Add the button-30 styles below */
                  .button-30 {
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
                  }
                  
                  .button-30:focus {
                    box-shadow: #D6D6E7 0 0 0 1.5px inset, rgba(45, 35, 66, 0.4) 0 2px 4px, rgba(45, 35, 66, 0.3) 0 7px 13px -3px, #D6D6E7 0 -3px 0 inset;
                  }
                  
                  .button-30:hover {
                    box-shadow: rgba(45, 35, 66, 0.4) 0 4px 8px, rgba(45, 35, 66, 0.3) 0 7px 13px -3px, #D6D6E7 0 -3px 0 inset;
                    transform: translateY(-2px);
                  }
                  
                  .button-30:active {
                    box-shadow: #D6D6E7 0 3px 7px inset;
                    transform: translateY(2px);
                  }
                  /* End of button-30 styles */
                  
                  table {
                    border-collapse: collapse;
                    width: 100%;
                  }
                  
                  th, td {
                    border: 1px solid #fff;
                    padding: 8px;
                    text-align: left;
                    font-size: 20px;
                  }
                  
                  th {
                    background-color: #555;
                    color: #fff;
                    font-weight: bold;
                  }
                  
                  td {
                    background-color: #222;
                  }
                  
                  @media screen and (max-width: 600px) {
                    h1 {
                      font-size: 28px;
                    }
                    
                    table {
                      font-size: 18px;
                    }
                  }
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
                  ${leaderboard}
                </table>
              </body>
            </html>
        `;

        res.send(html);
    });
});

app.listen(port, () => {
    console.log(`Server is running on http://localhost:${port}`);
});
