import re
from tkinter import *
from tkinter import messagebox
#Cambiamos el import para usar sólo la clase Database en vez de todas las funciones
from backend import Database
from book import Libro

"""
-----------------------Variables y objetos globales------------------------------
"""
#Instanciamos la clase y pasamos el nombre de la base de datos en el constructor
db = Database("library.db")
#Expresión regular para validar el nombre del autor
patron = re.compile(r"^(?:[A-Za-zÁÉÍÓÚáéíóúÑñÜü]\.|[A-Za-zÁÉÍÓÚáéíóúÑñÜü]+)(?:[ '-](?:[A-Za-zÁÉÍÓÚáéíóúÑñÜü]\.|[A-Za-zÁÉÍÓÚáéíóúÑñÜü]+))*$")

"""
-------------------------Validaciones------------------------------------------
"""

#Creamos una función para limitar el año a caracteres numéricos y cuatro dígitos
def validate_year(new_val: str) -> bool:
    
    if new_val == "": 
        return True #Permite borrar completamente el valor
    elif not new_val.isdigit():
        return False #Bloquea caracteres no-numéricos
    elif len(new_val) > 4:
        return False #Limitamos el string a cuatro dígitos
    
    return True

#Repetimos el procedimiento para el isbn
def validate_isbn(new_val: str) -> bool: 
    
    if new_val == "": 
        return True #Permite borrar completamente el valor
    elif not new_val.isdigit():
        return False #Bloquea caracteres no-numéricos
    elif len(new_val) > 10:
        return False #Limitamos el string a diez dígitos
    
    return True

#Ahora hacemos una para validar el nombre del autor:
def validate_author(nombre):
    return bool(patron.match(nombre))

"""----------------------FUNCIONES DEL CRUD------------------------"""

#Creamos una función que recupere los datos de la fila seleccionada en el Listbox y los coloque en sus respectivos entries. 
# Ya que será llamada mediante el evento de un widget, deberá llevar un parámetro llamado event

def get_selected_row(event: Event) -> None:

    try:
        #Creamos una variable global para guardar la fila seleccionada, se define como una variable normal precedida por la 
        # palabra reservada global
        global selected_row
        #llamamos al método curselection de booklist y lo guardamos en index para obtener el índice del elemento seleccionado
        index = booklist.curselection()[0]
        #Llamamos al método get, le pasamos index como argumento y guardamos el resultado en index
        selected_row = booklist.get(index)
        
        #Borramos cualquier valor previo que pudieran tener los entries y lo reemplazamos con los valores del registro seleccionado
        titulo.delete(0, END)
        titulo.insert(0, selected_row[1]) #Empezamos por el índice 1 ya que el 0 corresponde al id y este no debe ser manipulado por el usuario
        autor.delete(0, END)
        autor.insert(0, selected_row[2])
        año.delete(0, END)
        año.insert(0, selected_row[3])
        isbn.delete(0, END)
        isbn.insert(0, selected_row[4])
        
    except IndexError:
        pass

#Creamos una función que reciba los datos del backend y los muestre en nuestro Listbox
def view_command() -> None:
    #Antes que nada borramos todos los registros previos
    booklist.delete(0, END)
    #Obtenemos los registros de la tabla y los guardamos en rows
    rows = db.view_entries()
    #Iteramos a través de rows
    for r in rows:
        #Llamamos al método insert de nuestro listbox, este recibe dos argumentos: el índice donde se colocará
        #el elemento, en este caso END, es decir cada nuevo elemento se colocará al final de la lista, y el elemento
        #a insertar
        booklist.insert(END, r)

#Creamos una función wrapper para search_entry, ya que en el argumento command del constructor de Button no podemos pasar 
#directamente funciones con parámetros
def search_command() -> None:

    #Creamos un objeto de tipo libro y asignamos el texto los entries como valor a sus atributos
    libro = Libro()
    libro.titulo = titulo_t.get()
    libro.autor = autor_t.get()
    libro.año = año_t.get()
    libro.isbn = isbn_t.get()

    booklist.delete(0, END)
    #Llamamos a la función search_entry pasando como argumentos nuestros objetos StringVar 
    rows = db.search_entry(libro)
    for r in rows:
        booklist.insert(END, r)

#Hacemos lo mismo para add_command
def add_command() -> None:
    
    if not validate_author(autor_t.get()):
        messagebox.showerror("Autor Inválido", 
                            "El nombre del autor sólo puede contener letras y ciertos caracteres especiales (-, ', `, ü, ñ), también debe tener al menos 3 caracteres de largo")
    else: 
        libro = Libro()
        libro.titulo = titulo_t.get()
        libro.autor = autor_t.get()
        libro.año = año_t.get()
        libro.isbn = isbn_t.get()

        print(libro)

        db.add_entry(libro)
        #Mostramos un cuadro de diálogo con el nuevo registro
        messagebox.showinfo("Registro Añadido", "Se ha añadido correctamente el registro con la siguiente información: "+ f"{libro}")
        #Mostramos todos los registros
        view_command()
    
def update_command() -> None:
    #Si no se ha seleccionado ningún registro, enviamos una advertencia
    if not booklist.curselection():
        messagebox.showwarning("Selección Inválida", "No se ha seleccionado ningún registro para actualizar")
    elif not validate_author(autor_t.get()):
        messagebox.showerror("Autor Inválido", 
                            "El nombre del autor sólo puede contener letras y ciertos caracteres especiales (-, ', `, ü, ñ), también debe tener al menos 3 caracteres de largo")
    else: 
        #De lo contrario ejecutamos la actualización en la base de datos
        db.update_entry(id=selected_row[0], titulo= titulo_t.get() , autor=autor_t.get(), año=año_t.get(), isbn=isbn_t.get())
        messagebox.showinfo("Actualización Exitosa", f"Se ha actualizado correctamente el registro con la información: ${selected_row}")
        #Recargamos la lista
        view_command()

