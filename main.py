from tkinter import messagebox
from tkinter import *
from backend import *

#Creamos una función que recupere los datos de la fila seleccionada en el Listbox. Ya que será llamada mediante el evento de un widget,
#deberá llevar un parámetro llamado event
def get_selected_row(event: Event) -> None:
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

#Creamos una función que reciba los datos del backend y los muestre en nuestro Listbox
def view_command() -> None:
    #Antes que nada borramos todos los registros previos
    booklist.delete(0, END)
    #Obtenemos los registros de la tabla y los guardamos en rows
    rows = view_entries()
    #Iteramos a través de rows
    for r in rows:
        #Llamamos al método insert de nuestro listbox, este recibe dos argumentos: el índice donde se colocará
        #el elemento, en este caso END, es decir cada nuevo elemento se colocará al final de la lista, y el elemento
        #a insertar
        booklist.insert(END, r)

#Creamos una función wrapper para search_entry, ya que en el argumento command del constructor de Button no podemos pasar 
#directamente funciones con parámetros
def search_command() -> None:
    
    booklist.delete(0, END)
    #Llamamos a la función search_entry pasando como argumentos nuestros objetos StringVar 
    rows = search_entry(titulo_t.get(), autor_t.get(), año_t.get(), isbn_t.get())
    for r in rows:
        booklist.insert(END, r)

#Hacemos lo mismo para add_command
def add_command() -> None:
    
    add_entry(titulo_t.get(), autor_t.get(), año_t.get(), isbn_t.get())
    #Mostramos un cuadro de diálogo con el nuevo registro
    messagebox.showinfo("Registro Añadido", "Se ha añadido correctamente el registro con la siguiente información: "
                        + f"{(titulo_t.get(), autor_t.get(), año_t.get(), isbn_t.get())}")
    #Mostramos todos los registros
    view_command()

def update_command() -> None:
    #Si no se ha seleccionado ningún registro, enviamos una advertencia
    if not booklist.curselection():
        messagebox.showwarning("Selección Inválida", "No se ha seleccionado ningún registro para actualizar")
    else: 
        #De lo contrario ejecutamos la actualización en la base de datos
        update_entry(id=selected_row[0], titulo= titulo_t.get() , autor=autor_t.get(), año=año_t.get(), isbn=isbn_t.get())
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
            delete_entry(id)
            #Enviamos otro mensaje confirmando la eliminación
            messagebox.showinfo("Registro Eliminado", f"Se ha eliminado correctamente el registro con la siguiente información: {selected_row}")
            #Recargamos la lista
            view_command()

window = Tk()
#Definimos un tamaño fijo para la ventana y evitamos que el usuario puede redimensionarla
window.geometry("550x410")
window.resizable(False, False)
window.title("Inventario de Libros")

#----------Labels para los entries---------------
l1 = Label(window, font=("Arial", 10), text="Título")
l2 = Label(window, font=("Arial", 10), text="Autor")
l3 = Label(window, font=("Arial", 10), text="Año")
l4 = Label(window, font=("Arial", 10), text="ISBN")

l1.grid(padx=0, pady=8)
l2.grid(row=0, column=2, padx=0, pady=8)
l3.grid(row=1, pady=8)
l4.grid(row=1, column=2, pady=8)

#----------StringVars para los entries---------
titulo_t = StringVar()
autor_t = StringVar()
año_t = StringVar()
isbn_t = StringVar()

#-----Entries------
titulo = Entry(window, width=30, textvariable=titulo_t)
autor = Entry(window, width=30, textvariable=autor_t)
año = Entry(window, textvariable=año_t)
isbn = Entry(window, textvariable=isbn_t)


titulo.grid(row=0, column=1, padx=8, sticky=W)
autor.grid(row=0, column= 3, padx=8, sticky=W)
año.grid(row=1, column=1, sticky=W)
isbn.grid(row=1, column=3, sticky=W)

#-------Usaremos un listbox para desplegar todas las entradas de la bd-----
booklist = Listbox(window, height=20, width=55)
#Para abarcar más de una fila o columna, especificaremos los argumentos columnspan y rowspan en el método grid
booklist.grid(row=2, column=0, columnspan=3, rowspan=6, padx=8)

#Creamos una scrollbar para poder desplazarnos por la lista cuando los registros llenen todo el espacio visible 
sb = Scrollbar(window)
sb.grid(row=2, column=3, rowspan=6, sticky=W, pady=8, padx= 5)

#Enlazamos ambos widgets
booklist.configure(yscrollcommand=sb.set)
sb.configure(command=booklist.yview)

#LLamamos a la función get_selected_row de booklist con el método bind, este recibe dos argumentos: el tipo de evento entre dos pares 
#de corchetes angulares <>, en este caso ListboxSelect y la función que será ejecutada cuando se dispare dicho evento, pero solo el nombre
#de la función sin invocarla
booklist.bind("<<ListboxSelect>>", get_selected_row)


#--------Botones para las distintas acciones---------------

btn_view= Button(window, text="Ver todo", font=("Arial", 11), width=10, command=view_command) #Acoplamos la función al botón con el argumento show_data
btn_search= Button(window, text="Buscar", font=("Arial", 11), width=10, command=search_command)
btn_add = Button(window, text="Nuevo", font=("Arial", 11), width=10, command=add_command)
btn_update = Button(window, text="Modificar",  font=("Arial", 11), width=10, command=update_command)
btn_delete = Button(window, text="Eliminar",  font=("Arial", 11), width=10, command=delete_command)
btn_close = Button(window, text="Salir",  font=("Arial", 11), width=10)

btn_view.grid(row=2, column=3)
btn_search.grid(row=3, column=3,sticky=N)
btn_add.grid(row=4, column=3, sticky=N)
btn_update.grid(row=5, column=3, sticky=N)
btn_delete.grid(row=6, column=3, sticky=N)
btn_close.grid(row=7, column=3, sticky=N)

window.mainloop()