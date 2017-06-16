import threading
import rest as rest
import sqlite3

if "__main__" == __name__:
    import sqlite3

    conn = sqlite3.connect('sqlite.db')
    print ("Opened database successfully")

    conn.execute('''
        CREATE TABLE if not exists car (
            car_id INTEGER PRIMARY KEY AUTOINCREMENT,
            car_maker TEXT NOT NULL,
            car_model TEXT NOT NULL,
            car_year DATE NOT NULL);
        ''')

    conn.execute('''
        CREATE TABLE if not exists driver (
            driver_id INTEGER PRIMARY KEY AUTOINCREMENT,
            driver_firstName TEXT NOT NULL, 
            driver_lastName TEXT NOT NULL,
            car_id INTEGER,
            FOREIGN KEY(car_id) REFERENCES car(car_id) ON DELETE SET NULL);
        ''')
    print("Table created successfully")
    conn.close()
    rest.run('localhost', 8181)