def delete_command() -> None:
    
    #Verificamos si hay algún registro de la lista seleccionado,si no hay ninguno enviamos una advertencia
    if not booklist.curselection():
        messagebox.showwarning("Selección Inválida", "No se ha seleccionado ningún registro para eliminar")
    else:
        #Enviamos un mensaje de confirmación antes de borrar el registro
        respuesta = messagebox.askyesno("Confirmar Eliminación", "¡Esta acción es irreversible! ¿Desea continuar?")
        #Si la respuesta es positiva, eliminamos el registro
        if respuesta:
            id: int = selected_row[0]
            db.delete_entry(id)
            #Enviamos otro mensaje confirmando la eliminación
            messagebox.showinfo("Registro Eliminado", f"Se ha eliminado correctamente el registro con la siguiente información: {selected_row}")
            #Recargamos la lista
            view_command()

def close_app() -> None:
    
    respuesta: bool = messagebox.askokcancel("Confirmar salida","¿Salir de la aplicación? Se perderán todos los datos no guardados")
    if respuesta: 
        window.destroy()

"""--------------------Ventana Principal-------------------------"""
window = Tk()
#Definimos un tamaño fijo para la ventana y evitamos que el usuario puede redimensionarla
window.geometry("550x410")
window.resizable(False, False)
window.title("Inventario de Libros")

"""----------Labels para los entries---------------"""

l1 = Label(window, font=("Arial", 10), text="Título")
l2 = Label(window, font=("Arial", 10), text="Autor")
l3 = Label(window, font=("Arial", 10), text="Año")
l4 = Label(window, font=("Arial", 10), text="ISBN")

l1.grid(padx=0, pady=8)
l2.grid(row=0, column=2, padx=0, pady=8)
l3.grid(row=1, pady=8)
l4.grid(row=1, column=2, pady=8)

"""----------StringVars para los entries---------"""

titulo_t = StringVar()
autor_t = StringVar()
año_t = StringVar()
isbn_t = StringVar()

"""-------------------------Entries------------------------------"""

#Creamos una tupla, en su primer elemento usamos window.register para convertir nuestra función a un comando de tcl y en el segundo pasamos
#un string con el placeholder %P, que sirve para recibir el valor futuro introducido por el usuario
vcmd1: tuple  = (window.register(validate_year), "%P")
vcmd2: tuple = (window.register(validate_isbn), "%P")

titulo = Entry(window, width=30, textvariable=titulo_t)
autor = Entry(window, width=30, textvariable=autor_t)
#En el entry del año pasamos el atributo de validatecommand con el valor de nuestra tupla y especificamos validate="key" para que se ejecute
#la validación cada vez que el usuario presione una tecla para escribir
año = Entry(window, textvariable=año_t, validatecommand = vcmd1, validate="key")
isbn = Entry(window, textvariable=isbn_t, validatecommand=vcmd2, validate="key")


titulo.grid(row=0, column=1, padx=8, sticky=W)
autor.grid(row=0, column= 3, padx=8, sticky=W)
año.grid(row=1, column=1, sticky=W)
isbn.grid(row=1, column=3, sticky=W)

"""-------------------Listbox y Scrollbars-------------------------"""
booklist = Listbox(window, height=18, width=55)
#Para abarcar más de una fila o columna, especificaremos los argumentos columnspan y rowspan en el método grid
booklist.grid(row=2, column=0, columnspan=3, rowspan=6, padx=8)

#Creamos una scrollbar vertical para poder desplazarnos por la lista cuando los registros llenen todo el espacio visible 
sby = Scrollbar(window)
sby.grid(row=2, column=3, rowspan=6, sticky=W, pady=8, padx= 5)

#Creamos otra scrollbar horizontal para cuando se corten los datos de un libro concreto
sbx = Scrollbar(window, orient="horizontal")
sbx.grid(row=10, column=1, columnspan=2, pady=7)
#Enlazamos ambos widgets
booklist.configure(yscrollcommand=sby.set)
sby.configure(command=booklist.yview)

booklist.configure(xscrollcommand=sbx.set)
sbx.configure(command=booklist.xview)
#LLamamos a la función get_selected_row de booklist con el método bind, este recibe dos argumentos: el tipo de evento entre dos pares 
#de corchetes angulares <>, en este caso ListboxSelect y la función que será ejecutada cuando se dispare dicho evento, pero solo el nombre
#de la función sin invocarla
booklist.bind("<<ListboxSelect>>", get_selected_row)


"""--------Botones para las distintas acciones---------------"""

btn_view= Button(window, text="Ver todo", font=("Arial", 11), width=10, command=view_command) #Acoplamos la función al botón con el argumento show_data
btn_search= Button(window, text="Buscar", font=("Arial", 11), width=10, command=search_command)
btn_add = Button(window, text="Nuevo", font=("Arial", 11), width=10, command=add_command)
btn_update = Button(window, text="Modificar",  font=("Arial", 11), width=10, command=update_command)
btn_delete = Button(window, text="Eliminar",  font=("Arial", 11), width=10, command=delete_command)
btn_close = Button(window, text="Salir",  font=("Arial", 11), width=10, command=close_app)

btn_view.grid(row=2, column=3)
btn_search.grid(row=3, column=3,sticky=N)
btn_add.grid(row=4, column=3, sticky=N)
btn_update.grid(row=5, column=3, sticky=N)
btn_delete.grid(row=6, column=3, sticky=N)
btn_close.grid(row=7, column=3, sticky=N)

window.mainloop()