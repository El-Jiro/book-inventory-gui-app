from tkinter import *
from backend import *

#Creamos una función que reciba los datos del backend y los muestre en nuestro Listbox
def show_data() -> None:
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

l1.grid(padx=5, pady=8)
l2.grid(row=0, column=2, padx=5, pady=8)
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
#Para abarcar más de una fila o columna, especificaremos los argumebtos columnspan y rowspan en el método grid
booklist.grid(row=2, column=0, columnspan=3, rowspan=6, padx=8)

#Creamos una scrollbar para poder desplazarnos por la lista cuando los registros llenen todo el espacio visible 
sb = Scrollbar(window)
sb.grid(row=2, column=3, rowspan=6, sticky=W, pady=8, padx= 5)

#Enlazamos ambos widgets
booklist.configure(yscrollcommand=sb.set)
sb.configure(command=booklist.yview)

#--------Botones para las distintas acciones---------------
#Acoplamos la función al botón con el argumento show_data
btn_view= Button(window, text="Ver todo", font=("Arial", 11), width=10, command=show_data)
btn_search= Button(window, text="Buscar", font=("Arial", 11), width=10)
btn_add = Button(window, text="Nuevo", font=("Arial", 11), width=10)
btn_update = Button(window, text="Modificar",  font=("Arial", 11), width=10)
btn_delete = Button(window, text="Eliminar",  font=("Arial", 11), width=10)
btn_close = Button(window, text="Salir",  font=("Arial", 11), width=10)

btn_view.grid(row=2, column=3)
btn_search.grid(row=3, column=3,sticky=N)
btn_add.grid(row=4, column=3, sticky=N)
btn_update.grid(row=5, column=3, sticky=N)
btn_delete.grid(row=6, column=3, sticky=N)
btn_close.grid(row=7, column=3, sticky=N)

window.mainloop()