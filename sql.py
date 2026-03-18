import sqlite3

conn=sqlite3.connect("finannc_ledgar.db")
cursor=conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS inventory_ledger(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_name TEXT NOT NULL,
    units INTEGER NOT NULL,
    unit_price REAL NOT NULL,
    transaction_type TEXT CHECK(transaction_type IN ('RESTOCK','SALE'))
               )
               """)

cursor.execute("INSERT INTO inventory_ledger (product_name, units, unit_price, transaction_type) VALUES ('Processors', 100, 45.50, 'RESTOCK')")
cursor.execute("INSERT INTO inventory_ledger (product_name, units, unit_price, transaction_type) VALUES ('Processors', 15, 120.00, 'SALE')")
cursor.execute("INSERT INTO inventory_ledger (product_name, units, unit_price, transaction_type) VALUES ('Motherboards', 50, 85.00, 'RESTOCK')")

conn.commit()
conn.close()