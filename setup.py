#!/usr/bin/env python3
import sqlite3

db = sqlite3.connect("main.sqlite")

db.execute("CREATE TABLE IF NOT EXISTS users(\
        id INTEGER PRIMARY KEY, \
        password STRING NOT NULL, \
        user STRING UNIQUE, \
        salt STRING NOT NULL \
                );")

db.execute("CREATE TABLE IF NOT EXISTS products(\
        name STRING NOT NULL, \
        category STRING NOT NULL, \
        price REAL, \
        specs STRING, \
        quality INTEGER NOT NULL, \
        value INTEGER NOT NULL, \
        avg REAL, \
        voted INTEGER NOT NULL \
    );")


# do not touch the expiry column
db.execute("CREATE TABLE IF NOT EXISTS token(" + 
        "id INTEGER NOT NULL, " + 
        "token STRING PRIMARY KEY, " + 
        "expiry INTEGER NOT NULL " + 
                ");")

db.execute("CREATE TABLE IF NOT EXISTS products(\
        name STRING NOT NULL,\
        category STRING,\
        price REAL NOT NULL,\
        specs STRING NOT NULL,\
        value REAL DEFAULT 0,\
        price REAL DEFAULT 0,\
        review REAL DEFAULT 0,\
        votes REAL DEFAULT 0\
                )")

db.commit()
db.close()
