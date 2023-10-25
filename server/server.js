const express = require('express');
const app = express();
const path = require('path');
const ejs = require('ejs');
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

const cheerio = require('cheerio'); // Import the cheerio package

app.use(express.json());
app.get('/leaderboard', (req, res) => {
    const offset = parseInt(req.query.offset) || 0; // Get offset from query parameters
    const limit = 50; // Number of entries to load per request

    db.all('SELECT username, score FROM scores ORDER BY score DESC LIMIT ?, ?', [offset, limit], (err, rows) => {
        if (err) {
            return res.status(500).send('Internal Server Error.');
        }

        const leaderboard = rows.map((row) => ({ username: row.username, score: row.score }));
        res.json(leaderboard);
    });
});

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

app.use(express.static(path.join(__dirname, 'public')));

// Define a route to serve the index.html file on a GET request
app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

  // Serve static files from the 'public' directory
  app.use(express.static(path.join(__dirname, 'public')));
  
  app.listen(port, () => {
    console.log(`Server is running on http://localhost:${port}`);
  });