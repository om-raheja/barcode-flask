#!/usr/bin/env python3
import sqlite3

db = sqlite3.connect("main.sqlite")

db.execute('INSERT INTO products VALUES (\
        "Yuxin Little Magic", \
        "Rubiks Cube", \
        5.00, \
        "Really fast", \
        0.8, \
        0.8, \
        0, \
        0\
                )')

db.commit()
db.close()
