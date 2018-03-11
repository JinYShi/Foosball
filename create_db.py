#!/usr/bin/python3

import sqlite3

conn = sqlite3.connect('foosball.db')
print ("Opened database successfully");

#assume there are 5 users
conn.execute('''DROP TABLE IF EXISTS users;''')
conn.execute('''CREATE TABLE Users
       (user_ID    TEXT PRIMARY KEY     NOT NULL,
        user_name  TEXT,
        num_win    INT,
        num_total  INT);''')

conn.execute('''DROP TABLE IF EXISTS matches;''')
conn.execute('''CREATE TABLE Match
       (match_ID    TEXT PRIMARY KEY     NOT NULL,
        match_time  DATETIME DEFAULT CURRENT_TIMESTAMP
        );''')

#state: 0-lose, 1-win, 2-equal
conn.execute('''DROP TABLE IF EXISTS matches_state;''')
conn.execute('''CREATE TABLE Match_state
       (match_ID    TEXT  NOT NULL,
        user_ID     TEXT  NOT NULL,
        state       INT  NOT NULL,
        FOREIGN KEY(match_ID) REFERENCES matches(match_ID),
        FOREIGN KEY(user_ID) REFERENCES users(user_ID));''')

print ("Table created successfully");

conn.close()