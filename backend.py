import sqlite3

class Database:
    
    dbname = ""
    #Cambiamos el nombre de la función a __init__, esto hará que se ejecute inmediatamente cuando creemos un objeto de esta clase,
    #lo que en otros lenguajes vendría siendo el método constructor o simplemnte constructor. También deberemos especificar al menos 
    #un argumento llamado self (podemos ponerle cualquier nombre, pero self es la convención), de lo contrario dará un error al instanciar
    #la clase, ya que internamente cada instancia se pasa como argumento a este método aunque nosotros no la hayamos definido explícitamente.
    def __init__(self, dbname: str) -> None:

        self.dbname = dbname
        conn = sqlite3.connect(self.dbname)
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS books (id INTEGER PRIMARY KEY, titulo TEXT, autor TEXT, año INTEGER, isbn INTEGER)")
        conn.commit()
        conn.close()

    def add_entry(self, titulo: str, autor: str, año: int, isbn: int)-> None:

        conn = sqlite3.connect(self.dbname)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO books VALUES (NULL, ?, ?, ?, ?)", (titulo, autor, año, isbn))
        conn.commit()
        conn.close()

    def view_entries(self) -> list:

        conn = sqlite3.connect(self.dbname)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM books")
        data = cursor.fetchall()
        conn.close()
        return data

    #Pasamos un string vacío como valor default para los argumentos, así el usuario puede pasar solo uno y no dará error
    def search_entry(self, titulo: str = "", autor: str ="", año: int = "", isbn: int="") -> tuple:

        conn = sqlite3.connect(self.dbname)
        cursor = conn.cursor()
        #Uitlizamos el operador lógico OR para que realice la búsqueda con cualquiera de los cuatro campos de la tabla
        cursor.execute("SELECT * FROM books WHERE titulo = ? OR autor = ? OR año = ? OR isbn = ?", (titulo, autor, año, isbn))
        data = cursor.fetchall()
        conn.close()
        return data

    def update_entry(self, titulo: str, autor: str, año: int, isbn: int, id: int) -> None:
        
        conn = sqlite3.connect(self.dbname)
        cursor = conn.cursor()
        cursor.execute("UPDATE books SET titulo = ?, autor = ?, año = ?, isbn = ? WHERE id = ?", (titulo, autor, año, isbn, id))
        conn.commit()
        conn.close()

    def delete_entry(self, id: int) -> None:

        conn = sqlite3.connect(self.dbname)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM books WHERE id = ?", (id,))
        conn.commit()
        conn.close()
    


