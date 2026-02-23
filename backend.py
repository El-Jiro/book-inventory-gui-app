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


def view_entries() -> list:

    conn = sqlite3.connect("library.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM books")
    data = cursor.fetchall()
    conn.close()
    return data

#Pasamos un string vacío como valor default para los argumentos, así el usuario puede pasar solo uno y no dará error
def search_entry(titulo: str = "", autor: str ="", año: int = "", isbn: int="") -> tuple:

    conn = sqlite3.connect("library.db")
    cursor = conn.cursor()
    #Uitlizamos el operador lógico OR para que realice la búsqueda con cualquiera de los cuatro campos de la tabla
    cursor.execute("SELECT * FROM books WHERE titulo = ? OR autor = ? OR año = ? OR isbn = ?", (titulo, autor, año, isbn))
    data = cursor.fetchall()
    conn.close()
    return data

def delete_entry(id: int) -> None:

    conn = sqlite3.connect("library.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM books WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    


connect()
#add_entry("Cien Años de Soledad", "Gabriel García Márquez", 1985, 1135733462)
delete_entry(5)
#print(search_entry(autor="Michael Ende"))
print(view_entries())

