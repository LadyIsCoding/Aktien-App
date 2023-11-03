import sqlite3
from datetime import datetime

def save_data(user, symbol, price):
    db = sqlite3.connect("assets/database.db")
    cur = db.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS stocks (stockNr INTEGER PRIMARY KEY AUTOINCREMENT, \
                                                    buyer VARCHAR(24) NOT NULL, \
                                                    stock VARCHAR(6) NOT NULL, \
                                                    buy_price DECIMAL(8,2) NOT NULL, \
                                                    buy_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,\
                                                    sell_date TIMESTAMP NULL,\
                                                    sell_price DECIMAL(8,2) NULL);")
    
    cur.execute("INSERT INTO stocks (buyer, stock, buy_price) VALUES (?, ?, ?);", (user, symbol, price))
    
    db.commit()
    db.close()


def load_data(user):
    db = sqlite3.connect("assets/database.db")
    cur = db.cursor()

    cur.execute("SELECT stock, count(stock), sum(buy_price) \
                 FROM stocks WHERE buyer = ? AND sell_date IS NULL GROUP BY stock;", (user,))

    data = cur.fetchall()
    db.close()
    return data


def sell(user, symbol, sell_price):
    db = sqlite3.connect("assets/database.db")
    cur = db.cursor()

    cur.execute("SELECT stockNr \
                FROM stocks \
                WHERE buyer = ? AND stock = ? AND sell_date IS NULL\
                ORDER BY stockNr ASC\
                LIMIT 1;", (user, symbol))
    min_stockNr = cur.fetchone()[0]

    cur.execute("UPDATE stocks SET sell_date = ? WHERE stockNr = ?;", (datetime.now(), min_stockNr))
    db.commit()

    cur.execute("UPDATE stocks SET sell_price = ? WHERE stockNr = ?;", (sell_price, min_stockNr))
    db.commit()
    db.close()


def get_amount(user, symbol):
    db = sqlite3.connect("assets/database.db")
    cur = db.cursor()

    cur.execute("SELECT count(stock) as Amount \
                FROM stocks WHERE buyer = ? AND stock = ? AND sell_date is NULL GROUP BY stock;", (user, symbol))

    data = cur.fetchall()
    db.close()
    return data


def get_all_transactions(user):
    db = sqlite3.connect("assets/database.db")
    cur = db.cursor()

    cur.execute("SELECT stock, buy_price, buy_date, sell_date, sell_price \
                FROM stocks WHERE buyer = ?;", (user,))

    data = cur.fetchall()
    db.close()
    return data


def spend(user, symbol):
    db = sqlite3.connect("assets/database.db")
    cur = db.cursor()

    cur.execute("SELECT sum(buy_price) \
                 FROM stocks WHERE buyer = ? AND stock = ? GROUP BY stock;", (user,symbol))

    data = cur.fetchall()
    db.close()
    return data