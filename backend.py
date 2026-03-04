import sqlite3

class Database:

    #Cambiamos el nombre de la función a __init__, esto hará que se ejecute inmediatamente cuando creemos un objeto de esta clase,
    #lo que en otros lenguajes vendría siendo el método constructor o simplemnte constructor. También deberemos especificar al menos 
    #un argumento llamado self (podemos ponerle cualquier nombre, pero self es la convención), de lo contrario dará un error al instanciar
    #la clase, ya que internamente cada instancia se pasa como argumento a este método aunque nosotros no la hayamos definido explícitamente.
    #Lo mismo aplica para todos los métodos de instancia

    def __init__(self, dbname: str) -> None:

        #Convertimos cursor y conn en atributos de la clase añadiendoles el prefijo self, además de eliminar la línea que cierra la conexión
        self.conn = sqlite3.connect(dbname)
        self.cursor = self.conn.cursor()
        self.cursor.execute("CREATE TABLE IF NOT EXISTS books (id INTEGER PRIMARY KEY, titulo TEXT, autor TEXT, año INTEGER, isbn INTEGER)")
        self.conn.commit()

    def add_entry(self, titulo: str, autor: str, año: int, isbn: int)-> None:

        #Eliminamos las declaraciones de conn y cursor, puesto que ya están definidos en el constructor, 
        # ahora sólo tenemos que referirnos a ellos como atributos de la clase 
        self.cursor.execute("INSERT INTO books VALUES (NULL, ?, ?, ?, ?)", (titulo, autor, año, isbn))
        self.conn.commit()
        self.conn.close()

    def view_entries(self) -> list:

        self.cursor.execute("SELECT * FROM books")
        data = self.cursor.fetchall()
        self.conn.close()
        return data

    #Pasamos un string vacío como valor default para los argumentos, así el usuario puede pasar solo uno y no dará error
    def search_entry(self, titulo: str = "", autor: str ="", año: int = "", isbn: int="") -> tuple:

        #Uitlizamos el operador lógico OR para que realice la búsqueda con cualquiera de los cuatro campos de la tabla
        self.cursor.execute("SELECT * FROM books WHERE titulo = ? OR autor = ? OR año = ? OR isbn = ?", (titulo, autor, año, isbn))
        data = self.cursor.fetchall()
        self.conn.close()
        
        return data

    def update_entry(self, titulo: str, autor: str, año: int, isbn: int, id: int) -> None:
        
        self.cursor.execute("UPDATE books SET titulo = ?, autor = ?, año = ?, isbn = ? WHERE id = ?", (titulo, autor, año, isbn, id))
        self.conn.commit()
        self.conn.close()

    def delete_entry(self, id: int) -> None:

        self.cursor.execute("DELETE FROM books WHERE id = ?", (id,))
        self.conn.commit()
        self.conn.close()
    


