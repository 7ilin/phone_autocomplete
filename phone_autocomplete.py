#!/usr/bin/python

import sys
import os
import random
import sqlite3


NUM_PHONES = 100000

COUNTRY_CODE = '380'
OPERATORS = ('99', '97', '66', '63')
PHONE_TMPL = '{country_code}{operator}{number}'
LEN_NUMBER = 7

DB_NAME = 'users.db'
CREATE_CONTACTS = "CREATE TABLE contacts (id INTEGER PRIMARY KEY, phone TEXT NOT NULL);"
INSERT_CONTACTS_TMPL = "INSERT INTO contacts(phone) VALUES('%s');"
SELECT_PHONE_TMPL = "SELECT phone FROM contacts WHERE phone LIKE '%s%%' LIMIT 10;"


def generate_number():
    ch_lst = []
    for i in range(LEN_NUMBER):
        ch = random.randint(0, 9)
        ch_lst.append(ch)
    return ''.join(map(str, ch_lst))


def gen_phones():
    for i in range(NUM_PHONES):
        operator = random.choice(OPERATORS)
        phone = PHONE_TMPL.format(
            country_code=COUNTRY_CODE,
            operator=operator,
            number=generate_number())
        yield phone


def install_db(phones=gen_phones, db_name=DB_NAME):
    if os.path.exists(db_name):
        os.remove(db_name)
    with sqlite3.connect(db_name) as conn:
        c = conn.cursor()
        c.execute(CREATE_CONTACTS)
        for phone in phones():
            q = INSERT_CONTACTS_TMPL % phone
            c.execute(q)
        conn.commit()


def select(c, q):
    c.execute(q)
    return c.fetchall()


def phone_autocomplete(start_phone, db_name=DB_NAME):
    with sqlite3.connect(db_name) as conn:
        c = conn.cursor()
        q = SELECT_PHONE_TMPL % start_phone
        res = select(c, q)
        return list(map(lambda x: x[0], res))


if __name__ == '__main__':
    arg = sys.argv[1]
    if arg == 'install_db':
        install_db()
        print("DB installed")
    else:
        res = phone_autocomplete(arg)
        print(res)
