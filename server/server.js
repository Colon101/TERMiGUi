const express = require('express');
const sqlite3 = require('sqlite3').verbose();

const app = express();
const port = 3000;

app.use(express.json());

const db = new sqlite3.Database('leaderboard.db');

db.run(`
  CREATE TABLE IF NOT EXISTS scores (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    score INTEGER
  )
`);

app.post('/leaderboard', (req, res) => {
    const { username, score } = req.body;

    if (!username || !score) {
        res.status(400).send('Username and score are required.');
        return;
    }

    db.get('SELECT score FROM scores WHERE username = ?', [username], (err, row) => {
        if (err) {
            console.error(err);
            res.sendStatus(500);
            return;
        }

        if (row) {
            if (score > row.score) {
                db.run('UPDATE scores SET score = ? WHERE username = ?', [score, username], (err) => {
                    if (err) {
                        console.error(err);
                        res.sendStatus(500);
                    } else {
                        res.sendStatus(200);
                    }
                });
            } else {
                res.sendStatus(200);
            }
        } else {
            db.run('INSERT INTO scores (username, score) VALUES (?, ?)', [username, score], (err) => {
                if (err) {
                    console.error(err);
                    res.sendStatus(500);
                } else {
                    res.sendStatus(200);
                }
            });
        }
    });
});

app.get('/leaderboard', (req, res) => {
    db.all('SELECT username, score FROM scores ORDER BY score DESC', (err, rows) => {
        if (err) {
            console.error(err);
            res.sendStatus(500);
        } else {
            const leaderboard = rows
                .map(
                    (row, index) =>
                        `<tr><td>${index + 1}</td><td>${row.username}</td><td>${row.score}</td></tr>`
                )
                .join('');

            const html = `
          <!DOCTYPE html>
          <html>
            <head>
              <title>Leaderboard</title>
              <style>
                body {
                  background-color: #222;
                  color: #fff;
                  font-size: 24px;
                }
  
                table {
                  border-collapse: collapse;
                  width: 100%;
                }
  
                th,
                td {
                  border: 1px solid #fff;
                  padding: 8px;
                  text-align: left;
                  font-size: 24px;
                }
  
                h1 {
                  color: #fff;
                  font-size: 36px;
                }
              </style>
            </head>
            <body>
              <h1>Leaderboard</h1>
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
        }
    });
});

app.listen(port, () => {
    console.log(`Server is running on port ${port}`);
});