import sqlite3

#Creamos el archivo .db y nuestra primera tabla
def connect() -> None:

    conn = sqlite3.connect("library.db")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS books (id INTEGER PRIMARY KEY, titulo TEXT, autor TEXT, año INTEGER, isbn INTEGER)")
    conn.commit()
    conn.close()


def add_entry(titulo: str, autor: str, año: int, isbn: int)-> None:

    conn = sqlite3.connect("library.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO books VALUES (NULL, ?, ?, ?, ?)", (titulo, autor, año, isbn))
    conn.commit()
    conn.close()


connect()